# Harbour Board: iPad Air 2 home display

A full-screen board for your old iPad showing a live clock, Helston weather, your Outlook calendar and a to-do list. It's free to run and takes about 20 minutes to set up.

**What's in this folder**

| File | What it does |
|---|---|
| `index.html` | The display itself |
| `icon.png` | Home Screen icon |
| `events.json` | Your calendar events (GitHub fills this in for you) |
| `scripts/build_events.py` | Reads your Outlook calendar and writes `events.json` |
| `.github/workflows/calendar.yml` | Tells GitHub to run that script every 30 minutes |

---

## 1. Put it on GitHub (on your PC)

1. Sign up at **github.com** if you don't have an account. The free plan is fine.
2. Click **+** (top right) → **New repository**. Name it `harbour-board`, choose **Public**, and click **Create repository**.
3. Click **uploading an existing file**. Drag in `index.html`, `icon.png`, `events.json` and the whole `scripts` folder, then click **Commit changes**.
4. Create the workflow file by hand, because hidden folders don't always upload:
   **Add file → Create new file**. For the name, type `.github/workflows/calendar.yml` exactly (the slashes create the folders). Paste in the contents of `calendar.yml` from this folder, then click **Commit changes**.

## 2. Turn on the website

1. In the repository, go to **Settings → Pages**.
2. Under *Build and deployment*, set Source to **Deploy from a branch**, Branch to **main**, folder **/ (root)**, then **Save**.
3. After a minute or two the page shows your address, something like
   `https://YOUR-USERNAME.github.io/harbour-board/`
   Open it on your PC to check it works. The weather should load straight away.

## 3. Connect your Outlook calendar

1. Go to **outlook.live.com** → ⚙️ **Settings → Calendar → Shared calendars**.
2. Under **Publish a calendar**, pick your calendar, choose **Can view all details**, and click **Publish**.
3. Copy the **ICS** link (not the HTML one).
4. Back on GitHub: **Settings → Secrets and variables → Actions → New repository secret**.
   Name: `OUTLOOK_ICS_URL`. Secret: paste the ICS link. Click **Add secret**.
5. Go to the **Actions** tab. If asked, click to enable workflows. Pick **Update calendar → Run workflow**.
   After about a minute it turns green, and your events show on the board within 10 minutes. After that it updates by itself every 30 minutes.

> **Privacy:** the ICS link stays secret, but on a free account the repository is public, so `events.json` (event names and times) can be read by anyone who finds it. Outlook events marked *Private* always show as "Busy". To hide every event name, edit `.github/workflows/calendar.yml` and change `SHOW_DETAILS: "true"` to `"false"`.

## 4. Set up the iPad

1. Open your board's address in **Safari** on the iPad.
2. Tap **Share → Add to Home Screen → Add**. Always open it from that icon: it runs full screen with no Safari bars.
3. **Settings → Display & Brightness → Auto-Lock → Never**.
4. Optional, to lock it to the board: **Settings → Accessibility → Guided Access → On**. Open the board, triple-click the Home button and tap **Start**. Triple-click again to leave.
5. Keep it on charge on a stand. Because an old battery charging 24/7 can wear and swell over the years, a cheap smart plug that cuts power for a few hours a day helps.

## Using it

- **To-dos:** type in *Add a to-do* and tap Add. Tap an item to tick it off. Ticked items disappear the next day, or tap *Clear done*. They're saved on the iPad only.
- **Overnight:** the screen dims from 23:00 to 07:00. Tap anywhere to brighten it for two minutes.
- **Calendar:** the event happening now shows an amber dot, and finished ones fade.
- **Wind** is shown as a Beaufort force with direction (for example "F4 SW"). The arrow points the way the wind is blowing.
- The board reloads itself at 03:00 each night, so any changes you upload take effect by morning.

## Changing settings

On GitHub, open `index.html` and click the ✏️ pencil. The `CONFIG` block near the top controls:
- `place`, `latitude`, `longitude`: the weather location (find coordinates by right-clicking a spot in Google Maps)
- `hour12: true` for 12-hour times
- `nightDim`: dim hours and strength (`strength: 0` turns it off)

Click **Commit changes**. The live site updates in about a minute.

Weather data comes from Open-Meteo.com, which is free and needs no key.
