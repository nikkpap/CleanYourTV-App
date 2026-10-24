# CleanYourTV App

A Windows desktop app for cleaning up an Android TV over the network: debloat it, install the new
"Apple TV style" launcher, push themes, and put everything back when you want. One file,
`CleanYourTV.pyw`, that opens without a console window.

It is a front end for [Gathin's cleanyourtv toolkit](https://github.com/Gathin23/cleanyourtv)
([cleanyour.tv](https://cleanyour.tv)), which does all the real work: the ADB client, the debloat
lists, the undo records and the launcher. The app downloads the toolkit by itself and keeps it up to
date.

## Run it

1. Install [Python 3.9+](https://www.python.org/downloads/) for Windows.
2. Download `CleanYourTV.pyw` and double-click it. On the first start it installs what it needs
   (PyQt6 and the toolkit's packages), with a splash screen, and makes Desktop and Start menu shortcuts.
3. On the TV: Settings → Device preferences → About → press Build 7 times, then Developer options →
   Network/ADB debugging on. Enter the TV's IP on the Connect page.

`python CleanYourTV.pyw --demo` runs it against a simulated TV.

## What it does

- **Connect**: finds TVs on your network, recognises the model, picks the matching tested list and
  your saved profile for that hardware.
- **Backup**: package list, settings and an undo record before the first change.
- **Debloat**: the toolkit's tested lists, with its guards: core Android packages locked, the app
  that owns Home, the HDMI/tuner inputs and the setup wizard that owns Wi-Fi are skipped; packages
  are disabled, never uninstalled, in small batches with a screenshot from the TV after each one.
- **Extras**: builds and installs the launcher (finds or downloads Java and the Android SDK), with
  options for:
  - the Live TV app as a tile, in the stock launcher's blue;
  - a Live TV channels row, at the top above the apps or after them, where you hide and reorder
    channels (hold OK on one);
  - hold OK on an app for a menu: Open, Move, dock, App info, Uninstall;
  - the remote's Input and Home buttons, AdGuard DNS, animation speed and the clock screensaver.
- **Install apps from the PC**: pick an .apk (or an .apks/.xapk bundle) and it is copied to the TV and
  installed.
- **Copy apps to the PC**: tick one or more apps on the TV and they are saved as .apk / .apks files.
- **Themes**: the toolkit's themes and your own (wallpaper, columns, switches), pushed and verified.
- **Profiles**: save a whole setup and apply it to another box.
- **Finish**: restore, give Home back to the original launcher and remove only the new one (the
  debloat stays), and close network ADB.
- **Launcher report**: which build the TV runs, the Live TV pieces, the theme and any crash, to send
  on when something is off.

The launcher additions (Live TV row, tile menu) are added to the toolkit's launcher code before each
build, and only if every part of it still matches; they are also offered to the toolkit upstream.

## Safety

Nothing is uninstalled from the TV apart from the launcher this app installed, there is no root, and
every change can be undone from the Finish page or with the toolkit's `tools/restore.sh`. Read the
toolkit's [PROMPT.md](https://github.com/Gathin23/cleanyourtv/blob/main/PROMPT.md) for the rules the
app follows. Port 5555 is plaintext: close network ADB when you are done.

## Changes

See [CHANGELOG.md](CHANGELOG.md).

## Credits

- [Gathin](https://github.com/Gathin23): the cleanyourtv toolkit and the launcher (MIT).
- Nikolaos K. Paridis ([nikkpap](https://github.com/nikkpap)), ALU DEV TEAM: this app.

## Licence

MIT, see [LICENSE](LICENSE).
