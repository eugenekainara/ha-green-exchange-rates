# Green Exchange Rates for Home Assistant

A custom Home Assistant integration that reads USD/EUR exchange-rate ranges from a public Telegram channel and exposes four native Home Assistant sensors.

## Requirements

- **Home Assistant 2026.11.0 or newer** — the built-in Marketplace was introduced in this release.
- A public Telegram channel whose web preview is accessible without signing in.
- Internet access from Home Assistant.

## Install through Home Assistant Marketplace

1. Make sure Home Assistant is running **2026.11.0 or newer**.
2. Open **Settings → Marketplace**.
3. Select **Add from link**.
4. Enter this repository's GitHub URL, for example:
   `https://github.com/YOUR_GITHUB_USERNAME/green-exchange`
5. Select **Add**. If Marketplace asks for a content type, choose **Integration**.
6. Open the Green Exchange repository entry and select **Download / Install**.
7. If Home Assistant asks for a restart, restart Home Assistant.
8. Go to **Settings → Devices & services → Add integration**.
9. Search for **Green Exchange** and enter the public Telegram channel username. The default is `Obmen_Vasilkovskaya`; enter it without the `@`.

The repository must be public for Marketplace custom-repository installation. Marketplace may ask you to connect a GitHub account using its device sign-in flow.

## Configure polling

After adding the integration, open **Settings → Devices & services → Green Exchange → Configure** to change:

- **Refresh interval:** 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, or 30, or 60 minutes.
- **Start hour:** 0–23.
- **End hour:** 0–23, inclusive.

The hours use Home Assistant's local timezone. For example, start `8`, end `20`, interval `60` means refresh at 08:00, 09:00, …, 20:00. The integration fetches once immediately when loaded, then follows the configured schedule. Overnight windows are not currently supported; the end hour must be the same as or later than the start hour.

## Sensors

The integration creates:

- `sensor.green_exchange_usd_buy`
- `sensor.green_exchange_usd_sell`
- `sensor.green_exchange_eur_buy`
- `sensor.green_exchange_eur_sell`

The first number in each Telegram range is exposed as `buy`, and the second as `sell`.

All values are in UAH with two decimal places.

## Updating from GitHub

This repository is designed to work directly from its default branch (`main`); Git tags and GitHub Releases are not required for the branch-based workflow.

1. Make changes on your development machine.
2. Commit and push them to `main`.
3. Marketplace checks custom repositories for updates periodically. When an update appears under **Settings → Updates**, install it.
4. Restart Home Assistant when prompted to load the updated integration code.

Marketplace does not install code immediately on every `git push`. For custom repositories, it needs to detect the new commit and then you install the update.

## Data source and limitations

The integration reads the public Telegram web preview at `https://t.me/s/<channel>` and parses the latest visible post. It expects the post to contain currency markers and numeric ranges similar to:

- 🇺🇸 `46,10-46,35`
- 🇪🇺 `51,80-52,20`

If Telegram cannot be reached or the expected format is missing, the last successfully fetched sensor values remain available. The integration does not authenticate with Telegram.
