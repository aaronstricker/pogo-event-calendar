# Pokémon GO Raid Group Calendar

Free GitHub Pages site for the live **Pokemon Go Events** Google Calendar, plus an optional Discord webhook that posts a daily digest of events starting in the next 24 hours.

## 1) Create the GitHub repo
1. Create a **public** GitHub repository, e.g. `pokemon-go-calendar`.
2. Upload all files in this folder to the repository root.
3. Commit them.

## 2) Turn on GitHub Pages
1. Repository → **Settings → Pages**.
2. Build and deployment → **Deploy from a branch**.
3. Branch: `main`; folder: `/ (root)`.
4. Save.

Your URL will normally look like:
`https://YOUR-USERNAME.github.io/pokemon-go-calendar/`

Pin that URL in your Discord raid channel.

## 3) Create a Discord webhook
You need **Manage Webhooks** permission.
1. Discord server → **Server Settings → Integrations → Webhooks**.
2. **New Webhook**.
3. Name it `Pokémon GO Calendar` and select your raid/calendar channel.
4. **Copy Webhook URL**.

Treat the webhook URL like a password.

## 4) Save the webhook as a GitHub secret
1. GitHub repo → **Settings → Secrets and variables → Actions**.
2. **New repository secret**.
3. Name: `DISCORD_WEBHOOK_URL`.
4. Paste the webhook URL as the value.

## 5) Test the Discord post
1. GitHub repo → **Actions**.
2. Open **Pokémon GO Discord daily digest**.
3. Click **Run workflow**.

If an event starts in the next 24 hours, it posts to Discord. If not, it intentionally posts nothing.

The automatic schedule is 13:05 UTC daily: about 9:05 AM EDT / 8:05 AM EST in Pennsylvania.

## Event icon scheme
🟣 Max/G-Max/D-Max • 🟠 Mega • 🔴 Raids • 🟢 Community/Catch/Hatch • 🟡 Spotlight • 🔵 GBL • 🩷 Rocket • 🌊 Wild Area/GO Fest • ⚪ Deadlines • 🩵 General

## Privacy
The Google Calendar is public. Do not put personal information in it. Keep the Discord webhook URL only in GitHub Actions Secrets.
