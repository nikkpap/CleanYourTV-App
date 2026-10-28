# Changelog

## 1.4.4

Build & install: when the launcher on the TV carries another signature (built on another PC, or installed by CleanYourTV Mobile) and Android refuses the update, the app offers to replace it: Home back to the stock launcher, the other copy uninstalled, this build installed and made Home, the theme put back.

## 1.4.3

Launcher: a Bluetooth button in the top bar (Extras, on by default): the paired headphones and speakers, the connected one marked, OK connects one again (or opens the TV's Bluetooth list where the firmware keeps that to itself), Search opens the TV's pairing screen. BLUETOOTH_CONNECT is granted at install.

## 1.4.2

The undo list is also kept on the TV (/data/local/tmp/tidytv/disabled.txt, the same file TidyTV keeps), written before each change. Restore adds what is on it but not in this PC's record, so it works from any PC, and puts back what TidyTV turned off or removed too.

## 1.4.1

Connect → Tailscale: Invite a friend (the 4 steps as a ready message, Greek or English, to copy) and an API key (kept with Windows DPAPI): a new Android TV in your tailnet is named by you and set up on the next Find, tag:tv and no key expiry, so only you reach it and only its ADB port. The tag:tv rules are offered when missing.

## 1.4.0

Connect: TV in another home (Tailscale). Find my Tailscale TVs lists the devices in your Tailscale network, TVs with ADB open first, and connects to the one you pick by its 100.x address; Steps for the TV has the one-time setup there, and Get Tailscale the download. Nothing is forwarded on a router.

## 1.3.10

Backups and profiles are named by the hardware alone, e.g. "SkyworthDigital COSMOTE-TV TV Box (HY44G)": a backup folder adds only the date and time, no IP address; the profile name drops the Android version.

## 1.3.9

Starting a newer version while an older one (1.3.9 on) is open closes the older one and opens the new one, instead of bringing the old window back. The backup folder can no longer point at an old "CleanYourTV backups" folder, in any Documents location: it is Documents/CleanYourTV/backup.

## 1.3.8

Fixes for 1.3.6/1.3.7: a backup could still go to the old Documents/CleanYourTV backups when Windows kept the old folder busy; now the move copies what it cannot rename, and every start points saved folders at Documents/CleanYourTV. The profile name is always the hardware's (with the device code when the model is generic, e.g. "TV Box (HY44G)"), not the matched profile's.

## 1.3.7

Backup → Profiles: the name is filled in from the hardware on connect (maker, brand, model, Android version, e.g. "SkyworthDigital COSMOTE HY44G - Android 14"), and follows the TV you connect to until you type your own.

## 1.3.6

Everything of yours in one folder, Documents/CleanYourTV: `backup`, `profile`, `themes` (My theme included), `apps` and `toolkit`. The old Documents/CleanYourTV * folders and the My theme are moved there once at the first start, and saved settings follow them. Save & apply on My theme offers to keep a named copy in `themes`.

## 1.3.5

Themes: Add themes… takes a .zip of theme folders (or one theme) into Documents/CleanYourTV themes, where a toolkit update never touches them; they show first in the gallery, marked "mine", with their about.txt line and preview. Folder opens that place. Six new themes in `themes/`: aegean-night, meteora-dusk, olympus-mist, neon-grid, oled-black and ellada.

## 1.3.4

Faster start: the toolkit update check and download run in the background after the window opens, and the update is put in place at the next start, from the disk. The splash no longer waits on the network.

## 1.3.3

Backup → Save profile + apps: one <name>.zip with the profile (.cytv), the apps you pick (.apk/.apks) and the launcher switches. Apply to TV on such a zip sets a box of the same kind up in order: apps, launcher build, then the profile (its parts chosen, packages in batches with screenshots, backup and undo first).

## 1.3.2

Debloat: a package Android protects (devicelockcontroller on Android 14 and the like) is reported as that package, with pm's reason, instead of "this firmware refuses to disable packages".

## 1.3.1

Debloat: Report, the enabled packages by category with the tested-list count and note, ready to copy.

## 1.3.0

Extras: copy apps from the TV or box to this PC (one or many, the TV's own too if you want): .apk files, or .apks for apps in parts, named <package>_<version>, md5-checked, ready for Install an app from this PC.

## 1.2.9

The Live TV app is recognised on every brand the toolkit lists: Sony (tvx, tvlin), Philips, MediaTek (Xiaomi, Redmi, Nokia, Toshiba…), TCL, Xiaomi China, OnePlus, Hisense, Skyworth, Whale OS, SmartDevice, Vestel, Realtek, SDMC, Amlogic, Fire TV, Freebox and the generic AOSP / Google apps.

## 1.2.8

Live TV row: each channel once (a TV can list the same one twice: two tuners or a copy per user profile); the hold-OK menu has Unhide all channels and Original channel order.

## 1.2.7

The launcher switches on Extras (Live TV tile, row, icon, position, hold-OK menu, TV button, key helpers) are kept per TV model: a model seen before gets its own choices back on connect; a new one gets suggestions from what the TV has (Live TV app found or not).

## 1.2.6

Only one CleanYourTV runs at a time: starting it again brings the open window to the front.

## 1.2.5

About: keep the toolkit as zip files (toolkit.<date>.<version>.zip in Documents/CleanYourTV toolkit), the newest for use and the one before as a backup; Use the previous one, with updates paused until resumed.

## 1.2.4

Live TV row: hold OK on a channel to hide it, move it (Left/Right, OK places it) or show the hidden ones again. The launcher keeps these by channel number and name, so they survive reboots.

## 1.2.3

Hold-OK menu: Uninstall, for apps you installed (not the TV's own apps); Android asks before removing.

## 1.2.2

After Build & install the TV goes Home once more, so the Live TV row reads the channels with the permission just granted. Launcher report: "applied" when config.xml only carries this app's switch values. Tested: Sony Bravia (com.sony.dtv.tvx) gives the row its channels.

## 1.2.1

Works with the toolkit's newest launcher (single-row Home): the Live TV row and the Open entry were left out of builds since that change. A build without them now says so in a dialog, not only in the log.

## 1.2.0

The remote's TV button opens the TV's Live TV app directly (Sony com.sony.dtv.tvx and the others the app finds), through the Input button helper. A switch on Extras.

## 1.1.9

The launcher logs what the TV's channel list gave the Live TV row (rows, hidden, radio, unnamed), and the Launcher report presses Home first so that line is fresh: for TVs whose row stays empty (Sony).

## 1.1.8

Extras: install an app from this PC (Browse APK…): an .apk, the .apk parts of one app, or an .apks/.xapk bundle, copied to the TV with progress and installed or updated, errors in plain words.

## 1.1.7

The Live TV tile and row follow the TV's own Live TV app, found on connect (Sony com.sony.dtv.tvx, TCL, MediaTek and others), and the build writes it into the launcher's live_tv_package.

## 1.1.6

On/off switches in the iPhone style instead of checkboxes, everywhere in the app.

## 1.1.5

Hold OK on an app opens a menu like the stock launcher's: Open, Move (arrows), dock, App info (the launcher's tile_menu, with Open added; Greek labels). A switch on Extras, on by default.

## 1.1.4

Top Live TV row: the remote moves along the top bar again (Inputs, Wi-Fi, Settings), and Up from a channel goes to the button above it.

## 1.1.3

Live TV row can sit at the top, above the apps (default) or after them; Live TV tile icon in the stock launcher's blue, the app's own, or magenta. Both are options on Extras.

## 1.1.2

Released as CleanYourTV_v<version>.pyw.

## 1.1.1

Build & install turns on the Live TV tile and channels row itself (Extras switches, shared with My theme) and makes a theme already on the TV agree; name and version in the window title.

## 1.1.0

Launcher report; clean build; check the TV got this build; launcher crash report after build and theme; back to the original launcher (removes only the new one); Live TV app as a tile.

## 1.0.0

First release.
