"""Turn a published Outlook calendar (.ics link) into events.json for the display.

Runs on GitHub Actions. Reads the link from the OUTLOOK_ICS_URL secret, so the
link itself never appears in the repository.

Environment:
  ICS_URL       the calendar's ICS link (required, set from the repo secret)
  SHOW_DETAILS  "true" (default) to show event names, "false" to show "Busy"
  DAYS_AHEAD    how many days of events to keep (default 14)
  TIMEZONE      display time zone (default Europe/London)
"""

import json
import os
import sys
import urllib.request
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import icalendar
import recurring_ical_events

OUT_FILE = os.path.join(os.path.dirname(__file__), "..", "events.json")


def load_ics(url):
    # Outlook sometimes hands out webcal:// links; they are plain https underneath.
    if url.startswith("webcal://"):
        url = "https://" + url[len("webcal://"):]
    req = urllib.request.Request(url, headers={"User-Agent": "ipad-display/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def to_local(value, tz):
    """Return (local datetime or date, is_all_day)."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=tz)
        return value.astimezone(tz), False
    return value, True


def fmt(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%dT%H:%M")
    return value.isoformat()


def main():
    url = os.environ.get("ICS_URL", "").strip()
    tz = ZoneInfo(os.environ.get("TIMEZONE", "Europe/London"))
    show_details = os.environ.get("SHOW_DETAILS", "true").lower() != "false"
    days_ahead = int(os.environ.get("DAYS_AHEAD", "14"))

    today = datetime.now(tz).date()
    payload = {"updated": today.isoformat(), "events": []}

    if not url:
        payload["note"] = "No calendar link set yet (add the OUTLOOK_ICS_URL secret)."
        write(payload)
        print("No ICS_URL set; wrote an empty events.json")
        return

    cal = icalendar.Calendar.from_ical(load_ics(url))
    start = datetime.combine(today, time.min, tz)
    end = start + timedelta(days=days_ahead)

    events = []
    for ev in recurring_ical_events.of(cal).between(start, end):
        if str(ev.get("STATUS", "")).upper() == "CANCELLED":
            continue
        dtstart = ev.get("DTSTART")
        if dtstart is None:
            continue
        s, all_day = to_local(dtstart.dt, tz)

        dtend = ev.get("DTEND")
        if dtend is not None:
            e, _ = to_local(dtend.dt, tz)
        elif ev.get("DURATION") is not None:
            e = s + ev.get("DURATION").dt
        else:
            e = s + (timedelta(days=1) if all_day else timedelta(hours=1))

        title = str(ev.get("SUMMARY", "")).strip() or "Busy"
        private = str(ev.get("CLASS", "")).upper() in ("PRIVATE", "CONFIDENTIAL")
        if not show_details or private:
            title = "Busy"

        events.append({"title": title, "start": fmt(s), "end": fmt(e), "allDay": all_day})

    # All-day first on each day, then by time.
    events.sort(key=lambda x: (x["start"][:10], not x["allDay"], x["start"], x["title"]))
    payload["events"] = events
    write(payload)
    print(f"Wrote {len(events)} events")


def write(payload):
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # keep the last good events.json if anything fails
        print(f"Calendar update failed: {exc}", file=sys.stderr)
        sys.exit(1)
