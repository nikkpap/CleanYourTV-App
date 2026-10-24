#!/usr/bin/env python3
"""CleanYourTV - a desktop app for debloating an Android TV over network ADB.

Double-click this file on Windows (it opens without a console window), or run
    python CleanYourTV_v1.3.9.pyw            normal mode
    python CleanYourTV_v1.3.9.pyw --demo     a simulated TV, to try the app without one
Each release is named CleanYourTV_v<version>.pyw; the shortcuts follow the newest file you start.

It is a front end for the tools in this repository, not a replacement for them:
  * tools/tv.py        the ADB connection, shell commands and screenshots
  * tools/recovery.py  the undo record, written before the first change and replayed by Restore,
                       the same record tools/restore.sh and tools/restore.ps1 use
and it carries the same guards as tools/disable.sh: core Android packages are locked, the app that
owns Home, the HDMI/tuner input drivers and a setup wizard that owns the saved Wi-Fi network are
skipped, packages are disabled for user 0 (never uninstalled), one pm command per shell call, in
small batches with a screenshot from the TV after each one.

Needs Python 3.9+ with PyQt6 and the packages in tools/requirements.txt. When they are missing the
app offers to install them.

Changes
  1.3.9  Starting a newer version while an older one (1.3.9 on) is open closes the older one and opens the new one,
         instead of bringing the old window back. The backup folder can no longer point at an old "CleanYourTV
         backups" folder, in any Documents location: it is Documents/CleanYourTV/backup.
  1.3.8  Fixes for 1.3.6/1.3.7: a backup could still go to the old Documents/CleanYourTV backups when Windows kept the
         old folder busy; now the move copies what it cannot rename, and every start points saved folders at
         Documents/CleanYourTV. The profile name is always the hardware's (with the device code when the model is
         generic, e.g. "TV Box (HY44G)"), not the matched profile's.
  1.3.7  Backup → Profiles: the name is filled in from the hardware on connect (maker, brand, model, Android
         version), and follows the TV you connect to until you type your own.
  1.3.6  Everything of yours in one folder, Documents/CleanYourTV: backup, profile, themes (My theme included),
         apps and toolkit; the old Documents/CleanYourTV * folders and the My theme are moved there once, and
         saved settings follow. Save & apply on My theme offers to keep a named copy in themes.
  1.3.5  Themes: Add themes… takes a .zip of theme folders (or one theme) into Documents/CleanYourTV themes, where
         a toolkit update never touches them; they show first in the gallery, marked "mine", with their about.txt
         line and preview. Folder opens that place.
  1.3.4  Faster start: the toolkit update check and download run in the background after the window opens, and the
         update is put in place at the next start, from the disk. The splash no longer waits on the network.
  1.3.3  Backup → Save profile + apps: one <name>.zip with the profile (.cytv), the apps you pick (.apk/.apks) and
         the launcher switches. Apply to TV on such a zip sets a box of the same kind up in order: apps, launcher
         build, then the profile (its parts chosen, packages in batches with screenshots, backup and undo first).
  1.3.2  Debloat: a package Android protects (devicelockcontroller on Android 14 and the like) is reported as that
         package, with pm's reason, instead of "this firmware refuses to disable packages".
  1.3.1  Debloat: Report, the enabled packages by category with the tested-list count and note, ready to copy.
  1.3.0  Extras: copy apps from the TV or box to this PC (one or many, the TV's own too if you want): .apk files,
         or .apks for apps in parts, named <package>_<version>, md5-checked, ready for Install an app from this PC.
  1.2.9  The Live TV app is recognised on every brand the toolkit lists: Sony (tvx, tvlin), Philips, MediaTek
         (Xiaomi, Redmi, Nokia, Toshiba…), TCL, Xiaomi China, OnePlus, Hisense, Skyworth, Whale OS, SmartDevice,
         Vestel, Realtek, SDMC, Amlogic, Fire TV, Freebox and the generic AOSP / Google apps.
  1.2.8  Live TV row: each channel once (a TV can list the same one twice: two tuners or a copy per user profile);
         the hold-OK menu has Unhide all channels and Original channel order.
  1.2.7  The launcher switches on Extras (Live TV tile, row, icon, position, hold-OK menu, TV button, key helpers)
         are kept per TV model: a model seen before gets its own choices back on connect; a new one gets
         suggestions from what the TV has (Live TV app found or not).
  1.2.6  Only one CleanYourTV runs at a time: starting it again brings the open window to the front.
  1.2.5  About: keep the toolkit as zip files (toolkit.<date>.<version>.zip in Documents/CleanYourTV toolkit),
         the newest for use and the one before as a backup; Use the previous one, with updates paused until resumed.
  1.2.4  Live TV row: hold OK on a channel to hide it, move it (Left/Right, OK places it) or show the hidden ones
         again. The launcher keeps these by channel number and name, so they survive reboots.
  1.2.3  Hold-OK menu: Uninstall, for apps you installed (not the TV's own apps); Android asks before removing.
  1.2.2  After Build & install the TV goes Home once more, so the Live TV row reads the channels with the permission
         just granted (it showed only after the next Home press). Launcher report: "applied" when config.xml only
         carries this app's switch values.
  1.2.1  Works with the toolkit's newest launcher (single-row Home): the Live TV row and the Open entry were left out
         of builds since that change. A build without them now says so in a dialog, not only in the log.
  1.2.0  The remote's TV button opens the TV's Live TV app directly (Sony com.sony.dtv.tvx and the others the app
         finds): a KEYCODE_TV app key, through the Input button helper. A switch on Extras.
  1.1.9  The launcher logs what the TV's channel list gave the Live TV row (rows, hidden, radio, unnamed), and the
         Launcher report presses Home first so that line is fresh: for TVs whose row stays empty (Sony).
  1.1.8  Extras: install an app from this PC (Browse APK…): an .apk, the .apk parts of one app, or an
         .apks/.xapk bundle, copied to the TV with progress and installed or updated, errors in plain words.
  1.1.7  The Live TV tile and row follow the TV's own Live TV app, found on connect (Sony com.sony.dtv.tvx, TCL,
         MediaTek and others), and the build writes it into the launcher's live_tv_package.
  1.1.6  On/off switches in the iPhone style instead of checkboxes, everywhere in the app.
  1.1.5  Hold OK on an app opens a menu like the stock launcher's: Open, Move (arrows), dock, App info
         (the launcher's tile_menu, with Open added; Greek labels). A switch on Extras, on by default.
  1.1.4  Top Live TV row: the remote moves along the top bar again (Inputs, Wi-Fi, Settings), and Up from a
         channel goes to the button above it.
  1.1.3  Live TV row can sit at the top, above the apps (default) or after them; Live TV tile icon in the stock
         launcher's blue, the app's own, or magenta. Both are options on Extras.
  1.1.2  Released as CleanYourTV_v<version>.pyw.
  1.1.1  Build & install turns on the Live TV tile and channels row itself (Extras switches, shared with
         My theme) and makes a theme already on the TV agree; name and version in the window title.
  1.1.0  Launcher report; clean build; check the TV got this build; launcher crash report after build
         and theme; back to the original launcher (removes only the new one); Live TV app as a tile.
  1.0.0  First release.
"""
import os
import sys
from pathlib import Path

APP_NAME = "CleanYourTV"
APP_VERSION = "1.3.9"
HERE = Path(__file__).resolve().parent
DEMO = "--demo" in sys.argv
REPO_ZIP = "https://github.com/Gathin23/cleanyourtv/archive/refs/heads/main.zip"
PACKAGES = ["PyQt6", "adb-shell==0.4.4", "rsa==4.9.1", "cryptography>=46.0.7"]   # tools/requirements.txt + Qt
if os.name == "nt":
    APPDATA = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "CleanYourTV"
else:
    APPDATA = Path.home() / ".cleanyourtv"
TOOLKIT_HOME = APPDATA / "toolkit"
TOOLKIT_POINTER = APPDATA / "toolkit-path.txt"

# pythonw.exe starts with no console, so sys.stdout and sys.stderr are None, and the repo's tools
# print and write to stderr. Give them somewhere harmless to go.
class _Null:
    def write(self, *_):
        return 0

    def flush(self):
        pass

    def reconfigure(self, **_):
        pass


if sys.stdout is None:
    sys.stdout = _Null()
if sys.stderr is None:
    sys.stderr = _Null()

NO_WINDOW = 0x08000000 if os.name == "nt" else 0   # CREATE_NO_WINDOW
DETACHED = 0x00000008 if os.name == "nt" else 0    # DETACHED_PROCESS


def _gui_python():
    """pythonw.exe next to the running interpreter: the same Python, without a console window."""
    exe = Path(sys.executable)
    if os.name == "nt" and exe.name.lower() in ("python.exe", "py.exe"):
        w = exe.with_name("pythonw.exe")
        if w.exists():
            return str(w)
    return str(exe)


# Never show a console. Started with python.exe (a double-click with the wrong file association, a terminal,
# an editor's Run button), the app starts itself again with pythonw.exe and this copy leaves at once.
# --console keeps it attached, for reading tracebacks.
if os.name == "nt" and "--console" not in sys.argv and Path(sys.executable).name.lower() == "python.exe" \
        and _gui_python() != sys.executable and not os.environ.get("CYT_NO_SPLASH"):
    import subprocess as _sp
    _sp.Popen([_gui_python(), str(Path(__file__).resolve())] + sys.argv[1:], creationflags=DETACHED | NO_WINDOW,
              close_fds=True)
    sys.exit(0)


# ----------------------------------------------------------------------------------------------
# First run: the Python packages and the cleanyourtv toolkit (tools/, examples/, launcher/).
# The app can live anywhere (Downloads, Desktop); it finds the toolkit or fetches it once.
# ----------------------------------------------------------------------------------------------
def _is_toolkit(path):
    return path is not None and (path / "tools" / "tv.py").is_file() and (path / "tools" / "recovery.py").is_file()


def _find_toolkit():
    candidates = [HERE, HERE / "cleanyourtv", HERE / "cleanyourtv-main", HERE.parent]
    try:
        candidates.insert(0, Path(TOOLKIT_POINTER.read_text(encoding="utf-8").strip()))
    except OSError:
        pass
    candidates += [TOOLKIT_HOME / "cleanyourtv-main", Path.home() / "cleanyourtv",
                   Path.home() / "Documents" / "cleanyourtv", Path.home() / "Downloads" / "cleanyourtv-main",
                   Path.home() / "Downloads" / "cleanyourtv"]
    for c in candidates:
        if _is_toolkit(c):
            return c
    return None


def _console_python():
    exe = Path(sys.executable)
    if exe.name.lower() == "pythonw.exe":
        candidate = exe.with_name("python.exe")
        if candidate.exists():
            return str(candidate)
    return str(exe)


def _missing_modules():
    missing = []
    try:
        import PyQt6.QtSvg  # noqa: F401
    except ImportError:
        missing.append("PyQt6")
    for mod, pkg in (("adb_shell", "adb-shell"), ("rsa", "rsa"), ("cryptography", "cryptography")):
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)
    return missing


def _ensure_qt():
    """First run only: PyQt6 is needed to draw anything, so it comes in behind a small Tk splash."""
    try:
        import PyQt6.QtSvg  # noqa: F401
        return
    except ImportError:
        pass
    import subprocess
    import threading as _th
    try:
        import tkinter
        from tkinter import ttk, messagebox
    except Exception:
        msg = "CleanYourTV needs PyQt6. In a terminal run:\n\n  pip install " + " ".join(PACKAGES)
        sys.stderr.write(msg + "\n")
        if os.name == "nt":   # pythonw has no console to print to
            try:
                import ctypes
                ctypes.windll.user32.MessageBoxW(None, msg, APP_NAME, 0x10)
            except Exception:
                pass
        sys.exit(1)
    root = tkinter.Tk()
    root.overrideredirect(True)
    w, h = 460, 190
    root.geometry(f"{w}x{h}+{(root.winfo_screenwidth() - w) // 2}+{(root.winfo_screenheight() - h) // 2}")
    root.configure(bg="#111216")
    tkinter.Label(root, text="CleanYourTV", bg="#111216", fg="#eceef3", font=("Segoe UI", 18, "bold")).pack(pady=(26, 2))
    tkinter.Label(root, text="First start: installing what the app needs", bg="#111216", fg="#8a909c",
                  font=("Segoe UI", 10)).pack()
    style = ttk.Style(root)
    style.theme_use("default")
    style.configure("C.Horizontal.TProgressbar", troughcolor="#1a1c22", background="#4f7cff", thickness=6,
                    bordercolor="#111216", lightcolor="#4f7cff", darkcolor="#4f7cff")
    bar = ttk.Progressbar(root, style="C.Horizontal.TProgressbar", mode="indeterminate", length=380)
    bar.pack(pady=(20, 8))
    bar.start(12)
    line = tkinter.Label(root, text="Starting pip…", bg="#111216", fg="#5d636f", font=("Segoe UI", 9))
    line.pack()
    state = {"rc": None, "out": []}

    def work():
        in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)   # --user is refused inside a venv
        cmd = [_console_python(), "-m", "pip", "install", "--disable-pip-version-check"] + \
            ([] if in_venv else ["--user"]) + PACKAGES
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=NO_WINDOW)
        for ln in p.stdout:
            state["out"].append(ln)
            state["last"] = ln.strip()[:70]
        state["rc"] = p.wait()

    _th.Thread(target=work, daemon=True).start()

    def poll():
        if state.get("last"):
            line.config(text=state["last"])
        if state["rc"] is None:
            root.after(120, poll)
        else:
            root.quit()

    root.after(120, poll)
    root.mainloop()
    root.destroy()
    if state["rc"] != 0:
        r = tkinter.Tk()
        r.withdraw()
        messagebox.showerror(APP_NAME, "Installing PyQt6 failed:\n\n" + "".join(state["out"])[-1200:])
        sys.exit(1)
    subprocess.Popen([_gui_python(), str(Path(__file__).resolve())] + sys.argv[1:], creationflags=DETACHED | NO_WINDOW)
    sys.exit(0)


_ensure_qt()
# Qt 6.11 on Windows prints a harmless "Failed to register window class ...ThemeChangeObserverWindow" warning
# when its theme observer is set up a second time. Keep the console quiet; every other Qt message stays on.
os.environ["QT_LOGGING_RULES"] = ";".join(filter(None, [os.environ.get("QT_LOGGING_RULES", ""),
                                                        "qt.qpa.windowclass.warning=false"]))

# ----------------------------------------------------------------------------------------------
import contextlib
import io
import ipaddress
import json
import re
import shutil
import socket
import subprocess
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtCore import (QAbstractTableModel, QByteArray, QModelIndex, QObject, QPointF, QProcess,
                          QProcessEnvironment, QRectF, QRunnable, QSettings, QSize,
                          QSortFilterProxyModel, Qt, QEventLoop, QThread, QThreadPool, QTimer, QUrl,
                          QVariantAnimation, QEasingCurve, pyqtSignal)
from PyQt6.QtGui import (QColor, QDesktopServices, QFont, QFontDatabase, QIcon, QImage,
                         QKeySequence, QPainter, QPainterPath, QPen, QPixmap, QShortcut)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog,
                             QFileDialog, QFrame, QGridLayout, QHBoxLayout,
                             QHeaderView, QLabel, QLineEdit, QListWidget, QListWidgetItem,
                             QMainWindow, QMessageBox, QPlainTextEdit, QProgressBar, QPushButton,
                             QScrollArea, QSizePolicy, QSpinBox, QSplitter, QStackedWidget, QStyle,
                             QStyledItemDelegate, QTableView, QVBoxLayout, QWidget)

# PyQt6 ends the whole process on an exception escaping a slot (a button handler), and under pythonw that is a
# silent disappearance. Keep running instead: log it to the Activity log and to error.log for a bug report.
def _excepthook(etype, value, tb):
    import traceback
    text = "".join(traceback.format_exception(etype, value, tb))
    where = Path.home() / ".cleanyourtv" / "error.log"
    try:
        where.parent.mkdir(parents=True, exist_ok=True)
        with open(where, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + f"CleanYourTV {APP_VERSION}\n{text}\n")
    except OSError:
        pass
    try:
        log(f"Unexpected error, the app keeps running (details in {where}):\n{text.strip().splitlines()[-1]}",
            "error")
    except Exception:
        pass
    sys.__stderr__ and sys.__stderr__.write(text)


sys.excepthook = _excepthook

# ----------------------------------------------------------------------------------------------
# Startup splash: packages, toolkit, silent update check, every launch
# ----------------------------------------------------------------------------------------------
TOOLKIT_MANAGED = TOOLKIT_HOME / "cleanyourtv-main"
TOOLKIT_VERSION = TOOLKIT_HOME / "version.json"
LATEST_SHA_URL = "https://api.github.com/repos/Gathin23/cleanyourtv/commits/main"
# Kept across a toolkit update: the ADB key the TV already trusts, the build venv and the build state.
KEEP_ON_UPDATE = ["tools/adbkey", "tools/venv", "launcher/local.properties", "launcher/.gradle", "launcher/app/build"]
TOOLKIT_ZIPS_KEEP = 2    # the newest toolkit zip for use and the one before as a backup (About)
SPLASH_MIN_STEP = 0.45   # seconds each step stays on screen, so the user can read it
SPLASH_MIN_TOTAL = 2.6


def _http(url, accept=None, timeout=8):
    import urllib.request
    headers = {"User-Agent": f"CleanYourTV/{APP_VERSION}"}
    if accept:
        headers["Accept"] = accept
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout)


def _add_user_site():
    import importlib
    import site
    try:
        p = site.getusersitepackages()
        if p and p not in sys.path:
            sys.path.append(p)
    except Exception:
        pass
    importlib.invalidate_caches()


def _installed_version(dist):
    from importlib import metadata
    try:
        return metadata.version(dist)
    except metadata.PackageNotFoundError:
        return None


def _vtuple(v):
    return tuple(int(x) for x in re.findall(r"\d+", v or "")[:4])


def _unmet(requirements_file):
    """Pins from tools/requirements.txt that the installed packages don't meet."""
    specs = list(PACKAGES)
    try:
        specs = [l.split("#", 1)[0].strip() for l in Path(requirements_file).read_text().splitlines()]
        specs = [s for s in specs if s] + ["PyQt6"]
    except OSError:
        pass
    bad = []
    for spec in specs:
        m = re.match(r"([A-Za-z0-9_.\-]+)\s*(==|>=)?\s*([\w.]+)?", spec)
        if not m:
            continue
        name, op, want = m.groups()
        have = _installed_version(name)
        if have is None or (op == "==" and _vtuple(have) != _vtuple(want)) or \
                (op == ">=" and _vtuple(have) < _vtuple(want)):
            bad.append(spec)
    return bad


class StartupWorker(QThread):
    step = pyqtSignal(float, str, str)     # progress 0-1, status, detail
    ready = pyqtSignal(object)             # the toolkit folder
    failed = pyqtSignal(str)

    def say(self, p, status, detail=""):
        self.step.emit(p, status, detail)

    def pause(self, since):
        left = SPLASH_MIN_STEP - (time.time() - since)
        if left > 0:
            time.sleep(left)

    def run(self):
        try:
            self.ready.emit(self.work())
        except Exception as e:
            self.failed.emit(str(e) or type(e).__name__)

    def pip(self, specs, p0, p1):
        in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
        cmd = [_console_python(), "-m", "pip", "install", "--disable-pip-version-check", "--upgrade"] + \
              ([] if in_venv else ["--user"]) + specs
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                creationflags=NO_WINDOW)
        out, n = [], 0
        for line in proc.stdout:
            out.append(line)
            n += 1
            self.say(min(p1, p0 + (p1 - p0) * (1 - 1 / (1 + n / 6))), "Installing " + ", ".join(specs),
                     line.strip()[:90])
        if proc.wait() != 0:
            raise RuntimeError("pip could not install " + ", ".join(specs) + ":\n\n" + "".join(out)[-900:])
        _add_user_site()

    def fetch_toolkit(self, p0, p1, sha=None):
        """Download main.zip and swap it in. The old copy stays until the new one is complete."""
        TOOLKIT_HOME.mkdir(parents=True, exist_ok=True)
        tmp = TOOLKIT_HOME / "download.zip"
        try:
            with _http(REPO_ZIP, timeout=30) as r, open(tmp, "wb") as f:
                total, done = int(r.headers.get("Content-Length") or 0), 0
                while True:
                    buf = r.read(256 * 1024)
                    if not buf:
                        break
                    f.write(buf)
                    done += len(buf)
                    frac = done / total if total else min(0.95, done / 12e6)
                    self.say(p0 + (p1 - p0) * 0.8 * frac, "Downloading the toolkit",
                             f"{done / 1e6:.1f} MB" + (f" of {total / 1e6:.1f} MB" if total else ""))
            self.say(p0 + (p1 - p0) * 0.85, "Unpacking the toolkit")
            old = install_toolkit_zip(tmp, sha)
            try:
                keep_toolkit_zip(tmp, sha)
            except Exception:
                pass   # a full disk or a locked folder must not stop the app
            return old
        finally:
            try:
                tmp.unlink()
            except OSError:
                pass

    def latest_sha(self):
        try:
            with _http(LATEST_SHA_URL, accept="application/vnd.github.sha", timeout=6) as r:
                sha = r.read(80).decode("ascii", "replace").strip()
            return sha if re.fullmatch(r"[0-9a-f]{40}", sha) else None
        except Exception:
            return None

    def work(self):
        t0 = time.time()
        # 1. Python packages
        s = time.time()
        self.say(0.06, "Checking Python packages")
        if not DEMO:
            missing = [p for p in _missing_modules() if p != "PyQt6"]
            if missing:
                self.pip([p for p in PACKAGES if any(p.lower().startswith(m.lower()) for m in missing)], 0.08, 0.3)
        self.pause(s)
        # 2. Toolkit
        s = time.time()
        self.say(0.32, "Looking for the CleanYourTV toolkit")
        repo = _find_toolkit()
        if repo is None and not DEMO:
            sha = self.latest_sha()
            repo = self.fetch_toolkit(0.34, 0.7, sha)
        self.pause(s)
        repo = repo or HERE
        # 3. Silent update check (only the copy this app manages; your own clone is left alone)
        s = time.time()
        self.say(0.72, "Checking for updates")
        managed = _is_toolkit(repo) and TOOLKIT_HOME.resolve() in repo.resolve().parents
        if DEMO:
            self.pause(s)
            self.say(0.82, "Up to date", "demo mode: nothing is downloaded")
        elif managed and QSettings("CleanYourTV", "CleanYourTV").value("toolkit_hold", ""):
            held = QSettings("CleanYourTV", "CleanYourTV").value("toolkit_hold", "")
            self.say(0.84, "Using the previous toolkit", f"version {held[:7]}, updates paused (About)")
        elif managed:
            # The check and the download run in the background once the window is open (download_toolkit_update);
            # here only an update fetched last time is put in place, from the disk: no waiting on the network.
            pending = pending_toolkit()
            if pending:
                zip_path, sha = pending
                self.say(0.76, "Installing the toolkit update", f"version {sha[:7]}, downloaded last time")
                try:
                    repo = install_toolkit_zip(zip_path, sha)
                    try:
                        keep_toolkit_zip(zip_path, sha)
                    except Exception:
                        pass
                    self.say(0.86, "Toolkit updated", f"version {sha[:7]}")
                except Exception as e:
                    self.say(0.86, "Update postponed", str(e)[:90])
                finally:
                    clear_pending_toolkit()
            else:
                try:
                    current = json.loads(TOOLKIT_VERSION.read_text()).get("sha") or ""
                except (OSError, ValueError):
                    current = ""
                self.say(0.84, "Toolkit ready", f"version {current[:7]}" if current else "")
        else:
            self.say(0.84, "Using your own toolkit copy", str(repo)[:90])
        self.pause(s)
        # 4. The toolkit's own pins (tools/requirements.txt), in case an update changed them
        s = time.time()
        self.say(0.88, "Checking requirements")
        if not DEMO:
            bad = _unmet(repo / "tools" / "requirements.txt")
            if bad:
                self.pip(bad, 0.88, 0.95)
        self.pause(s)
        # 5. Done
        self.say(1.0, "Ready")
        left = SPLASH_MIN_TOTAL - (time.time() - t0)
        if left > 0:
            time.sleep(left)
        return repo


def install_toolkit_zip(zip_path, sha=None):
    """Unpack a toolkit zip (GitHub's main.zip layout) and swap it in for the managed copy, keeping the ADB key,
    the build venv and the build state. The old copy stays until the new one is complete."""
    import zipfile
    TOOLKIT_HOME.mkdir(parents=True, exist_ok=True)
    stage = TOOLKIT_HOME / ".staging"
    shutil.rmtree(stage, ignore_errors=True)
    try:
        dest = stage.resolve()
        with zipfile.ZipFile(zip_path) as z:
            for m in z.infolist():
                t = (dest / m.filename).resolve()
                if t != dest and dest not in t.parents:
                    raise RuntimeError(f"unexpected path in the archive: {m.filename}")
            z.extractall(dest)
        new = stage / "cleanyourtv-main"
        if not _is_toolkit(new):
            raise RuntimeError("the zip did not contain the toolkit (tools/tv.py)")
        old = TOOLKIT_MANAGED
        if old.exists():
            for rel in KEEP_ON_UPDATE:
                src = old / rel
                if src.exists():
                    (new / rel).parent.mkdir(parents=True, exist_ok=True)
                    shutil.rmtree(new / rel, ignore_errors=True)
                    shutil.move(str(src), str(new / rel))
            retired = TOOLKIT_HOME / f".old-{int(time.time())}"
            try:
                old.rename(retired)
            except OSError as e:
                # A file in use (a build still running): put the kept items back, try next launch.
                for rel in KEEP_ON_UPDATE:
                    if (new / rel).exists() and not (old / rel).exists():
                        shutil.move(str(new / rel), str(old / rel))
                raise RuntimeError(f"the toolkit is in use, update postponed ({e})")
            new.rename(old)
            shutil.rmtree(retired, ignore_errors=True)
        else:
            new.rename(old)
        if sha:
            TOOLKIT_VERSION.write_text(json.dumps({"sha": sha, "updated": time.strftime("%Y-%m-%d %H:%M")}))
        return old
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def _documents():
    """The Documents folder Windows really uses: OneDrive moves it, so ~/Documents may not be it."""
    from PyQt6.QtCore import QStandardPaths
    d = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
    return Path(d) if d else Path.home() / "Documents"


PENDING_ZIP = TOOLKIT_HOME / "pending.zip"
PENDING_META = TOOLKIT_HOME / "pending.json"


def pending_toolkit():
    """(zip, version) of a toolkit update downloaded in the background last time, or None."""
    try:
        sha = json.loads(PENDING_META.read_text()).get("sha", "")
    except (OSError, ValueError):
        return None
    if PENDING_ZIP.is_file() and re.fullmatch(r"[0-9a-f]{40}", sha or ""):
        return PENDING_ZIP, sha
    return None


def clear_pending_toolkit():
    for f in (PENDING_ZIP, PENDING_META):
        try:
            f.unlink()
        except OSError:
            pass


def latest_toolkit_sha(deadline=10.0):
    """The toolkit's newest version on GitHub, or None when the network does not answer within deadline seconds
    (a slow DNS lookup is not covered by urllib's own timeout, hence the thread)."""
    out = {}

    def ask():
        try:
            with _http(LATEST_SHA_URL, accept="application/vnd.github.sha", timeout=deadline) as r:
                out["sha"] = r.read(80).decode("ascii", "replace").strip()
        except Exception:
            pass

    t = threading.Thread(target=ask, daemon=True)
    t.start()
    t.join(deadline)
    sha = out.get("sha", "")
    return sha if re.fullmatch(r"[0-9a-f]{40}", sha) else None


def download_toolkit_update():
    """In the background while the app runs: when GitHub has a newer toolkit, download it to pending.zip. The next
    start puts it in place before anything uses the toolkit. Returns the new version, or None."""
    import zipfile
    if DEMO or not (TOOLKIT_HOME.resolve() in REPO.resolve().parents):
        return None
    if QSettings("CleanYourTV", "CleanYourTV").value("toolkit_hold", ""):
        return None
    latest = latest_toolkit_sha()
    try:
        current = json.loads(TOOLKIT_VERSION.read_text()).get("sha")
    except (OSError, ValueError):
        current = None
    pend = pending_toolkit()
    if not latest or latest == current or (pend and pend[1] == latest):
        return None
    part = TOOLKIT_HOME / "pending.zip.part"
    with _http(REPO_ZIP, timeout=60) as r, open(part, "wb") as f:
        shutil.copyfileobj(r, f, 256 * 1024)
    with zipfile.ZipFile(part) as z:
        if "cleanyourtv-main/tools/tv.py" not in z.namelist():
            part.unlink()
            raise RuntimeError("the download is not the toolkit")
    part.replace(PENDING_ZIP)
    PENDING_META.write_text(json.dumps({"sha": latest, "downloaded": time.strftime("%Y-%m-%d %H:%M")}))
    return latest


def cyt_home():
    """Documents/CleanYourTV: everything of yours the app keeps, one subfolder per kind."""
    return _documents() / "CleanYourTV"


# Where each kind lived before 1.3.6, as Documents/<old name>, and its subfolder of cyt_home() now.
CYT_FOLDERS = (("CleanYourTV backups", "backup"), ("CleanYourTV profiles", "profile"),
               ("CleanYourTV themes", "themes"), ("CleanYourTV apps", "apps"), ("CleanYourTV toolkit", "toolkit"))


def _merge_move(old, new):
    """Moves old into new; when new exists, moves what new lacks and leaves clashes in old."""
    if not old.exists():
        return
    if not new.exists():
        new.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(old), str(new))
            return
        except OSError:
            new.mkdir(parents=True, exist_ok=True)   # moved child by child below
    for child in list(old.iterdir()):
        if (new / child.name).exists():
            continue
        try:
            shutil.move(str(child), str(new / child.name))
        except OSError:   # Windows refuses a rename while something has the folder open: copy instead
            if child.is_dir():
                shutil.copytree(child, new / child.name)
                shutil.rmtree(child, ignore_errors=True)
            else:
                shutil.copy2(child, new / child.name)
                try:
                    child.unlink()
                except OSError:
                    pass
    try:
        old.rmdir()
    except OSError:
        pass   # a clash left something behind; it stays where it was


def migrate_documents(settings=None):
    """Moves the old Documents/CleanYourTV * folders and the My theme into Documents/CleanYourTV/, once,
    and points saved settings (backup folder, apps folder, applied themes) at the new places."""
    docs, home = _documents(), cyt_home()
    moves = [(docs / old, home / new) for old, new in CYT_FOLDERS]
    moves.append((APPDATA / "my-theme", home / "themes" / "my-theme"))
    done = []
    existed = [(o, n) for o, n in moves if o.exists()]
    for old, new in moves:
        if old.exists():
            try:
                _merge_move(old, new)
            except OSError as e:
                log(f"could not move everything from {old} to {new}: {e}", "warn")
            done.append((old, new))
            if old.exists():
                log(f"{old} still has files in use or with the same name as in {new}; they stay there", "warn")
    for sub in ("backup", "profile", "themes", "apps", "toolkit"):
        try:
            (home / sub).mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
    if settings is not None:   # every start: a setting can still point at an old folder
        done = moves
        for k in settings.allKeys():
            v = settings.value(k)
            if not isinstance(v, str):
                continue
            if "\\" in v or "/" in v:
                tail = Path(v.replace("\\", "/"))
                hit = next(((p, sub) for p in [tail, *tail.parents] for old_name, sub in CYT_FOLDERS
                            if p.name == old_name), None)
                if hit:   # an old folder in any Documents (OneDrive moves it): to its place in CleanYourTV/
                    p, sub = hit
                    rest = tail.relative_to(p)
                    settings.setValue(k, str(home / sub / rest) if str(rest) != "." else str(home / sub))
                    continue
            for old, new in done:
                o = str(old)
                vv, oo = v.replace("/", os.sep).rstrip(os.sep), o.replace("/", os.sep)
                if vv.lower() == oo.lower() or vv.lower().startswith(oo.lower() + os.sep):
                    settings.setValue(k, str(new) + vv[len(oo):])
                    break
    return [(o, n) for o, n in existed if not o.exists()]


def toolkit_archive_dir():
    return cyt_home() / "toolkit"


def toolkit_zips():
    """The kept toolkit zips, newest first."""
    d = toolkit_archive_dir()
    if not d.is_dir():
        return []
    return sorted(d.glob("toolkit.*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)


def toolkit_zip_sha(path):
    m = re.match(r"toolkit\.[0-9-]+\.([0-9a-f]{7,40})\.zip$", Path(path).name)
    return m.group(1) if m else None


def keep_toolkit_zip(src_zip, sha):
    """With the About switch on: a copy of a toolkit zip as toolkit.<date>.<version>.zip in Documents, the newest
    TOOLKIT_ZIPS_KEEP kept. Returns the copy, or None when the switch is off."""
    if QSettings("CleanYourTV", "CleanYourTV").value("keep_toolkit_zips", "false") != "true":
        return None
    d = toolkit_archive_dir()
    d.mkdir(parents=True, exist_ok=True)
    ver = (sha or "unknown")[:7]
    for p in d.glob(f"toolkit.*.{ver}.zip"):   # the same version again: one copy is enough
        p.unlink()
    target = d / f"toolkit.{time.strftime('%Y-%m-%d')}.{ver}.zip"
    shutil.copyfile(src_zip, target)
    for old in toolkit_zips()[TOOLKIT_ZIPS_KEEP:]:
        try:
            old.unlink()
        except OSError:
            pass
    return target


def zip_current_toolkit():
    """The toolkit in use as a zip in the same layout as GitHub's, for the first copy after the switch goes on.
    Leaves out what is this PC's own: the ADB key, the venv and the build state."""
    import zipfile
    import tempfile
    root = TOOLKIT_MANAGED
    if not _is_toolkit(root):
        raise RuntimeError("no toolkit managed by this app on this PC")
    try:
        sha = json.loads(TOOLKIT_VERSION.read_text()).get("sha")
    except (OSError, ValueError):
        sha = None
    skip = [root / r for r in KEEP_ON_UPDATE] + [root / "launcher" / ".livetv-orig"]
    fd, tmp = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for f in root.rglob("*"):
                if not f.is_file() or "__pycache__" in f.parts or any(f == s or s in f.parents for s in skip):
                    continue
                z.write(f, "cleanyourtv-main/" + f.relative_to(root).as_posix())
        return keep_toolkit_zip(tmp, sha)
    finally:
        os.unlink(tmp)


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint |
                         Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(520, 300)
        self.shown_p, self.target_p = 0.0, 0.0
        self.status, self.detail = "Starting", ""
        self.phase = 0.0
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4f7cff" '
               'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" '
               'height="14" rx="2.5"/><polyline points="17 2 12 7 7 2"/></svg>')
        self.logo = QSvgRenderer(QByteArray(svg.encode()))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)
        scr = QApplication.primaryScreen().availableGeometry()
        self.move(scr.center().x() - self.width() // 2, scr.center().y() - self.height() // 2)

    def set_step(self, p, status, detail):
        self.target_p = max(self.target_p, p)
        self.status, self.detail = status, detail
        self.update()

    def tick(self):
        self.shown_p += (self.target_p - self.shown_p) * 0.12
        self.phase = (self.phase + 0.012) % 1.0
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect()).adjusted(8, 8, -8, -8)
        path = QPainterPath()
        path.addRoundedRect(r, 20, 20)
        p.fillPath(path, QColor("#111216"))
        # soft accent glow at the top
        from PyQt6.QtGui import QRadialGradient
        g = QRadialGradient(QPointF(r.center().x(), r.top()), r.width() * 0.55)
        g.setColorAt(0, QColor(79, 124, 255, 70))
        g.setColorAt(1, QColor(79, 124, 255, 0))
        p.save()
        p.setClipPath(path)
        p.fillRect(r, g)
        p.restore()
        p.setPen(QPen(QColor("#24262e"), 1))
        p.drawPath(path)
        self.logo.render(p, QRectF(r.center().x() - 28, r.top() + 34, 56, 56))
        p.setPen(QColor("#eceef3"))
        f = QFont(self.font())
        f.setPointSizeF(20)
        f.setWeight(QFont.Weight.DemiBold)
        p.setFont(f)
        p.drawText(QRectF(r.left(), r.top() + 98, r.width(), 36), Qt.AlignmentFlag.AlignCenter, APP_NAME)
        f.setPointSizeF(9.5)
        f.setWeight(QFont.Weight.Normal)
        p.setFont(f)
        p.setPen(QColor("#8a909c"))
        p.drawText(QRectF(r.left(), r.top() + 134, r.width(), 20), Qt.AlignmentFlag.AlignCenter,
                   f"Version {APP_VERSION}  ·  Android TV debloat")
        # progress bar with a moving sheen
        bar = QRectF(r.left() + 56, r.top() + 182, r.width() - 112, 6)
        bp = QPainterPath()
        bp.addRoundedRect(bar, 3, 3)
        p.fillPath(bp, QColor("#1f2128"))
        fill = QRectF(bar.left(), bar.top(), max(6.0, bar.width() * self.shown_p), bar.height())
        fp = QPainterPath()
        fp.addRoundedRect(fill, 3, 3)
        p.fillPath(fp, QColor("#4f7cff"))
        sheen_x = fill.left() + (fill.width() + 60) * self.phase - 60
        from PyQt6.QtGui import QLinearGradient
        lg = QLinearGradient(sheen_x, 0, sheen_x + 60, 0)
        lg.setColorAt(0, QColor(255, 255, 255, 0))
        lg.setColorAt(0.5, QColor(255, 255, 255, 90))
        lg.setColorAt(1, QColor(255, 255, 255, 0))
        p.save()
        p.setClipPath(fp)
        p.fillRect(fill, lg)
        p.restore()
        f.setPointSizeF(10)
        f.setWeight(QFont.Weight.DemiBold)
        p.setFont(f)
        p.setPen(QColor("#eceef3"))
        p.drawText(QRectF(bar.left(), bar.bottom() + 12, bar.width() - 50, 20),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.status + "…" * (self.shown_p < 0.995))
        p.setPen(QColor("#8a909c"))
        p.drawText(QRectF(bar.left(), bar.bottom() + 12, bar.width(), 20),
                   Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{int(self.shown_p * 100)}%")
        f.setPointSizeF(8.5)
        f.setWeight(QFont.Weight.Normal)
        p.setFont(f)
        p.setPen(QColor("#5d636f"))
        detail = p.fontMetrics().elidedText(self.detail, Qt.TextElideMode.ElideMiddle, int(bar.width()))
        p.drawText(QRectF(bar.left(), bar.bottom() + 32, bar.width(), 18),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, detail)
        p.drawText(QRectF(r.left(), r.bottom() - 30, r.width(), 18), Qt.AlignmentFlag.AlignCenter,
                   "by Nikolaos K. Paridis  ·  toolkit by Gathin")
        p.end()


_QAPP = None   # the one QApplication: kept here so the splash's app is the main window's app too


def make_app():
    global _QAPP
    app = QApplication.instance() or QApplication(sys.argv)
    _QAPP = app
    app.setApplicationName(APP_NAME)
    app.setStyle("Fusion")
    fams = set(QFontDatabase.families())
    for fam in ("Segoe UI Variable Text", "Segoe UI", "Inter", "SF Pro Text", "Noto Sans", "DejaVu Sans"):
        if fam in fams:
            f = QFont(fam, 10)
            f.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
            app.setFont(f)
            break
    return app


_INSTANCE = None   # the QLocalServer that marks this copy of the app as the running one


def single_instance():
    """True when this is the only CleanYourTV running. Otherwise the running one is asked to come to the front and
    this one should quit: two copies would share one ADB connection, one settings file and one toolkit folder."""
    global _INSTANCE
    import getpass
    from PyQt6.QtNetwork import QLocalServer, QLocalSocket
    make_app()
    try:
        user = getpass.getuser()
    except Exception:
        user = "user"
    name = "CleanYourTV-" + re.sub(r"[^A-Za-z0-9]", "_", user)
    probe = QLocalSocket()
    probe.connectToServer(name)
    if probe.waitForConnected(500):
        # "show <version>": an older copy that is running steps aside for this newer one ("yield") and closes;
        # the same or a newer one comes to the front and this start quits.
        probe.write(f"show {APP_VERSION}\n".encode())
        probe.flush()
        probe.waitForBytesWritten(500)
        answer = bytes(probe.readAll()) if probe.waitForReadyRead(1500) else b""
        probe.disconnectFromServer()
        if b"yield" not in answer:
            return False
        for _ in range(60):   # up to 15 s for the older copy to finish closing
            time.sleep(0.25)
            p2 = QLocalSocket()
            p2.connectToServer(name)
            if not p2.waitForConnected(200):
                break
            p2.disconnectFromServer()
        else:
            return False
    QLocalServer.removeServer(name)   # a socket file left by a crash (Linux/macOS); nothing on Windows
    _INSTANCE = QLocalServer()
    _INSTANCE.listen(name)
    return True


def bring_to_front(win):
    """Another start of the app asked for the running one: show the window, restored and on top."""
    if _INSTANCE is None:
        return

    def newer(v):
        try:
            return tuple(int(x) for x in v.split(".")) > tuple(int(x) for x in APP_VERSION.split("."))
        except ValueError:
            return False

    def show():
        step_aside = False
        while _INSTANCE.hasPendingConnections():
            c = _INSTANCE.nextPendingConnection()
            c.disconnected.connect(c.deleteLater)
            line = bytes(c.readAll()) if (c.bytesAvailable() or c.waitForReadyRead(300)) else b""
            parts = line.decode("utf-8", "replace").split()
            if len(parts) >= 2 and parts[0] == "show" and newer(parts[1]):
                c.write(b"yield\n")
                c.flush()
                c.waitForBytesWritten(500)
                step_aside = True
        if step_aside:
            log("a newer CleanYourTV was started; this one closes so it can take over", "info")
            _INSTANCE.close()
            QTimer.singleShot(100, win.close)
            QTimer.singleShot(300, QApplication.quit)
            return
        win.setWindowState((win.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive)
        win.showNormal() if win.isMinimized() else win.show()
        win.raise_()
        win.activateWindow()
        QApplication.alert(win, 3000)   # flashes the taskbar button where Windows will not hand over the focus

    _INSTANCE.newConnection.connect(show)
    if _INSTANCE.hasPendingConnections():   # someone knocked while the splash was still up
        QTimer.singleShot(0, show)


def startup():
    """Show the splash, run the checks, return the toolkit folder."""
    if __name__ == "__main__" and not os.environ.get("CYT_MULTI") and not single_instance():
        sys.exit(0)
    if os.environ.get("CYT_NO_SPLASH"):
        return _find_toolkit() or HERE
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("CleanYourTV.App")
        except Exception:
            pass
    make_app()   # kept in _QAPP: the main window reuses this same application
    while True:
        splash = SplashScreen()
        splash.show()
        worker = StartupWorker()
        result = {}
        loop = QEventLoop()
        worker.step.connect(splash.set_step)
        worker.ready.connect(lambda r: (result.update(repo=r), loop.quit()))
        worker.failed.connect(lambda m: (result.update(error=m), loop.quit()))
        worker.start()
        loop.exec()
        worker.wait()
        splash.close()
        if "repo" in result:
            return Path(result["repo"])
        box = QMessageBox()
        box.setWindowTitle(APP_NAME)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setText("CleanYourTV could not get ready.")
        box.setInformativeText(result.get("error", "")[:1500] + "\n\nCheck the internet connection and try again, "
                               "or pick a cleanyourtv folder you already have.")
        retry = box.addButton("Try again", QMessageBox.ButtonRole.AcceptRole)
        pick = box.addButton("Choose folder…", QMessageBox.ButtonRole.ActionRole)
        box.addButton("Quit", QMessageBox.ButtonRole.RejectRole)
        box.exec()
        if box.clickedButton() is retry:
            continue
        if box.clickedButton() is pick:
            d = QFileDialog.getExistingDirectory(None, "Pick the cleanyourtv folder (with tools and examples)")
            if d and _is_toolkit(Path(d)):
                return Path(d)
            continue
        sys.exit(1)


REPO = startup()
if _is_toolkit(REPO):
    try:
        APPDATA.mkdir(parents=True, exist_ok=True)
        TOOLKIT_POINTER.write_text(str(REPO), encoding="utf-8")
    except OSError:
        pass
TOOLS = REPO / "tools"
EXAMPLES = REPO / "examples"
LAUNCHER = REPO / "launcher"

sys.path.insert(0, str(TOOLS))
# tools/tv.py exits at import when TV_HOST is unset; the real address is set on connect.
os.environ.setdefault("TV_HOST", "0.0.0.0")
if DEMO:
    tvmod = None
    try:
        import recovery as recmod
    except Exception:
        recmod = None
else:
    import tv as tvmod
    import recovery as recmod

DATA = Path.home() / ".cleanyourtv"
GUI_LISTS = DATA / "gui-lists"
SHOTS = DATA / "shots"


DEFAULT_BACKUPS = cyt_home() / "backup"
PACKAGE_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)+")
COMPONENT_RE = re.compile(r"^([A-Za-z0-9_.]+)/([A-Za-z0-9_.$]+)$")
HOME_QUERY = "cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME"
HOME_CLAIMS = "cmd package query-activities --brief -a android.intent.action.MAIN -c android.intent.category.HOME"
SETUPWRAITH = "com.google.android.tungsten.setupwraith"
OUR_LAUNCHER = "com.gathin.tvhome"
KNOWN_STOCK = ["com.google.android.tvlauncher", "com.google.android.apps.tv.launcherx",
               "com.google.android.leanbacklauncher", "com.mitv.tvhome"]
NOT_LAUNCHERS = {SETUPWRAITH, "com.android.tv.settings", "com.android.settings", "com.android.provision"}

# Same patterns as tools/disable.sh, disable.ps1 and recovery.py (#884).
CORE_RE = re.compile(r"^(android|com\.android\.systemui|com\.android\.shell|com\.android\.phone|com\.android\.settings|com\.android\.tv\.settings|com\.(google\.)?android\.(permissioncontroller|packageinstaller|ext\.services|ext\.shared|modulemetadata)|com\.google\.android\.overlay\.modules.*|com\.android\.providers\..*)$")
CORE_OK = re.compile(r"^com\.android\.providers\.(calendar|contacts|userdictionary|blockednumber)$")


def is_core(name):
    return bool(CORE_RE.match(name)) and not CORE_OK.match(name)


# ----------------------------------------------------------------------------------------------
# Theme
# ----------------------------------------------------------------------------------------------
C = {
    "bg": "#0c0d10", "side": "#111216", "card": "#15161b", "card2": "#1a1c22", "line": "#24262e",
    "line2": "#2e313b", "text": "#eceef3", "muted": "#8a909c", "dim": "#5d636f",
    "accent": "#4f7cff", "accent2": "#6a91ff", "ok": "#35d39a", "warn": "#ffb547", "bad": "#ff5d6e",
    "violet": "#a98bff", "teal": "#3cc8d8", "sky": "#5cb3ff",
}

CATEGORIES = {
    # key: (label, colour, ask-before-disabling, description)
    "core":       ("Core – locked", "#ff5d6e", True,  "Android itself needs this. The app will never disable it."),
    "factory":    ("Factory", "#8a909c", True,  "Factory/test menu. Never launch it; leave it alone unless a tested list disables it."),
    "launcher":   ("Launcher", "#5cb3ff", True,  "Answers the Home button. Guarded: kept while nothing else can take Home."),
    "keep":       ("Keep – TV needs it", "#35d39a", True,  "Inputs, tuner, remote, Bluetooth, keyboard, Play Store/Services or setup."),
    "telemetry":  ("Telemetry", "#ff7a59", False, "Analytics, logging, usage reporting or ACR."),
    "ads":        ("Ads & content", "#ffb547", False, "Ads, recommendation rows, promos, demo content."),
    "background": ("Background", "#e6d35a", False, "Cleaners, share/transfer duplicates, tips, user centre."),
    "voice":      ("Voice", "#a98bff", True,  "Voice assistant / hotword. Your remote's mic button may need it."),
    "cast":       ("Cast / mirror", "#a98bff", True,  "Chromecast, Miracast, DIAL, DLNA, screen mirroring."),
    "update":     ("Updates", "#a98bff", True,  "System or app update service."),
    "streaming":  ("Streaming", "#3cc8d8", True,  "A streaming app. Only disable it if you never use it."),
    "preload":    ("Preloaded app", "#7d8cff", True,  "An app that came installed. Disable only what you don't use."),
    "system":     ("System", "#5d636f", False, "Other system package. Check Details before disabling."),
}
ASK_CATEGORIES = {k for k, v in CATEGORIES.items() if v[2]}

RULES = [
    ("factory", r"factory|fac\.menu|hkcfac|\.at\.factory|productiontest|factorymenu|factorytest|factory_test|\.fac\b"),
    ("launcher", r"launcher|tvhome|homescreen|firehomestarter|\.home$"),
    ("keep", r"^com\.android\.vending$|^com\.google\.android\.gms$|^com\.google\.android\.gsf|inputmethod|\.ime$|\.ime\.|leanbackime|keyboard|bluetooth|tvinput|livetv|\.tv\.input|tuner|channelscan|hdmi|\.cec|remotecontrol|\.rcu|systemui|webview|tvprovider|mediabrowser|\.oobe|setupwizard|setupwraith|mediatek\.tv|tvserver|inputsource|sourcemenu|\.tvsource|fireinputdevices|uxcontroller|autopair"),
    ("telemetry", r"analytic|telemetry|metric|logger|logcollect|\.log\.|feedback|bugreport|crash|diagnos|\.acr\b|\.acr\.|inscape|tracking|tracker|statistic|\.stats|usagestat|\.report|samba|alibi|dpcclient|candeebug|\.gel$|perfcollect|hedwig"),
    ("ads", r"(^|\.)ads?(\.|$)|adservice|advert|recommend|patchwall|promo|shoptv|\.shop|democontent|\.demo|sneakpeek|screensaver|banner|tvrecommendation|partnercustomizer|\.mall\b|aisense|\.sponsor"),
    ("voice", r"katniss|alexa|assistant|voice|speech|hotword|vizzini|pumpkin|\.vui|\.asr|aiassist|xiaoai"),
    ("cast", r"(?<!broad)cast|miracast|dialservice|\.dial$|dlna|mirror|airplay|\.wfd|whisperplay|whisperlink|fling"),
    ("update", r"(^|\.)ota(\.|$)|update|upgrade|fota"),
    ("streaming", r"netflix|youtube|primevideo|\.avod|firebat|disney|spotify|hulu|hbo|twitch|plex|kodi|atve|appletv|paramount|peacock|dazn|deezer|tidal|crunchyroll|pluto|rakuten|iqiyi|qqlive|bilibili|ertflix|mubi|tubi|viki|vimeo|skyshowtime|canalplus|joyn|zdf|ardmediathek|bbc\.iplayer|itv|vix|rtve|rai\.play|mediaset"),
    ("background", r"clean|boost|optimi|\.share|transfer|filemanager|\.wallpaper|weather|\.news\b|\.tips|\.help\b|userguide|usercenter|\.manual"),
]
RULES = [(k, re.compile(p)) for k, p in RULES]


def categorize(name, system):
    if is_core(name):
        return "core"
    low = name.lower()
    for key, rx in RULES:
        if rx.search(low):
            return key
    return "system" if system else "preload"


ICONS = {
    "tv": '<rect x="2" y="7" width="20" height="14" rx="2.5"/><polyline points="17 2 12 7 7 2"/>',
    "backup": '<rect x="3" y="3" width="18" height="5" rx="1.5"/><path d="M5 8v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.3 7 12 12 20.7 7"/><line x1="12" y1="22" x2="12" y2="12"/>',
    "remote": '<rect x="7" y="2" width="10" height="20" rx="3"/><circle cx="12" cy="8" r="2.2"/><path d="M12 14h.01M12 17.5h.01"/>',
    "spark": '<path d="M12 3l1.9 5.6L19.5 10.5l-5.6 1.9L12 18l-1.9-5.6L4.5 10.5l5.6-1.9z"/><path d="M19 3v3M17.5 4.5h3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-2.6-6.4"/><polyline points="21 3 21 9 15 9"/>',
    "camera": '<path d="M4 7h3l2-3h6l2 3h3a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="4"/>',
    "home": '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/>',
    "back": '<path d="M9 14 4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/>',
    "menu": '<line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/>',
    "volup": '<path d="M11 5 6 9H3v6h3l5 4z"/><path d="M16 9a4 4 0 0 1 0 6"/><path d="M19 6a8 8 0 0 1 0 12"/>',
    "voldown": '<path d="M11 5 6 9H3v6h3l5 4z"/><path d="M16 9a4 4 0 0 1 0 6"/>',
    "mute": '<path d="M11 5 6 9H3v6h3l5 4z"/><line x1="22" y1="9" x2="16" y2="15"/><line x1="16" y1="9" x2="22" y2="15"/>',
    "play": '<polygon points="7 4 19 12 7 20 7 4"/>',
    "input": '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M8 21h8M12 17v4"/><path d="m10 9 3 2-3 2"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    "power": '<path d="M18.4 6.6a9 9 0 1 1-12.8 0"/><line x1="12" y1="2" x2="12" y2="12"/>',
    "folder": '<path d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "plug": '<path d="M9 2v6M15 2v6"/><path d="M6 8h12v4a6 6 0 0 1-12 0z"/><path d="M12 18v4"/>',
    "wifi": '<path d="M2 8.8a15 15 0 0 1 20 0"/><path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8.5 16a5 5 0 0 1 7 0"/><path d="M12 19.5h.01"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "undo": '<path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-15-6.7L3 13"/>',
    "log": '<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "save": '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>',
    "palette": '<circle cx="13.5" cy="6.5" r="1"/><circle cx="17.5" cy="10.5" r="1"/><circle cx="8.5" cy="7.5" r="1"/><circle cx="6.5" cy="12.5" r="1"/><path d="M12 2a10 10 0 0 0 0 20 2 2 0 0 0 2-2v-.5a2 2 0 0 1 2-2h1.5A4.5 4.5 0 0 0 22 13 10 10 0 0 0 12 2z"/>',
    "keyboard": '<rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 14h10"/>',
}


def icon(name, color=None, size=20):
    color = color or C["text"]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" '
           f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')
    renderer = QSvgRenderer(QByteArray(svg.encode()))
    ico = QIcon()
    for scale in (1, 2):
        pm = QPixmap(size * scale, size * scale)
        pm.fill(Qt.GlobalColor.transparent)
        p = QPainter(pm)
        renderer.render(p)
        p.end()
        pm.setDevicePixelRatio(scale)
        ico.addPixmap(pm)
    return ico


def _write_check_svg():
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / "ui-check.svg"
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" '
                    'stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">'
                    '<polyline points="20 6 9 17 4 12"/></svg>')
    return path.as_posix()


def stylesheet():
    check = _write_check_svg()
    return f"""
    * {{ outline: none; }}
    QWidget {{ background: {C['bg']}; color: {C['text']}; font-size: 10pt; }}
    QToolTip {{ background: {C['card2']}; color: {C['text']}; border: 1px solid {C['line2']}; padding: 6px 8px; border-radius: 6px; }}
    #Sidebar {{ background: {C['side']}; border-right: 1px solid {C['line']}; }}
    #Sidebar QLabel {{ background: transparent; }}
    QPushButton#Nav {{ text-align: left; padding: 10px 12px; border: none; border-radius: 10px;
        background: transparent; color: {C['muted']}; font-weight: 600; }}
    QPushButton#Nav:hover {{ background: #191b21; color: {C['text']}; }}
    QPushButton#Nav:checked {{ background: #1c2232; color: white; }}
    QFrame#Card {{ background: {C['card']}; border: 1px solid {C['line']}; border-radius: 14px; }}
    QFrame#Card QLabel, QFrame#Card QCheckBox {{ background: transparent; }}
    QFrame#Card QWidget#Clear {{ background: transparent; }}
    QFrame#Banner {{ border-radius: 12px; }}
    QFrame#Banner QLabel {{ background: transparent; }}
    QLabel#H1 {{ font-size: 19pt; font-weight: 650; }}
    QLabel#H2 {{ font-size: 11.5pt; font-weight: 650; }}
    QLabel#Muted {{ color: {C['muted']}; }}
    QLabel#Dim {{ color: {C['dim']}; font-size: 9pt; }}
    QLabel#Key {{ color: {C['muted']}; font-size: 9pt; }}
    QLabel#Val {{ font-weight: 600; }}
    QLabel#Big {{ font-size: 24pt; font-weight: 300; }}
    QPushButton {{ background: {C['card2']}; border: 1px solid {C['line2']}; border-radius: 9px;
        padding: 8px 14px; color: {C['text']}; font-weight: 600; }}
    QPushButton:hover {{ background: #22252d; border-color: #3a3e4a; }}
    QPushButton:pressed {{ background: #191b20; }}
    QPushButton:disabled {{ color: {C['dim']}; background: #14151a; border-color: {C['line']}; }}
    QPushButton#Primary {{ background: {C['accent']}; border: 1px solid {C['accent2']}; color: white; }}
    QPushButton#Primary:hover {{ background: {C['accent2']}; }}
    QPushButton#Primary:disabled {{ background: #23304f; border-color: #2a3a60; color: #8797c0; }}
    QPushButton#Danger {{ background: #2a1519; border: 1px solid #5b2730; color: #ff8d99; }}
    QPushButton#Danger:hover {{ background: #361a20; }}
    QPushButton#Ghost {{ background: transparent; border: 1px solid transparent; color: {C['muted']}; }}
    QPushButton#Ghost:hover {{ background: {C['card2']}; color: {C['text']}; }}
    QPushButton#Key {{ background: {C['card2']}; border: 1px solid {C['line2']}; border-radius: 22px;
        min-width: 44px; min-height: 44px; max-width: 44px; max-height: 44px; padding: 0; }}
    QPushButton#Key:hover {{ background: #262a34; }}
    QPushButton#Key:pressed {{ background: {C['accent']}; }}
    QLineEdit, QSpinBox, QComboBox {{ background: #0f1014; border: 1px solid {C['line2']}; border-radius: 9px;
        padding: 7px 10px; selection-background-color: {C['accent']}; }}
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{ border: 1px solid {C['accent']}; }}
    QComboBox::drop-down {{ border: none; width: 22px; }}
    QComboBox QAbstractItemView {{ background: {C['card']}; border: 1px solid {C['line2']};
        selection-background-color: #1f2a44; padding: 4px; outline: none; }}
    QSpinBox::up-button, QSpinBox::down-button {{ width: 0; border: none; }}
    QPlainTextEdit {{ background: #0a0b0d; border: none; border-top: 1px solid {C['line']};
        font-family: "Cascadia Mono", "Consolas", "JetBrains Mono", monospace; font-size: 9pt; color: #b9bfcb; }}
    QPlainTextEdit#Box {{ border: 1px solid {C['line2']}; border-radius: 10px; padding: 6px; }}
    QTableView {{ background: {C['card']}; border: 1px solid {C['line']}; border-radius: 12px;
        gridline-color: transparent; alternate-background-color: #17181e; selection-background-color: #1d2740;
        selection-color: {C['text']}; }}
    QTableView::item {{ padding: 4px 6px; border: none; }}
    QHeaderView::section {{ background: {C['card']}; color: {C['muted']}; border: none;
        border-bottom: 1px solid {C['line']}; padding: 8px 6px; font-weight: 600; }}
    QTableCornerButton::section {{ background: {C['card']}; border: none; }}
    QListWidget {{ background: {C['card']}; border: 1px solid {C['line']}; border-radius: 10px; padding: 4px; }}
    QListWidget::item {{ padding: 7px 8px; border-radius: 7px; }}
    QListWidget::item:selected {{ background: #1d2740; color: {C['text']}; }}
    QListWidget::item:hover {{ background: #1b1d23; }}
    QScrollArea {{ border: none; }}
    QScrollBar:vertical {{ background: transparent; width: 10px; margin: 3px; }}
    QScrollBar::handle:vertical {{ background: #2b2f39; border-radius: 4px; min-height: 30px; }}
    QScrollBar::handle:vertical:hover {{ background: #3a3f4c; }}
    QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 3px; }}
    QScrollBar::handle:horizontal {{ background: #2b2f39; border-radius: 4px; min-width: 30px; }}
    QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
    QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}
    QCheckBox {{ spacing: 9px; }}
    QCheckBox::indicator, QTableView::indicator, QListWidget::indicator {{ width: 16px; height: 16px;
        border-radius: 5px; border: 1px solid #3b404c; background: #0f1014; }}
    QCheckBox::indicator:hover, QTableView::indicator:hover {{ border-color: {C['accent']}; }}
    QCheckBox::indicator:checked, QTableView::indicator:checked, QListWidget::indicator:checked {{
        background: {C['accent']}; border-color: {C['accent']}; image: url({check}); }}
    QProgressBar {{ background: #0f1014; border: 1px solid {C['line2']}; border-radius: 6px; height: 10px;
        text-align: center; color: transparent; }}
    QProgressBar::chunk {{ background: {C['accent']}; border-radius: 5px; }}
    QSplitter::handle {{ background: {C['line']}; }}
    QDialog {{ background: {C['card']}; }}
    QDialog QLabel, QDialog QCheckBox, QDialog QWidget#Clear {{ background: transparent; }}
    QMessageBox {{ background: {C['card']}; }}
    QMessageBox QLabel {{ background: transparent; }}
    """


# ----------------------------------------------------------------------------------------------
# Background work
# ----------------------------------------------------------------------------------------------
class Bus(QObject):
    log = pyqtSignal(str, str)            # level, text
    shot = pyqtSignal(str)                # path of a new screenshot from the TV
    connection = pyqtSignal(bool, dict)   # connected?, device info
    packages_changed = pyqtSignal()


BUS = None


def log(text, level="info"):
    if BUS is not None:
        BUS.log.emit(level, text)


class JobSignals(QObject):
    result = pyqtSignal(object)
    error = pyqtSignal(str)
    done = pyqtSignal()


class Job(QRunnable):
    """Runs fn(*args) off the UI thread. The result or the error comes back as a signal."""
    _alive = set()

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn, self.args, self.kwargs = fn, args, kwargs
        self.signals = JobSignals()
        self.setAutoDelete(True)

    def run(self):
        try:
            value = self.fn(*self.args, **self.kwargs)
        except SystemExit as e:   # the repo's tools stop with SystemExit and a readable message
            self.signals.error.emit(str(e.code) if e.code not in (None, 0, 1) else "stopped")
        except RuntimeError as e:   # the app's own messages, written for people: no class name in front
            self.signals.error.emit(str(e) or type(e).__name__)
        except Exception as e:
            self.signals.error.emit(f"{type(e).__name__}: {e}" if str(e) else type(e).__name__)
        else:
            self.signals.result.emit(value)
        finally:
            self.signals.done.emit()
            Job._alive.discard(self)


# One thread talks to the TV, so commands never interleave on the connection.
TV_POOL = QThreadPool()
TV_POOL.setMaxThreadCount(1)
NET_POOL = QThreadPool()
NET_POOL.setMaxThreadCount(4)


def run_job(fn, *args, on_result=None, on_error=None, on_done=None, pool=None, **kwargs):
    job = Job(fn, *args, **kwargs)
    if on_result:
        job.signals.result.connect(on_result)
    job.signals.error.connect(on_error or (lambda m: log(m, "error")))
    if on_done:
        job.signals.done.connect(on_done)
    Job._alive.add(job)
    (pool or TV_POOL).start(job)
    return job


# ----------------------------------------------------------------------------------------------
# The TV
# ----------------------------------------------------------------------------------------------
class FakeDev:
    """A simulated Google TV for --demo, answering the commands this app sends."""

    def __init__(self):
        self.pkgs = {
            # name: system?
            "android": True, "com.android.systemui": True, "com.android.shell": True,
            "com.android.tv.settings": True, "com.android.providers.settings": True,
            "com.android.providers.tv": True, "com.android.permissioncontroller": True,
            "com.android.packageinstaller": True, "com.android.vending": True,
            "com.google.android.gms": True, "com.google.android.gsf": True,
            "com.google.android.apps.tv.launcherx": True, SETUPWRAITH: True,
            "com.google.android.tvrecommendations": True, "com.google.android.katniss": True,
            "com.google.android.speech.pumpkin": True, "com.google.android.apps.mediashell": True,
            "com.google.android.feedback": True, "com.google.android.leanbackime": True,
            "com.google.android.tv.remote.service": True, "com.android.bluetooth": True,
            "com.mediatek.tvinput": True, "com.mediatek.wwtv.tvcenter": True,
            "com.tcl.tvweishi": True, "com.tcl.usercenter": True, "com.tcl.ui_mediaCenter": True,
            "com.tcl.partnercustomizer": True, "com.tcl.guard": True, "com.tcl.versionupdateApp": True,
            "com.tcl.waterfall.overseas": True, "com.tcl.logger": True, "com.tcl.screensaver": True,
            "com.tcl.factory.view": True, "com.tcl.tvinput": True, "com.tcl.MultiScreenInteraction_TV": True,
            "com.tcl.esticker": True, "com.tcl.messagebox": True, "com.tcl.common.weather": True,
            "tv.inscape.tvclient.inscapeacr": True, "com.google.android.youtube.tv": True,
            "com.netflix.ninja": True, "com.amazon.amazonvideo.livingroom": False,
            "com.disney.disneyplus": False, "com.spotify.tv.android": False, "com.android.webview": True,
            "com.google.android.tv.frameworkpackagestubs": True, "com.android.providers.calendar": True,
            "com.google.android.apps.tv.dreamx": True, "com.google.android.tungsten.overscan": True,
            "com.android.printspooler": True, "com.android.dreams.basic": True, OUR_LAUNCHER: False,
        }
        self.disabled = {"com.android.printspooler"}
        self.props = {
            "ro.product.model": "Smart TV Pro (demo)", "ro.product.device": "G10_demo",
            "ro.product.manufacturer": "TCL", "ro.build.version.release": "12",
            "ro.build.version.sdk": "31", "ro.build.display.id": "V8-R51MT05-LF1V3.0 (demo)",
            "ro.adb.secure": "1", "service.adb.tcp.port": "5555", "sys.boot_completed": "1",
        }
        self.settings = {"private_dns_mode": "opportunistic", "private_dns_specifier": "null",
                         "window_animation_scale": "1.0", "transition_animation_scale": "1.0",
                         "animator_duration_scale": "1.0",
                         "screen_off_timeout": "900000"}
        self.focus = 0

    def shell(self, cmd, read_timeout_s=None, **_):
        time.sleep(0.04)
        c = cmd.strip()
        if c == "getprop":
            return "\n".join(f"[{k}]: [{v}]" for k, v in self.props.items()) + "\n"
        if c.startswith("getprop "):
            return self.props.get(c.split()[1], "") + "\n"
        if c.startswith("pm list packages"):
            flags = [a for a in c.split()[3:] if a.startswith("-")]
            filt = [a for a in c.split()[3:] if not a.startswith("-")]
            names = sorted(n for n in self.pkgs if not filt or filt[0] in n)
            if "-d" in flags:
                names = [n for n in names if n in self.disabled]
            if "-e" in flags:
                names = [n for n in names if n not in self.disabled]
            if "-s" in flags:
                names = [n for n in names if self.pkgs[n]]
            if "-3" in flags:
                names = [n for n in names if not self.pkgs[n]]
            return "".join(f"package:{n}\n" for n in names)
        if c.startswith("pm path "):
            return f"package:/data/app/{c.split()[-1]}-1/base.apk\n"
        if c.startswith("pm install-create"):
            return "Success: created install session [1]\n"
        if c.startswith("pm install-write"):
            return "Success: streamed\n"
        if c.startswith("pm install -r") or c.startswith("pm install-commit"):
            self.pkgs.setdefault("com.example.sideloaded", False)
            return "Success\n"
        if c.startswith("pm disable-user"):
            name = c.split()[-1]
            self.disabled.add(name)
            return f"Package {name} new state: disabled-user\n"
        if c.startswith("pm enable"):
            name = c.split()[-1]
            self.disabled.discard(name)
            return f"Package {name} new state: enabled\n"
        if "resolve-activity" in c:
            if "com.google.android.apps.tv.launcherx" in self.disabled:
                return "priority=0 preferredOrder=0 match=0x108000 specificIndex=-1 isDefault=false\n" \
                       f"{SETUPWRAITH}/.RecoveryActivity\n"
            return "priority=0 preferredOrder=0\ncom.google.android.apps.tv.launcherx/" \
                   "com.google.android.apps.tv.launcherx.home.HomeActivity\n"
        if "LEANBACK_LAUNCHER" in c:
            return "".join(f"{p}/.Main\n" for p in ("com.google.android.youtube.tv", "com.netflix.ninja",
                           "com.amazon.amazonvideo.livingroom", "com.disney.disneyplus", "com.spotify.tv.android"))
        if "query-activities" in c:
            return ("com.google.android.apps.tv.launcherx/com.google.android.apps.tv.launcherx.home.HomeActivity\n"
                    f"{SETUPWRAITH}/.RecoveryActivity\ncom.android.tv.settings/.FallbackHome\n")
        if "screencap" in c:
            return "rc=0\n"
        if c.startswith("dumpsys connectivity"):
            return "Transports: WIFI\n"
        if c.startswith("dumpsys usb"):
            return "host_connected=false\n"
        if c.startswith("dumpsys wifi"):
            return "cname=com.android.settings\n"
        if "TV_INPUT_HARDWARE" in c:
            return "com.mediatek.tvinput\ncom.tcl.tvinput\n"
        if c.startswith("dumpsys package "):
            name = c.split()[2]
            return (f"Packages:\n  Package [{name}] (3b1f2a1):\n    userId=1000\n    versionName=1.4.2\n"
                    f"    codePath=/system/priv-app/{name.split('.')[-1]}\n    flags=[ SYSTEM HAS_CODE ]\n"
                    "    Activity Resolver Table:\n      .MainActivity\n    Service:\n      .SyncService\n")
        if c.startswith("dumpsys activity"):
            return "topResumedActivity=ActivityRecord{1 u0 com.google.android.apps.tv.launcherx/.home.HomeActivity}\n"
        if c.startswith("settings get "):
            return self.settings.get(c.split()[-1], "null") + "\n"
        if c.startswith("settings put "):
            parts = c.split()
            self.settings[parts[3]] = parts[4]
            return ""
        if c.startswith("echo "):
            return c[5:].strip("'\"") + "\n"
        if c.startswith("settings delete "):
            self.settings.pop(c.split()[-1], None)
            return ""
        if c.startswith("settings list"):
            return "\n".join(f"{k}={v}" for k, v in self.settings.items()) + "\n"
        if c.startswith("cat /proc/meminfo"):
            return "MemTotal:        1984512 kB\n"
        if "Somnambulator" in c:   # like the TV box this was tested on
            return ("Starting: Intent { cmp=com.android.systemui/.Somnambulator }\nError type 3\nError: Activity class "
                    "{com.android.systemui/com.android.systemui.Somnambulator} does not exist.\n")
        if c.startswith("am start -a "):
            return "Starting: Intent { act=" + c.split()[3] + " }\n"
        if c.startswith("input keyevent"):
            key = c.split()[-1]
            self.focus += {"KEYCODE_DPAD_RIGHT": 1, "KEYCODE_DPAD_LEFT": -1}.get(key, 0)
            return ""
        if c.startswith("wm "):
            return "Physical size: 1920x1080\n" if "size" in c else "Physical density: 320\n"
        if c == "reboot":
            time.sleep(1.5)
            return ""
        return ""

    def pull(self, remote, local, **_):
        img = QImage(1280, 720, QImage.Format.Format_RGB32)
        img.fill(QColor("#050506"))
        p = QPainter(img)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QColor("#f2f2f2"))
        f = QFont("Segoe UI", 34)
        f.setWeight(QFont.Weight.Light)
        p.setFont(f)
        p.drawText(60, 100, time.strftime("%H:%M"))
        p.setFont(QFont("Segoe UI", 12))
        p.setPen(QColor("#9a9a9a"))
        p.drawText(62, 132, "Good afternoon  ·  demo TV screen")
        apps = ["YouTube", "Netflix", "Prime", "Disney+", "Spotify", "Live TV"]
        colors = ["#e33", "#b0060f", "#1a98ff", "#113ccf", "#1db954", "#555"]
        band = QRectF(40, 440, 1200, 220)
        p.setBrush(QColor("#141416"))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(band, 30, 30)
        sel = self.focus % len(apps)
        for i, (name, col) in enumerate(zip(apps, colors)):
            r = QRectF(70 + i * 192, 480, 170, 100)
            if i == sel:
                r = r.adjusted(-8, -8, 8, 8)
            p.setBrush(QColor(col))
            p.drawRoundedRect(r, 16, 16)
            p.setPen(QColor("white"))
            p.drawText(r, Qt.AlignmentFlag.AlignCenter, name)
            p.setPen(Qt.PenStyle.NoPen)
        p.end()
        img.save(local, "PNG")

    def close(self):
        pass


class TVClient:
    def __init__(self):
        self.dev = None
        self.host = ""
        self.port = 5555
        self.info = {}
        self.lock = threading.RLock()

    @property
    def connected(self):
        return self.dev is not None

    def connect(self, host, port, timeout=120):
        with self.lock:
            self.close()
            self.host, self.port = host, int(port)
            if DEMO:
                if not hasattr(self, "_fake"):
                    self._fake = FakeDev()
                self.dev = self._fake
                time.sleep(0.6)
                return
            tvmod.HOST, tvmod.PORT = host, int(port)
            os.environ["TV_HOST"], os.environ["TV_PORT"] = host, str(port)
            self.dev = tvmod.connect(timeout=timeout)

    def close(self):
        with self.lock:
            if self.dev is not None:
                try:
                    self.dev.close()
                except Exception:
                    pass
            self.dev = None

    def sh(self, cmd, timeout=120, quiet=False, retry=True):
        with self.lock:
            if self.dev is None:
                raise RuntimeError("Not connected to a TV")
            log(f"$ {cmd}", "cmd")
            try:
                out = self.dev.shell(cmd, read_timeout_s=float(timeout)) or ""
            except Exception as e:
                if not retry:
                    raise
                log(f"connection hiccup ({type(e).__name__}), reconnecting…", "warn")
                self.connect(self.host, self.port, timeout=30)
                out = self.dev.shell(cmd, read_timeout_s=float(timeout)) or ""
            if not quiet and out.strip():
                lines = out.rstrip().splitlines()
                shown = "\n".join(lines[:40]) + (f"\n… {len(lines) - 40} more lines" if len(lines) > 40 else "")
                log(shown, "out")
            return out

    def prop(self, name):
        return self.sh(f"getprop {name}", quiet=True).strip()

    def packages(self, flag=""):
        out = self.sh(f"pm list packages {flag}".strip(), quiet=True)
        return {line.split(":", 1)[1].strip() for line in out.splitlines()
                if line.startswith("package:") and PACKAGE_RE.fullmatch(line.split(":", 1)[1].strip())}

    def home_owner(self):
        out = self.sh(HOME_QUERY, quiet=True)
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        pkg = lines[-1].split("/")[0] if lines else ""
        if PACKAGE_RE.fullmatch(pkg) and pkg != "android":
            return pkg, lines[-1]
        # Before Android 7 there is no `cmd`; dumpsys activity names the Home process (#795).
        for line in self.sh("dumpsys activity", quiet=True).splitlines():
            m = re.search(r"mHomeProcess:.*[: ]([A-Za-z0-9_.]+)/[A-Za-z0-9_.]+", line.strip())
            if m:
                return m.group(1), ""
        return ("android" if pkg == "android" else ""), (lines[-1] if lines else "")

    def home_claimants(self):
        names = set()
        for line in self.sh(HOME_CLAIMS, quiet=True).splitlines():
            m = COMPONENT_RE.match(line.strip())
            if m and not m.group(2).endswith("FallbackHome"):
                names.add(m.group(1))
        return names

    def screenshot(self, keys=(), wait=0.9):
        SHOTS.mkdir(parents=True, exist_ok=True)
        local = str(SHOTS / f"tv-{time.strftime('%Y%m%d-%H%M%S')}-{int(time.time() * 1000) % 1000:03d}.png")
        with self.lock:
            if self.dev is None:
                raise RuntimeError("Not connected to a TV")
            for i, key in enumerate(keys):
                if i:
                    time.sleep(0.5)
                self.sh(f"input keyevent {keycode(key)}", quiet=True)
            if keys:
                time.sleep(wait)
            if DEMO:
                self.dev.pull("", local)
                rc = 0
            else:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                    rc = tvmod.screenshot(self.dev, local)
                msg = buf.getvalue().strip()
                if rc != 0:
                    top = self.sh("dumpsys activity activities | grep topResumedActivity", quiet=True).strip()
                    raise RuntimeError((msg or "The capture came back empty.") +
                                       (f"\n\nOn screen now: {top}" if top else ""))
        # Keep the shots folder from growing forever.
        old = sorted(SHOTS.glob("tv-*.png"))[:-60]
        for p in old:
            try:
                p.unlink()
            except OSError:
                pass
        return local


TV = TVClient()


def keycode(name):
    return name if name.isdigit() or name.startswith("KEYCODE_") else "KEYCODE_" + name


# ----------------------------------------------------------------------------------------------
# Community lists from examples/
# ----------------------------------------------------------------------------------------------
class Preset:
    def __init__(self, folder, path, header, names):
        self.folder, self.path, self.header, self.names = folder, path, header, names

    @property
    def title(self):
        return self.folder if self.path.name == "debloat.txt" else f"{self.folder} / {self.path.name}"


def load_examples():
    counts, notes, presets = Counter(), {}, []
    if not EXAMPLES.is_dir():
        return counts, notes, presets
    for d in sorted(EXAMPLES.iterdir()):
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.txt")):
            try:
                text = f.read_text(encoding="utf-8-sig", errors="replace")
            except OSError:
                continue
            header, names, section = [], [], ""
            for line in text.splitlines():
                s = line.strip()
                if s.startswith("#"):
                    comment = s.lstrip("#").strip()
                    if not names and len(header) < 4 and comment:
                        header.append(comment)
                    if comment and len(comment) <= 90 and not comment.lower().startswith(("apply", "undo")):
                        section = comment
                    continue
                body, _, inline = s.partition("#")
                parts = body.split()
                if not parts or not PACKAGE_RE.fullmatch(parts[0]):
                    continue
                name = parts[0]
                names.append(name)
                counts[name] += 1
                note = inline.strip() or section
                if note and name not in notes:
                    notes[name] = note[:110]
            if names:
                presets.append(Preset(d.name, f, " ".join(header), names))
    return counts, notes, presets


def suggest_preset(presets, info):
    model = info.get("model", "").lower()
    device = info.get("device", "").lower()
    maker = info.get("manufacturer", "").lower()
    best, best_score = None, 0
    for p in presets:
        head = p.header.lower()
        folder = p.folder.lower()
        score = 0
        if model and len(model) > 3 and (model in head or model.replace(" ", "-") in folder):
            score += 6
        if device and len(device) > 2 and (device in head or device in folder):
            score += 3
        if maker and maker.split()[0] in folder:
            score += 1
        if score > best_score:
            best, best_score = p, score
    return best if best_score >= 3 else None


GENERIC_MODELS = {"tv box", "android tv", "smart tv", "box", "tv", "android box", "google tv", "atv", "set top box"}


def hardware_score(saved, info):
    """How surely a saved TV (a profile's "tv") is the same hardware as the connected one; 0 means no."""
    def v(d, k):
        return str((d or {}).get(k) or "").strip().lower()
    if not saved or not info:
        return 0
    score = 0
    same_model = v(saved, "model") and v(saved, "model") == v(info, "model")
    same_device = v(saved, "device") and v(saved, "device") == v(info, "device")
    score += 3 * bool(same_model) + 3 * bool(same_device)
    score += sum(1 for k in ("manufacturer", "board", "platform", "hardware", "brand")
                 if v(saved, k) and v(saved, k) == v(info, k))
    score += 2 * bool(v(saved, "build") and v(saved, "build") == v(info, "build"))
    return score if (same_model and same_device) or score >= 7 else 0


def match_presets(presets, installed, info=None):
    """Rank the tested lists by how much of each one this TV's firmware carries.

    Common Google packages appear in most lists and say little; vendor packages (com.amlogic.*, com.tcl.*) appear
    in few and say a lot, so every package weighs 1 / (number of lists that name it). A model or device name in a
    list's header adds a bonus. Returns [(score, matched, total, preset)], best first."""
    df = Counter()
    for p in presets:
        df.update(set(p.names))
    info = info or {}
    model = (info.get("model") or "").lower()
    device = (info.get("device") or "").lower()
    ranked = []
    for p in presets:
        names = set(p.names)
        hit = names & installed
        if not hit:
            continue
        score = sum(1.0 / df[n] for n in hit)
        head, folder = p.header.lower(), p.folder.lower()
        # The same hardware named in a list's header wins over any package overlap.
        if model and len(model) > 3 and model not in GENERIC_MODELS and \
                (model in head or model.replace(" ", "-") in folder):
            score += 50
        if device and len(device) > 2 and device not in GENERIC_MODELS and (device in head or device in folder):
            score += 30
        ranked.append((score, len(hit), len(names), p))
    ranked.sort(key=lambda t: (-t[0], -t[1]))
    return ranked


# ----------------------------------------------------------------------------------------------
# Widgets
# ----------------------------------------------------------------------------------------------
def card(*, spacing=10, margins=18):
    f = QFrame()
    f.setObjectName("Card")
    lay = QVBoxLayout(f)
    lay.setContentsMargins(margins, margins - 2, margins, margins)
    lay.setSpacing(spacing)
    return f, lay


def label(text, name=None, wrap=False, rich=False):
    l = QLabel(text)
    if name:
        l.setObjectName(name)
    if wrap:
        l.setWordWrap(True)
    if rich:
        l.setTextFormat(Qt.TextFormat.RichText)
        l.setOpenExternalLinks(True)
    else:
        l.setTextFormat(Qt.TextFormat.PlainText)
    return l


class Toggle(QCheckBox):
    """An on/off switch in the iPhone style: a rounded track with a sliding knob, the label beside it.
    A QCheckBox underneath, so isChecked, setChecked, toggled and the rest work as before."""
    W, H, GAP = 44, 24, 12

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._pos = 0.0
        self._anim = QVariantAnimation(self)
        self._anim.setDuration(170)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.valueChanged.connect(self._moved)
        self.toggled.connect(self._slide)

    def _moved(self, v):
        self._pos = float(v)
        self.update()

    def _slide(self, on):
        end = 1.0 if on else 0.0
        if not self.isVisible():
            self._anim.stop()
            self._pos = end
            self.update()
            return
        self._anim.stop()
        self._anim.setStartValue(self._pos)
        self._anim.setEndValue(end)
        self._anim.start()

    def showEvent(self, e):
        if self._anim.state() != QVariantAnimation.State.Running:
            self._pos = 1.0 if self.isChecked() else 0.0
        super().showEvent(e)

    def sizeHint(self):
        fm = self.fontMetrics()
        w = self.W + (self.GAP + fm.horizontalAdvance(self.text()) + 2 if self.text() else 0)
        return QSize(w, max(self.H + 6, fm.height() + 6))

    def minimumSizeHint(self):
        return QSize(self.W, self.H + 6)

    def hitButton(self, pos):
        return self.rect().contains(pos)

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        enabled = self.isEnabled()
        y = (self.height() - self.H) / 2
        track = QRectF(1, y, self.W - 2, self.H)
        off, on = QColor(C["line2"]), QColor(C["ok"])
        t = self._pos
        mix = QColor(int(off.red() + (on.red() - off.red()) * t), int(off.green() + (on.green() - off.green()) * t),
                     int(off.blue() + (on.blue() - off.blue()) * t))
        if not enabled:
            mix.setAlpha(110)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(mix)
        p.drawRoundedRect(track, self.H / 2, self.H / 2)
        if self.hasFocus() and self.focusPolicy() != Qt.FocusPolicy.NoFocus:
            p.setPen(QPen(QColor(C["accent2"]), 1.5))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(track.adjusted(-2, -2, 2, 2), self.H / 2 + 2, self.H / 2 + 2)
            p.setPen(Qt.PenStyle.NoPen)
        d = self.H - 4
        x = track.left() + 2 + (track.width() - 4 - d) * t
        p.setBrush(QColor(0, 0, 0, 60))
        p.drawEllipse(QRectF(x, y + 3, d, d))                 # soft shadow under the knob
        p.setBrush(QColor("#ffffff") if enabled else QColor(200, 200, 205))
        p.drawEllipse(QRectF(x, y + 2, d, d))
        if self.text():
            p.setPen(self.palette().color(self.foregroundRole()) if enabled else QColor(C["dim"]))
            p.setFont(self.font())
            r = QRectF(self.W + self.GAP, 0, self.width() - self.W - self.GAP, self.height())
            p.drawText(r, int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft), self.text())
        p.end()


def button(text, kind=None, ico=None, tip=None):
    b = QPushButton(text.replace("&", "&&"))
    if kind:
        b.setObjectName(kind)
    if ico:
        b.setIcon(icon(ico, "white" if kind == "Primary" else (C["bad"] if kind == "Danger" else C["text"]), 18))
        b.setIconSize(QSize(17, 17))
    if tip:
        b.setToolTip(tip)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b


def hbox(*widgets, spacing=8, stretch_at=None):
    w = QWidget()
    w.setObjectName("Clear")
    lay = QHBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(spacing)
    for i, x in enumerate(widgets):
        if x is None:
            lay.addStretch(1)
        elif isinstance(x, int):
            lay.addSpacing(x)
        else:
            lay.addWidget(x)
    return w


class Banner(QFrame):
    """A coloured note: info, ok, warn or bad."""

    def __init__(self, text="", kind="info"):
        super().__init__()
        self.setObjectName("Banner")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 11, 14, 11)
        lay.setSpacing(11)
        self.ico = QLabel()
        self.ico.setFixedWidth(20)
        self.ico.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.text = QLabel()
        self.text.setWordWrap(True)
        self.text.setTextFormat(Qt.TextFormat.RichText)
        self.text.setOpenExternalLinks(True)
        lay.addWidget(self.ico)
        lay.addWidget(self.text, 1)
        self.set(text, kind)

    def set(self, text, kind="info"):
        col = {"info": C["sky"], "ok": C["ok"], "warn": C["warn"], "bad": C["bad"]}[kind]
        ico = {"info": "info", "ok": "check", "warn": "info", "bad": "x"}[kind]
        qc = QColor(col)
        self.setStyleSheet(f"QFrame#Banner {{ background: rgba({qc.red()},{qc.green()},{qc.blue()},22); "
                           f"border: 1px solid rgba({qc.red()},{qc.green()},{qc.blue()},70); border-radius: 12px; }}")
        self.ico.setPixmap(icon(ico, col, 18).pixmap(18, 18))
        self.text.setText(text)
        self.setVisible(bool(text))


class Pill(QLabel):
    def __init__(self, text="", color=C["muted"]):
        super().__init__()
        self.set(text, color)

    def set(self, text, color):
        qc = QColor(color)
        self.setText(text)
        self.setStyleSheet(f"background: rgba({qc.red()},{qc.green()},{qc.blue()},28); color: {color}; "
                           f"border: 1px solid rgba({qc.red()},{qc.green()},{qc.blue()},80); "
                           "border-radius: 11px; padding: 3px 10px; font-weight: 600; font-size: 9pt;")


class ShotView(QLabel):
    """Shows the latest TV screenshot, scaled with rounded corners."""

    def __init__(self, placeholder="No screenshot yet"):
        super().__init__()
        self.placeholder = placeholder
        self.pix = None
        self.path = ""
        self.setMinimumSize(240, 135)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_path(self, path):
        pm = QPixmap(path)
        if not pm.isNull():
            self.pix, self.path = pm, path
            self.update()

    def heightForWidth(self, w):
        return int(w * 9 / 16)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        r = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        w = r.width()
        h = w * 9 / 16
        if h > r.height():
            h = r.height()
            w = h * 16 / 9
        box = QRectF(r.x() + (r.width() - w) / 2, r.y() + (r.height() - h) / 2, w, h)
        path = QPainterPath()
        path.addRoundedRect(box, 12, 12)
        p.fillPath(path, QColor("#08090b"))
        if self.pix:
            p.setClipPath(path)
            p.drawPixmap(box.toRect(), self.pix)
            p.setClipping(False)
        else:
            p.setPen(QColor(C["dim"]))
            p.drawText(box, Qt.AlignmentFlag.AlignCenter, self.placeholder)
        p.setPen(QPen(QColor(C["line2"]), 1))
        p.drawPath(path)
        p.end()


class DPad(QWidget):
    pressed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setFixedSize(210, 210)
        self.hover = None
        self.down = None
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def region(self, pos):
        c = QPointF(self.width() / 2, self.height() / 2)
        dx, dy = pos.x() - c.x(), pos.y() - c.y()
        d = (dx * dx + dy * dy) ** 0.5
        if d > self.width() / 2:
            return None
        if d < self.width() * 0.2:
            return "DPAD_CENTER"
        if abs(dx) > abs(dy):
            return "DPAD_RIGHT" if dx > 0 else "DPAD_LEFT"
        return "DPAD_DOWN" if dy > 0 else "DPAD_UP"

    def mouseMoveEvent(self, e):
        r = self.region(e.position())
        if r != self.hover:
            self.hover = r
            self.update()

    def leaveEvent(self, _):
        self.hover = None
        self.update()

    def mousePressEvent(self, e):
        self.down = self.region(e.position())
        self.update()

    def mouseReleaseEvent(self, e):
        r = self.region(e.position())
        if r and r == self.down:
            self.pressed.emit(r)
        self.down = None
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        outer = QRectF(2, 2, w - 4, w - 4)
        p.setPen(QPen(QColor(C["line2"]), 1))
        p.setBrush(QColor(C["card2"]))
        p.drawEllipse(outer)
        # hovered / pressed quadrant
        active = self.down or self.hover
        if active and active != "DPAD_CENTER":
            start = {"DPAD_RIGHT": -45, "DPAD_UP": 45, "DPAD_LEFT": 135, "DPAD_DOWN": 225}[active]
            path = QPainterPath()
            c = outer.center()
            path.moveTo(c)
            path.arcTo(outer, start, 90)
            path.closeSubpath()
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(C["accent"]) if self.down else QColor("#252935"))
            p.drawPath(path)
        # arrows
        p.setPen(QPen(QColor(C["text"]), 2.4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                      Qt.PenJoinStyle.RoundJoin))
        c = outer.center()
        rr = w * 0.37
        s = 7
        for ang, (ax, ay) in {"u": (0, -1), "d": (0, 1), "l": (-1, 0), "r": (1, 0)}.items():
            cx, cy = c.x() + ax * rr, c.y() + ay * rr
            if ax:
                p.drawLine(QPointF(cx - ax * s / 2, cy - s), QPointF(cx + ax * s / 2, cy))
                p.drawLine(QPointF(cx + ax * s / 2, cy), QPointF(cx - ax * s / 2, cy + s))
            else:
                p.drawLine(QPointF(cx - s, cy - ay * s / 2), QPointF(cx, cy + ay * s / 2))
                p.drawLine(QPointF(cx, cy + ay * s / 2), QPointF(cx + s, cy - ay * s / 2))
        inner = QRectF(c.x() - w * 0.19, c.y() - w * 0.19, w * 0.38, w * 0.38)
        p.setPen(QPen(QColor(C["line2"]), 1))
        p.setBrush(QColor(C["accent"]) if self.down == "DPAD_CENTER" else
                   QColor("#2a2f3b") if self.hover == "DPAD_CENTER" else QColor("#1f222a"))
        p.drawEllipse(inner)
        p.setPen(QColor(C["text"]))
        f = self.font()
        f.setBold(True)
        p.setFont(f)
        p.drawText(inner, Qt.AlignmentFlag.AlignCenter, "OK")
        p.end()


# ----------------------------------------------------------------------------------------------
# Package table
# ----------------------------------------------------------------------------------------------
def package_report_text(rows, info):
    """The enabled packages as plain text, grouped by category, to paste in a chat and ask which can go."""
    head = [f"CleanYourTV {APP_VERSION} · package report",
            f"TV: {info.get('manufacturer', '')} {info.get('model', '')} ({info.get('device', '')}), Android "
            f"{info.get('release', '')} (SDK {info.get('sdk', '')}), firmware {info.get('build', '')}",
            f"Home: {info.get('home', '')} · Live TV app: {info.get('live_tv_app') or 'none found'}",
            "Columns: package | lists that disable it | note. Core packages are locked and never disabled.", ""]
    enabled = [r for r in rows if not r["disabled"]]
    disabled = [r for r in rows if r["disabled"]]
    out = head + [f"ENABLED: {len(enabled)} · already disabled: {len(disabled)}", ""]
    for cat, (title, _col, _ask, _desc) in CATEGORIES.items():
        group = sorted((r for r in enabled if r["cat"] == cat), key=lambda r: r["name"])
        if not group:
            continue
        out.append(f"== {title} ({len(group)})")
        for r in group:
            out.append(f"{r['name']} | {r['community'] or 0} | {r['note'] or ''}".rstrip(" |"))
        out.append("")
    if disabled:
        out.append(f"== Already disabled ({len(disabled)})")
        out += sorted(r["name"] for r in disabled)
    return "\n".join(out)


class PackageModel(QAbstractTableModel):
    HEAD = ["", "Package", "Category", "State", "Lists", "Note"]
    checked_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.rows = []

    def set_rows(self, rows):
        self.beginResetModel()
        self.rows = rows
        self.endResetModel()
        self.checked_changed.emit()

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEAD)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.HEAD[section]
        return None

    def flags(self, index):
        f = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.column() == 0 and not self.rows[index.row()]["core"]:
            f |= Qt.ItemFlag.ItemIsUserCheckable
        return f

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        r = self.rows[index.row()]
        col = index.column()
        if role == Qt.ItemDataRole.CheckStateRole and col == 0:
            if r["core"]:
                return None
            return Qt.CheckState.Checked if r["checked"] else Qt.CheckState.Unchecked
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 1:
                return r["name"]
            if col == 2:
                return CATEGORIES[r["cat"]][0]
            if col == 3:
                return "Disabled" if r["disabled"] else "Enabled"
            if col == 4:
                return f"{r['community']}" if r["community"] else ""
            if col == 5:
                return r["note"]
        if role == Qt.ItemDataRole.UserRole:   # sort keys
            if col == 0:
                return int(r["checked"])
            if col == 4:
                return r["community"]
            if col == 2:
                return list(CATEGORIES).index(r["cat"])
            return self.data(index)
        if role == Qt.ItemDataRole.ToolTipRole:
            if col in (2, 0):
                return CATEGORIES[r["cat"]][1 + 2]
            if col == 4 and r["community"]:
                return f"Disabled in {r['community']} tested lists under examples/"
            if col == 5:
                return r["note"]
            return r["name"]
        if role == Qt.ItemDataRole.ForegroundRole:
            if col == 3:
                return QColor(C["muted"] if r["disabled"] else C["ok"])
            if col in (4, 5):
                return QColor(C["muted"])
            if r["disabled"] and col == 1:
                return QColor(C["muted"])
        if role == Qt.ItemDataRole.FontRole and col == 1:
            f = QFont()
            f.setFamilies(["Cascadia Mono", "Consolas", "JetBrains Mono", "monospace"])
            f.setPointSizeF(9.3)
            return f
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            r = self.rows[index.row()]
            if r["core"]:
                return False
            r["checked"] = Qt.CheckState(value) == Qt.CheckState.Checked
            self.dataChanged.emit(index, index)
            self.checked_changed.emit()
            return True
        return False

    def set_checked(self, names, value=True):
        names = set(names)
        for r in self.rows:
            if r["name"] in names and not r["core"]:
                r["checked"] = value
        if self.rows:
            self.dataChanged.emit(self.index(0, 0), self.index(len(self.rows) - 1, 0))
        self.checked_changed.emit()

    def checked(self):
        return [r for r in self.rows if r["checked"]]


class FilterProxy(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.cat = ""
        self.state = "all"
        self.setSortRole(Qt.ItemDataRole.UserRole)

    def set_filter(self, text=None, cat=None, state=None):
        if text is not None:
            self.text = text.lower().strip()
        if cat is not None:
            self.cat = cat
        if state is not None:
            self.state = state
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):
        r = self.sourceModel().rows[row]
        if self.text and self.text not in r["name"].lower() and self.text not in r["note"].lower():
            return False
        if self.cat and r["cat"] != self.cat:
            return False
        if self.state == "enabled" and r["disabled"]:
            return False
        if self.state == "disabled" and not r["disabled"]:
            return False
        if self.state == "selected" and not r["checked"]:
            return False
        if self.state == "suggested" and not (r["community"] or r["cat"] in ("telemetry", "ads", "background")):
            return False
        return True


class CategoryDelegate(QStyledItemDelegate):
    def paint(self, p, option, index):
        model = index.model()
        src = model.mapToSource(index)
        r = model.sourceModel().rows[src.row()]
        name, col = CATEGORIES[r["cat"]][0], QColor(CATEGORIES[r["cat"]][1])
        if option.state & QStyle.StateFlag.State_Selected:
            p.fillRect(option.rect, QColor("#1d2740"))
        p.save()
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        f = QFont(option.font)
        f.setPointSizeF(8.6)
        f.setBold(True)
        p.setFont(f)
        w = p.fontMetrics().horizontalAdvance(name) + 18
        rect = QRectF(option.rect.x() + 6, option.rect.center().y() - 10, w, 20)
        bg = QColor(col)
        bg.setAlpha(34)
        p.setBrush(bg)
        border = QColor(col)
        border.setAlpha(90)
        p.setPen(QPen(border, 1))
        p.drawRoundedRect(rect, 10, 10)
        p.setPen(col)
        p.drawText(rect, Qt.AlignmentFlag.AlignCenter, name)
        p.restore()


# ----------------------------------------------------------------------------------------------
# Dialogs
# ----------------------------------------------------------------------------------------------
class Dialog(QDialog):
    def __init__(self, parent, title, width=560):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(width)
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(22, 20, 22, 18)
        self.lay.setSpacing(12)
        self.lay.addWidget(label(title, "H2"))

    def buttons(self, ok_text="Continue", cancel_text="Cancel", ok_kind="Primary"):
        row = QHBoxLayout()
        row.addStretch(1)
        if cancel_text:
            c = button(cancel_text)
            c.clicked.connect(self.reject)
            row.addWidget(c)
        o = button(ok_text, ok_kind)
        o.clicked.connect(self.accept)
        o.setDefault(True)
        row.addWidget(o)
        self.lay.addLayout(row)
        return o


class ChecklistDialog(Dialog):
    """Ask which of these the user uses. Ticked ones are kept."""

    def __init__(self, parent, rows):
        super().__init__(parent, "Which of these do you use?", 640)
        self.lay.addWidget(label(
            "These are streaming apps, voice, casting, updates, launchers or things the TV may need. "
            "Tick everything you use: ticked packages stay enabled, the rest will be disabled.",
            "Muted", wrap=True))
        self.list = QListWidget()
        self.list.setMinimumHeight(min(420, 44 + 38 * len(rows)))
        for r in sorted(rows, key=lambda r: (list(CATEGORIES).index(r["cat"]), r["name"])):
            it = QListWidgetItem(f"{r['name']}    ·  {CATEGORIES[r['cat']][0]}")
            it.setData(Qt.ItemDataRole.UserRole, r["name"])
            it.setToolTip(CATEGORIES[r["cat"]][3] + (f"\n{r['note']}" if r["note"] else ""))
            it.setFlags(it.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            # Things the TV needs start ticked (kept); apps and services start unticked.
            keep = r["cat"] in ("keep", "launcher", "factory")
            it.setCheckState(Qt.CheckState.Checked if keep else Qt.CheckState.Unchecked)
            if keep:
                it.setForeground(QColor(C["warn"]))
            self.list.addItem(it)
        self.lay.addWidget(self.list)
        self.lay.addWidget(label("Orange rows are things the TV itself may need; they start ticked.", "Dim"))
        self.buttons("Keep ticked, disable the rest")

    def kept(self):
        return {self.list.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.list.count())
                if self.list.item(i).checkState() == Qt.CheckState.Checked}


class BatchDialog(Dialog):
    """After each batch: show the TV screen and ask whether to carry on."""

    def __init__(self, parent, number, total, done, failed, shot, error):
        super().__init__(parent, f"Batch {number} of {total} done", 720)
        self.choice = "stop"
        txt = f"Disabled {len(done)} package{'s' if len(done) != 1 else ''}."
        if failed:
            txt += f"  {len(failed)} did not change: " + ", ".join(
                f"{n} ({REFUSED[n]})" if n in REFUSED else n for n in failed)
        self.lay.addWidget(label(txt, "Muted", wrap=True))
        view = ShotView("No screenshot")
        view.setMinimumSize(640, 360)
        if shot:
            view.set_path(shot)
        self.lay.addWidget(view)
        if error:
            self.lay.addWidget(Banner(error.replace("\n", "<br>"), "warn"))
        self.lay.addWidget(label("Does the TV still look and work right? Use the remote or the Remote page "
                                 "to check before you go on.", "Muted", wrap=True))
        row = QHBoxLayout()
        undo = button("Undo this batch", "Danger", "undo")
        undo.clicked.connect(lambda: self._pick("undo"))
        stop = button("Stop here")
        stop.clicked.connect(lambda: self._pick("stop"))
        go = button("Looks fine, continue" if number < total else "Finish", "Primary", "check")
        go.clicked.connect(lambda: self._pick("go"))
        go.setDefault(True)
        row.addWidget(undo)
        row.addStretch(1)
        row.addWidget(stop)
        row.addWidget(go)
        self.lay.addLayout(row)

    def _pick(self, choice):
        self.choice = choice
        self.accept()


class TextDialog(Dialog):
    def __init__(self, parent, title, text, width=760):
        super().__init__(parent, title, width)
        box = QPlainTextEdit(text)
        box.setObjectName("Box")
        box.setReadOnly(True)
        box.setMinimumHeight(420)
        self.lay.addWidget(box)
        self.buttons("Close", None, None)


def ask(parent, title, text, ok="Continue", kind="Primary"):
    d = Dialog(parent, title, 520)
    d.lay.addWidget(label(text, "Muted", wrap=True, rich="<" in text))
    d.buttons(ok, "Cancel", kind)
    return d.exec() == QDialog.DialogCode.Accepted


def hardware_name(info):
    """A profile name from the hardware: maker, brand when it differs, model and Android version."""
    info = info or {}
    model = (info.get("model") or "").strip()
    parts = []
    for k in ("manufacturer", "brand"):
        v = (info.get(k) or "").strip()
        if v and v.lower() not in ("unknown", "android") and v.lower() not in " ".join(parts + [model]).lower():
            parts.append(v)
    name = " ".join(parts + [model]).strip() or "TV"
    dev = (info.get("device") or "").strip()
    if dev and dev.lower() not in name.lower():   # a generic model ("TV Box") says little; the device code does
        name += f" ({dev})"
    rel = (info.get("release") or "").strip()
    return f"{name} - Android {rel}" if rel else name


def ask_name(parent, title, text, default="", ok="Save", cancel="Cancel"):
    """A short question with a name to type; the name, or "" when cancelled or left empty."""
    d = Dialog(parent, title, 520)
    d.lay.addWidget(label(text, "Muted", wrap=True, rich="<" in text))
    box = QLineEdit(default)
    box.setPlaceholderText("Name, e.g. full-black-nikos")
    d.lay.addWidget(box)
    d.buttons(ok, cancel)
    box.setFocus()
    return box.text().strip() if d.exec() == QDialog.DialogCode.Accepted else ""


def inform(parent, title, text, kind="info"):
    d = Dialog(parent, title, 520)
    d.lay.addWidget(Banner(text, kind))
    d.buttons("OK", None)
    d.exec()


# ----------------------------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------------------------
class Page(QScrollArea):
    title = ""
    subtitle = ""

    def __init__(self, win):
        super().__init__()
        self.win = win
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        inner = QWidget()
        self.body = QVBoxLayout(inner)
        self.body.setContentsMargins(28, 6, 28, 24)
        self.body.setSpacing(14)
        self.setWidget(inner)

    def need_tv(self):
        if not TV.connected:
            inform(self, "Not connected", "Connect to your TV first, on the <b>Connect</b> page.", "warn")
            return False
        return True

    def on_connection(self, ok, info):
        pass


class ConnectPage(Page):
    title = "Connect"
    subtitle = "Find your TV on the network and open an ADB connection"

    def __init__(self, win):
        super().__init__(win)
        s = win.settings

        c, lay = card()
        lay.addWidget(label("Your TV", "H2"))
        self.host = QComboBox()
        self.host.setEditable(True)
        self.host.lineEdit().setPlaceholderText("TV IP address, e.g. 192.168.1.50")
        for h in s.value("recent_hosts", [], list) or []:
            self.host.addItem(h)
        self.host.setCurrentText(s.value("host", "") or "")
        self.host.setMinimumWidth(260)
        self.port = QSpinBox()
        self.port.setRange(1, 65535)
        self.port.setValue(int(s.value("port", 5555)))
        self.port.setFixedWidth(90)
        self.find_btn = button("Find TVs", None, "search", "Look for devices with port 5555 open on your network")
        self.connect_btn = button("Connect", "Primary", "plug")
        self.disconnect_btn = button("Disconnect", "Ghost")
        self.disconnect_btn.hide()
        lay.addWidget(hbox(self.host, label("Port", "Muted"), self.port, self.find_btn, None,
                           self.disconnect_btn, self.connect_btn))
        self.status = Banner("", "info")
        lay.addWidget(self.status)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setFixedHeight(6)
        self.progress.hide()
        lay.addWidget(self.progress)
        self.body.addWidget(c)

        # Device facts
        c, lay = card()
        lay.addWidget(label("Device", "H2"))
        grid = QGridLayout()
        grid.setHorizontalSpacing(28)
        grid.setVerticalSpacing(10)
        self.facts = {}
        for i, (key, title) in enumerate([("model", "Model"), ("manufacturer", "Manufacturer"),
                                          ("android", "Android"), ("build", "Firmware"),
                                          ("ram", "RAM"), ("network", "Network"),
                                          ("home", "Home screen"), ("adbsecure", "ADB security")]):
            box = QVBoxLayout()
            box.setSpacing(2)
            box.addWidget(label(title, "Key"))
            v = label("—", "Val")
            v.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            box.addWidget(v)
            self.facts[key] = v
            grid.addLayout(box, i // 4, i % 4)
        lay.addLayout(grid)
        self.dev_notes = Banner("", "warn")
        lay.addWidget(self.dev_notes)
        self.body.addWidget(c)

        # How-to
        c, lay = card()
        lay.addWidget(label("Before you connect", "H2"))
        lay.addWidget(label(
            "1.  On the TV open Settings → Device Preferences → About and press <b>Build</b> seven times "
            "to unlock Developer options.<br>"
            "2.  In Developer options switch on <b>USB debugging</b> (and <b>Network/ADB debugging</b> if the "
            "TV has it).<br>"
            "3.  Find the TV's IP under Settings → Network, or press <b>Find TVs</b>.<br>"
            "4.  Press <b>Connect</b>. The TV shows <b>“Allow USB debugging?”</b> – tick "
            "<i>Always allow from this computer</i> and choose OK.<br><br>"
            "<span style='color:#8a909c'>Some boxes cut power to their USB ports while USB debugging is on. "
            "If your network runs through a <b>USB Ethernet adapter</b>, plan to finish everything in one "
            "sitting: the adapter only comes back once debugging is off, which also closes this "
            "connection.</span>", wrap=True, rich=True))
        self.body.addWidget(c)

        # Wireless debugging (Google TV)
        c, lay = card()
        lay.addWidget(label("Wireless debugging (Google TV, Android 11+)", "H2"))
        lay.addWidget(label(
            "If Connect is refused, your TV may only offer Wireless debugging. On the TV: Developer options → "
            "Wireless debugging → Pair device with pairing code. Enter what it shows. This uses the "
            "<b>adb</b> program from Android platform-tools, which must be installed.", "Muted", wrap=True,
            rich=True))
        self.pair_addr = QLineEdit()
        self.pair_addr.setPlaceholderText("IP:pair-port  e.g. 192.168.1.50:37123")
        self.pair_code = QLineEdit()
        self.pair_code.setPlaceholderText("6-digit code")
        self.pair_code.setFixedWidth(130)
        self.conn_port = QLineEdit()
        self.conn_port.setPlaceholderText("connect port (top of the screen)")
        self.conn_port.setFixedWidth(230)
        self.pair_btn = button("Pair & open port 5555")
        lay.addWidget(hbox(self.pair_addr, self.pair_code, self.conn_port, self.pair_btn))
        lay.addWidget(label("Android switches Wireless debugging off whenever Wi-Fi drops; pair again then.",
                            "Dim"))
        self.body.addWidget(c)
        self.body.addStretch(1)

        self.find_btn.clicked.connect(self.find)
        self.connect_btn.clicked.connect(self.do_connect)
        self.disconnect_btn.clicked.connect(self.do_disconnect)
        self.pair_btn.clicked.connect(self.pair)
        self.host.lineEdit().returnPressed.connect(self.do_connect)
        if DEMO:
            self.host.setCurrentText("192.168.1.77")
        self.auto = False

    # --- auto ---------------------------------------------------------------------------------
    def auto_connect(self):
        """At start: the last TV if it answers, otherwise the only TV the network scan finds."""
        if TV.connected:
            return
        host = self.host.currentText().strip()
        port = int(self.port.value())
        self.auto = True
        if host:
            self.status.set(f"Looking for your TV at <b>{host}</b>…", "info")
            run_job(lambda: _port_open(host, port), pool=NET_POOL,
                    on_result=lambda ok: self.do_connect() if ok else self._auto_scan(host))
        else:
            self._auto_scan(None)

    def _auto_scan(self, missed):
        if missed:
            self.status.set(f"<b>{missed}</b> did not answer (TV off, or a new address?). Searching the network…", "info")
        self.find()

    # --- find -------------------------------------------------------------------------------
    def find(self):
        self.find_btn.setEnabled(False)
        self.status.set("Looking for devices with network ADB (port 5555) on your network…", "info")
        self.progress.show()
        run_job(scan_network, int(self.port.value()), pool=NET_POOL, on_result=self.found,
                on_done=lambda: (self.find_btn.setEnabled(True), self.progress.hide()))

    def found(self, hits):
        if not hits:
            self.auto = False
            self.status.set("No device with port 5555 open was found. Check that Network/USB debugging is on, "
                            "or type the TV's IP (TV Settings → Network).", "warn")
            return
        current = self.host.currentText()
        for ip, name in hits:
            text = ip
            if self.host.findText(text) < 0:
                self.host.addItem(text)
        self.host.setCurrentText(hits[0][0] if not current else current)
        names = ", ".join(f"<b>{ip}</b>" + (f" ({n})" if n else "") for ip, n in hits)
        self.status.set(f"Found: {names}. Pick one and press Connect.", "ok")
        if len(hits) == 1:
            self.host.setCurrentText(hits[0][0])
            if self.auto and not TV.connected:
                self.do_connect()
        self.auto = False

    # --- connect ----------------------------------------------------------------------------
    def do_connect(self):
        host = self.host.currentText().strip()
        if not host:
            self.status.set("Type the TV's IP address first, or press Find TVs.", "warn")
            return
        self.connect_btn.setEnabled(False)
        self.progress.show()
        self.status.set("Connecting… <b>Look at your TV now:</b> if it asks “Allow USB debugging?”, tick "
                        "<i>Always allow from this computer</i> and choose <b>OK</b>. (Waits up to 2 minutes.)",
                        "info")
        run_job(connect_and_probe, host, int(self.port.value()), on_result=self.connected,
                on_error=self.failed, on_done=lambda: (self.connect_btn.setEnabled(True), self.progress.hide()))

    def connected(self, info):
        s = self.win.settings
        host = TV.host
        s.setValue("host", host)
        s.setValue("port", TV.port)
        recent = [host] + [h for h in (s.value("recent_hosts", [], list) or []) if h != host]
        s.setValue("recent_hosts", recent[:8])
        BUS.connection.emit(True, info)

    def failed(self, msg):
        TV.close()
        hint = ""
        low = msg.lower()
        if "refused" in low:
            hint = ("The TV refused the connection: network ADB is off. Switch on USB debugging (and "
                    "Network debugging), or use Wireless debugging below.")
        elif "no route" in low and sys.platform == "darwin":
            hint = "macOS Local Network privacy may be blocking this app; allow it in System Settings → Privacy."
        elif "timed out" in low or "timeout" in low:
            hint = "No answer. Is the TV on, at this address, and was the “Allow USB debugging?” prompt accepted?"
        self.status.set(f"Could not connect: {msg}" + (f"<br><br>{hint}" if hint else ""), "bad")

    def do_disconnect(self):
        # On the TV thread: a command still running finishes first, and the window stays responsive meanwhile.
        self.disconnect_btn.setEnabled(False)
        run_job(TV.close, on_done=lambda: (self.disconnect_btn.setEnabled(True), BUS.connection.emit(False, {})))

    def on_connection(self, ok, info):
        self.connect_btn.setVisible(not ok)
        self.disconnect_btn.setVisible(ok)
        if not ok:
            self.status.set("Disconnected.", "info")
            for v in self.facts.values():
                v.setText("—")
            self.dev_notes.set("")
            return
        self.status.set(f"Connected to <b>{info.get('model')}</b> at {TV.host}:{TV.port}. "
                        "Next: make a backup.", "ok")
        f = self.facts
        f["model"].setText(f"{info.get('model')}  ({info.get('device')})")
        f["manufacturer"].setText(info.get("manufacturer") or "—")
        f["android"].setText(f"{info.get('release')}  (SDK {info.get('sdk')})")
        f["build"].setText(info.get("build") or "—")
        f["build"].setToolTip(info.get("build") or "")
        f["ram"].setText(info.get("ram") or "—")
        f["network"].setText(info.get("transport") or "—")
        f["home"].setText(info.get("home") or "—")
        f["home"].setToolTip(info.get("home_component") or "")
        f["adbsecure"].setText("Prompt required" if info.get("adb_secure") != "0" else "OPEN (ro.adb.secure=0)")
        f["adbsecure"].setStyleSheet(f"color: {C['bad'] if info.get('adb_secure') == '0' else C['ok']};")
        notes = []
        if info.get("adb_secure") == "0":
            notes.append("This firmware has <b>ro.adb.secure=0</b>: any device on your network gets a shell on "
                         "port 5555 without the Allow prompt. Close debugging when you are done (Finish page).")
        if info.get("cvte"):
            notes.append("This is a <b>CVTE board</b>: leave its stock launcher enabled unless a tested list for "
                         "this exact board disables it, and reboot once before anything else after changing "
                         "Home (#741).")
        if info.get("transport") == "ETHERNET":
            notes.append("The TV is on <b>Ethernet</b>. If that runs through a USB adapter, finish the whole job "
                         "in one sitting: it only comes back once USB debugging is off.")
        if info.get("usb_host") == "false" and info.get("transport") == "WIFI":
            notes.append("USB host shows <b>nothing connected</b>. If you normally use a USB Ethernet adapter, the "
                         "box has fallen back to Wi-Fi.")
        if info.get("sdk_int", 99) < 26:
            notes.append(f"Android SDK {info.get('sdk')} is below 26: the replacement launcher cannot be installed "
                         "here; the debloat still works.")
        self.dev_notes.set("<br><br>".join(notes), "warn")

    # --- pair -------------------------------------------------------------------------------
    def pair(self):
        adb = shutil.which("adb")
        if not adb:
            inform(self, "adb not found", "Install Android SDK Platform-Tools and make sure <b>adb</b> is on your "
                   "PATH, then try again.", "warn")
            return
        addr, code, cport = self.pair_addr.text().strip(), self.pair_code.text().strip(), self.conn_port.text().strip()
        if not re.fullmatch(r"[\w.\-]+:\d+", addr) or not re.fullmatch(r"\d{6}", code):
            inform(self, "Check the fields", "Enter the pairing address as IP:port and the 6-digit code.", "warn")
            return
        ip = addr.split(":")[0]
        if cport and not cport.isdigit():
            inform(self, "Check the fields", "The connect port is a number.", "warn")
            return
        self.pair_btn.setEnabled(False)
        run_job(adb_pair, adb, addr, code, ip, cport, pool=NET_POOL,
                on_result=lambda _: (self.host.setCurrentText(ip),
                                     self.status.set("Paired and port 5555 opened. Press Connect.", "ok")),
                on_error=lambda m: self.status.set(f"Pairing failed: {m}", "bad"),
                on_done=lambda: self.pair_btn.setEnabled(True))


def _port_open(host, port, timeout=1.5):
    if DEMO:
        return True
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def scan_network(port):
    if DEMO:
        time.sleep(1.2)
        return [("192.168.1.77", "android-tv.lan")]
    flags = 0x08000000 if os.name == "nt" else 0
    candidates = set()
    try:
        out = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=10, creationflags=flags).stdout
        candidates.update(re.findall(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", out))
    except Exception:
        pass
    # Our own /24, for TVs that are not in the ARP cache yet.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        mine = s.getsockname()[0]
        s.close()
        net = ipaddress.ip_network(mine + "/24", strict=False)
        candidates.update(str(h) for h in net.hosts())
        candidates.discard(mine)
    except OSError:
        pass
    good = []
    for c in candidates:
        try:
            a = ipaddress.ip_address(c)
            if a.is_private and not a.is_multicast and not str(a).endswith(".255"):
                good.append(c)
        except ValueError:
            pass

    def probe(ip):
        try:
            with socket.create_connection((ip, port), timeout=0.45):
                return ip
        except OSError:
            return None

    with ThreadPoolExecutor(96) as ex:
        hits = [h for h in ex.map(probe, good) if h]

    def name(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except OSError:
            return ""

    with ThreadPoolExecutor(8) as ex:
        names = list(ex.map(name, hits))
    return sorted(zip(hits, names), key=lambda t: tuple(int(x) for x in t[0].split(".")))


def adb_pair(adb, addr, code, ip, cport):
    flags = 0x08000000 if os.name == "nt" else 0

    def run(args, timeout=40):
        log("$ adb " + " ".join(args), "cmd")
        p = subprocess.run([adb] + args, capture_output=True, text=True, timeout=timeout, creationflags=flags)
        out = (p.stdout + p.stderr).strip()
        if out:
            log(out, "out")
        return p.returncode, out

    rc, out = run(["pair", addr, code])
    if rc != 0 or "success" not in out.lower():
        raise RuntimeError(out or "adb pair failed")
    if cport:
        target = f"{ip}:{cport}"
        rc, out = run(["connect", target])
        if "connected" not in out.lower():
            raise RuntimeError(out or "adb connect failed")
        run(["-s", target, "tcpip", "5555"])
        time.sleep(2)
    return True


def connect_and_probe(host, port):
    TV.connect(host, port)
    log(f"connected to {host}:{port}", "ok")
    props = {k: TV.prop(k) for k in ("ro.product.model", "ro.product.device", "ro.product.manufacturer",
                                     "ro.build.version.release", "ro.build.version.sdk",
                                     "ro.build.display.id", "ro.adb.secure", "ro.product.board",
                                     "ro.board.platform", "ro.hardware", "ro.product.brand")}
    home, component = TV.home_owner()
    transport = re.findall(r"Transports: ([A-Z]+)", TV.sh("dumpsys connectivity | grep -o 'Transports: [A-Z]*'",
                                                          quiet=True))
    usb = re.findall(r"host_connected=(\w+)", TV.sh("dumpsys usb | grep host_connected", quiet=True))
    mem = re.findall(r"MemTotal:\s+(\d+)", TV.sh("cat /proc/meminfo | head -1", quiet=True))
    sdk = props["ro.build.version.sdk"]
    cvte = bool(TV.sh("pm list packages com.cvte.", quiet=True).strip())
    try:
        live_app = detect_live_tv_app()
    except Exception:
        live_app = ""
    info = {
        "model": props["ro.product.model"] or "Android TV", "device": props["ro.product.device"],
        "manufacturer": props["ro.product.manufacturer"], "release": props["ro.build.version.release"],
        "sdk": sdk, "sdk_int": int(sdk) if sdk.isdigit() else 0, "build": props["ro.build.display.id"],
        "adb_secure": props["ro.adb.secure"], "home": home, "home_component": component,
        "transport": transport[0] if transport else "", "usb_host": usb[0] if usb else "",
        "ram": f"{int(mem[0]) / 1024 / 1024:.1f} GB" if mem else "", "cvte": cvte,
        "board": props["ro.product.board"], "platform": props["ro.board.platform"],
        "hardware": props["ro.hardware"], "brand": props["ro.product.brand"], "live_tv_app": live_app,
    }
    TV.info = info
    return info


# Live TV / tuner apps named in the toolkit's tested lists and device notes (examples/, docs/devices/), vendor apps
# first and the generic ones last. Only a fallback: the app the TV itself names for channels wins (detect_live_tv_app).
LIVE_TV_APPS = [
    "com.sony.dtv.tvx",                 # Sony BRAVIA (Android TV 9+ / Google TV)
    "com.sony.dtv.tvlin",               # Sony BRAVIA, older firmware
    "org.droidtv.playtv",               # Philips (TP Vision)
    "com.mediatek.wwtv.tvcenter",       # MediaTek boards: Xiaomi, Redmi, Nokia, Toshiba, many others
    "com.tcl.tv",                       # TCL, Thomson, Alcatel
    "com.mitv.livetv",                  # Xiaomi (newer Global firmware)
    "com.xiaomi.mitv.tvplayer",         # Xiaomi / Redmi China
    "com.heytap.tv.livetv",             # OnePlus / Realme TV
    "com.jamdeo.tv.livetv",             # Hisense (Android TV)
    "com.skyworth.tv",                  # Skyworth / Coocaa
    "com.zeasn.livetv",                 # Whale OS sets (Zeasn)
    "com.smartdevice.livetv",           # SmartDevice / Kalley and similar
    "com.apps.livetv",                  # sets with com.apps.atv / com.apps.dtv tuners
    "com.vt.tv.tvcenter",               # VT boards
    "com.cltv.hybrid",                  # Vestel / iWedia CLTV (not com.cltv.fast, the FAST channels app)
    "com.realtek.tv",                   # Realtek boards
    "com.sdmc.tv",                      # SDMC boxes with a tuner
    "com.droidlogic.droidlivetv",       # Amlogic reference
    "com.amazon.tv.livetv",             # Fire TV Edition sets
    "net.oqee.androidtv",               # Freebox (IPTV is the Live TV)
    "com.hisense.tv.tvplayer",
    "com.android.tv",                   # AOSP Live TV
    "com.google.android.tv",            # Google's Live Channels
]


def detect_live_tv_app():
    """The TV's own Live TV app: the one that tunes a channel (as the stock launcher's channel tiles do), else a
    known tuner app that is installed; "" for a box without one."""
    out = TV.sh("cmd package resolve-activity --brief -a android.intent.action.VIEW "
                "-d content://android.media.tv/channel/1 -t vnd.android.cursor.item/channel", quiet=True)
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    m = COMPONENT_RE.match(lines[-1]) if lines else None
    installed = TV.packages()
    # A launcher that answers for channels (some Google TV homes do) is not the Live TV app.
    if m and m.group(1) in installed and m.group(1) not in ["android", OUR_LAUNCHER] + KNOWN_STOCK \
            and "launcher" not in m.group(1):
        return m.group(1)
    return next((p for p in LIVE_TV_APPS if p in installed), "")


class BackupPage(Page):
    title = "Backup"
    subtitle = "Save the TV's current state before changing anything"

    def __init__(self, win):
        super().__init__(win)
        c, lay = card()
        lay.addWidget(label("Full backup", "H2"))
        lay.addWidget(label(
            "Saves the full package list, the disabled packages, getprop, every system/secure/global setting, "
            "the Home owner and the display size/density into one folder on this PC. It changes nothing on "
            "the TV. Do this once before debloating.", "Muted", wrap=True))
        where = win.settings.value("backup_dir", str(DEFAULT_BACKUPS)) or str(DEFAULT_BACKUPS)
        if Path(where.replace("\\", "/")).name in [o for o, _ in CYT_FOLDERS]:   # a pre-1.3.6 folder
            where = str(DEFAULT_BACKUPS)
            win.settings.setValue("backup_dir", where)
        self.where = QLineEdit(where)
        browse = button("Browse…", None, "folder")
        browse.clicked.connect(self.browse)
        lay.addWidget(hbox(self.where, browse))
        self.go = button("Create backup", "Primary", "save")
        self.open = button("Open folder", None, "folder")
        self.open.hide()
        lay.addWidget(hbox(self.go, self.open, None))
        self.bar = QProgressBar()
        self.bar.setFixedHeight(8)
        self.bar.hide()
        lay.addWidget(self.bar)
        self.result = Banner("")
        lay.addWidget(self.result)
        self.body.addWidget(c)

        c, lay = card()
        lay.addWidget(label("Undo records", "H2"))
        lay.addWidget(label(
            "Separately from this backup, before the first package is disabled the app writes an undo record "
            f"to {DATA} (one per TV and list). Restore on the Finish page replays it, and so do "
            "tools\\restore.ps1 and tools/restore.sh. Keep that folder.", "Muted", wrap=True))
        self.records = QListWidget()
        self.records.setMinimumHeight(120)
        lay.addWidget(self.records)
        b = button("Open records folder", None, "folder")
        b.clicked.connect(lambda: open_path(DATA))
        lay.addWidget(hbox(b, None))
        self.body.addWidget(c)

        # Profiles
        c, lay = card()
        lay.addWidget(label("Profiles", "H2"))
        lay.addWidget(label(
            "Save everything you set up on this TV as one file: the disabled packages, the theme with its wallpapers, "
            "Private DNS, animation speed and the screensaver. Apply it later to put it all back after a reset, or "
            "set up a second box the same way. Packages go through the Debloat page with all its checks.",
            "Muted", wrap=True))
        self.prof_name = QLineEdit()
        self.prof_name.setPlaceholderText("Profile name, e.g. Living room box")
        self.prof_save = button("Save profile", "Primary", "save")
        self.prof_bundle = button("Save profile + apps", None, "box",
                                  "One .zip with the profile and the apps you installed, to set up another box "
                                  "of the same kind in one go")
        lay.addWidget(hbox(self.prof_name, self.prof_save, self.prof_bundle))
        self.profiles = QListWidget()
        self.profiles.setMinimumHeight(130)
        lay.addWidget(self.profiles)
        self.prof_apply = button("Apply to TV", "Primary", "check")
        self.prof_import = button("Import…", None, "folder", "Copy a .cytv profile or a .zip bundle into your "
                                                             "profiles")
        self.prof_open = button("Open folder", "Ghost", "folder")
        self.prof_del = button("Delete", "Ghost", "x")
        lay.addWidget(hbox(self.prof_apply, self.prof_import, None, self.prof_open, self.prof_del))
        self.prof_msg = Banner("")
        lay.addWidget(self.prof_msg)
        self.body.addWidget(c)
        self.body.addStretch(1)
        self.prof_save.clicked.connect(self.save_profile)
        self.prof_bundle.clicked.connect(self.save_bundle)
        self.bundle_sig = ProgressSignal()
        self.bundle_sig.step.connect(lambda d, t, w: self.prof_msg.set(
            (f"Copying {w}… {d / 1048576:.1f} of {t / 1048576:.1f} MB" if t > 1000 else
             f"Installing app {min(d + 1, t)} of {t}: {w}…") if w else "Apps done.", "info"))
        self.prof_apply.clicked.connect(self.apply_profile)
        self.prof_import.clicked.connect(self.import_profile)
        self.prof_open.clicked.connect(lambda: (PROFILE_DIR.mkdir(parents=True, exist_ok=True), open_path(PROFILE_DIR)))
        self.prof_del.clicked.connect(self.delete_profile)
        self.profiles.itemDoubleClicked.connect(lambda _: self.apply_profile())
        self.refresh_profiles()
        self.go.clicked.connect(self.backup)
        self.open.clicked.connect(lambda: open_path(self.last))
        self.last = ""
        self.refresh_records()

    def on_connection(self, ok, info):
        self.win.matched_profile = None
        if not ok:
            self.refresh_profiles()
            return
        cur = self.prof_name.text().strip()
        if not cur or cur == getattr(self, "_auto_name", None):   # not typed by you: follow the hardware
            self._auto_name = hardware_name(info)
            self.prof_name.setText(self._auto_name)
        self.refresh_profiles()
        best, best_score = None, 0
        for i in range(self.profiles.count()):
            it = self.profiles.item(i)
            tv = it.data(Qt.ItemDataRole.UserRole + 1)
            sc = hardware_score(tv, info)
            if sc > best_score:
                best, best_score = it, sc
        if best:
            self.profiles.setCurrentItem(best)
            name = best.data(Qt.ItemDataRole.UserRole + 2)
            best.setText("✓ this TV   ·   " + best.text())
            best.setForeground(QColor(C["ok"]))
            self.win.matched_profile = (Path(best.data(Qt.ItemDataRole.UserRole)), name)
            self.prof_msg.set(f"Connected hardware matches your profile <b>{name}</b>; it is selected. Press "
                              "<b>Apply to TV</b> to set this box up like before.", "ok")
            cp = self.win.page_list[0]
            cp.status.set(cp.status.text.text() + f"<br>Found your saved profile <b>{name}</b> for this hardware: it "
                          "is selected on <b>Backup → Profiles</b>.", "ok")

    def refresh_profiles(self):
        self.profiles.clear()
        files = sorted(list(PROFILE_DIR.glob("*.cytv")) + list(PROFILE_DIR.glob("*.zip")),
                       key=lambda p: p.stat().st_mtime, reverse=True) if PROFILE_DIR.is_dir() else []
        import zipfile
        for f in files:
            prof = {}
            try:
                apps = ""
                if f.suffix == ".zip":
                    meta, prof = read_bundle(f)
                    apps = f"   ·   📦 {len(meta.get('apps', []))} apps"
                else:
                    with zipfile.ZipFile(f) as z:
                        prof = json.loads(z.read("profile.json").decode("utf-8"))
                txt = (f"{prof.get('name', f.stem)}   ·   {(prof.get('tv') or {}).get('model') or '?'}   ·   "
                       f"{len(prof.get('disabled_packages', []))} packages   ·   "
                       f"theme: {((prof.get('theme') or {}).get('from')) or 'none'}{apps}   ·   "
                       f"{prof.get('created', '')}")
            except Exception:
                txt = f"{f.stem}   ·   (unreadable)"
            it = QListWidgetItem(txt)
            it.setData(Qt.ItemDataRole.UserRole, str(f))
            it.setData(Qt.ItemDataRole.UserRole + 1, prof.get("tv") or {})
            it.setData(Qt.ItemDataRole.UserRole + 2, prof.get("name", f.stem))
            self.profiles.addItem(it)
        if files:
            self.profiles.setCurrentRow(0)
        else:
            it = QListWidgetItem("No profiles yet. Connect, set up the TV, then Save profile.")
            it.setFlags(Qt.ItemFlag.NoItemFlags)
            self.profiles.addItem(it)

    def _current_profile(self):
        it = self.profiles.currentItem()
        return Path(it.data(Qt.ItemDataRole.UserRole)) if it and it.data(Qt.ItemDataRole.UserRole) else None

    def save_profile(self):
        if not self.need_tv():
            return
        name = self.prof_name.text().strip() or hardware_name(TV.info)
        dest = PROFILE_DIR / f"{_safe_name(name)}.cytv"
        if dest.exists() and not ask(self, "Replace profile?", f"A profile called <b>{name}</b> exists. Replace it "
                                     "with the TV's current setup?", "Replace"):
            return
        theme = self.win.settings.value(f"theme_applied/{TV.host}", "") or ""
        self.prof_save.setEnabled(False)
        self.prof_msg.set("Reading the TV…", "info")
        run_job(save_profile, name, theme, on_result=lambda p: (
            self.prof_msg.set(f"Saved <b>{p.name}</b> in {PROFILE_DIR}.", "ok"), self.refresh_profiles()),
                on_error=lambda m: self.prof_msg.set(f"Could not save the profile: {m}", "bad"),
                on_done=lambda: self.prof_save.setEnabled(True))

    def import_profile(self):
        f, _ = QFileDialog.getOpenFileName(self, "Import profile", str(Path.home()),
                                           "CleanYourTV profile or bundle (*.cytv *.zip)")
        if not f:
            return
        try:
            read_bundle(f) if f.lower().endswith(".zip") else read_profile(f)
            PROFILE_DIR.mkdir(parents=True, exist_ok=True)
            if Path(f).resolve().parent != PROFILE_DIR.resolve():
                shutil.copyfile(f, PROFILE_DIR / Path(f).name)
            self.refresh_profiles()
            self.prof_msg.set(f"Imported <b>{Path(f).name}</b>.", "ok")
        except Exception as e:
            self.prof_msg.set(f"Not a usable profile: {e}", "bad")

    def delete_profile(self):
        p = self._current_profile()
        if p and ask(self, "Delete profile?", f"Delete <b>{p.name}</b> from this PC? The TV is not changed.",
                     "Delete", "Danger"):
            try:
                p.unlink()
            except OSError as e:
                self.prof_msg.set(str(e), "bad")
            self.refresh_profiles()

    # ---- profile + apps bundles ---------------------------------------------------------------------------------
    def save_bundle(self):
        """Save profile, then pick the apps to put in with it: one .zip for the next box of this kind."""
        if not self.need_tv():
            return
        name = self.prof_name.text().strip() or hardware_name(TV.info)
        dest = PROFILE_DIR / f"{_safe_name(name)}.zip"
        if dest.exists() and not ask(self, "Replace bundle?", f"<b>{dest.name}</b> exists. Replace it with this TV's "
                                     "current setup and apps?", "Replace"):
            return
        theme = self.win.settings.value(f"theme_applied/{TV.host}", "") or ""
        ex = next(p for p in self.win.page_list if isinstance(p, ExtrasPage))
        extras = {"model": ex.model_key(TV.info or {}), "switches": ex.extras_now()}
        self.prof_bundle.setEnabled(False)
        self.prof_msg.set("Reading the TV…", "info")

        def picked(res):
            cytv, apps = res
            d = PickAppsDialog(self, apps, "")
            d.setWindowTitle("Apps to put in the bundle")
            if d.dest.parentWidget() is not d:   # the Save to row: the apps go into the bundle instead
                d.dest.parentWidget().hide()
            d.ticked = {p for p, sysapp in apps if not sysapp and p != OUR_LAUNCHER}
            d.fill()
            d.ok.setText("Make the bundle")
            if d.exec() != QDialog.DialogCode.Accepted:
                self.prof_bundle.setEnabled(True)
                self.prof_msg.set(f"Profile saved as <b>{cytv.name}</b>; no bundle made.", "info")
                self.refresh_profiles()
                return
            import tempfile
            work = Path(tempfile.mkdtemp(prefix="cyt-bundle-"))

            def build():
                try:
                    saved, notes = pull_apps(sorted(d.ticked), work, self.bundle_sig) if d.ticked else ([], [])
                    out = make_bundle(cytv, saved, dest, extras)
                    cytv.unlink()   # it lives inside the bundle now
                    return out, saved, notes
                finally:
                    shutil.rmtree(work, ignore_errors=True)

            run_job(build, on_result=lambda r: (self.prof_msg.set(
                f"Saved <b>{r[0].name}</b>: the profile and {len(r[1])} app{'s' if len(r[1]) != 1 else ''}"
                + (f" ({r[0].stat().st_size / 1048576:.0f} MB)" if r[0].exists() else "") + f", in {PROFILE_DIR}."
                + ("<br>" + "<br>".join(r[2]) if r[2] else ""), "ok"), self.refresh_profiles()),
                    on_error=lambda m: self.prof_msg.set(f"Could not make the bundle: {m}", "bad"),
                    on_done=lambda: self.prof_bundle.setEnabled(True))

        run_job(lambda: (save_profile(name, theme), tv_apps(True)), on_result=picked,
                on_error=lambda m: (self.prof_msg.set(f"Could not save the profile: {m}", "bad"),
                                    self.prof_bundle.setEnabled(True)))

    def setup_from_bundle(self, path):
        """Apps, then the launcher, then the profile: a box of the same kind set up from one file."""
        try:
            meta, prof = read_bundle(path)
        except Exception as e:
            self.prof_msg.set(f"Could not read the bundle: {e}", "bad")
            return
        apps = meta.get("apps", [])
        has_launcher = launcher_installed()
        steps = []
        if apps:
            steps.append(f"install {len(apps)} app{'s' if len(apps) != 1 else ''}: " + ", ".join(apps[:5]) +
                         (" …" if len(apps) > 5 else ""))
        steps.append("the launcher is already installed: kept" if has_launcher else
                     "build and install the launcher, with the switches saved in the bundle")
        steps.append(f"apply the profile <b>{prof.get('name')}</b>: you choose its parts, packages go in batches "
                     "with a screenshot after each")
        if not ask(self, "Set up this box from the bundle?",
                   "In this order:<br>" + "<br>".join(f"{i + 1}. {t}" for i, t in enumerate(steps)) +
                   "<br><br>A full backup and an undo record are saved before the first package changes.",
                   "Set it up"):
            return
        import tempfile
        work = Path(tempfile.mkdtemp(prefix="cyt-setup-"))
        cytv, files = unpack_bundle(path, work)
        ex = next(p for p in self.win.page_list if isinstance(p, ExtrasPage))
        sw = (meta.get("extras") or {}).get("switches")

        def profile_step(_code=0):
            if _code not in (0, None):
                self.win.go("Backup")
                self.prof_msg.set("The launcher build did not finish, so the profile was not applied. Fix the build "
                                  "on Extras, then press Apply to TV here again: installed apps are not redone.",
                                  "bad")
                return
            self.win.go("Backup")
            self.apply_profile(cytv)

        def launcher_step(results):
            bad = [f"{n}: {e}" for n, e in results if e]
            if results:
                log(f"bundle apps: {len(results) - len(bad)} installed, {len(bad)} not", "ok" if not bad else "warn")
                self._bundle_done = getattr(self, "_bundle_done", set()) | {str(path)}
            if bad:
                self.prof_msg.set("Some apps were not installed:<br>" + "<br>".join(bad[:6]), "warn")
            if sw:
                ex.set_extras(sw)
                ex.save_extras()
            if has_launcher:
                profile_step()
                return
            ex.on_build_finished = profile_step
            self.win.go("Extras")
            ex.build_install()
            if DEMO:
                QTimer.singleShot(300, lambda: (setattr(ex, "on_build_finished", None), profile_step(0)))

        if files and str(path) not in getattr(self, "_bundle_done", set()):
            self.prof_msg.set(f"Installing {len(files)} apps…", "info")
            run_job(install_bundle_apps, files, self.bundle_sig, on_result=launcher_step,
                    on_error=lambda m: self.prof_msg.set(f"Apps stopped: {m}", "bad"))
        else:
            launcher_step([])

    def apply_profile(self, path=None):
        p = Path(path) if path else self._current_profile()
        if not p:
            return
        if not self.need_tv():
            return
        if p.suffix == ".zip":
            self.setup_from_bundle(p)
            return
        try:
            prof, theme = read_profile(p)
        except Exception as e:
            self.prof_msg.set(f"Could not read the profile: {e}", "bad")
            return

        def state():
            return TV.packages(), TV.packages("-d"), launcher_installed()

        def go(res):
            installed, disabled_now, has_launcher = res
            d = ProfileApplyDialog(self, prof, theme, installed, disabled_now, has_launcher)
            if d.exec() != QDialog.DialogCode.Accepted:
                return
            parts = d.chosen()
            self.prof_msg.set("Saving this TV's own state first: full backup and undo records…", "info")
            groups = parts & {"dns", "anim", "dream"}
            backup_root = Path(self.where.text().strip() or DEFAULT_BACKUPS)

            def prepare():
                folder = make_backup(backup_root)
                remember_settings([f"{ns}/{key}" for _g, ns, key in PROFILE_SETTINGS])
                if "packages" in parts and d.todo:
                    save_record(d.todo)   # package states, Home and animation scales, before anything changes
                return folder

            def prepared(folder):
                self.win.backup_done = True
                self.last = str(folder)
                self.open.show()
                log(f"backup of this TV before the profile: {folder}", "ok")
                self.prof_msg.set("Applying the profile…", "info")
                start()

            def then_theme(_=None):
                if "theme" in parts and theme:
                    self.prof_msg.set("Applying the theme…", "info")
                    run_job(apply_theme, theme, on_result=lambda shot: (BUS.shot.emit(shot), then_packages()),
                            on_error=lambda m: (self.prof_msg.set(f"Theme failed: {m}", "bad"), then_packages()))
                else:
                    then_packages()

            def then_packages():
                if "packages" in parts and d.todo:
                    page = self.win.page_list[2]
                    page.model.set_checked([r["name"] for r in page.model.rows], False)
                    page.model.set_checked(d.todo, True)
                    page.state.setCurrentIndex(page.state.findData("selected"))
                    self.win.go("Debloat")
                    page.banner.set(f"From profile <b>{prof.get('name')}</b>: {len(d.todo)} packages ticked. Untick "
                                    "anything you want to keep; the usual checks and batches follow.", "info")
                    self.prof_msg.set("Settings and theme done; packages continue on the Debloat page.", "ok")
                    QTimer.singleShot(300, page.disable_selected)
                else:
                    self.prof_msg.set(f"Profile <b>{prof.get('name')}</b> applied.", "ok")

            def start():
                if groups:
                    run_job(apply_profile_settings, prof, groups, on_result=then_theme,
                            on_error=lambda m: (self.prof_msg.set(f"Settings failed: {m}", "bad"), then_theme()))
                else:
                    then_theme()

            run_job(prepare, on_result=prepared,
                    on_error=lambda m: self.prof_msg.set(f"Nothing was changed: the backup or undo record could not "
                                                         f"be written ({m}).", "bad"))

        run_job(state, on_result=go, on_error=lambda m: self.prof_msg.set(f"Could not read the TV: {m}", "bad"))

    def refresh_records(self):
        self.records.clear()
        if DATA.is_dir():
            for p in sorted(DATA.glob("recovery-*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
                try:
                    rec = json.loads(p.read_text())
                    txt = f"{rec.get('created', '')[:19]}   {rec.get('host', '')}   " \
                          f"{len(rec.get('packages', {}))} packages   {Path(rec.get('list', '')).name}"
                except Exception:
                    txt = p.name
                self.records.addItem(txt)
        if not self.records.count():
            self.records.addItem("No undo records yet.")

    def browse(self):
        d = QFileDialog.getExistingDirectory(self, "Backup folder", self.where.text())
        if d:
            self.where.setText(d)

    def backup(self):
        if not self.need_tv():
            return
        if not self.where.text().strip():
            self.where.setText(str(DEFAULT_BACKUPS))
        self.win.settings.setValue("backup_dir", self.where.text())
        self.go.setEnabled(False)
        self.bar.show()
        self.bar.setRange(0, 0)
        self.result.set("Reading the TV…", "info")
        run_job(make_backup, Path(self.where.text()), on_result=self.done,
                on_error=lambda m: self.result.set(f"Backup failed: {m}", "bad"),
                on_done=lambda: (self.go.setEnabled(True), self.bar.hide()))

    def done(self, folder):
        self.last = str(folder)
        self.win.backup_done = True
        self.open.show()
        self.result.set(f"Backup saved to <b>{folder}</b>. You can start debloating.", "ok")
        log(f"backup written to {folder}", "ok")


def make_backup(root):
    info = TV.info or {}
    tag = re.sub(r"[^A-Za-z0-9._-]+", "-", f"{info.get('model', 'tv')}_{TV.host}").strip("-")
    folder = root / f"{tag}_{time.strftime('%Y-%m-%d_%H%M%S')}"
    folder.mkdir(parents=True, exist_ok=True)
    items = [
        ("packages-all.txt", "pm list packages -f"),
        ("packages-disabled.txt", "pm list packages -d"),
        ("packages-system.txt", "pm list packages -s"),
        ("packages-thirdparty.txt", "pm list packages -3"),
        ("packages-including-uninstalled.txt", "pm list packages -u"),
        ("getprop.txt", "getprop"),
        ("settings-global.txt", "settings list global"),
        ("settings-secure.txt", "settings list secure"),
        ("settings-system.txt", "settings list system"),
        ("home.txt", HOME_QUERY),
        ("home-claimants.txt", HOME_CLAIMS),
        ("display.txt", "wm size; wm density; echo display_density_forced=$(settings get secure display_density_forced)"),
        ("accessibility.txt", "settings get secure enabled_accessibility_services"),
    ]
    for name, cmd in items:
        (folder / name).write_text(TV.sh(cmd, quiet=True), encoding="utf-8")
    (folder / "README.txt").write_text(
        f"CleanYourTV backup of {info.get('model')} ({TV.host}) taken {time.strftime('%Y-%m-%d %H:%M')}.\n"
        "Nothing here is applied automatically. To put a package back: pm enable <package>\n"
        "packages-disabled.txt lists what was ALREADY disabled before cleanup: leave those as they are.\n",
        encoding="utf-8")
    return folder


class DebloatPage(Page):
    title = "Debloat"
    subtitle = "Pick what to switch off. Packages are disabled, never uninstalled"

    def __init__(self, win):
        super().__init__(win)
        self.setWidgetResizable(True)
        self.counts, self.notes, self.presets = load_examples()
        self.model = PackageModel()
        self.proxy = FilterProxy()
        self.proxy.setSourceModel(self.model)
        self.running = False

        # toolbar
        tb = QFrame()
        tb.setObjectName("Card")
        tl = QVBoxLayout(tb)
        tl.setContentsMargins(14, 12, 14, 12)
        tl.setSpacing(10)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search packages or notes…")
        self.search.addAction(icon("search", C["muted"]), QLineEdit.ActionPosition.LeadingPosition)
        self.search.setClearButtonEnabled(True)
        self.cat = QComboBox()
        self.cat.addItem("All categories", "")
        for k, v in CATEGORIES.items():
            self.cat.addItem(v[0], k)
        self.state = QComboBox()
        for text, key in [("All packages", "all"), ("Suggested", "suggested"), ("Enabled", "enabled"),
                          ("Disabled", "disabled"), ("Selected", "selected")]:
            self.state.addItem(text, key)
        self.reload = button("", None, "refresh", "Reload the package list from the TV")
        self.report_btn = button("Report", None, "log", "The enabled packages as text, to copy and ask about")
        self.report_btn.clicked.connect(self.package_report)
        tl.addWidget(hbox(self.search, self.cat, self.state, self.reload, self.report_btn))

        self.preset = QComboBox()
        self.preset.setMinimumWidth(320)
        self.preset.addItem("Load a tested list from examples/…", None)
        for p in self.presets:
            self.preset.addItem(f"{p.title}  ({len(p.names)})", p)
        self.preset.setToolTip("Community-tested debloat lists, one per TV model. Comment lines explain each group.")
        self.load_preset = button("Select from list", None, "list")
        self.sel_suggested = button("Select suggested", None, "spark",
                                    "Telemetry, ads and background services, plus anything a tested list disables")
        self.sel_none = button("Clear", "Ghost")
        tl.addWidget(hbox(self.preset, self.load_preset, None, self.sel_suggested, self.sel_none))
        self.preset_note = label("", "Dim", wrap=True)
        self.preset_note.hide()
        tl.addWidget(self.preset_note)
        self.body.addWidget(tb)

        self.banner = Banner("Connect to your TV to list its packages.", "info")
        self.body.addWidget(self.banner)

        # table + live view
        split = QSplitter(Qt.Orientation.Horizontal)
        split.setHandleWidth(10)
        split.setStyleSheet("QSplitter::handle { background: transparent; }")
        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.setShowGrid(False)
        self.table.verticalHeader().hide()
        self.table.verticalHeader().setDefaultSectionSize(34)
        self.table.setItemDelegateForColumn(2, CategoryDelegate(self.table))
        h = self.table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        h.resizeSection(0, 36)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        h.resizeSection(1, 300)
        h.resizeSection(2, 150)
        h.resizeSection(3, 76)
        h.resizeSection(4, 56)
        h.setStretchLastSection(True)
        h.setHighlightSections(False)
        self.table.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.table.setMinimumHeight(380)
        split.addWidget(self.table)

        side = QFrame()
        side.setObjectName("Card")
        sl = QVBoxLayout(side)
        sl.setContentsMargins(14, 12, 14, 14)
        sl.setSpacing(10)
        sl.addWidget(label("TV screen", "H2"))
        self.view = ShotView("Press Capture to see the TV")
        self.view.setMinimumHeight(150)
        sl.addWidget(self.view)
        cap = button("Capture", None, "camera")
        cap.clicked.connect(self.win_capture)
        sl.addWidget(hbox(cap, None))
        sl.addWidget(label("Batch size", "Key"))
        self.batch = QSpinBox()
        self.batch.setRange(1, 20)
        self.batch.setValue(int(win.settings.value("batch", 5)))
        self.batch.setToolTip("Packages per batch. After every batch the app captures the TV and asks before going on.")
        sl.addWidget(self.batch)
        sl.addWidget(label("A batch can take something load-bearing with it, so the app stops after each one "
                           "and shows you the TV.", "Dim", wrap=True))
        sl.addStretch(1)
        side.setMinimumWidth(270)
        split.addWidget(side)
        split.setStretchFactor(0, 3)
        split.setStretchFactor(1, 1)
        split.setSizes([800, 300])
        self.body.addWidget(split, 1)

        # action bar
        ab = QFrame()
        ab.setObjectName("Card")
        al = QHBoxLayout(ab)
        al.setContentsMargins(14, 10, 14, 10)
        self.count = label("Nothing selected", "Muted")
        self.details = button("Details", None, "info", "dumpsys package for the highlighted row")
        self.enable = button("Enable selected", None, "undo")
        self.disable = button("Disable selected", "Primary", "x")
        al.addWidget(self.count)
        al.addStretch(1)
        al.addWidget(self.details)
        al.addWidget(self.enable)
        al.addWidget(self.disable)
        self.body.addWidget(ab)

        self.search.textChanged.connect(lambda t: self.proxy.set_filter(text=t))
        self.cat.currentIndexChanged.connect(lambda _: self.proxy.set_filter(cat=self.cat.currentData()))
        self.state.currentIndexChanged.connect(lambda _: self.proxy.set_filter(state=self.state.currentData()))
        self.reload.clicked.connect(self.load)
        self.load_preset.clicked.connect(self.apply_preset)
        self.preset.currentIndexChanged.connect(self.preset_changed)
        self.sel_suggested.clicked.connect(self.select_suggested)
        self.sel_none.clicked.connect(lambda: self.model.set_checked([r["name"] for r in self.model.rows], False))
        self.model.checked_changed.connect(self.update_count)
        self.details.clicked.connect(self.show_details)
        self.enable.clicked.connect(self.enable_selected)
        self.disable.clicked.connect(self.disable_selected)
        self.table.doubleClicked.connect(lambda _: self.show_details())
        BUS.shot.connect(self.view.set_path)
        BUS.packages_changed.connect(self.load)
        self.update_count()

    def win_capture(self):
        self.win.capture()

    def package_report(self):
        rows = self.model.rows
        if not rows:
            self.banner.set("Connect to your TV first: the report lists its packages.", "warn")
            return
        text = package_report_text(rows, TV.info or {})
        d = Dialog(self, "Package report", 860)
        d.lay.addWidget(label("Copy this and paste it in the chat to ask which enabled packages are safe to disable "
                              "on this TV. It holds the model and package names only: no IP, account or serial.",
                              "Muted", wrap=True))
        box = QPlainTextEdit(text)
        box.setObjectName("Box")
        box.setReadOnly(True)
        box.setMinimumHeight(440)
        d.lay.addWidget(box)
        copy = button("Copy", "Primary", "save")
        copy.clicked.connect(lambda: (QApplication.clipboard().setText(text), copy.setText("Copied ✓")))
        d.lay.addWidget(hbox(copy, None))
        d.buttons("Close", None, "Ghost")
        d.exec()

    def on_connection(self, ok, info):
        if not ok:
            self.model.set_rows([])
            self.banner.set("Connect to your TV to list its packages.", "info")
            return
        self.user_picked_preset = False
        self.load()

    def preset_changed(self):
        if not getattr(self, "_auto_preset", False):
            self.user_picked_preset = True
        p = self.preset.currentData()
        if p:
            self.preset_note.setText(p.header[:400])
            self.preset_note.show()
        else:
            self.preset_note.hide()

    def load(self):
        if not TV.connected:
            return
        self.banner.set("Reading packages from the TV…", "info")
        run_job(read_packages, on_result=self.loaded, on_error=lambda m: self.banner.set(f"Could not list "
                                                                                          f"packages: {m}", "bad"))

    def loaded(self, data):
        allp, system, disabled = data
        keep_checked = {r["name"] for r in self.model.checked()}
        rows = []
        for n in sorted(allp):
            cat = categorize(n, n in system)
            rows.append({"name": n, "system": n in system, "disabled": n in disabled, "cat": cat,
                         "core": cat == "core", "community": self.counts.get(n, 0),
                         "note": self.notes.get(n, ""), "checked": n in keep_checked and n not in disabled})
        self.model.set_rows(rows)
        en = len(allp) - len(disabled)
        summary = f"{len(allp)} packages on the TV: {en} enabled, {len(disabled)} disabled."
        best = None
        if not getattr(self, "user_picked_preset", False):
            ranked = match_presets(self.presets, set(allp), TV.info)
            # Worth suggesting only when a real share of the list is on this TV.
            ranked = [t for t in ranked if t[0] >= 30 or (t[1] >= 4 and t[1] / t[2] >= 0.4)]
            if ranked:
                best = ranked[0]
                self._auto_preset = True
                self.preset.setCurrentIndex(self.preset.findData(best[3]))
                self._auto_preset = False
        prof = getattr(self.win, "matched_profile", None)
        if prof:
            self.banner.set(f"{summary} This hardware has your saved profile <b>{prof[1]}</b>: apply it from "
                            "<b>Backup → Profiles</b> to set it up exactly like before."
                            + (f" Closest tested list: <b>{best[3].title}</b>." if best else ""), "ok")
        elif best:
            score, hit, total, p = best
            why = "made for this hardware" if score >= 30 else f"{hit} of its {total} packages are on this TV"
            self.banner.set(f"{summary} Tested list selected: <b>{p.title}</b>, {why}. Read its notes below, then "
                            "press <b>Select from list</b>.", "ok")
        else:
            self.banner.set(f"{summary} No tested list matches this firmware closely; tick what you want off, or use "
                            "<b>Select suggested</b>.", "info")

    def update_count(self):
        n = len(self.model.checked())
        self.count.setText(f"{n} selected" if n else "Nothing selected")
        self.disable.setEnabled(n > 0 and not self.running)
        self.enable.setEnabled(n > 0 and not self.running)

    def apply_preset(self):
        p = self.preset.currentData()
        if not p:
            inform(self, "Pick a list", "Choose a TV model from the list first.", "info")
            return
        installed = {r["name"]: r for r in self.model.rows}
        here = [n for n in p.names if n in installed and not installed[n]["disabled"] and not is_core(n)]
        gone = [n for n in p.names if n not in installed]
        already = [n for n in p.names if n in installed and installed[n]["disabled"]]
        self.model.set_checked(here, True)
        self.state.setCurrentIndex(self.state.findData("selected"))
        self.banner.set(f"Ticked <b>{len(here)}</b> packages from <b>{p.title}</b>. {len(already)} already disabled, "
                        f"{len(gone)} not on this TV. Untick anything you use before disabling.", "ok")

    def select_suggested(self):
        names = [r["name"] for r in self.model.rows if not r["disabled"] and not r["core"]
                 and r["cat"] in ("telemetry", "ads", "background")]
        self.model.set_checked(names, True)
        self.state.setCurrentIndex(self.state.findData("selected"))
        self.banner.set(f"Ticked {len(names)} telemetry, ad and background packages. Streaming apps, voice, "
                        "casting and updates are left to you.", "info")

    def current_row(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return None
        return self.model.rows[self.proxy.mapToSource(idx).row()]

    def show_details(self):
        r = self.current_row()
        if not r or not self.need_tv():
            return
        name = r["name"]

        def fetch():
            out = TV.sh(f"dumpsys package {name}", quiet=True)
            keep = []
            for line in out.splitlines():
                if re.search(r"Package \[|versionName|codePath|userId=|flags=|enabled=|installer|"
                             r"Activity|Service|Receiver|Provider|permission", line) or line.startswith("      "):
                    keep.append(line)
            return "\n".join(keep[:400]) or out[:20000]

        run_job(fetch, on_result=lambda t: TextDialog(
            self, name, f"{CATEGORIES[r['cat']][0]}: {CATEGORIES[r['cat']][3]}\n"
                        + (f"Community lists: {r['community']}   Note: {r['note']}\n" if r["community"] else "")
                        + "\n" + t).exec())

    def enable_selected(self):
        rows = [r for r in self.model.checked() if r["disabled"]]
        if not rows:
            inform(self, "Nothing to enable", "None of the selected packages are disabled.", "info")
            return
        if not self.need_tv():
            return
        names = [r["name"] for r in rows]

        def go():
            for n in names:
                TV.sh(f"pm enable {n}")
            return TV.packages("-d")

        run_job(go, on_result=lambda d: (log(f"enabled {len(names)} packages", "ok"), self.load(),
                                         self.model.set_checked(names, False)))

    # --- disable ------------------------------------------------------------------------------
    def disable_selected(self):
        if not self.need_tv():
            return
        rows = [r for r in self.model.checked() if not r["disabled"]]
        if not rows:
            inform(self, "Nothing to disable", "The selected packages are already disabled.", "info")
            return
        core = [r["name"] for r in rows if r["core"] or is_core(r["name"])]
        rows = [r for r in rows if r["name"] not in core]
        if not self.win.backup_done and not ask(
                self, "No backup yet", "You have not made a backup in this session. The undo record is still "
                "written before anything changes, but a full backup is better. Continue without one?",
                "Continue without backup", "Danger"):
            self.win.go("Backup")
            return
        sensitive = [r for r in rows if r["cat"] in ASK_CATEGORIES]
        if sensitive:
            d = ChecklistDialog(self, sensitive)
            if d.exec() != QDialog.DialogCode.Accepted:
                return
            kept = d.kept()
            rows = [r for r in rows if r["name"] not in kept]
        if not rows:
            return
        names = [r["name"] for r in rows]
        self.set_running(True)
        self.banner.set("Checking the list against the TV: Home owner, HDMI/tuner drivers, setup wizard Wi-Fi…",
                        "info")
        run_job(guard_check, names, on_result=lambda res: self.after_guard(res, core),
                on_error=lambda m: (self.banner.set(f"Check failed, nothing was changed: {m}", "bad"),
                                    self.set_running(False)))

    def set_running(self, on):
        self.running = on
        self.update_count()
        self.reload.setEnabled(not on)

    def after_guard(self, res, core):
        names, skipped = res
        msg = ""
        if core:
            msg += "<b>Locked (core Android, never disabled):</b> " + ", ".join(core) + "<br>"
        for n, why in skipped:
            msg += f"<b>Skipped {n}:</b> {why}<br>"
        if not names:
            self.banner.set((msg or "") + "Nothing left to disable.", "warn")
            self.set_running(False)
            return
        size = self.batch.value()
        self.win.settings.setValue("batch", size)
        batches = [names[i:i + size] for i in range(0, len(names), size)]
        text = (f"Disable <b>{len(names)}</b> package{'s' if len(names) != 1 else ''} in <b>{len(batches)}</b> "
                f"batch{'es' if len(batches) != 1 else ''} of up to {size}. Before the first one, the app saves "
                "an undo record of the current state. After each batch you'll see the TV screen.")
        if msg:
            text = msg + "<br>" + text
        if not ask(self, "Ready to disable", text, "Disable"):
            self.set_running(False)
            self.banner.set("Cancelled. Nothing was changed.", "info")
            return
        self.banner.set("Saving the undo record…", "info")
        run_job(save_record, names, on_result=lambda _: self.run_batch(batches, 0, []),
                on_error=lambda m: (self.banner.set(f"No undo record could be written, so nothing was disabled: "
                                                    f"{m}", "bad"), self.set_running(False)))

    def run_batch(self, batches, i, done_total):
        self.banner.set(f"Batch {i + 1} of {len(batches)}: disabling {', '.join(batches[i])}…", "info")
        run_job(disable_batch, batches[i], on_result=lambda res: self.batch_done(batches, i, done_total, res),
                on_error=lambda m: (self.banner.set(f"Batch {i + 1} stopped: {m}", "bad"), self.set_running(False),
                                    self.load()))

    def batch_done(self, batches, i, done_total, res):
        done, failed, shot, shot_err = res
        if shot:
            BUS.shot.emit(shot)
        # Only a whole first batch refused without a reason per package means the firmware blocks pm disable-user;
        # a protected package or two (Android 14 protects some, e.g. devicelockcontroller) is just that package.
        if not done and len(failed) >= 3 and i == 0 and not any(n in REFUSED for n in failed):
            self.set_running(False)
            self.load()
            inform(self, "This firmware refuses to disable packages",
                   "The TV did not disable any package of the first batch (checked with pm list packages -d, not "
                   "the exit code). Some firmware (Fire OS 5, for one) refuses pm disable-user for every package, "
                   "and there is nothing to debloat on such a set. Use the TV's own privacy toggles and the "
                   "ad-blocking DNS on the Extras page instead (docs/TROUBLESHOOTING.md).", "bad")
            return
        done_total = done_total + done
        d = BatchDialog(self, i + 1, len(batches), done, failed, shot, shot_err)
        d.exec()
        if d.choice == "undo":
            run_job(lambda: [TV.sh(f"pm enable {n}") for n in done],
                    on_result=lambda _: (self.banner.set(f"Batch {i + 1} undone; stopped there.", "warn"),
                                         self.load()))
            self.set_running(False)
            return
        if d.choice == "go" and i + 1 < len(batches):
            self.run_batch(batches, i + 1, done_total)
            return
        self.set_running(False)
        self.load()
        self.model.set_checked(done_total, False)
        left = sum(len(b) for b in batches[i + 1:])
        self.banner.set(f"Disabled {len(done_total)} packages." + (f" Stopped with {left} still to go." if left else "")
                        + " When you are done, go to <b>Finish</b> and reboot once to see what sticks.", "ok")


def read_packages():
    allp = TV.packages()
    if not allp:
        raise RuntimeError("the TV returned no packages")
    return allp, TV.packages("-s"), TV.packages("-d")


def guard_check(names):
    """The guards from tools/disable.sh, run against the TV. Returns (names to disable, [(skipped, why)])."""
    skipped = []
    names = [n for n in names if PACKAGE_RE.fullmatch(n) and not is_core(n)]
    # Setup wizard owning the saved Wi-Fi network: Android deletes the network when it is disabled.
    if SETUPWRAITH in names:
        wifi = TV.sh("dumpsys wifi | grep -o 'cname=[^ ]*'", quiet=True)
        if "cname=" not in wifi:
            skipped.append((SETUPWRAITH, "could not check which app owns the saved Wi-Fi networks. If the TV uses "
                                         "Ethernet, disable it from tools/disable.ps1 with FORCE_SETUPWRAITH=1."))
        elif re.search(r"cname=[^ ]*setupwraith", wifi):
            skipped.append((SETUPWRAITH, "the saved Wi-Fi network belongs to it, and disabling it would delete that "
                                         "network and take the TV off Wi-Fi and ADB. Forget the network and join it "
                                         "again in Settings, then try again."))
        if any(s[0] == SETUPWRAITH for s in skipped):
            names.remove(SETUPWRAITH)
    # CVTE boards keep their stock launcher (#741): without it a JVC set hung on its boot animation.
    if (TV.info or {}).get("cvte"):
        for p in [n for n in names if n.startswith("com.cvte.tv.launcher")]:
            names.remove(p)
            skipped.append((p, "this is a CVTE board, and its stock launcher stays enabled unless the tested list for "
                               "this exact board disables it (#741). Use tools\\disable.ps1 with that list if it does."))
    # Home guard (#239): never leave the TV with nothing that can answer HOME.
    home, _ = TV.home_owner()
    if not home:
        log("could not tell which app owns Home, so the Home guard did not run: check by hand that your "
            "launcher is not in the list (#795)", "warn")
    elif home in names:
        others = [p for p in TV.home_claimants() if p != home and p not in names and p not in NOT_LAUNCHERS
                  and not re.search(r"factorytest|factory_test|factorymode", p)]
        if not others:
            names.remove(home)
            skipped.append((home, "it owns Home and no other launcher is installed and staying enabled. Install the "
                                  "new launcher first (Extras page), then disable the old one."))
    # TV input drivers (#321): with one disabled, HDMI/AV/tuner show No Signal for good.
    if names:
        loop = ("for p in " + " ".join(names) + "; do dumpsys package $p | sed -n -E "
                "'/requested permissions:/,/(install|runtime) permissions:|User [0-9]+:/p' | "
                "grep -q TV_INPUT_HARDWARE && echo $p; done; true")
        hw = {l.strip() for l in TV.sh(loop, quiet=True, timeout=300).splitlines() if l.strip()}
        for p in list(names):
            if p in hw:
                names.remove(p)
                skipped.append((p, "it asks for TV_INPUT_HARDWARE, so it drives the HDMI/AV/tuner inputs. Disabled, "
                                   "they show No Signal until a full restore and a cold boot (#321)."))
    return names, skipped


def gui_list_path():
    tag = re.sub(r"[^A-Za-z0-9.-]", "_", TV.host or "no-host")
    return GUI_LISTS / f"{tag}.txt"


def save_record(names):
    """Append names to this TV's list and let tools/recovery.py record their state before any change."""
    path = gui_list_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if path.exists():
        existing = [l.split("#", 1)[0].strip() for l in path.read_text(encoding="utf-8").splitlines()]
        existing = [l for l in existing if l]
    new = [n for n in names if n not in existing]
    if not path.exists():
        path.write_text(f"# CleanYourTV: packages disabled from the app on {TV.info.get('model', '')} "
                        f"({TV.host}).\n# Undo: Finish page → Restore, or tools\\restore.ps1 -TvHost {TV.host} "
                        f"\"{path}\"\n", encoding="utf-8")
    if new:
        with open(path, "a", encoding="utf-8") as f:
            f.write("".join(n + "\n" for n in new))
    if DEMO or recmod is None:
        log(f"(demo) would record the state of {len(names)} packages in {path}", "warn")
        return path
    buf = io.StringIO()
    with TV.lock, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        recmod.save(str(path), TV.host)
    out = buf.getvalue().strip()
    if out:
        log(out, "ok")
    return path


def settings_undo_path(host=None):
    tag = re.sub(r"[^A-Za-z0-9.-]", "_", host or TV.host or "no-host")
    return DATA / f"settings-undo-{tag}.json"


SETTING_KEY_RE = re.compile(r"(global|secure|system)/[A-Za-z0-9_]+")


def remember_settings(keys):
    """Record the TV's own value of each setting before the app first changes it. The first value wins, like the
    package record: a later run must not record the app's own change as the original."""
    path = settings_undo_path()
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rec.get("settings"), dict):
            raise ValueError
    except (OSError, ValueError):
        rec = {"created": time.strftime("%Y-%m-%d %H:%M"), "host": TV.host, "model": TV.info.get("model"),
               "settings": {}}
    new = [k for k in keys if SETTING_KEY_RE.fullmatch(k) and k not in rec["settings"]]
    if not new or DEMO and not TV.connected:
        return
    for k in new:
        ns, key = k.split("/")
        rec["settings"][k] = TV.sh(f"settings get {ns} {key}", quiet=True).strip()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    os.replace(tmp, path)
    log(f"recorded the TV's own value of {len(new)} setting{'s' if len(new) != 1 else ''} before changing them", "ok")


def settings_from_commands(cmds):
    return [f"{m.group(1)}/{m.group(2)}" for c in cmds
            for m in [re.match(r"settings (?:put|delete) (global|secure|system) ([A-Za-z0-9_]+)", c.strip())] if m]


def settings_restore_commands(host):
    try:
        rec = json.loads(settings_undo_path(host).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    cmds = []
    for k, v in (rec.get("settings") or {}).items():
        if not SETTING_KEY_RE.fullmatch(k):
            continue
        ns, key = k.split("/")
        v = str(v).strip()
        if v in ("", "null"):
            cmds.append(f"settings delete {ns} {key}")
        elif SETTING_VALUE_RE.fullmatch(v):
            cmds.append(f"settings put {ns} {key} {v}")
    return cmds


REFUSED = {}   # package -> why the TV refused it, from the last batch


def refusal_reason(out):
    """pm's answer when it would not disable one package, in a few words; "" when it said nothing useful."""
    o = out.lower()
    if "protected" in o:
        return "protected by Android (cannot be disabled)"
    if "cannot disable" in o or "can't disable" in o or "not allowed" in o or "securityexception" in o:
        return "the TV does not allow disabling it"
    if "unknown package" in o or "not found" in o:
        return "not on this TV"
    return ""


def disable_batch(names):
    REFUSED.clear()
    outs = {}
    for n in names:   # one pm command per shell call: chained commands can stop after the first
        outs[n] = TV.sh(f"pm disable-user --user 0 {n}")
    disabled = TV.packages("-d")
    done = [n for n in names if n in disabled]
    failed = [n for n in names if n not in disabled]
    for n in failed:
        why = refusal_reason(outs.get(n, ""))
        if why:
            REFUSED[n] = why
    shot, err = None, None
    try:
        TV.sh("input keyevent KEYCODE_HOME", quiet=True)
        time.sleep(1.5)
        shot = TV.screenshot()
    except Exception as e:
        err = str(e)
    return done, failed, shot, err


class RemotePage(Page):
    title = "Remote & screen"
    subtitle = "Press remote buttons and see the TV screen"

    def __init__(self, win):
        super().__init__(win)
        row = QHBoxLayout()
        row.setSpacing(14)

        c, lay = card(spacing=14)
        c.setFixedWidth(300)
        lay.addWidget(label("Remote", "H2"))
        self.pad = DPad()
        lay.addWidget(self.pad, 0, Qt.AlignmentFlag.AlignHCenter)
        grid = QGridLayout()
        grid.setSpacing(12)
        keys = [("back", "BACK", "Back (Esc)"), ("home", "HOME", "Home (H)"), ("menu", "MENU", "Menu"),
                ("voldown", "VOLUME_DOWN", "Volume down (-)"), ("mute", "VOLUME_MUTE", "Mute"),
                ("volup", "VOLUME_UP", "Volume up (+)"),
                ("input", "TV_INPUT", "Input / source"), ("play", "MEDIA_PLAY_PAUSE", "Play / pause (Space)"),
                ("gear", "SETTINGS", "Settings")]
        for i, (ico_name, key, tip) in enumerate(keys):
            b = QPushButton()
            b.setObjectName("Key")
            b.setIcon(icon(ico_name, C["text"], 20))
            b.setIconSize(QSize(20, 20))
            b.setToolTip(tip)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _, k=key: self.press(k))
            grid.addWidget(b, i // 3, i % 3, Qt.AlignmentFlag.AlignCenter)
        lay.addLayout(grid)
        self.text = QLineEdit()
        self.text.setPlaceholderText("Type text into the TV…")
        self.text.returnPressed.connect(self.send_text)
        lay.addWidget(self.text)
        self.auto = Toggle("Capture after each key")
        self.auto.setChecked(win.settings.value("auto_capture", "true") == "true")
        self.auto.toggled.connect(lambda v: win.settings.setValue("auto_capture", "true" if v else "false"))
        lay.addWidget(self.auto)
        lay.addWidget(label("Keyboard: arrows, Enter = OK, Esc/Backspace = Back, H = Home, +/- volume.", "Dim",
                            wrap=True))
        lay.addStretch(1)
        row.addWidget(c, 0, Qt.AlignmentFlag.AlignTop)

        c, lay = card()
        top = QHBoxLayout()
        top.addWidget(label("TV screen", "H2"))
        top.addStretch(1)
        self.cap = button("Capture", "Primary", "camera")
        self.save = button("Save PNG…", None, "save")
        top.addWidget(self.save)
        top.addWidget(self.cap)
        lay.addLayout(top)
        self.view = ShotView("Press Capture to grab the TV screen")
        self.view.setMinimumSize(560, 315)
        lay.addWidget(self.view, 1)
        self.msg = Banner("")
        lay.addWidget(self.msg)
        lay.addWidget(label("Live TV, HDMI and some streaming apps (Netflix) capture as an empty image: that is "
                            "the TV protecting the picture, not a broken debloat.", "Dim", wrap=True))
        row.addWidget(c, 1)
        self.body.addLayout(row)
        self.body.addStretch(1)

        self.pad.pressed.connect(self.press)
        self.cap.clicked.connect(lambda: self.win.capture())
        self.save.clicked.connect(self.save_png)
        BUS.shot.connect(self.view.set_path)
        self.busy = False
        self.pending = False

    def keyPressEvent(self, e):
        k = e.key()
        m = {Qt.Key.Key_Up: "DPAD_UP", Qt.Key.Key_Down: "DPAD_DOWN", Qt.Key.Key_Left: "DPAD_LEFT",
             Qt.Key.Key_Right: "DPAD_RIGHT", Qt.Key.Key_Return: "DPAD_CENTER", Qt.Key.Key_Enter: "DPAD_CENTER",
             Qt.Key.Key_Escape: "BACK", Qt.Key.Key_Backspace: "BACK", Qt.Key.Key_H: "HOME",
             Qt.Key.Key_Plus: "VOLUME_UP", Qt.Key.Key_Minus: "VOLUME_DOWN", Qt.Key.Key_Space: "MEDIA_PLAY_PAUSE"}
        if k in m and not self.text.hasFocus():
            self.press(m[k])
        else:
            super().keyPressEvent(e)

    def press(self, key):
        if not self.need_tv():
            return
        run_job(lambda: TV.sh(f"input keyevent {keycode(key)}", quiet=True))
        if self.auto.isChecked():
            self.schedule_capture()

    def schedule_capture(self):
        # Coalesce: several quick key presses give one capture afterwards.
        if self.busy:
            self.pending = True
            return
        self.busy = True
        QTimer.singleShot(700, self._capture)

    def _capture(self):
        self.win.capture(on_done=self._captured)

    def _captured(self):
        self.busy = False
        if self.pending:
            self.pending = False
            self.schedule_capture()

    def send_text(self):
        t = self.text.text()
        if not t or not self.need_tv():
            return
        safe = re.sub(r"[^A-Za-z0-9@._\-+:/ ]", "", t).replace(" ", "%s")
        run_job(lambda: TV.sh(f"input text '{safe}'", quiet=True))
        self.text.clear()
        if self.auto.isChecked():
            self.schedule_capture()

    def save_png(self):
        if not self.view.path:
            return
        dest, _ = QFileDialog.getSaveFileName(self, "Save screenshot", str(Path.home() / Path(self.view.path).name),
                                              "PNG (*.png)")
        if dest:
            shutil.copyfile(self.view.path, dest)


# ----------------------------------------------------------------------------------------------
# Build toolchain for the launcher: a JDK Gradle 8.9 can run on (17-22) and the Android SDK
# ----------------------------------------------------------------------------------------------
JDK_MIN, JDK_MAX = 17, 22          # AGP 8.5 needs 17+, Gradle 8.9 runs on up to 22
SDK_PLATFORM, SDK_BUILD_TOOLS = "android-34", "34.0.0"
JDK_HOME_DIR = APPDATA / "jdk"
SDK_HOME_DIR = APPDATA / "android-sdk"
TEMURIN_URL = {
    "nt": "https://api.adoptium.net/v3/binary/latest/21/ga/windows/x64/jdk/hotspot/normal/eclipse",
}.get(os.name, "")
CMDLINE_FALLBACK = "https://dl.google.com/android/repository/commandlinetools-win-15859902_latest.zip"
SDK_LICENSE_URL = "https://developer.android.com/studio/terms"


def java_major(home):
    home = Path(home)
    try:
        m = re.search(r'JAVA_VERSION="(\d+)(?:\.(\d+))?', (home / "release").read_text(errors="replace"))
        if m:
            v = int(m.group(1))
            return int(m.group(2) or 0) if v == 1 else v
    except OSError:
        pass
    exe = home / "bin" / ("java.exe" if os.name == "nt" else "java")
    if exe.is_file():
        try:
            p = subprocess.run([str(exe), "-version"], capture_output=True, text=True, timeout=20,
                               creationflags=NO_WINDOW)
            m = re.search(r'version "(\d+)(?:\.(\d+))?', p.stderr + p.stdout)
            if m:
                v = int(m.group(1))
                return int(m.group(2) or 0) if v == 1 else v
        except Exception:
            pass
    return 0


def _globs(base, patterns):
    out = []
    if not base:
        return out
    base = Path(base)
    for pat in patterns:
        try:
            out += sorted(base.glob(pat), reverse=True)
        except OSError:
            pass
    return out


def jdk_candidates():
    c = []
    for var in ("JAVA_HOME", "JDK_HOME"):
        if os.environ.get(var):
            c.append(Path(os.environ[var]))
    c += _globs(JDK_HOME_DIR, ["*"])
    if os.name == "nt":
        local = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        for pf in {os.environ.get("ProgramFiles"), os.environ.get("ProgramW6432"), os.environ.get("ProgramFiles(x86)"),
                   "C:\\Program Files"}:
            c += _globs(pf, ["Android/Android Studio*/jbr", "Android/Android Studio*/jre", "Android Studio*/jbr",
                             "Eclipse Adoptium/jdk-*", "Eclipse Foundation/jdk-*", "Java/jdk*", "Microsoft/jdk-*",
                             "Zulu/zulu*", "Amazon Corretto/jdk*", "BellSoft/LibericaJDK-*", "OpenJDK/jdk-*",
                             "JetBrains/*/jbr"])
        c += _globs(local, ["Programs/Android Studio*/jbr", "Android/Android Studio*/jbr",
                            "JetBrains/Toolbox/apps/*/jbr", "JetBrains/Toolbox/apps/*/*/*/jbr",
                            "Programs/Eclipse Adoptium/jdk-*"])
    elif sys.platform == "darwin":
        c += _globs("/Applications", ["Android Studio*.app/Contents/jbr/Contents/Home"])
        c += _globs("/Library/Java/JavaVirtualMachines", ["*/Contents/Home"])
    else:
        c += _globs("/usr/lib/jvm", ["*"]) + _globs(Path.home(), ["android-studio/jbr"]) + _globs("/opt", ["android-studio/jbr"])
    c += _globs(Path.home(), [".jdks/*", ".gradle/jdks/*"])
    seen, out = set(), []
    for p in c:
        key = str(p).lower()
        if key not in seen and (p / "bin" / ("java.exe" if os.name == "nt" else "java")).is_file():
            seen.add(key)
            out.append(p)
    return out


def find_jdk():
    """(home, major) of the best JDK in range, preferring 21, then 17, then the newest in range."""
    found = [(p, java_major(p)) for p in jdk_candidates()]
    ok = [(p, v) for p, v in found if JDK_MIN <= v <= JDK_MAX]
    if not ok:
        return None, found
    ok.sort(key=lambda t: (t[1] != 21, t[1] != 17, -t[1]))
    return ok[0], found


def sdk_candidates():
    c = [Path(os.environ[v]) for v in ("ANDROID_HOME", "ANDROID_SDK_ROOT") if os.environ.get(v)]
    if os.name == "nt":
        c.append(Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "Android" / "Sdk")
    elif sys.platform == "darwin":
        c.append(Path.home() / "Library" / "Android" / "sdk")
    else:
        c.append(Path.home() / "Android" / "Sdk")
    c.append(SDK_HOME_DIR)
    return c


def find_sdk():
    for p in sdk_candidates():
        if p.is_dir() and any((p / d).exists() for d in ("platforms", "build-tools", "cmdline-tools", "platform-tools")):
            return p
    return None


def sdk_missing(sdk):
    miss = []
    if not (sdk / "platforms" / SDK_PLATFORM).is_dir():
        miss.append(f"platforms;{SDK_PLATFORM}")
    if not (sdk / "build-tools" / SDK_BUILD_TOOLS).is_dir():
        miss.append(f"build-tools;{SDK_BUILD_TOOLS}")
    return miss


def sdkmanager_path(sdk):
    name = "sdkmanager.bat" if os.name == "nt" else "sdkmanager"
    for cand in [sdk / "cmdline-tools" / "latest" / "bin" / name] + _globs(sdk, [f"cmdline-tools/*/bin/{name}"]) \
            + [sdk / "tools" / "bin" / name]:
        if cand.is_file():
            return cand
    return None


def _download(url, dest, say):
    import urllib.request
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": f"CleanYourTV/{APP_VERSION}"})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        total = int(r.headers.get("Content-Length") or 0)
        done, last = 0, 0
        while True:
            buf = r.read(1 << 20)
            if not buf:
                break
            f.write(buf)
            done += len(buf)
            if done - last >= 8 << 20 or (total and done == total):
                last = done
                say(f"  {done / 1e6:.0f} MB" + (f" of {total / 1e6:.0f} MB" if total else ""))


def _safe_extract(zip_path, dest):
    import zipfile
    dest = Path(dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        for m in z.infolist():
            t = (dest / m.filename).resolve()
            if t != dest and dest not in t.parents:
                raise RuntimeError(f"unexpected path in the archive: {m.filename}")
        z.extractall(dest)
        tops = {n.split("/", 1)[0] for n in z.namelist() if n.strip("/")}
    return [dest / t for t in tops]


def install_jdk(say):
    if not TEMURIN_URL:
        raise RuntimeError("Install a JDK 17 or 21 with your package manager, then try again.")
    say("Downloading Eclipse Temurin JDK 21 (about 200 MB, once)…")
    tmp = APPDATA / "jdk-download.zip"
    try:
        _download(TEMURIN_URL, tmp, say)
        say("Unpacking the JDK…")
        tops = _safe_extract(tmp, JDK_HOME_DIR)
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass
    for t in tops:
        if java_major(t) >= JDK_MIN:
            say(f"JDK ready: {t}")
            return t
    raise RuntimeError("the downloaded JDK could not be started")


def cmdline_tools_url():
    import urllib.request
    try:
        req = urllib.request.Request("https://dl.google.com/android/repository/repository2-3.xml",
                                     headers={"User-Agent": f"CleanYourTV/{APP_VERSION}"})
        xml = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        osname = {"nt": "win"}.get(os.name, "mac" if sys.platform == "darwin" else "linux")
        names = re.findall(rf"commandlinetools-{osname}-(\d+)_latest\.zip", xml)
        if names:
            return f"https://dl.google.com/android/repository/commandlinetools-{osname}-{max(names, key=int)}_latest.zip"
    except Exception:
        pass
    return CMDLINE_FALLBACK


def install_sdk(sdk, jdk, say):
    """Command-line tools if missing, then platform 34 and build-tools 34.0.0. Licences were accepted by the user."""
    sdk = Path(sdk)
    sdk.mkdir(parents=True, exist_ok=True)
    mgr = sdkmanager_path(sdk)
    if not mgr:
        url = cmdline_tools_url()
        say(f"Downloading the Android command-line tools…\n  {url}")
        tmp = APPDATA / "cmdline-tools.zip"
        stage = APPDATA / "cmdline-stage"
        shutil.rmtree(stage, ignore_errors=True)
        try:
            _download(url, tmp, say)
            say("Unpacking…")
            _safe_extract(tmp, stage)
        finally:
            try:
                tmp.unlink()
            except OSError:
                pass
        target = sdk / "cmdline-tools" / "latest"
        shutil.rmtree(target, ignore_errors=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(stage / "cmdline-tools"), str(target))
        shutil.rmtree(stage, ignore_errors=True)
        mgr = sdkmanager_path(sdk)
        if not mgr:
            raise RuntimeError("the command-line tools did not unpack as expected")
    env = dict(os.environ, JAVA_HOME=str(jdk), ANDROID_HOME=str(sdk), ANDROID_SDK_ROOT=str(sdk))
    env["PATH"] = str(Path(jdk) / "bin") + os.pathsep + env.get("PATH", "")

    def run(args, feed=None):
        say("$ sdkmanager " + " ".join(args))
        argv = [str(mgr), f"--sdk_root={sdk}"] + args
        if os.name == "nt":
            # sdkmanager is a .bat: cmd.exe splits unquoted arguments at ';' and '=', which turned
            # platforms;android-34 into two unknown packages. Quote every argument.
            argv = " ".join('"' + a.replace('"', '') + '"' for a in argv)
        p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, env=env, creationflags=NO_WINDOW)
        if feed:
            try:
                p.stdin.write(feed)
                p.stdin.flush()
            except OSError:
                pass
        try:
            p.stdin.close()
        except OSError:
            pass
        last, shown = "", {}
        for line in p.stdout:
            line = line.rstrip()
            if not line or line.startswith("[") or line == last:
                continue
            last = line
            # sdkmanager redraws its progress bar many times a second: one line per file per 10% is enough.
            bar = re.search(r"^(.*?)\s*\[[^\]]*\]\s*(\d+)%", line)
            if bar:
                what, pct = bar.group(1).strip(), int(bar.group(2))
                step = pct // 10
                if shown.get(what, -1) >= step:
                    continue
                shown[what] = step
                line = f"{what.rsplit('/', 1)[-1]}  {pct}%"
            say("  " + line[:160])
        p.wait()
        if p.returncode != 0:
            raise RuntimeError(f"sdkmanager {' '.join(args)} failed (exit {p.returncode})")

    run(["--licenses"], feed="y\n" * 30)
    run(["platform-tools", f"platforms;{SDK_PLATFORM}", f"build-tools;{SDK_BUILD_TOOLS}"])
    still = sdk_missing(sdk)
    if still:
        # Never claim success that the folder does not show. With the licences accepted, the Android Gradle
        # plugin downloads missing platforms and build-tools by itself, so the build can still go ahead.
        say("Not installed yet: " + ", ".join(still) + ". Gradle will try to download them itself during the build.")
    else:
        say("Android SDK ready.")
    return sdk


# ----------------------------------------------------------------------------------------------
# Live TV row: a channels row on the launcher's Home (live_tv_row). The launcher has no such row, so
# this app adds it to the toolkit's launcher code before every build: the toolkit itself is updated from
# GitHub and would otherwise lose it. All or nothing; a launcher that changed upstream builds without it.
# ----------------------------------------------------------------------------------------------
LIVETV_PERMISSION = "android.permission.READ_TV_LISTINGS"
LIVETV_EDITS = [
    ('AndroidManifest.xml',
     '    <uses-permission android:name="yandex.tv.permission.ACCESS_TV_SOURCE" />\n',
     '    <uses-permission android:name="yandex.tv.permission.ACCESS_TV_SOURCE" />\n    <!-- live_tv_row: reads the tuner\'s channels for the Live TV row (ChannelRow). A runtime permission,\n         granted with pm grant by CleanYourTV; without it the row does not appear. -->\n    <uses-permission android:name="android.permission.READ_TV_LISTINGS" />\n    <!-- tile_menu Uninstall: opens Android\'s own uninstall prompt for an app the person installed. -->\n    <uses-permission android:name="android.permission.REQUEST_DELETE_PACKAGES" />\n'),
    ('AndroidManifest.xml',
     '    <queries>\n',
     '    <queries>\n        <!-- live_tv_row: the TV provider that lists the tuner\'s channels (ChannelRow). -->\n        <provider android:authorities="android.media.tv" />\n'),
    ('res/values/config.xml',
     '    <bool name="boot_to_live_tv">false</bool>\n',
     '    <bool name="boot_to_live_tv">false</bool>\n\n    <!-- A "Live TV" row of the tuner\'s channels after the app grid, read from the TV provider (needs\n         READ_TV_LISTINGS, granted over ADB). OK on a channel tunes it in the Live TV app. Off by default; a\n         theme can set "live_tv_row": true. -->\n    <bool name="live_tv_row">false</bool>\n    <!-- Where the Live TV row sits: "bottom" after the app grid, or "top" above the dock, where the top shelf\n         usually shows the focused app\'s name. A theme can set "live_tv_row_position". -->\n    <string name="live_tv_row_position" translatable="false">bottom</string>\n'),
    ('res/values/strings.xml',
     '</resources>',
     '    <!-- Title of the Live TV row (live_tv_row). -->\n    <string name="live_tv_row" translatable="false">Live TV</string>\n    <!-- Hold-OK tile menu: opens the app, like OK (tile_menu). -->\n    <string name="tile_open">Open</string>\n    <string name="tile_uninstall">Uninstall</string>\n    <!-- Hold OK on a channel in the Live TV row (live_tv_row). -->\n    <string name="channel_move">Move</string>\n    <string name="channel_hide">Hide this channel</string>\n    <string name="channel_show_hidden">Unhide all channels (%1$d)</string>\n    <string name="channel_reset_order">Original channel order</string>\n    <string name="channel_move_hint">Left and Right move the channel, OK places it.</string>\n</resources>'),
    ('java/com/gathin/tvhome/AppAdapter.java',
     '    private final boolean showLibrary;\n',
     '    private final boolean showLibrary;\n    /** The Live TV row (live_tv_row), shown after the app tiles while it has channels; null when off. */\n    private ChannelRow channelRow;\n'),
    ('java/com/gathin/tvhome/AppAdapter.java',
     '        if (viewType == 1) {\n',
     '        if (viewType == 2) return channelRow.createRowHolder(parent);\n        if (viewType == 1) {\n'),
    ('java/com/gathin/tvhome/AppAdapter.java',
     '        if (isLibraryAt(position)) return;\n        Holder h = (Holder) holder;\n',
     '        if (isLibraryAt(position) || isChannelsAt(position)) return;\n        Holder h = (Holder) holder;\n'),
    ('java/com/gathin/tvhome/AppAdapter.java',
     '        return items.size() + (showLibrary ? 1 : 0);\n',
     '        return items.size() + (hasChannels() ? 1 : 0) + (showLibrary ? 1 : 0);\n'),
    ('java/com/gathin/tvhome/AppAdapter.java',
     '    boolean isLibraryAt(int position) { return showLibrary && position == items.size(); }\n',
     '    boolean isLibraryAt(int position) { return showLibrary && position == libraryPosition(); }\n\n    /** Where the library pill sits: after the apps, and after the Live TV row when that is shown. */\n    int libraryPosition() { return items.size() + (hasChannels() ? 1 : 0); }\n\n    void setChannelRow(ChannelRow row) { channelRow = row; }\n\n    boolean hasChannels() { return channelRow != null && channelRow.size() > 0; }\n\n    int channelsPosition() { return items.size(); }\n\n    boolean isChannelsAt(int position) { return hasChannels() && position == items.size(); }\n'),
    ('java/com/gathin/tvhome/AppAdapter.java',
     '    @Override public int getItemViewType(int position) { return isLibraryAt(position) ? 1 : 0; }\n',
     '    @Override public int getItemViewType(int position) { return isLibraryAt(position) ? 1 : isChannelsAt(position) ? 2 : 0; }\n'),
    ('java/com/gathin/tvhome/AppAdapter.java',
     '        return isLibraryAt(position) ? Long.MIN_VALUE : items.get(position)',
     '        if (isChannelsAt(position)) return Long.MIN_VALUE + 1;\n        return isLibraryAt(position) ? Long.MIN_VALUE : items.get(position)'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '    private boolean libraryFocusPending;\n',
     '    private boolean libraryFocusPending;\n    /** The Live TV row (live_tv_row; null when off), the channel used last, and whether to go back to it. */\n    private ChannelRow channelRow;\n    private int lastChannel;\n    private boolean channelFocusPending;\n    /** live_tv_row_position "top": the row is its own view above the dock, moved with the grid (placeTopChannels). */\n    private boolean channelsOnTop;\n    private RecyclerView.ViewHolder topChannels;\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '        adapter = new AppAdapter(this, this, COLUMNS, cfg);\n',
     '        adapter = new AppAdapter(this, this, COLUMNS, cfg);\n        if (ChannelRow.enabled(this)) {\n            channelRow = new ChannelRow(channelListener, animations && !reducedMotion);\n            channelsOnTop = ChannelRow.onTop(this);\n            if (channelsOnTop) addTopChannels();\n            else adapter.setChannelRow(channelRow);\n        }\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     'adapter.isLibraryAt(position) ? COLUMNS : 1; }',
     '(adapter.isLibraryAt(position) || adapter.isChannelsAt(position)) ? COLUMNS : 1; }'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '        RecyclerView.ViewHolder footer = grid.findViewHolderForAdapterPosition(adapter.appCount());\n        final boolean restoreLibrary = adapter.isLibraryAt(adapter.appCount()) && footer != null\n',
     '        RecyclerView.ViewHolder footer = grid.findViewHolderForAdapterPosition(adapter.libraryPosition());\n        final boolean restoreLibrary = adapter.isLibraryAt(adapter.libraryPosition()) && footer != null\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '                && footer.itemView.findViewById(R.id.btnLibrary).hasFocus();\n',
     '                && footer.itemView.findViewById(R.id.btnLibrary).hasFocus();\n        RecyclerView.ViewHolder channelsHolder = adapter.hasChannels()\n                ? grid.findViewHolderForAdapterPosition(adapter.channelsPosition()) : null;\n        final boolean restoreChannels = (channelsHolder != null && channelsHolder.itemView.hasFocus())\n                || (topChannels != null && topChannels.itemView.hasFocus());\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '            if (restoreLibrary) grid.post(this::focusLibrary);\n            else restoreFocus();\n',
     '            if (restoreLibrary) grid.post(this::focusLibrary);\n            else if (restoreChannels) grid.post(this::focusChannels);\n            else restoreFocus();\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '            if (returnToLibrary || libraryFocusPending) focusLibrary();\n            else focusTile(pos >= 0 ? pos : returnSlot);\n',
     '            if (returnToLibrary || libraryFocusPending) focusLibrary();\n            else if (channelFocusPending && (adapter.hasChannels() || topChannelsShown())) focusChannels();\n            else focusTile(pos >= 0 ? pos : returnSlot);\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '            if (forward && position == adapter.focusablePosition(count - 1) && adapter.isLibraryAt(count)) {\n                focusLibrary();\n',
     '            if (forward && position == adapter.focusablePosition(count - 1) && hasFooter()) {\n                focusFooter();\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '            if (position >= lastRowStart) {\n                if (adapter.isLibraryAt(count)) focusLibrary();\n',
     '            if (position >= lastRowStart) {\n                focusFooter();\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '    @Override public void onLibraryFocused() {\n        libraryFocusPending = false;\n',
     '    @Override public void onLibraryFocused() {\n        libraryFocusPending = false;\n        channelFocusPending = false;\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '    @Override public void onLibraryUp() {\n        if (adapter.appCount() == 0) { firstTopButton().requestFocus(); return; }\n',
     '    @Override public void onLibraryUp() {\n        if (adapter.hasChannels()) { focusChannels(); return; }\n        focusLastRow();\n    }\n\n    /** Up from a footer: the last app row, in the column used last, or the top bar when there are no apps. */\n    private void focusLastRow() {\n        if (adapter.appCount() == 0) { firstTopButton().requestFocus(); return; }\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '        int position = adapter.appCount();\n        if (!adapter.isLibraryAt(position)) return;\n',
     '        int position = adapter.libraryPosition();\n        if (!adapter.isLibraryAt(position)) return;\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '                RecyclerView.ViewHolder footer = grid.findViewHolderForAdapterPosition(adapter.appCount());\n                if (footer != null && adapter.isLibraryAt(adapter.appCount())\n',
     '                RecyclerView.ViewHolder footer = grid.findViewHolderForAdapterPosition(adapter.libraryPosition());\n                if (footer != null && adapter.isLibraryAt(adapter.libraryPosition())\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '    private void cancelPendingFocusScroll() {\n',
     '    private boolean hasFooter() {\n        return adapter.hasChannels() || adapter.isLibraryAt(adapter.libraryPosition());\n    }\n\n    /** Down from the last app row, or Right from the last app: the Live TV row, else the library pill. */\n    private void focusFooter() {\n        if (adapter.hasChannels()) focusChannels();\n        else if (adapter.isLibraryAt(adapter.libraryPosition())) focusLibrary();\n    }\n\n    /** Focuses the Live TV row on the channel used last, scrolling the grid to it first when needed. */\n    private void focusChannels() {\n        if (channelsOnTop) { focusTopChannels(); return; }\n        if (channelRow == null || !adapter.hasChannels()) return;\n        cancelPendingFocusScroll();\n        libraryFocusPending = false;\n        final int position = adapter.channelsPosition();\n        RecyclerView.ViewHolder holder = grid.findViewHolderForAdapterPosition(position);\n        if (holder != null) {\n            Rect visible = new Rect();\n            if (holder.itemView.getGlobalVisibleRect(visible) && visible.height() >= holder.itemView.getHeight()) {\n                if (channelRow.focus(holder, lastChannel)) channelFocusPending = false;\n                return;\n            }\n        }\n        if (!animations) {\n            grid.scrollToPosition(position);\n            grid.post(() -> {\n                RecyclerView.ViewHolder h = grid.findViewHolderForAdapterPosition(position);\n                if (h != null && channelRow.focus(h, lastChannel)) channelFocusPending = false;\n            });\n            return;\n        }\n        pendingFocusScroll = new RecyclerView.OnScrollListener() {\n            @Override public void onScrollStateChanged(@NonNull RecyclerView rv, int state) {\n                if (state != RecyclerView.SCROLL_STATE_IDLE) return;\n                rv.removeOnScrollListener(this);\n                if (pendingFocusScroll != this) return;\n                pendingFocusScroll = null;\n                RecyclerView.ViewHolder h = rv.findViewHolderForAdapterPosition(position);\n                if (h != null && channelRow.focus(h, lastChannel)) channelFocusPending = false;\n            }\n        };\n        grid.addOnScrollListener(pendingFocusScroll);\n        grid.smoothScrollToPosition(position);\n    }\n\n    private final ChannelRow.Listener channelListener = new ChannelRow.Listener() {\n        @Override public void onChannelOpen(int index, ChannelRow.Channel channel) {\n            lastChannel = index;\n            channelFocusPending = true;\n            open(ChannelRow.viewIntent(MainActivity.this, channel.id, liveTvPkg));\n        }\n\n        @Override public void onChannelFocused(int index) {\n            lastChannel = index;\n            channelFocusPending = false;\n            libraryFocusPending = false;\n            hideGlass();\n            hideHero();\n        }\n\n        @Override public void onChannelsUp() {\n            channelFocusPending = false;\n            if (channelsOnTop) {\n                topButtonAbove(getCurrentFocus()).requestFocus();\n                return;\n            }\n            focusLastRow();\n        }\n\n        @Override public void onChannelsEdited() {\n            loadChannels();\n        }\n\n        @Override public void onChannelsDown() {\n            if (channelsOnTop) { focusTile(lastFocused % COLUMNS); return; }\n            if (adapter.isLibraryAt(adapter.libraryPosition())) focusLibrary();\n        }\n    };\n\n    /** The Live TV row above the dock (live_tv_row_position "top"): a view of its own over the grid\'s top room. */\n    private void addTopChannels() {\n        FrameLayout root = findViewById(R.id.root);\n        topChannels = channelRow.createRowHolder(root);\n        View row = topChannels.itemView;\n        row.setVisibility(View.GONE);\n        root.addView(row, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,\n                ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.TOP | Gravity.LEFT));\n        // A new height changes the room the grid keeps above the dock.\n        row.addOnLayoutChangeListener((v, l, t, r, b, ol, ot, or, ob) -> {\n            if (b - t != ob - ot) grid.post(grid::requestLayout);\n            placeTopChannels();\n        });\n        grid.addOnScrollListener(new RecyclerView.OnScrollListener() {\n            @Override\n            public void onScrolled(@NonNull RecyclerView rv, int dx, int dy) {\n                placeTopChannels();\n            }\n        });\n    }\n\n    private boolean topChannelsShown() {\n        return topChannels != null && channelRow != null && channelRow.size() > 0\n                && topChannels.itemView.getVisibility() == View.VISIBLE;\n    }\n\n    /** The room the top row needs above the dock, 0 when it is not shown. */\n    private int topChannelsRoom() {\n        return topChannelsShown() ? topChannels.itemView.getHeight() + (int) (AppAdapter.TOP_ROOM_DP * density) : 0;\n    }\n\n    /** Puts the top row just above the dock and moves it with the grid, fading it out as the grid scrolls. */\n    private void placeTopChannels() {\n        if (topChannels == null) return;\n        View row = topChannels.itemView;\n        if (!(row.getParent() instanceof View)) return;\n        int[] g = new int[2];\n        int[] r = new int[2];\n        grid.getLocationInWindow(g);\n        ((View) row.getParent()).getLocationInWindow(r);\n        int width = grid.getWidth() - grid.getPaddingLeft() - grid.getPaddingRight() + (int) (24 * density);\n        ViewGroup.LayoutParams lp = row.getLayoutParams();\n        if (width > 0 && lp.width != width) {\n            lp.width = width;\n            row.setLayoutParams(lp);\n        }\n        // Placed with margins, not translation: Android\'s focus search goes by layout position, so a row moved\n        // only by translation would still sit at the top for the remote and take Left/Right from the top bar.\n        int gridTop = g[1] - r[1];\n        int top = Math.max(gridTop, gridTop + grid.getPaddingTop() - row.getHeight() - (int) (14 * density));\n        int left = g[0] - r[0] + grid.getPaddingLeft() - (int) (12 * density);\n        if (lp instanceof ViewGroup.MarginLayoutParams) {\n            ViewGroup.MarginLayoutParams m = (ViewGroup.MarginLayoutParams) lp;\n            if (m.topMargin != top || m.leftMargin != left) {\n                m.topMargin = top;\n                m.leftMargin = left;\n                row.setLayoutParams(m);\n            }\n        }\n        // While the grid is scrolled the row moves up with it and fades; it takes no focus then.\n        int offset = grid.computeVerticalScrollOffset();\n        row.setTranslationY(-offset);\n        float fade = row.getHeight() > 0 ? Math.min(1f, offset / (row.getHeight() * 0.5f)) : 0f;\n        row.setAlpha(1f - fade);\n        if (row instanceof ViewGroup) {\n            ((ViewGroup) row).setDescendantFocusability(offset > 0\n                    ? ViewGroup.FOCUS_BLOCK_DESCENDANTS : ViewGroup.FOCUS_AFTER_DESCENDANTS);\n        }\n    }\n\n    /** The shown top-bar button nearest above a view (a channel in the top row): Inputs, Wi-Fi, ..., Settings. */\n    private View topButtonAbove(View from) {\n        View best = firstTopButton();\n        if (from == null) return best;\n        int[] at = new int[2];\n        from.getLocationOnScreen(at);\n        float x = at[0] + from.getWidth() / 2f;\n        float bestDist = Float.MAX_VALUE;\n        for (View b : new View[]{btnInputs, btnWifi, btnReorder, btnLibraryTop, findViewById(R.id.btnSettings)}) {\n            if (b == null || b.getVisibility() != View.VISIBLE || !b.isFocusable()) continue;\n            b.getLocationOnScreen(at);\n            float d = Math.abs(at[0] + b.getWidth() / 2f - x);\n            if (d < bestDist) {\n                bestDist = d;\n                best = b;\n            }\n        }\n        return best;\n    }\n\n    /** Focuses the top row on the channel used last, with the grid back at its top. */\n    private void focusTopChannels() {\n        if (!topChannelsShown()) return;\n        cancelPendingFocusScroll();\n        libraryFocusPending = false;\n        if (grid.computeVerticalScrollOffset() > 0) {\n            // Back to the top first: the row takes focus again once the grid is there (placeTopChannels).\n            grid.scrollToPosition(0);\n            grid.post(() -> {\n                placeTopChannels();\n                if (channelRow.focus(topChannels, lastChannel)) channelFocusPending = false;\n            });\n            return;\n        }\n        if (channelRow.focus(topChannels, lastChannel)) channelFocusPending = false;\n    }\n\n    /** An app the person installed (not part of the firmware, not an update of a firmware app): one that can go. */\n    private boolean removableApp(String pkg) {\n        if (pkg == null || pkg.equals(getPackageName())) return false;\n        try {\n            android.content.pm.ApplicationInfo ai = getPackageManager().getApplicationInfo(pkg, 0);\n            return (ai.flags & (android.content.pm.ApplicationInfo.FLAG_SYSTEM\n                    | android.content.pm.ApplicationInfo.FLAG_UPDATED_SYSTEM_APP)) == 0;\n        } catch (android.content.pm.PackageManager.NameNotFoundException e) {\n            return false;\n        }\n    }\n\n    /** Reads the channels off the main thread, then shows, updates or drops the Live TV row. */\n    private void loadChannels() {\n        final android.content.Context app = getApplicationContext();\n        new Thread(() -> {\n            final List<ChannelRow.Channel> fresh = ChannelRow.load(app, ChannelRow.MAX);\n            runOnUiThread(() -> {\n                if (isDestroyed() || channelRow == null) return;\n                boolean had = adapter.hasChannels();\n                if (!channelRow.setChannels(fresh)) return;\n                if (channelsOnTop) {\n                    if (topChannels != null) topChannels.itemView.setVisibility(channelRow.size() > 0 ? View.VISIBLE : View.GONE);\n                    grid.requestLayout();\n                    return;\n                }\n                boolean has = adapter.hasChannels();\n                int pos = adapter.channelsPosition();\n                if (had && !has) adapter.notifyItemRemoved(pos);\n                else if (!had && has) adapter.notifyItemInserted(pos);\n            });\n        }, "live-tv-channels").start();\n    }\n\n    private void cancelPendingFocusScroll() {\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '    private void focusTile(int position) {\n        libraryFocusPending = false;\n',
     '    private void focusTile(int position) {\n        libraryFocusPending = false;\n        channelFocusPending = false;\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '            if (adapter.isLibraryAt(0)) focusLibrary();\n            else firstTopButton().requestFocus();\n',
     '            if (hasFooter()) focusFooter();\n            else firstTopButton().requestFocus();\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '        if (openLiveTvAfterBoot()) return;\n',
     '        if (channelRow != null) loadChannels();   // a channel scan since last time shows up here\n        if (openLiveTvAfterBoot()) return;\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '            if (!MainActivity.this.dockRow) want = (int) (AppAdapter.TOP_ROOM_DP * density);\n',
     '            if (!MainActivity.this.dockRow) want = (int) (AppAdapter.TOP_ROOM_DP * density);\n            // live_tv_row_position "top": room above the dock for the Live TV row.\n            want = Math.max(want, topChannelsRoom());\n            if (topChannels != null) grid.post(MainActivity.this::placeTopChannels);\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '    private void showHero(int position, float dockTopInRoot) {\n',
     "    private void showHero(int position, float dockTopInRoot) {\n        // The Live TV row on top takes the shelf's place; the glow stays.\n        hero.setVisibility(topChannelsShown() ? View.INVISIBLE : View.VISIBLE);\n"),
    ('java/com/gathin/tvhome/MainActivity.java',
     '            if (position < COLUMNS) return false;          // dock row: let focus move to the top bar\n',
     '            if (position < COLUMNS) {\n                if (topChannelsShown()) { focusTopChannels(); return true; }   // the Live TV row above the dock\n                return false;          // dock row: let focus move to the top bar\n            }\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '                // Back to the dock tile Up came from, not wherever the focus finder lands.\n',
     '                // Back to the dock tile Up came from, not wherever the focus finder lands; the Live TV row\n                // above the dock comes first when it is there.\n                if (topChannelsShown()) { focusTopChannels(); return true; }\n'),
    ('java/com/gathin/tvhome/MainActivity.java',
     '        if (dockRow && position < adapter.movableCount()) {\n',
     "        // Open first, as in the stock launcher's menu.\n        addSettingsMenuRow(rows, popup, R.string.tile_open, () -> {\n            if (card != null) card.performClick();\n        });\n        if (dockRow && position < adapter.movableCount()) {\n"),
    ('java/com/gathin/tvhome/MainActivity.java',
     '        // Dock tiles sit near the bottom of the screen: open the menu above the tile when it would not fit below.\n',
     '        // Uninstall, last, for apps the person installed: Android\'s own prompt asks before anything goes.\n        if (removableApp(pkg)) {\n            addSettingsMenuRow(rows, popup, R.string.tile_uninstall, () -> open(\n                    new Intent(Intent.ACTION_DELETE, Uri.parse("package:" + pkg))));\n            panel.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED);\n            popup.setWidth(Math.max((int) (200 * density), panel.getMeasuredWidth()));\n        }\n        // Dock tiles sit near the bottom of the screen: open the menu above the tile when it would not fit below.\n'),
]
LIVETV_FILES = {
    '../test/java/com/gathin/tvhome/ChannelOrderTest.java': 'package com.gathin.tvhome;\n\nimport static org.junit.Assert.assertEquals;\nimport static org.junit.Assert.assertTrue;\n\nimport java.util.ArrayList;\nimport java.util.Arrays;\nimport java.util.List;\n\nimport org.junit.Test;\n\npublic class ChannelOrderTest {\n\n    private static List<String> sorted(String... numbers) {\n        List<String> list = new ArrayList<>(Arrays.asList(numbers));\n        list.sort(ChannelOrder::compareNumbers);\n        return list;\n    }\n\n    @Test\n    public void numbersCompareAsNumbers() {\n        assertEquals(Arrays.asList("2", "5", "10", "36", "143"), sorted("143", "10", "2", "36", "5"));\n    }\n\n    @Test\n    public void subChannelsFollowTheirMain() {\n        assertEquals(Arrays.asList("5", "5-1", "5-2", "6"), sorted("5-2", "6", "5", "5-1"));\n        assertEquals(Arrays.asList("36.1", "36.2", "36.10"), sorted("36.10", "36.1", "36.2"));\n    }\n\n    @Test\n    public void unnumberedChannelsGoLast() {\n        assertEquals(Arrays.asList("1", "7", ""), sorted("7", "", "1"));\n        assertEquals(Arrays.asList("3", null), sorted(null, "3"));\n        assertEquals(0, ChannelOrder.compareNumbers(null, ""));\n    }\n\n    @Test\n    public void leadingZerosAndHugeNumbersAreFine() {\n        assertEquals(0, ChannelOrder.compareNumbers("007", "7"));\n        assertTrue(ChannelOrder.compareNumbers("99999999999999999999", "100000000000000000000") < 0);\n    }\n\n    @Test\n    public void digitsSortBeforeLetters() {\n        assertEquals(Arrays.asList("9", "A1"), sorted("A1", "9"));\n    }\n\n    @Test\n    public void nameBreaksTies() {\n        List<String[]> list = new ArrayList<>();\n        list.add(new String[]{"5", "star"});\n        list.add(new String[]{"5", "Alpha"});\n        list.add(new String[]{"3", "Zeta"});\n        list.sort(ChannelOrder.by(c -> c[0], c -> c[1]));\n        assertEquals("Zeta", list.get(0)[1]);\n        assertEquals("Alpha", list.get(1)[1]);\n        assertEquals("star", list.get(2)[1]);\n    }\n\n    private static List<String> arranged(List<String> sorted, java.util.Set<String> hidden, List<String> order) {\n        return ChannelOrder.arrange(sorted, s -> s, hidden, order);\n    }\n\n    @Test\n    public void hiddenChannelsAreLeftOut() {\n        assertEquals(Arrays.asList("1|A", "3|C"),\n                arranged(Arrays.asList("1|A", "2|B", "3|C"), new java.util.HashSet<>(Arrays.asList("2|B")),\n                        new ArrayList<>()));\n    }\n\n    @Test\n    public void savedOrderComesFirstThenTheRestInNumberOrder() {\n        assertEquals(Arrays.asList("3|C", "1|A", "2|B", "4|D"),\n                arranged(Arrays.asList("1|A", "2|B", "3|C", "4|D"), new java.util.HashSet<>(),\n                        Arrays.asList("3|C", "1|A")));\n    }\n\n    @Test\n    public void goneChannelsInTheSavedOrderAreSkipped() {\n        assertEquals(Arrays.asList("2|B", "1|A"),\n                arranged(Arrays.asList("1|A", "2|B"), new java.util.HashSet<>(), Arrays.asList("9|Z", "2|B")));\n    }\n\n    @Test\n    public void aChannelListedTwiceShowsOnce() {\n        assertEquals(Arrays.asList("5|X", "1|A"),\n                arranged(Arrays.asList("1|A", "5|X", "5|X"), new java.util.HashSet<>(), Arrays.asList("5|X")));\n        assertEquals(Arrays.asList("1|A", "2|B"),\n                arranged(Arrays.asList("1|A", "1|A", "2|B", "2|B"), new java.util.HashSet<>(), new ArrayList<>()));\n    }\n}\n',
    'java/com/gathin/tvhome/ChannelOrder.java': 'package com.gathin.tvhome;\n\nimport java.util.Comparator;\n\n/**\n * Orders tuner channels the way a remote\'s number keys do: by display number, compared part by part as\n * numbers ("2" before "10", "5-1" after "5", "36.2" after "36.1"), with unnumbered channels last and the name\n * as the tie-breaker. Plain Java, so it is tested on the JVM (ChannelOrderTest).\n */\nfinal class ChannelOrder {\n    private ChannelOrder() {\n    }\n\n    /** Compares two display numbers; null or empty sorts after any number. */\n    static int compareNumbers(String a, String b) {\n        boolean noA = a == null || a.trim().isEmpty();\n        boolean noB = b == null || b.trim().isEmpty();\n        if (noA || noB) return noA == noB ? 0 : (noA ? 1 : -1);\n        String[] pa = a.trim().split("[^0-9A-Za-z]+");\n        String[] pb = b.trim().split("[^0-9A-Za-z]+");\n        for (int i = 0; i < Math.max(pa.length, pb.length); i++) {\n            if (i >= pa.length) return -1;   // "5" before "5-1"\n            if (i >= pb.length) return 1;\n            int c = comparePart(pa[i], pb[i]);\n            if (c != 0) return c;\n        }\n        return 0;\n    }\n\n    private static int comparePart(String x, String y) {\n        boolean nx = isDigits(x), ny = isDigits(y);\n        if (nx && ny) {\n            // Compare as numbers without overflow: strip leading zeros, then by length, then by digits.\n            String sx = stripZeros(x), sy = stripZeros(y);\n            if (sx.length() != sy.length()) return sx.length() < sy.length() ? -1 : 1;\n            return sx.compareTo(sy);\n        }\n        if (nx != ny) return nx ? -1 : 1;   // digits before letters\n        return x.compareToIgnoreCase(y);\n    }\n\n    private static boolean isDigits(String s) {\n        if (s.isEmpty()) return false;\n        for (int i = 0; i < s.length(); i++) if (s.charAt(i) < \'0\' || s.charAt(i) > \'9\') return false;\n        return true;\n    }\n\n    private static String stripZeros(String s) {\n        int i = 0;\n        while (i < s.length() - 1 && s.charAt(i) == \'0\') i++;\n        return s.substring(i);\n    }\n\n    /** Number first, then the name, case-insensitively. */\n    static <T> Comparator<T> by(java.util.function.Function<T, String> number, java.util.function.Function<T, String> name) {\n        return (x, y) -> {\n            int c = compareNumbers(number.apply(x), number.apply(y));\n            if (c != 0) return c;\n            String nx = name.apply(x), ny = name.apply(y);\n            return (nx == null ? "" : nx).compareToIgnoreCase(ny == null ? "" : ny);\n        };\n    }\n\n    /**\n     * The row as the person arranged it: each channel once (by key), those whose key is hidden left out, the saved\n     * order first, and channels not in it after, in their number order. Keys that no longer match are skipped.\n     */\n    static <T> java.util.List<T> arrange(java.util.List<T> sorted, java.util.function.Function<T, String> key,\n                                         java.util.Set<String> hidden, java.util.List<String> order) {\n        // The same channel can come more than once (two tuners, or a copy per user profile): keep the first.\n        java.util.List<T> rest = new java.util.ArrayList<>();\n        java.util.Set<String> seen = new java.util.HashSet<>();\n        for (T t : sorted) {\n            String k = key.apply(t);\n            if (!hidden.contains(k) && seen.add(k)) rest.add(t);\n        }\n        java.util.List<T> out = new java.util.ArrayList<>(rest.size());\n        for (String k : order) {\n            for (java.util.Iterator<T> it = rest.iterator(); it.hasNext(); ) {\n                T t = it.next();\n                if (k.equals(key.apply(t))) {\n                    out.add(t);\n                    it.remove();\n                }\n            }\n        }\n        out.addAll(rest);\n        return out;\n    }\n}\n',
    'java/com/gathin/tvhome/ChannelRow.java': 'package com.gathin.tvhome;\n\nimport android.app.AlertDialog;\nimport android.content.Context;\nimport android.content.SharedPreferences;\nimport android.content.Intent;\nimport android.content.pm.PackageManager;\nimport android.database.Cursor;\nimport android.media.tv.TvContract;\nimport android.media.tv.TvContract.Channels;\nimport android.net.Uri;\nimport android.util.Log;\nimport android.view.KeyEvent;\nimport android.view.LayoutInflater;\nimport android.view.View;\nimport android.view.ViewGroup;\nimport android.widget.TextView;\nimport android.widget.Toast;\n\nimport androidx.annotation.NonNull;\nimport androidx.recyclerview.widget.LinearLayoutManager;\nimport androidx.recyclerview.widget.RecyclerView;\n\nimport org.json.JSONObject;\n\nimport java.io.File;\nimport java.nio.charset.StandardCharsets;\nimport java.nio.file.Files;\nimport java.util.ArrayList;\nimport java.util.Arrays;\nimport java.util.HashSet;\nimport java.util.List;\nimport java.util.Objects;\nimport java.util.Set;\n\n/**\n * The "Live TV" row after the app grid ({@code live_tv_row}, off by default): the tuner\'s channels as the\n * TV provider lists them, in number order, each tile showing its number and name. OK tunes the channel in\n * the Live TV app (ACTION_VIEW on the channel\'s URI, as the stock launcher does).\n *\n * Reading channels needs READ_TV_LISTINGS, a runtime permission granted over ADB at install; without it the\n * row simply does not appear. With only that permission the provider returns the channels marked\n * searchable (the default for tuner channels) and refuses a selection, so the whole table is read and\n * filtered here (docs/watch-next.md). Nothing here touches the network.\n */\nfinal class ChannelRow {\n    private static final String TAG = "TvHome.LiveTv";\n    static final String PERMISSION = "android.permission.READ_TV_LISTINGS";\n    /** Enough for a row; a full channel list belongs to the Live TV app. Keeps memory flat on 1 GB TVs. */\n    static final int MAX = 60;\n\n    interface Listener {\n        void onChannelOpen(int index, Channel channel);\n\n        void onChannelFocused(int index);\n\n        void onChannelsUp();\n\n        void onChannelsDown();\n\n        /** A channel was hidden or the hidden ones were shown again: read the row anew. */\n        void onChannelsEdited();\n    }\n\n    static final class Channel {\n        final long id;\n        final String number;\n        final String name;\n\n        Channel(long id, String number, String name) {\n            this.id = id;\n            this.number = number;\n            this.name = name;\n        }\n\n        @Override\n        public boolean equals(Object o) {\n            if (!(o instanceof Channel)) return false;\n            Channel c = (Channel) o;\n            return id == c.id && Objects.equals(number, c.number) && Objects.equals(name, c.name);\n        }\n\n        @Override\n        public int hashCode() {\n            return Objects.hash(id, number, name);\n        }\n    }\n\n    private final Listener listener;\n    private final boolean animate;\n    private final List<Channel> list = new ArrayList<>();\n    private final Tiles tiles = new Tiles();\n    /** The row\'s own list view, and the channel being moved with Left/Right (-1 when none). */\n    private RecyclerView listView;\n    private int moving = -1;\n\n    /** The person\'s choices, kept across reboots: hidden channels and the order, by number and name. */\n    private static final String PREFS = "live_tv_row";\n    private static final String HIDDEN = "hidden";\n    private static final String ORDER = "order";\n\n    ChannelRow(Listener listener, boolean animate) {\n        this.listener = listener;\n        this.animate = animate;\n        tiles.setHasStableIds(true);\n    }\n\n    int size() {\n        return list.size();\n    }\n\n    /**\n     * Whether the row is on: {@code live_tv_row} in config.xml, overridden by a theme\'s config.json (the file the\n     * theme tools push into the launcher\'s external files folder). Read here rather than in Config, so this row\n     * depends on nothing else in the launcher\'s code.\n     */\n    static boolean enabled(Context ctx) {\n        boolean on = ctx.getResources().getBoolean(R.bool.live_tv_row);\n        Object v = themeValue(ctx, "live_tv_row");\n        return v instanceof Boolean ? (Boolean) v : on;\n    }\n\n    /** Whether the row sits above the dock: {@code live_tv_row_position} "top" (config.xml or theme); else after the apps. */\n    static boolean onTop(Context ctx) {\n        String where = ctx.getString(R.string.live_tv_row_position);\n        Object v = themeValue(ctx, "live_tv_row_position");\n        if (v instanceof String) where = (String) v;\n        return "top".equalsIgnoreCase(where.trim());\n    }\n\n    /** One key of the theme\'s config.json, or null when there is no theme, no such key, or the file is unreadable. */\n    private static Object themeValue(Context ctx, String key) {\n        File dir = ctx.getExternalFilesDir(null);\n        File theme = dir == null ? null : new File(dir, "config.json");\n        if (theme == null || !theme.isFile()) return null;\n        try {\n            return new JSONObject(new String(Files.readAllBytes(theme.toPath()), StandardCharsets.UTF_8)).opt(key);\n        } catch (Exception e) {   // unreadable or not JSON: the launcher\'s own Config ignores it the same way\n            return null;\n        }\n    }\n\n    /** Replaces the channels; false when nothing changed (the row is left alone). */\n    boolean setChannels(List<Channel> fresh) {\n        if (fresh.equals(list)) return false;\n        list.clear();\n        list.addAll(fresh);\n        tiles.notifyDataSetChanged();\n        return true;\n    }\n\n    /** The footer view: a title and a horizontal list of channel tiles. */\n    RecyclerView.ViewHolder createRowHolder(ViewGroup parent) {\n        View row = LayoutInflater.from(parent.getContext()).inflate(R.layout.row_live_tv, parent, false);\n        RecyclerView rv = row.findViewById(R.id.channel_list);\n        listView = rv;\n        rv.setLayoutManager(new LinearLayoutManager(parent.getContext(), RecyclerView.HORIZONTAL, false));\n        rv.setItemAnimator(null);\n        rv.setAdapter(tiles);\n        return new RecyclerView.ViewHolder(row) { };\n    }\n\n    /** Focuses the channel at index in this row\'s list, scrolling to it first when needed. */\n    boolean focus(RecyclerView.ViewHolder row, int index) {\n        if (list.isEmpty() || row == null) return false;\n        final int i = Math.max(0, Math.min(index, list.size() - 1));\n        final RecyclerView rv = row.itemView.findViewById(R.id.channel_list);\n        if (rv == null) return false;\n        RecyclerView.ViewHolder vh = rv.findViewHolderForAdapterPosition(i);\n        if (vh != null) return vh.itemView.requestFocus();\n        rv.scrollToPosition(i);\n        rv.post(() -> {\n            RecyclerView.ViewHolder h = rv.findViewHolderForAdapterPosition(i);\n            View target = h != null ? h.itemView : rv.getChildAt(0);\n            if (target != null) target.requestFocus();\n        });\n        return true;\n    }\n\n    /** The intent that tunes a channel: in the configured Live TV app when it takes it, else whichever does. */\n    static Intent viewIntent(Context ctx, long channelId, String liveTvPackage) {\n        Uri uri = TvContract.buildChannelUri(channelId);\n        Intent view = new Intent(Intent.ACTION_VIEW, uri);\n        if (liveTvPackage != null && !liveTvPackage.isEmpty()) {\n            Intent own = new Intent(view).setPackage(liveTvPackage);\n            if (ctx.getPackageManager().resolveActivity(own, 0) != null) return own;\n        }\n        return view;\n    }\n\n    /** Reads the channels off the UI thread\'s back; an empty list when there are none or no permission. */\n    static List<Channel> load(Context ctx, int max) {\n        List<Channel> out = new ArrayList<>();\n        if (ctx.checkSelfPermission(PERMISSION) != PackageManager.PERMISSION_GRANTED) {\n            Log.i(TAG, "READ_TV_LISTINGS is not granted, so there is no Live TV row "\n                    + "(pm grant com.gathin.tvhome " + PERMISSION + ")");\n            return out;\n        }\n        String[] projection = {Channels._ID, Channels.COLUMN_DISPLAY_NUMBER, Channels.COLUMN_DISPLAY_NAME,\n                Channels.COLUMN_BROWSABLE, Channels.COLUMN_SERVICE_TYPE};\n        Cursor c = null;\n        try {\n            try {\n                c = ctx.getContentResolver().query(Channels.CONTENT_URI, projection, null, null, null);\n            } catch (IllegalArgumentException e) {\n                // A provider that does not offer one of these columns: read them all and use what is there.\n                c = ctx.getContentResolver().query(Channels.CONTENT_URI, null, null, null, null);\n            }\n            if (c == null) {\n                Log.i(TAG, "Live TV row: the TV provider gave no channel list (no tuner, or no provider)");\n                return out;\n            }\n            int id = c.getColumnIndex(Channels._ID);\n            int num = c.getColumnIndex(Channels.COLUMN_DISPLAY_NUMBER);\n            int name = c.getColumnIndex(Channels.COLUMN_DISPLAY_NAME);\n            int browsable = c.getColumnIndex(Channels.COLUMN_BROWSABLE);\n            int service = c.getColumnIndex(Channels.COLUMN_SERVICE_TYPE);\n            if (id < 0) return out;\n            int rows = 0, hidden = 0, radio = 0, unnamed = 0;\n            while (c.moveToNext()) {\n                rows++;\n                // Hidden from the channel list in the Live TV app\'s settings: hidden here too.\n                if (browsable >= 0 && !c.isNull(browsable) && c.getInt(browsable) == 0) { hidden++; continue; }\n                if (service >= 0 && Channels.SERVICE_TYPE_AUDIO.equals(c.getString(service))) { radio++; continue; }\n                String n = num >= 0 ? clean(c.getString(num)) : "";\n                String label = name >= 0 ? clean(c.getString(name)) : "";\n                if (n.isEmpty() && label.isEmpty()) { unnamed++; continue; }\n                out.add(new Channel(c.getLong(id), n, label));\n            }\n            // What the provider let this app see: a firmware that shows other apps only the channels it marks\n            // searchable gives 0 rows here even with channels tuned (the Launcher report shows this line).\n            Log.i(TAG, "Live TV row: provider gave " + rows + " rows; hidden " + hidden + ", radio " + radio\n                    + ", no name " + unnamed);\n        } catch (RuntimeException e) {\n            // SecurityException on firmware that guards the table more tightly, or a provider that is missing.\n            Log.w(TAG, "channels could not be read: " + e);\n            out.clear();\n        } finally {\n            if (c != null) c.close();\n        }\n        out.sort(ChannelOrder.by(ch -> ch.number, ch -> ch.name));\n        SharedPreferences prefs = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE);\n        Set<String> hiddenKeys = prefs.getStringSet(HIDDEN, new HashSet<>());\n        String saved = prefs.getString(ORDER, "");\n        List<String> order = saved.isEmpty() ? new ArrayList<>() : Arrays.asList(saved.split("\\n"));\n        int all = out.size();\n        out = new ArrayList<>(ChannelOrder.arrange(out, ChannelRow::key, hiddenKeys, order));\n        Log.i(TAG, "Live TV row: " + out.size() + " channels (" + (all - out.size()) + " hidden by you or listed twice)");\n        return out.size() > max ? new ArrayList<>(out.subList(0, max)) : out;\n    }\n\n    /** A channel as the person\'s choices remember it: number and name, which survive a reboot (ids can change on a rescan). */\n    static String key(Channel c) {\n        return c.number + "|" + c.name;\n    }\n\n    /** Hold OK on a channel: hide it, move it, or bring back the hidden ones. */\n    private void showMenu(View tile, int index) {\n        if (index < 0 || index >= list.size()) return;\n        final Context ctx = tile.getContext();\n        final Channel c = list.get(index);\n        final SharedPreferences prefs = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE);\n        final Set<String> hiddenKeys = new HashSet<>(prefs.getStringSet(HIDDEN, new HashSet<>()));\n        final boolean ordered = !prefs.getString(ORDER, "").isEmpty();\n        List<String> items = new ArrayList<>();\n        final List<Runnable> actions = new ArrayList<>();\n        items.add(ctx.getString(R.string.channel_move));\n        actions.add(() -> startMove(tile, index));\n        items.add(ctx.getString(R.string.channel_hide));\n        actions.add(() -> {\n            hiddenKeys.add(key(c));\n            prefs.edit().putStringSet(HIDDEN, hiddenKeys).apply();\n            listener.onChannelsEdited();\n        });\n        if (!hiddenKeys.isEmpty()) {\n            items.add(ctx.getString(R.string.channel_show_hidden, hiddenKeys.size()));\n            actions.add(() -> {\n                prefs.edit().remove(HIDDEN).apply();\n                listener.onChannelsEdited();\n            });\n        }\n        if (ordered) {\n            items.add(ctx.getString(R.string.channel_reset_order));\n            actions.add(() -> {\n                prefs.edit().remove(ORDER).apply();\n                listener.onChannelsEdited();\n            });\n        }\n        String title = (c.number + " " + c.name).trim();\n        new AlertDialog.Builder(ctx)\n                .setTitle(title)\n                .setItems(items.toArray(new String[0]), (d, which) -> actions.get(which).run())\n                .show();\n    }\n\n    private void startMove(View tile, int index) {\n        moving = index;\n        tile.setScaleX(1.16f);\n        tile.setScaleY(1.16f);\n        tile.setAlpha(0.85f);\n        tile.requestFocus();\n        Toast.makeText(tile.getContext(), R.string.channel_move_hint, Toast.LENGTH_LONG).show();\n    }\n\n    /** Left/Right while moving: the channel trades places with its neighbour, and focus stays on it. */\n    private void moveBy(int step) {\n        int to = moving + step;\n        if (moving < 0 || to < 0 || to >= list.size()) return;\n        Channel c = list.remove(moving);\n        list.add(to, c);\n        tiles.notifyItemMoved(moving, to);\n        moving = to;\n        if (listView != null) listView.scrollToPosition(to);\n    }\n\n    /** OK or Back while moving: the channel stays where it is and the order is saved. */\n    private void endMove(View tile) {\n        moving = -1;\n        tile.setScaleX(1.08f);\n        tile.setScaleY(1.08f);\n        tile.setAlpha(1f);\n        List<String> keys = new ArrayList<>();\n        for (Channel c : list) keys.add(key(c));\n        tile.getContext().getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit()\n                .putString(ORDER, String.join("\\n", keys)).apply();\n    }\n\n    private static String clean(String s) {\n        return s == null ? "" : s.trim();\n    }\n\n    private final class Tiles extends RecyclerView.Adapter<Tile> {\n        @NonNull\n        @Override\n        public Tile onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {\n            return new Tile(LayoutInflater.from(parent.getContext()).inflate(R.layout.item_channel, parent, false));\n        }\n\n        @Override\n        public void onBindViewHolder(@NonNull Tile holder, int position) {\n            holder.bind(list.get(position));\n        }\n\n        @Override\n        public int getItemCount() {\n            return list.size();\n        }\n\n        @Override\n        public long getItemId(int position) {\n            return list.get(position).id;\n        }\n    }\n\n    private final class Tile extends RecyclerView.ViewHolder {\n        final TextView number;\n        final TextView name;\n\n        Tile(View v) {\n            super(v);\n            number = v.findViewById(R.id.channel_number);\n            name = v.findViewById(R.id.channel_name);\n            v.setOnClickListener(x -> {\n                if (moving >= 0) return;   // OK while moving is handled in the key listener\n                int p = getBindingAdapterPosition();\n                if (p >= 0 && p < list.size()) listener.onChannelOpen(p, list.get(p));\n            });\n            v.setOnLongClickListener(x -> {\n                if (moving >= 0) return true;\n                showMenu(x, getBindingAdapterPosition());\n                return true;\n            });\n            v.setOnFocusChangeListener((x, focused) -> {\n                float s = focused ? (moving >= 0 && getBindingAdapterPosition() == moving ? 1.16f : 1.08f) : 1f;\n                if (animate) x.animate().scaleX(s).scaleY(s).setDuration(140).start();\n                else {\n                    x.setScaleX(s);\n                    x.setScaleY(s);\n                }\n                int p = getBindingAdapterPosition();\n                if (focused && p >= 0) listener.onChannelFocused(p);\n            });\n            v.setOnKeyListener((x, key, event) -> {\n                boolean down = event.getAction() == KeyEvent.ACTION_DOWN;\n                if (moving >= 0) {\n                    boolean rtlMove = x.getLayoutDirection() == View.LAYOUT_DIRECTION_RTL;\n                    if (key == KeyEvent.KEYCODE_DPAD_LEFT || key == KeyEvent.KEYCODE_DPAD_RIGHT) {\n                        if (down) moveBy((key == KeyEvent.KEYCODE_DPAD_RIGHT) != rtlMove ? 1 : -1);\n                        return true;\n                    }\n                    if (key == KeyEvent.KEYCODE_DPAD_CENTER || key == KeyEvent.KEYCODE_ENTER\n                            || key == KeyEvent.KEYCODE_BACK || key == KeyEvent.KEYCODE_ESCAPE) {\n                        if (!down) endMove(x);\n                        return true;\n                    }\n                    return key == KeyEvent.KEYCODE_DPAD_UP || key == KeyEvent.KEYCODE_DPAD_DOWN;\n                }\n                if (key == KeyEvent.KEYCODE_DPAD_UP || key == KeyEvent.KEYCODE_DPAD_DOWN) {\n                    if (down) {\n                        if (key == KeyEvent.KEYCODE_DPAD_UP) listener.onChannelsUp();\n                        else listener.onChannelsDown();\n                    }\n                    return true;\n                }\n                // The row\'s ends: focus stays put instead of wandering into the grid or the top bar.\n                boolean rtl = x.getLayoutDirection() == View.LAYOUT_DIRECTION_RTL;\n                int p = getBindingAdapterPosition();\n                int toStart = rtl ? KeyEvent.KEYCODE_DPAD_RIGHT : KeyEvent.KEYCODE_DPAD_LEFT;\n                int toEnd = rtl ? KeyEvent.KEYCODE_DPAD_LEFT : KeyEvent.KEYCODE_DPAD_RIGHT;\n                return (key == toStart && p == 0) || (key == toEnd && p == list.size() - 1);\n            });\n        }\n\n        void bind(Channel c) {\n            number.setText(c.number);\n            number.setVisibility(c.number.isEmpty() ? View.GONE : View.VISIBLE);\n            name.setText(c.name.isEmpty() ? c.number : c.name);\n            itemView.setContentDescription((c.number + " " + c.name).trim());\n        }\n    }\n}\n',
    'res/drawable/banner_tv_blue.xml': '<?xml version="1.0" encoding="utf-8"?>\n<!-- Banner for the Live TV tile in the stock launcher\'s blue (config.xml app_banners, package=banner_tv_blue):\n     a blue field with the Live TV glyph, like banner_tv in another colour. -->\n<layer-list xmlns:android="http://schemas.android.com/apk/res/android">\n    <item android:width="320dp" android:height="180dp">\n        <shape android:shape="rectangle">\n            <gradient android:angle="315" android:startColor="#FF3A50FF" android:endColor="#FF1B2FD6" />\n        </shape>\n    </item>\n    <item android:width="76dp" android:height="76dp" android:gravity="center"\n        android:drawable="@drawable/ic_livetv" />\n</layer-list>\n',
    'res/drawable/channel_bg.xml': '<?xml version="1.0" encoding="utf-8"?>\n<!-- Channel tile in the Live TV row: frosted at rest, brighter with a white edge when focused. -->\n<selector xmlns:android="http://schemas.android.com/apk/res/android">\n    <item android:state_focused="true">\n        <shape android:shape="rectangle">\n            <corners android:radius="14dp" />\n            <solid android:color="#4DFFFFFF" />\n            <stroke android:width="2dp" android:color="#E6FFFFFF" />\n        </shape>\n    </item>\n    <item>\n        <shape android:shape="rectangle">\n            <corners android:radius="14dp" />\n            <solid android:color="#22FFFFFF" />\n            <stroke android:width="1dp" android:color="#1FFFFFFF" />\n        </shape>\n    </item>\n</selector>\n',
    'res/layout/item_channel.xml': '<?xml version="1.0" encoding="utf-8"?>\n<!-- One channel in the Live TV row: number on top, name in the middle, like the stock launcher\'s tiles. -->\n<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"\n    android:id="@+id/channel_card"\n    android:layout_width="210dp"\n    android:layout_height="104dp"\n    android:layout_marginStart="8dp"\n    android:layout_marginEnd="8dp"\n    android:background="@drawable/channel_bg"\n    android:focusable="true"\n    android:clickable="true">\n\n    <TextView\n        android:id="@+id/channel_number"\n        android:layout_width="match_parent"\n        android:layout_height="wrap_content"\n        android:layout_gravity="top|center_horizontal"\n        android:layout_marginTop="16dp"\n        android:gravity="center"\n        android:singleLine="true"\n        android:textColor="#B3FFFFFF"\n        android:textSize="16sp"\n        android:fontFamily="@string/font_body" />\n\n    <TextView\n        android:id="@+id/channel_name"\n        android:layout_width="match_parent"\n        android:layout_height="wrap_content"\n        android:layout_gravity="center"\n        android:layout_marginTop="12dp"\n        android:paddingStart="12dp"\n        android:paddingEnd="12dp"\n        android:gravity="center"\n        android:singleLine="true"\n        android:ellipsize="end"\n        android:textColor="#FFFFFFFF"\n        android:textSize="19sp"\n        android:textStyle="bold"\n        android:fontFamily="@string/font_body" />\n</FrameLayout>\n',
    'res/layout/row_live_tv.xml': '<?xml version="1.0" encoding="utf-8"?>\n<!-- The Live TV row after the app grid (live_tv_row): a title and the tuner\'s channels, see ChannelRow. -->\n<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"\n    android:layout_width="match_parent"\n    android:layout_height="wrap_content"\n    android:orientation="vertical"\n    android:paddingTop="10dp"\n    android:paddingBottom="18dp"\n    android:clipChildren="false"\n    android:clipToPadding="false">\n\n    <TextView\n        android:id="@+id/channel_title"\n        android:layout_width="wrap_content"\n        android:layout_height="wrap_content"\n        android:paddingStart="8dp"\n        android:paddingEnd="8dp"\n        android:text="@string/live_tv_row"\n        android:textColor="#CCFFFFFF"\n        android:textSize="15sp"\n        android:fontFamily="@string/font_body" />\n\n    <androidx.recyclerview.widget.RecyclerView\n        android:id="@+id/channel_list"\n        android:layout_width="match_parent"\n        android:layout_height="132dp"\n        android:paddingStart="4dp"\n        android:paddingEnd="4dp"\n        android:paddingTop="12dp"\n        android:paddingBottom="12dp"\n        android:clipChildren="false"\n        android:clipToPadding="false"\n        android:overScrollMode="never" />\n</LinearLayout>\n',
    'res/values-el/strings_cleanyourtv.xml': '<?xml version="1.0" encoding="utf-8"?>\n<!-- Greek for the hold-OK tile menu (tile_menu), added by CleanYourTV. Everything else falls back to English. -->\n<resources>\n    <string name="tile_open">Άνοιγμα</string>\n    <string name="tile_uninstall">Απεγκατάσταση</string>\n    <string name="channel_move">Μετακίνηση</string>\n    <string name="channel_hide">Απόκρυψη καναλιού</string>\n    <string name="channel_show_hidden">Επανεμφάνιση όλων των κρυμμένων (%1$d)</string>\n    <string name="channel_reset_order">Αρχική σειρά καναλιών</string>\n    <string name="channel_move_hint">Αριστερά και δεξιά μετακινούν το κανάλι, το OK το αφήνει.</string>\n    <string name="tile_move">Μετακίνηση</string>\n    <string name="tile_add_to_dock">Προσθήκη στη μπάρα</string>\n    <string name="tile_replace_in_dock">Αντικατάσταση με άλλη εφαρμογή</string>\n    <string name="library_app_info">Πληροφορίες εφαρμογής</string>\n    <string name="reorder_hint">Τα βέλη μετακινούν την εφαρμογή, το Back την αφήνει. Ξανά Back για τέλος.</string>\n</resources>\n',
}
def _read_raw(path):
    """The file exactly as stored: no newline translation, so a CRLF checkout stays CRLF."""
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def _crlf(text, s):
    return s.replace("\n", "\r\n") if "\r\n" in text else s


def livetv_state(launcher, edits, new_files):
    """'applied', 'pristine' or 'mixed' (with the reason) for this launcher folder."""
    main = Path(launcher) / "app" / "src" / "main"
    applied_all, pristine_all, reasons = True, True, []
    cache = {}
    for rel, old, new in edits:
        p = main / rel
        try:
            t = cache.setdefault(rel, _read_raw(p))
        except OSError as e:
            return "mixed", f"{rel}: {e}"
        has_new = _crlf(t, new) in t and (old not in new or t.count(_crlf(t, old)) == t.count(_crlf(t, new)))
        has_old = t.count(_crlf(t, old)) == 1
        if not has_new:
            applied_all = False
        if not has_old or has_new and old not in new:
            pristine_all = False
            if not has_new and not has_old:
                reasons.append(f"{rel}: expected code not found")
    files_there = all((main / rel).is_file() for rel in new_files)
    files_absent = not any((main / rel).is_file() for rel in new_files)
    if applied_all and files_there:
        return "applied", ""
    if pristine_all and files_absent:
        return "pristine", ""
    return "mixed", "; ".join(reasons[:3]) or "partly applied"


def apply_livetv(launcher, edits, new_files):
    """Returns (True, message) when the launcher has the Live TV row afterwards, else (False, why)."""
    launcher = Path(launcher)
    main = launcher / "app" / "src" / "main"
    backup = launcher / ".livetv-orig"
    state, why = livetv_state(launcher, edits, new_files)
    if state == "applied":
        return True, "already in this launcher"
    if state == "mixed" and backup.is_dir():
        # Put the untouched files back and start again.
        for f in backup.rglob("*"):
            if f.is_file():
                target = main / f.relative_to(backup)
                target.write_bytes(f.read_bytes())
        for rel in new_files:
            try:
                (main / rel).unlink()
            except OSError:
                pass
        state, why = livetv_state(launcher, edits, new_files)
    if state != "pristine":
        return False, f"this toolkit version's launcher code has changed ({why})"
    texts = {}
    for rel, old, new in edits:
        t = texts.get(rel)
        if t is None:
            t = _read_raw(main / rel)
        o, n = _crlf(t, old), _crlf(t, new)
        if t.count(o) != 1:
            return False, f"{rel}: expected code found {t.count(o)} times"
        texts[rel] = t.replace(o, n, 1)
    for rel in texts:
        b = backup / rel
        b.parent.mkdir(parents=True, exist_ok=True)
        if not b.exists():
            b.write_bytes((main / rel).read_bytes())
    for rel, t in texts.items():
        (main / rel).write_text(t, encoding="utf-8", newline="")
    for rel, content in new_files.items():
        p = main / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="")
    state, why = livetv_state(launcher, edits, new_files)
    return (state == "applied"), ("added" if state == "applied" else f"check after writing failed ({why})")


def tv_preflight():
    """Right before the build script: wake the TV, then check both the port and our own connection answer."""
    host, port = TV.host, TV.port
    try:
        TV.sh("input keyevent KEYCODE_WAKEUP", quiet=True, timeout=15)
    except Exception:
        pass
    time.sleep(1.5)
    if not _port_open(host, port, timeout=5):
        raise RuntimeError(f"The TV at {host} does not answer on port {port}. It may have gone to sleep or to "
                           "standby during the download, or its address changed. Wake it with the remote, check it is "
                           "on the same network (Connect page), then press Build & install again: Java and the "
                           "Android SDK are ready now, so the build starts straight away.")
    if "ok" not in TV.sh("echo ok", quiet=True, timeout=20):
        raise RuntimeError("The TV answers but the connection does not work. Disconnect and Connect again on the "
                           "Connect page, then press Build & install again.")
    return True


def _decode_output(data):
    """Console output: UTF-8 when it is, else the console's own code page (Greek Windows: cp737/cp1253)."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        for codec in ("oem", "mbcs"):
            try:
                return data.decode(codec)
            except (LookupError, UnicodeDecodeError):
                pass
        return data.decode("latin-1")


def launcher_has_livetv():
    """True when the installed launcher was built with the Live TV row (it declares READ_TV_LISTINGS)."""
    if DEMO:
        return True
    out = TV.sh(f"dumpsys package {OUR_LAUNCHER} | grep -c {LIVETV_PERMISSION}", quiet=True).strip()
    return out.isdigit() and int(out) > 0


def grant_livetv():
    TV.sh(f"pm grant {OUR_LAUNCHER} {LIVETV_PERMISSION} 2>&1; true")


def clean_launcher_build(launcher):
    """Deletes the launcher's build outputs and Gradle's project cache, so the next build compiles everything
    again and can never pick up an APK from an earlier build. Returns what was removed."""
    launcher = Path(launcher)
    gw = launcher / ("gradlew.bat" if os.name == "nt" else "gradlew")
    if gw.is_file() and not DEMO:
        try:   # a running Gradle daemon keeps files in .gradle open on Windows
            subprocess.run([str(gw), "--stop", "-q"], cwd=str(launcher), capture_output=True, timeout=60,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except Exception:
            pass
    gone = []
    for rel in ("app/build", "build", ".gradle"):
        d = launcher / rel
        if d.is_dir():
            shutil.rmtree(d, ignore_errors=True)
            gone.append(rel + (" (partly: a file is still in use)" if d.exists() else ""))
    return gone


def tv_stamp():
    """The TV's clock in logcat's -T format, to read only what happens after this moment."""
    return TV.sh("date '+%m-%d %H:%M:%S.000'", quiet=True).strip()


def launcher_crash_since(stamp):
    """The launcher's crash report logged on the TV since stamp, as a few lines, or ""."""
    if not stamp or not re.fullmatch(r"\d\d-\d\d \d\d:\d\d:\d\d\.\d{3}", stamp):
        return ""
    for cmd in (f"logcat -b crash -d -T '{stamp}' 2>/dev/null", f"logcat -d -T '{stamp}' 2>/dev/null | "
                                                               "grep -A25 'FATAL EXCEPTION'"):
        out = TV.sh(cmd, quiet=True, timeout=30)
        blocks = re.split(r"(?=^.*FATAL EXCEPTION)", out, flags=re.M)
        for b in blocks:
            if f"Process: {OUR_LAUNCHER}" in b:
                keep = [l.split(": ", 1)[-1].strip() for l in b.splitlines()
                        if "Exception" in l or "Error" in l or f"at {OUR_LAUNCHER}" in l or "Caused by" in l]
                return "\n".join(keep[:12])
    return ""


def launcher_update_age():
    """Seconds since the launcher on the TV was last installed or updated, or None when unknown."""
    import datetime
    upd = re.search(r"lastUpdateTime=(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)",
                    TV.sh(f"dumpsys package {OUR_LAUNCHER} | grep lastUpdateTime", quiet=True))
    now = TV.sh("date '+%Y-%m-%d %H:%M:%S'", quiet=True).strip()
    try:
        f = "%Y-%m-%d %H:%M:%S"
        return (datetime.datetime.strptime(now, f) - datetime.datetime.strptime(upd.group(1), f)).total_seconds()
    except (AttributeError, ValueError):
        return None


def launcher_report():
    """Everything needed to tell why the launcher on the TV does not show what was built: which build the TV runs,
    the Live TV pieces, the theme on the TV, the launcher's own log lines and any crash. Plain text to send on."""
    import hashlib
    out = [f"CleanYourTV {APP_VERSION}  ·  {time.strftime('%Y-%m-%d %H:%M:%S')}", ""]

    def sec(title):
        out.extend(["", f"== {title}"])

    def sh(cmd, limit=60):
        try:
            txt = TV.sh(cmd, quiet=True, timeout=40).rstrip()
        except Exception as e:
            txt = f"(failed: {e})"
        lines = txt.splitlines()
        out.extend(lines[:limit] + ([f"... {len(lines) - limit} more"] if len(lines) > limit else []))
        return txt

    sec("This computer")
    out.append(f"toolkit launcher: {LAUNCHER}")
    try:
        state = livetv_state(LAUNCHER, LIVETV_EDITS, LIVETV_FILES)
        if state[0] == "mixed":   # config.xml carries this app's switch values, which the check does not expect
            code = livetv_state(LAUNCHER, [e for e in LIVETV_EDITS if not e[0].endswith("config.xml")], LIVETV_FILES)
            if code[0] == "applied":
                state = ("applied", "config.xml set by this app's switches")
        out.append(f"Live TV row patch: {state}")
    except Exception as e:
        out.append(f"Live TV row patch: unreadable ({e})")
    out.append(f"config.xml: {config_xml_arrays()}")
    live_pkg, _ = launcher_hidden_defaults()
    out.append(f"live_tv_package: {live_pkg or '(none)'}" +
               (" (found on the TV)" if TV.connected and TV.info.get("live_tv_app") else ""))
    apk = LAUNCHER / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
    local_md5 = ""
    if apk.is_file():
        local_md5 = hashlib.md5(apk.read_bytes()).hexdigest()
        out.append(f"built APK: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(apk.stat().st_mtime))}, "
                   f"{apk.stat().st_size} bytes, md5 {local_md5}")
    else:
        out.append("built APK: none in app/build (never built here, or cleaned)")
    if not TV.connected:
        out.append("", )
        out.append("Not connected to a TV: connect and run this again for the TV's side.")
        return "\n".join(out)

    sec("Which launcher build the TV runs")
    path = ""
    for line in TV.sh(f"pm path {OUR_LAUNCHER}", quiet=True).splitlines():
        if line.startswith("package:") and line.strip().endswith("base.apk"):
            path = line.split(":", 1)[1].strip()
    if path:
        tv_md5 = (TV.sh(f"md5sum '{path}'", quiet=True).split() or [""])[0]
        out.append(f"installed: {path}  md5 {tv_md5}")
        out.append("-> the TV runs THIS computer's latest build" if local_md5 and tv_md5 == local_md5 else
                   "-> the TV runs a DIFFERENT build from the one in app/build")
    else:
        out.append("the new launcher is NOT installed")
    sh(f"dumpsys package {OUR_LAUNCHER} | grep -E 'versionName|lastUpdateTime|firstInstallTime|READ_TV_LISTINGS'")
    sh("date '+TV clock: %Y-%m-%d %H:%M:%S'")
    sh(HOME_QUERY + " | tail -n 1")

    sec("Theme on the TV (config.json)")
    sh(f"content read --uri {THEME_URI}/config.json 2>&1 | head -c 2500", 80)
    sh(f"content read --uri {THEME_URI}/theme_revision 2>&1 | head -c 80")

    sec("Live TV app")
    if live_pkg:
        sh(f"pm list packages -d | grep -c '{live_pkg}' | sed 's/^/disabled: /'")
        sh("cmd package query-activities --brief -a android.intent.action.MAIN "
           f"-c android.intent.category.LEANBACK_LAUNCHER | grep -i '{live_pkg}' || echo 'no LEANBACK_LAUNCHER entry'")
        sh("cmd package query-activities --brief -a android.intent.action.MAIN "
           f"-c android.intent.category.LAUNCHER | grep -i '{live_pkg}' || echo 'no LAUNCHER entry'")

    sec("Channels in the TV provider")
    sh("content query --uri content://android.media.tv/channel --projection display_number:display_name:browsable "
       "2>&1 | head -12")
    sh("content query --uri content://android.media.tv/channel --projection _id 2>/dev/null | grep -c Row "
       "| sed 's/^/channels: /'")
    sh("dumpsys tv_input 2>/dev/null | grep -iE 'inputId|TvInputInfo' | head -10")

    sec("Launcher log")
    # Home once, so the launcher reads the channels again and logs what the TV provider gave it.
    sh("input keyevent KEYCODE_HOME; sleep 4; echo pressed Home", 2)
    sh("logcat -d -t 6000 2>/dev/null | grep -E 'TvHome' | tail -40", 45)
    sec("Launcher crashes")
    sh(f"logcat -b crash -d -t 400 2>/dev/null | grep -A20 'Process: {OUR_LAUNCHER}' | tail -45", 50)
    text = "\n".join(out)
    if TV.host:
        text = text.replace(TV.host, "<tv ip>")
    return text


class ProgressSignal(QObject):
    step = pyqtSignal(int, int, str)      # done, total, what


APK_DIR = "/data/local/tmp/cyt-apk"


def apks_from(paths, workdir):
    """The .apk files to install from what was picked: .apk files as they are (several = one app's splits), or
    the .apk files inside an .apks / .xapk bundle (a zip). Returns (apks, notes)."""
    import zipfile
    apks, notes = [], []
    for p in map(Path, paths):
        if p.suffix.lower() == ".apk":
            apks.append(p)
            continue
        try:
            with zipfile.ZipFile(p) as z:
                names = [n for n in z.namelist() if n.lower().endswith(".apk") and "/" not in n.strip("/")]
                if not names:
                    raise RuntimeError(f"{p.name} has no .apk inside")
                out = Path(workdir) / p.stem
                out.mkdir(parents=True, exist_ok=True)
                for n in names:
                    target = out / Path(n).name
                    target.write_bytes(z.read(n))
                    apks.append(target)
                if any(n.lower().endswith(".obb") for n in z.namelist()):
                    notes.append(f"{p.name} also carries game data (.obb), which is not copied: the app downloads "
                                 "it itself, or copy it to Android/obb on the TV")
        except zipfile.BadZipFile:
            raise RuntimeError(f"{p.name} is neither an .apk nor an .apks/.xapk bundle")
    if not apks:
        raise RuntimeError("no .apk file was picked")
    return apks, notes


def install_apks(paths, sig=None):
    """Copies the picked app to the TV and installs it with pm (several .apk files go in as one app's splits).
    Returns a short result line."""
    import tempfile
    work = Path(tempfile.mkdtemp(prefix="cyt-apk-"))
    try:
        apks, notes = apks_from(paths, work)
        total = sum(a.stat().st_size for a in apks)
        before = TV.packages()
        TV.sh(f"rm -rf {APK_DIR}; mkdir -p {APK_DIR}", quiet=True)
        sent = 0
        remote = []
        for i, a in enumerate(apks):
            dest = f"{APK_DIR}/{i}.apk"
            size = a.stat().st_size
            log(f"copying {a.name} ({size / 1048576:.1f} MB) to the TV", "info")
            if DEMO:
                for k in range(5):
                    time.sleep(0.05)
                    if sig:
                        sig.step.emit(sent + size * (k + 1) // 5, total, a.name)
            else:
                moved = [0]

                def tick(_path, chunk, _total, base=sent, name=a.name):
                    moved[0] += chunk          # adb-shell reports each chunk, not the running total
                    if sig:
                        sig.step.emit(base + min(moved[0], size), total, name)

                try:
                    with TV.lock:
                        TV.dev.push(str(a), dest, read_timeout_s=300.0, transport_timeout_s=300.0,
                                    progress_callback=tick)
                except Exception as e:   # some adbd builds refuse the sync protocol: plain shell instead
                    log(f"direct copy failed ({type(e).__name__}), copying in chunks", "warn")
                    push_file(a, dest, progress=(lambda d, n, base=sent, sz=size, nm=a.name:
                                                 sig and sig.step.emit(base + sz * d // n, total, nm)))
                got = TV.sh(f"stat -c %s {dest} 2>/dev/null || wc -c < {dest}", quiet=True).strip()
                if got != str(size):
                    raise RuntimeError(f"{a.name} did not arrive whole ({got or 'nothing'} of {size} bytes)")
            sent += size
            remote.append((dest, size, a.name))
        if sig:
            sig.step.emit(total, total, "installing…")
        log("installing on the TV (the TV may ask to confirm, or check the app first)", "info")
        if len(remote) == 1:
            out = TV.sh(f"pm install -r {remote[0][0]}", timeout=600)
        else:
            out = TV.sh(f"pm install-create -r -S {total}", timeout=120)
            sid = re.search(r"\[(\d+)\]", out)
            if not sid:
                raise RuntimeError(f"the TV refused to start the install: {out.strip()[:200]}")
            for i, (dest, size, _n) in enumerate(remote):
                w = TV.sh(f"pm install-write -S {size} {sid.group(1)} {i}.apk {dest}", timeout=600)
                if "Success" not in w and "uccess" not in w:
                    TV.sh(f"pm install-abandon {sid.group(1)}", quiet=True)
                    raise RuntimeError(f"the TV refused part {i + 1}: {w.strip()[:200]}")
            out = TV.sh(f"pm install-commit {sid.group(1)}", timeout=600)
        if "Success" not in out:
            why = re.search(r"Failure \[([^\]]+)\]", out)
            raise RuntimeError(apk_failure(why.group(1) if why else out.strip()[:200] or "the TV gave no answer"))
        new = sorted(TV.packages() - before)
        msg = (f"Installed <b>{new[0]}</b>." if len(new) == 1 else
               "Installed: it updated an app that was already on the TV." if not new else
               "Installed: " + ", ".join(new) + ".")
        return msg + ("<br>" + "<br>".join(notes) if notes else "")
    finally:
        try:
            TV.sh(f"rm -rf {APK_DIR}", quiet=True, retry=False)
        except Exception:
            pass
        shutil.rmtree(work, ignore_errors=True)


def tv_apps(include_system=False):
    """(package, from the firmware) for the apps on the TV, the person's own first, each group by name."""
    third = TV.packages("-3")
    pk = TV.packages() if include_system else set(third)
    return sorted(((p, p not in third) for p in pk), key=lambda x: (x[1], x[0]))


def pull_file(remote, local, tick=None):
    """Copies one file from the TV: adb's sync protocol, or base64 in 1 MB pieces through the shell when the TV
    refuses that. Checked with md5 either way."""
    import base64
    import hashlib
    size = int((TV.sh(f"stat -c %s '{remote}' 2>/dev/null", quiet=True).strip() or "0").split()[0] or 0)
    got = [0]

    def step(_p, chunk, _t):
        got[0] += chunk
        if tick:
            tick(min(got[0], size), size)

    try:
        with TV.lock:
            TV.dev.pull(remote, str(local), progress_callback=step, read_timeout_s=300.0, transport_timeout_s=300.0)
    except Exception as e:
        log(f"direct copy failed ({type(e).__name__}), copying in pieces", "warn")
        with open(local, "wb") as f:
            n = max(1, (size + 1048575) // 1048576)
            for i in range(n):
                out = TV.sh(f"dd if='{remote}' bs=1048576 skip={i} count=1 2>/dev/null | base64", quiet=True,
                            timeout=120)
                f.write(base64.b64decode("".join(out.split())))
                if tick:
                    tick(min((i + 1) * 1048576, size), size)
    want = (TV.sh(f"md5sum '{remote}'", quiet=True).split() or [""])[0]
    have = hashlib.md5(Path(local).read_bytes()).hexdigest()
    if want and want != have:
        raise RuntimeError(f"{Path(remote).name} arrived damaged (md5 mismatch)")
    return size


def pull_apps(pkgs, dest, sig=None):
    """Copies apps from the TV to this PC: one .apk, or an .apks bundle (base + splits, which Install takes back).
    Named <package>_<version>. Returns (saved files, notes)."""
    import tempfile
    import zipfile
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    plan = []
    for pkg in pkgs:
        if not PACKAGE_RE.fullmatch(pkg):
            continue
        paths = [l.split(":", 1)[1].strip() for l in TV.sh(f"pm path {pkg}", quiet=True).splitlines()
                 if l.startswith("package:") and l.strip().endswith(".apk")]
        ver = re.search(r"versionName=(\S+)", TV.sh(f"dumpsys package {pkg} | grep -m1 versionName", quiet=True))
        plan.append((pkg, paths, re.sub(r"[^A-Za-z0-9._-]", "_", ver.group(1)) if ver else "unknown"))
    sizes = {}
    for _pkg, paths, _v in plan:
        for path in paths:
            out = TV.sh(f"stat -c %s '{path}' 2>/dev/null", quiet=True).strip()
            sizes[path] = int(out) if out.isdigit() else 0
    total = sum(sizes.values()) or 1
    done = [0]
    saved, notes = [], []
    work = Path(tempfile.mkdtemp(prefix="cyt-pull-"))
    try:
        for pkg, paths, ver in plan:
            if not paths:
                notes.append(f"{pkg}: the TV gave no file for it")
                continue
            local = []
            for i, path in enumerate(paths):
                part = work / pkg / Path(path).name
                part.parent.mkdir(parents=True, exist_ok=True)
                base = done[0]
                if DEMO:
                    part.write_bytes(b"demo")
                    if sig:
                        sig.step.emit(base + sizes[path], total, pkg)
                else:
                    pull_file(path, part, (lambda d, _s, b=base, n=pkg: sig and sig.step.emit(b + d, total, n)))
                done[0] = base + sizes[path]
                local.append(part)
            if len(local) == 1:
                target = dest / f"{pkg}_{ver}.apk"
                shutil.copyfile(local[0], target)
            else:   # base.apk and its split_*.apk parts: one .apks file, the format Install reads back
                target = dest / f"{pkg}_{ver}.apks"
                with zipfile.ZipFile(target, "w", zipfile.ZIP_STORED) as z:
                    for f in local:
                        z.write(f, f.name)
            saved.append(target)
            log(f"saved {target.name}", "ok")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return saved, notes


class PickAppsDialog(Dialog):
    """Which apps to copy from the TV, and where to."""

    def __init__(self, parent, apps, dest):
        super().__init__(parent, "Copy apps from the TV", 620)
        self.all = apps
        self.lay.addWidget(label("Tick the apps to copy. Apps made of several parts are saved as one .apks file, "
                                 "which Install an app from this PC takes back.", "Muted", wrap=True))
        self.find = QLineEdit()
        self.find.setPlaceholderText("Filter by name, e.g. stremio")
        self.lay.addWidget(self.find)
        self.system = Toggle("Show the TV's own apps too")
        self.lay.addWidget(self.system)
        self.list = QListWidget()
        self.list.setMinimumHeight(300)
        self.lay.addWidget(self.list)
        self.dest = QLineEdit(str(dest))
        browse = button("Folder…", None, "folder")
        browse.clicked.connect(self.browse)
        self.lay.addWidget(hbox(label("Save to", "Muted"), self.dest, browse))
        self.ok = self.buttons("Copy to this PC")
        self.ticked = set()
        self.find.textChanged.connect(self.fill)
        self.system.toggled.connect(self.fill)
        self.list.itemChanged.connect(self.changed)
        self.fill()

    def fill(self, *_):
        self.list.blockSignals(True)
        self.list.clear()
        q = self.find.text().strip().lower()
        for pkg, sysapp in self.all:
            if sysapp and not self.system.isChecked():
                continue
            if q and q not in pkg.lower():
                continue
            it = QListWidgetItem(pkg + ("   · TV's own" if sysapp else ""))
            it.setData(Qt.ItemDataRole.UserRole, pkg)
            it.setFlags(it.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            it.setCheckState(Qt.CheckState.Checked if pkg in self.ticked else Qt.CheckState.Unchecked)
            self.list.addItem(it)
        self.list.blockSignals(False)
        self.ok.setEnabled(bool(self.ticked))

    def changed(self, it):
        pkg = it.data(Qt.ItemDataRole.UserRole)
        (self.ticked.add if it.checkState() == Qt.CheckState.Checked else self.ticked.discard)(pkg)
        self.ok.setEnabled(bool(self.ticked))

    def browse(self):
        d = QFileDialog.getExistingDirectory(self, "Save the apps to", self.dest.text())
        if d:
            self.dest.setText(d)


def apk_failure(code):
    """pm's failure code in plain words."""
    plain = {
        "INSTALL_FAILED_UPDATE_INCOMPATIBLE": "an app with the same name is installed with a different signature: "
                                              "uninstall that one first",
        "INSTALL_FAILED_VERSION_DOWNGRADE": "the TV already has a newer version of this app",
        "INSTALL_FAILED_OLDER_SDK": "the app needs a newer Android than this TV has",
        "INSTALL_FAILED_NO_MATCHING_ABIS": "the app is built for another processor (try the armeabi-v7a or arm64 "
                                           "version)",
        "INSTALL_FAILED_INSUFFICIENT_STORAGE": "the TV is out of storage",
        "INSTALL_FAILED_VERIFICATION_FAILURE": "the TV's app check (Play Protect) refused it",
        "INSTALL_FAILED_USER_RESTRICTED": "installing from the computer is switched off on the TV (Developer options "
                                          "→ Install via USB/ADB)",
        "INSTALL_PARSE_FAILED_NOT_APK": "the file is not an Android app",
        "INSTALL_FAILED_MISSING_SPLIT": "this app comes in several parts: pick all its .apk files together, or "
                                        "its .apks/.xapk bundle",
    }
    key = next((k for k in plain if k in code), None)
    return f"Not installed: {plain[key]} ({key})." if key else f"Not installed: {code}"


class ExtrasPage(Page):
    title = "Extras"
    subtitle = "Ad-blocking DNS, faster animations and the Apple TV style launcher"
    line = pyqtSignal(str)

    def __init__(self, win):
        super().__init__(win)
        # Private DNS
        c, lay = card()
        lay.addWidget(hbox(label("Ad-blocking DNS", "H2"), None, self._pill("dns")))
        lay.addWidget(label(
            "Sets Android's Private DNS to AdGuard's ad-blocking resolver (dns.adguard-dns.com), which blocks ad "
            "and tracking domains for every app. Android 9 and newer. It does <b>not</b> block YouTube ads, and "
            "it can't remove ads a launcher builds into its own feed. Check an app still plays afterwards.",
            "Muted", wrap=True, rich=True))
        self.dns_on = button("Turn on AdGuard DNS", "Primary", "shield")
        self.dns_off = button("Turn off (automatic)", None, "undo")
        lay.addWidget(hbox(self.dns_on, self.dns_off, None))
        self.body.addWidget(c)

        # Animations
        c, lay = card()
        lay.addWidget(hbox(label("Snappier menus", "H2"), None, self._pill("anim")))
        lay.addWidget(label("Halves the window, transition and animator durations. Makes a slow TV feel quicker; "
                            "Restore on the Finish page puts the recorded values back.", "Muted", wrap=True))
        self.anim_fast = button("Animations 0.5×", None, "spark")
        self.anim_norm = button("Normal (1×)", "Ghost")
        lay.addWidget(hbox(self.anim_fast, self.anim_norm, None))
        self.body.addWidget(c)

        # Clock screensaver
        c, lay = card()
        lay.addWidget(hbox(label("Clock screensaver", "H2"), None, self._pill("dream")))
        lay.addWidget(label(
            "The launcher's own screensaver: a thin clock and the date drifting slowly over a soft glow. It replaces "
            "the TV's screensaver (photos, ambient mode) and starts when the TV sits idle. Needs the CleanYourTV "
            "launcher installed. For a clock only while Home is idle, use “Clock screensaver after” in My theme.",
            "Muted", wrap=True))
        self.dream_wait = QComboBox()
        for text, ms in [("after 5 min", 300000), ("after 10 min", 600000), ("after 15 min", 900000),
                         ("after 30 min", 1800000), ("after 1 hour", 3600000)]:
            self.dream_wait.addItem(text, ms)
        self.dream_wait.setCurrentIndex(1)
        self.dream_on = button("Use the clock", "Primary", "check")
        self.dream_test = button("Show it now", None, "play", "Start the screensaver now; any key closes it")
        self.dream_off = button("Back to the TV's own", "Ghost", "undo")
        lay.addWidget(hbox(label("Start", "Muted"), self.dream_wait, self.dream_on, self.dream_test, None,
                           self.dream_off))
        self.body.addWidget(c)

        # Launcher
        c, lay = card()
        lay.addWidget(hbox(label("Apple TV style launcher", "H2"), None, self._pill("tool"), self._pill("launcher")))
        lay.addWidget(label(
            "Builds the launcher in launcher/ (black background, dock, glass highlight, clock, Inputs/Wi-Fi/"
            "Settings pills) and installs it as Home. The TV needs Android 8.0+ (SDK 26). This PC needs Java 17–22 "
            "and the Android SDK: the app finds them, or offers to download them on the first build. The build "
            "script checks Home afterwards and puts the stock launcher back if the takeover failed. Change the dock "
            "later on the Themes page. This app also adds the Live TV app as a tile and a Live TV channels row, at the "
            "top or after the apps: choose below.",
            "Muted", wrap=True))
        self.extras_for = label("", "Muted", wrap=True, rich=True)
        lay.addWidget(self.extras_for)
        self.input_svc = Toggle("Input button opens the input switcher (Google TV, InputKeyService)")
        self.home_svc = Toggle("Home button sends ALL_APPS (Xiaomi sticks, HomeKeyService)")
        lay.addWidget(self.input_svc)
        lay.addWidget(self.home_svc)
        self.tv_key_b = Toggle("The remote's TV button opens the Live TV app directly (needs the Input button helper)")
        self.tv_key_b.setChecked(win.settings.value("tv_key", "0") == "1")
        self.tv_key_b.toggled.connect(lambda on: win.settings.setValue("tv_key", "1" if on else "0"))
        # The TV button goes through InputKeyService: on together, and off with it.
        self.tv_key_b.toggled.connect(lambda on: on and self.input_svc.setChecked(True))
        self.input_svc.toggled.connect(lambda on: on or self.tv_key_b.setChecked(False))
        lay.addWidget(self.tv_key_b)
        self.live_tile_b = Toggle("Live TV app as a tile, like the stock launcher")
        self.live_row_b = Toggle("Live TV channels row")
        for cb, key in ((self.live_tile_b, "live_tile"), (self.live_row_b, "live_row")):
            cb.setChecked(win.settings.value(key, "1") != "0")
            cb.toggled.connect(lambda on, k=key: self._live_switch(k, on))
        self.live_icon = QComboBox()
        for k, text, _ in LIVE_ICONS:
            self.live_icon.addItem(text, k)
        self.live_pos = QComboBox()
        for k, text in LIVE_POSITIONS:
            self.live_pos.addItem(text, k)
        for combo, key, default in ((self.live_icon, "live_icon", "blue"), (self.live_pos, "live_pos", "top")):
            i = combo.findData(win.settings.value(key, default))
            combo.setCurrentIndex(max(0, i))
            combo.currentIndexChanged.connect(lambda _i, c=combo, k=key: win.settings.setValue(k, c.currentData()))
        self.live_tile_b.toggled.connect(self.live_icon.setEnabled)
        self.live_row_b.toggled.connect(self.live_pos.setEnabled)
        self.live_icon.setEnabled(self.live_tile_b.isChecked())
        self.live_pos.setEnabled(self.live_row_b.isChecked())
        lay.addWidget(hbox(self.live_tile_b, None, label("Icon", "Muted"), self.live_icon))
        lay.addWidget(hbox(self.live_row_b, None, label("Position", "Muted"), self.live_pos))
        self.tile_menu_b = Toggle("Hold OK on an app opens a menu: Open, Move (arrows), dock, App info, Uninstall")
        self.tile_menu_b.setChecked(win.settings.value("tile_menu", "1") != "0")
        self.tile_menu_b.toggled.connect(lambda on: win.settings.setValue("tile_menu", "1" if on else "0"))
        self._extras_key = ""
        self._extras_loading = False
        for sw in (self.input_svc, self.home_svc, self.live_tile_b, self.live_row_b, self.tile_menu_b, self.tv_key_b):
            sw.toggled.connect(lambda _on: self.save_extras())
        for combo in (self.live_icon, self.live_pos):
            combo.currentIndexChanged.connect(lambda _i: self.save_extras())
        lay.addWidget(self.tile_menu_b)
        lay.addWidget(label("On some sets (TCL G09) a key helper costs the volume key repeat: hold volume up "
                            "before and after to check. CVTE boards: never enable a helper in the same pass as "
                            "changing Home (#741).", "Dim", wrap=True))
        self.prep = button("Prepare tools", None, "box", "Creates tools\\venv with adb-shell, which the build "
                                                         "script uses")
        self.build = button("Build & install", "Primary", "tv")
        self.clean = Toggle("Clean build")
        self.clean.setToolTip("Deletes the previous build first, so everything is compiled again and the TV can only "
                              "get the fresh launcher. Takes a minute or two longer.")
        self.clean.setChecked(win.settings.value("clean_build", "1") == "1")
        self.clean.toggled.connect(lambda on: win.settings.setValue("clean_build", "1" if on else "0"))
        self.cfg = button("Open config.xml", "Ghost", "folder")
        self.diag = button("Launcher report", "Ghost", "search", "Collects which build the TV runs, the Live TV pieces, "
                                                               "the theme on the TV and the launcher's log, to send on")
        lay.addWidget(hbox(self.prep, self.build, self.clean, None, self.diag, self.cfg))
        self.out = QPlainTextEdit()
        self.out.setObjectName("Box")
        self.out.setReadOnly(True)
        self.out.setMinimumHeight(170)
        self.out.hide()
        lay.addWidget(self.out)
        self.body.addWidget(c)

        # Install an app from this PC
        c, lay = card()
        lay.addWidget(label("Install an app from this PC", "H2"))
        lay.addWidget(label("Pick an .apk (or all the .apk parts of one app, or an .apks/.xapk bundle): it is copied "
                            "to the TV and installed, or updated if it is already there. Use apps made for Android "
                            "TV, from a source you trust.", "Muted", wrap=True))
        self.apk_btn = button("Browse APK…", "Primary", "folder")
        self.apk_btn.clicked.connect(self.install_apk)
        lay.addWidget(hbox(self.apk_btn, None))
        self.apk_bar = QProgressBar()
        self.apk_bar.setFixedHeight(8)
        self.apk_bar.setTextVisible(False)
        self.apk_bar.hide()
        lay.addWidget(self.apk_bar)
        self.apk_msg = Banner("")
        lay.addWidget(self.apk_msg)
        self.apk_sig = ProgressSignal()
        self.apk_sig.step.connect(self._apk_step)
        self.body.addWidget(c)

        # Copy apps from the TV to this PC
        c, lay = card()
        lay.addWidget(label("Copy apps from the TV to this PC", "H2"))
        lay.addWidget(label("Saves one or more apps from the TV or box as .apk files (or .apks when an app comes in "
                            "parts), to keep them or to install them on another TV with the card above.", "Muted",
                            wrap=True))
        self.pull_btn = button("Choose apps…", "Primary", "save")
        self.pull_btn.clicked.connect(self.pull_apps)
        self.pull_open = button("Open folder", None, "folder")
        self.pull_open.clicked.connect(lambda: open_path(Path(getattr(self, "pull_dest", "") or
                                                              cyt_home() / "apps")))
        self.pull_open.hide()
        lay.addWidget(hbox(self.pull_btn, self.pull_open, None))
        self.pull_bar = QProgressBar()
        self.pull_bar.setFixedHeight(8)
        self.pull_bar.setTextVisible(False)
        self.pull_bar.hide()
        lay.addWidget(self.pull_bar)
        self.pull_msg = Banner("")
        lay.addWidget(self.pull_msg)
        self.pull_sig = ProgressSignal()
        self.pull_sig.step.connect(lambda d, t, w: (self.pull_bar.setValue(int(1000 * d / max(t, 1))),
                                                    self.pull_msg.set(f"Copying {w}… {d / 1048576:.1f} of "
                                                                      f"{t / 1048576:.1f} MB", "info")))
        self.body.addWidget(c)
        self.body.addStretch(1)

        self.dns_on.clicked.connect(lambda: self.settings_job([
            "settings put global private_dns_specifier dns.adguard-dns.com",
            "settings put global private_dns_mode hostname"], "AdGuard DNS on. Open an app and check it still plays."))
        self.dns_off.clicked.connect(lambda: self.settings_job(
            ["settings put global private_dns_mode opportunistic"], "Private DNS back to automatic."))
        self.anim_fast.clicked.connect(lambda: self.settings_job(
            [f"settings put global {k} 0.5" for k in ("window_animation_scale", "transition_animation_scale",
                                                      "animator_duration_scale")], "Animations at 0.5×."))
        self.anim_norm.clicked.connect(lambda: self.settings_job(
            [f"settings put global {k} 1.0" for k in ("window_animation_scale", "transition_animation_scale",
                                                      "animator_duration_scale")], "Animations back to 1×."))
        self.prep.clicked.connect(self.prepare)
        self.dream_on.clicked.connect(self.dream_enable)
        self.dream_test.clicked.connect(self.dream_now)
        self.dream_off.clicked.connect(self.dream_disable)
        self.build.clicked.connect(self.build_install)
        self.diag.clicked.connect(self.report)
        self.cfg.clicked.connect(lambda: open_path(LAUNCHER / "app" / "src" / "main" / "res" / "values" / "config.xml"))
        self.proc = None
        self.line.connect(self._say)
        self.refresh_toolchain()

    def _pill(self, key):
        p = Pill("—", C["muted"])
        setattr(self, f"pill_{key}", p)
        return p

    # ---- the launcher switches, remembered per TV model -------------------------------------------------------
    @staticmethod
    def model_key(info):
        brand = info.get("brand") or info.get("manufacturer") or ""
        raw = f"{brand} {info.get('model', '')} {info.get('device', '')}".strip()
        return re.sub(r"[^A-Za-z0-9._ -]", "_", raw)[:80]

    def extras_now(self):
        return {"input_svc": self.input_svc.isChecked(), "home_svc": self.home_svc.isChecked(),
                "live_tile": self.live_tile_b.isChecked(), "live_row": self.live_row_b.isChecked(),
                "tile_menu": self.tile_menu_b.isChecked(), "tv_key": self.tv_key_b.isChecked(),
                "live_icon": self.live_icon.currentData(), "live_pos": self.live_pos.currentData()}

    def set_extras(self, d):
        self._extras_loading = True
        try:
            # The helper first: the TV-button switch turns it on and goes off with it.
            for key, t in (("input_svc", self.input_svc), ("home_svc", self.home_svc),
                           ("live_tile", self.live_tile_b), ("live_row", self.live_row_b),
                           ("tile_menu", self.tile_menu_b), ("tv_key", self.tv_key_b)):
                if key in d:
                    t.setChecked(bool(d[key]))
            for key, c in (("live_icon", self.live_icon), ("live_pos", self.live_pos)):
                i = c.findData(d.get(key))
                if i >= 0:
                    c.setCurrentIndex(i)
        finally:
            self._extras_loading = False

    def save_extras(self):
        if self._extras_loading or not self._extras_key or not TV.connected:
            return
        self.win.settings.setValue(f"extras/{self._extras_key}", json.dumps(self.extras_now()))
        self.extras_for.setText(f"Launcher switches for <b>{self._extras_name}</b>: saved for this model, used "
                                "again whenever a TV of this model connects.")

    def apply_extras_for(self, info):
        """Every TV model keeps its own switches. A model seen before gets what was chosen for it; a new one starts
        from the current switches, with the Live TV ones set by what this TV has."""
        self._extras_key = self.model_key(info)
        self._extras_name = info.get("model") or "this TV"
        saved = self.win.settings.value(f"extras/{self._extras_key}", "")
        try:
            d = json.loads(saved) if saved else None
        except ValueError:
            d = None
        live = info.get("live_tv_app") or ""
        if d:
            self.set_extras(d)
            self.extras_for.setText(f"Launcher switches for <b>{self._extras_name}</b>: the ones you chose for this "
                                    "model last time.")
            return
        d = self.extras_now()
        d.update(live_tile=bool(live), live_row=bool(live), tile_menu=True)
        if not live:
            d["tv_key"] = False
        self.set_extras(d)
        self.extras_for.setText(
            f"Launcher switches for <b>{self._extras_name}</b>: suggested for this TV " +
            (f"(Live TV app found: {live}). " if live else "(no Live TV app or tuner found, so the Live TV ones are "
                                                          "off). ") +
            "Change any of them and they are kept for this model.")

    def on_connection(self, ok, info):
        if ok:
            self.apply_extras_for(info)
            self.refresh()
            sdk = info.get("sdk_int", 0)
            self.build.setEnabled(sdk >= 26)
            self.build.setToolTip("" if sdk >= 26 else f"SDK {sdk} is below 26: the launcher cannot be installed")
            self.dns_on.setEnabled(sdk >= 28)
        else:
            for k in ("dns", "anim", "launcher", "dream"):
                getattr(self, f"pill_{k}").set("—", C["muted"])

    def refresh(self):
        def read():
            mode = TV.sh("settings get global private_dns_mode", quiet=True).strip()
            spec = TV.sh("settings get global private_dns_specifier", quiet=True).strip()
            anim = TV.sh("settings get global window_animation_scale", quiet=True).strip()
            home, _ = TV.home_owner()
            dream = TV.sh("settings get secure screensaver_components", quiet=True).strip()
            return mode, spec, anim, home, dream

        def show(v):
            mode, spec, anim, home, dream = v
            if DREAM_COMPONENT in dream:
                self.pill_dream.set("Clock on", C["ok"])
            else:
                self.pill_dream.set("TV's own" if dream in ("", "null") else dream.split("/")[0].split(".")[-1],
                                    C["muted"])
            if mode == "hostname" and "adguard" in spec:
                self.pill_dns.set("AdGuard on", C["ok"])
            elif mode == "hostname":
                self.pill_dns.set(spec, C["sky"])
            else:
                self.pill_dns.set("Off", C["muted"])
            self.pill_anim.set(f"{anim or '1.0'}×" if anim not in ("null", "") else "1×", C["sky"])
            self.pill_launcher.set("Installed – Home" if home == OUR_LAUNCHER else f"Home: {home or '?'}",
                                   C["ok"] if home == OUR_LAUNCHER else C["muted"])

        run_job(read, on_result=show)

    def dream_enable(self):
        if not self.need_tv():
            return
        ms = self.dream_wait.currentData()

        host = TV.host
        had_wait = bool(self.win.settings.value(f"dream_prev_wait/{host}", ""))

        def go():
            if not launcher_installed():
                raise RuntimeError("Install the CleanYourTV launcher first (Build & install above).")
            remember_settings(["secure/screensaver_components", "secure/screensaver_enabled",
                               "secure/screensaver_activate_on_sleep", "system/screen_off_timeout"])
            prev = TV.sh("settings get secure screensaver_components", quiet=True).strip()
            # When to start: the TV's "Start screensaver after" setting.
            prev_wait = TV.sh("settings get system screen_off_timeout", quiet=True).strip()
            TV.sh(f"settings put secure screensaver_components {DREAM_COMPONENT}")
            TV.sh("settings put secure screensaver_enabled 1")
            TV.sh("settings put secure screensaver_activate_on_sleep 1")
            TV.sh(f"settings put system screen_off_timeout {int(ms)}")
            return prev, prev_wait

        def remember(res):
            # QSettings belongs to the main thread, so the TV's previous values are stored here.
            prev, prev_wait = res
            if DREAM_COMPONENT not in prev:
                self.win.settings.setValue(f"dream_prev/{host}", prev)
            if not had_wait:
                self.win.settings.setValue(f"dream_prev_wait/{host}", prev_wait)

        run_job(go, on_result=lambda res: (remember(res), log("clock screensaver on", "ok"), self.refresh(), inform(
            self, "Clock screensaver on", f"It starts when the TV sits idle {self.dream_wait.currentText()}. Press "
            "<b>Show it now</b> to see it, any remote key closes it.", "ok")),
                on_error=lambda m: inform(self, "Clock screensaver", m, "bad"))

    def dream_now(self):
        if not self.need_tv():
            return
        self.dream_test.setEnabled(False)

        def go():
            # The system's "start the screensaver now" activity, where the firmware has it.
            out = TV.sh("am start -n com.android.systemui/.Somnambulator 2>&1")
            if "Error" not in out and "does not exist" not in out:
                time.sleep(3)
                return "started", TV.screenshot()
            # Not on this firmware, and `cmd dreams` needs root: open the TV's screensaver settings instead,
            # where "Clock" is now selected and the TV offers its own "Start now".
            for action in ("android.settings.DREAM_SETTINGS", "android.settings.DISPLAY_SETTINGS"):
                out = TV.sh(f"am start -a {action} 2>&1")
                if "Error" not in out:
                    time.sleep(2)
                    return "settings", TV.screenshot()
            return "none", None

        def done(res):
            how, shot = res
            if shot:
                BUS.shot.emit(shot)
            if how == "settings":
                inform(self, "Screensaver settings opened on the TV",
                       "This TV has no way to start a screensaver from the computer, so its <b>Screensaver</b> "
                       "settings are open on the TV now. <b>Clock</b> should be the selected screensaver there; use "
                       "the TV's <b>Start now</b> to see it. It also starts by itself when the TV sits idle.", "info")
            elif how == "none":
                inform(self, "Can't start it from here",
                       "This TV allows neither starting the screensaver nor opening its settings from the computer. "
                       "The clock is still set: it starts by itself when the TV sits idle.", "warn")

        run_job(go, on_result=done, on_done=lambda: self.dream_test.setEnabled(True))

    def dream_disable(self):
        if not self.need_tv():
            return
        prev = self.win.settings.value(f"dream_prev/{TV.host}", "") or ""
        prev_wait = self.win.settings.value(f"dream_prev_wait/{TV.host}", "") or ""

        def go():
            # The whole saved value goes into a shell command, so all of it must be component names.
            if prev and prev != "null" and all(COMPONENT_RE.match(c) for c in prev.split(",")):
                TV.sh(f"settings put secure screensaver_components {prev}")
            else:
                TV.sh("settings delete secure screensaver_components")
            if prev_wait.isdigit():
                TV.sh(f"settings put system screen_off_timeout {prev_wait}")

        run_job(go, on_result=lambda _: (log("screensaver back to the TV's own", "ok"), self.refresh()))

    def settings_job(self, cmds, done):
        if not self.need_tv():
            return

        def go():
            remember_settings(settings_from_commands(cmds))
            for c in cmds:
                TV.sh(c)

        run_job(go, on_result=lambda _: (log(done, "ok"), self.refresh()))

    def _venv_python(self):
        p = TOOLS / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        return p if p.exists() else None

    def _stream(self, program, args, env=None, cwd=None, after=None, keep=False):
        self.out.show()
        if not keep:
            self.out.clear()
        self.proc = QProcess(self)
        self.proc.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        if env:
            e = QProcessEnvironment.systemEnvironment()
            for k, v in env.items():
                e.insert(k, v)
            self.proc.setProcessEnvironment(e)
        if cwd:
            self.proc.setWorkingDirectory(str(cwd))
        self.proc.readyReadStandardOutput.connect(
            lambda: self.out.appendPlainText(_decode_output(bytes(self.proc.readAllStandardOutput())).rstrip()))

        def finished(code, _status):
            self.out.appendPlainText(f"\n— finished with exit code {code} —")
            self.prep.setEnabled(True)
            self.build.setEnabled(TV.info.get("sdk_int", 0) >= 26)
            if after:
                after(code)

        def failed(err):
            if err != QProcess.ProcessError.FailedToStart:
                return   # a crash still ends in finished()
            self.out.appendPlainText(f"\n— could not start {program}: {self.proc.errorString()} —")
            self.prep.setEnabled(True)
            self.build.setEnabled(TV.info.get("sdk_int", 0) >= 26)

        self.proc.finished.connect(finished)
        self.proc.errorOccurred.connect(failed)
        self.prep.setEnabled(False)
        self.build.setEnabled(False)
        self.out.appendPlainText(f"$ {program} {' '.join(args)}")
        self.proc.start(program, args)

    def prepare(self):
        py = _console_python()
        venv = TOOLS / "venv"
        if self._venv_python():
            args = ["-m", "pip", "install", "-r", str(TOOLS / "requirements.txt")]
            self._stream(str(self._venv_python()), args)
            return
        # create, then install
        self._stream(py, ["-m", "venv", str(venv)],
                     after=lambda code: code == 0 and self._venv_python() and self._stream(
                         str(self._venv_python()), ["-m", "pip", "install", "-r", str(TOOLS / "requirements.txt")]))

    def _say(self, text):
        self.out.show()
        self.out.appendPlainText(text)

    def refresh_toolchain(self):
        def check():
            return find_jdk(), find_sdk()

        def show(res):
            (best, found), sdk = res
            if best:
                j = f"Java {best[1]} ✓"
                col = C["ok"]
            elif found:
                j = "Java " + "/".join(sorted({str(v) for _, v in found if v})) + " – needs 17–22"
                col = C["warn"]
            else:
                j = "No Java"
                col = C["warn"]
            if sdk:
                miss = sdk_missing(sdk)
                a = "Android SDK ✓" if not miss else "Android SDK: needs " + ", ".join(m.split(";")[1] for m in miss)
                col = col if not miss else C["warn"]
            else:
                a = "No Android SDK"
                col = C["warn"]
            self.pill_tool.set(f"{j}  ·  {a}", col)

        run_job(check, on_result=show, pool=NET_POOL)

    def build_install(self):
        if not self.need_tv():
            return
        if DEMO:
            self.out.show()
            self.out.setPlainText("(demo) would check Java and the Android SDK, then run "
                                  "launcher\\build-and-install.ps1 -TvHost 192.168.1.77")
            return
        if not self._venv_python():
            inform(self, "Prepare tools first", "The build script talks to the TV through tools\\venv. Press "
                   "<b>Prepare tools</b> once, then build.", "warn")
            return
        if TV.info.get("cvte") and (self.input_svc.isChecked() or self.home_svc.isChecked()):
            inform(self, "CVTE board", "On a CVTE board, install the launcher without key helpers first, reboot "
                   "once and check Home and ADB come back. Enable a helper in a later pass (#741).", "warn")
            return
        if not ask(self, "Build and install the launcher?",
                   "This builds the launcher with Gradle (a few minutes the first time), installs it, makes it Home "
                   "and disables the stock launcher. If Home does not end up on the new launcher, the script "
                   "re-enables the stock one.", "Build & install"):
            return
        self.out.show()
        self.out.clear()
        self._say("Checking Java and the Android SDK…")
        self.build.setEnabled(False)
        run_job(lambda: (find_jdk(), find_sdk()), pool=NET_POOL, on_result=self._toolchain_checked,
                on_error=lambda m: (self._say(f"Check failed: {m}"), self.build.setEnabled(True)))

    def _toolchain_checked(self, res):
        (best, found), sdk = res
        steps = []
        jdk = best[0] if best else None
        if best:
            self._say(f"Java {best[1]}: {best[0]}")
        else:
            have = ", ".join(f"Java {v} ({p})" for p, v in found if v) or "none"
            self._say(f"No Java between {JDK_MIN} and {JDK_MAX} found (found: {have}). Gradle 8.9 cannot run on "
                      "newer Java, e.g. 25 fails with \"Unsupported class file major version 69\".")
            if not TEMURIN_URL or not ask(
                    self, "Download Java 21 for the build?",
                    f"The launcher builds with Java {JDK_MIN}–{JDK_MAX}, and this PC has none (your other Java stays "
                    "as it is). Download <b>Eclipse Temurin JDK 21</b> (about 200 MB, free, open source) into "
                    f"{JDK_HOME_DIR}? It is used only for this build.", "Download Java 21"):
                self._say("Stopped: install Android Studio (it brings Java 21) or a JDK 17/21, then try again.")
                self.build.setEnabled(True)
                return
            steps.append("jdk")
        miss = sdk_missing(sdk) if sdk else None
        if sdk and not miss:
            self._say(f"Android SDK: {sdk}")
        else:
            target = sdk or SDK_HOME_DIR
            what = ("the Android SDK (command-line tools, platform-tools, platform 34, build-tools 34.0.0, "
                    "about 400 MB)") if not sdk else "these Android SDK packages: " + ", ".join(miss)
            if not ask(self, "Set up the Android SDK?",
                       f"The build needs {what}, installed into <b>{target}</b>.<br><br>Installing them means "
                       "accepting Google's <a href='" + SDK_LICENSE_URL + "'>Android SDK License Agreement</a> "
                       "(and the licences sdkmanager lists for these packages). Do you accept them and want to "
                       "install?", "I accept – install"):
                self._say("Stopped: the Android SDK is needed. Install Android Studio, or press Build again and "
                          "accept the SDK setup.")
                self.build.setEnabled(True)
                return
            steps.append(("sdk", target))
        if not steps:
            self._run_build(jdk, sdk)
            return

        say = self.line.emit

        def prepare():
            j = jdk
            if "jdk" in steps:
                j = install_jdk(say)
            s = sdk
            for st in steps:
                if isinstance(st, tuple):
                    s = install_sdk(st[1], j, say)
            return j, s

        run_job(prepare, pool=NET_POOL, on_result=lambda r: (self.refresh_toolchain(), self._run_build(*r)),
                on_error=lambda m: (self._say(f"Setup failed: {m}"), self.build.setEnabled(True)))

    def install_apk(self):
        if not self.need_tv():
            return
        start = self.win.settings.value("apk_dir", str(Path.home() / "Downloads"))
        files, _ = QFileDialog.getOpenFileNames(self, "Pick the app to install", start,
                                                "Android apps (*.apk *.apks *.xapk);;All files (*)")
        if not files:
            return
        self.win.settings.setValue("apk_dir", str(Path(files[0]).parent))
        self.apk_btn.setEnabled(False)
        self.apk_bar.setRange(0, 1000)
        self.apk_bar.setValue(0)
        self.apk_bar.show()
        self.apk_msg.set(f"Copying {Path(files[0]).name}" + (f" and {len(files) - 1} more" if len(files) > 1 else "") +
                         " to the TV…", "info")

        def done(msg):
            self.apk_msg.set(msg, "ok")
            BUS.packages_changed.emit()

        run_job(install_apks, files, self.apk_sig, on_result=done,
                on_error=lambda m: self.apk_msg.set(m, "bad"),
                on_done=lambda: (self.apk_btn.setEnabled(True), self.apk_bar.hide()))

    def pull_apps(self):
        if not self.need_tv():
            return
        self.pull_btn.setEnabled(False)
        self.pull_msg.set("Reading the apps on the TV…", "info")

        def chosen(apps):
            self.pull_btn.setEnabled(True)
            self.pull_msg.set("")
            dest = self.win.settings.value("pull_dir", str(cyt_home() / "apps"))
            d = PickAppsDialog(self, apps, dest)
            if d.exec() != QDialog.DialogCode.Accepted or not d.ticked:
                return
            dest = d.dest.text().strip() or dest
            self.win.settings.setValue("pull_dir", dest)
            self.pull_dest = dest
            self.pull_btn.setEnabled(False)
            self.pull_bar.setRange(0, 1000)
            self.pull_bar.setValue(0)
            self.pull_bar.show()
            self.pull_open.hide()

            def done(res):
                saved, notes = res
                msg = (f"Saved {len(saved)} app{'s' if len(saved) != 1 else ''} to <b>{dest}</b>: " +
                       ", ".join(p.name for p in saved[:6]) + (" …" if len(saved) > 6 else ""))
                self.pull_msg.set(msg + ("<br>" + "<br>".join(notes) if notes else ""), "ok" if saved else "warn")
                self.pull_open.show()

            run_job(pull_apps, sorted(d.ticked), dest, self.pull_sig, on_result=done,
                    on_error=lambda m: self.pull_msg.set(f"Copy stopped: {m}", "bad"),
                    on_done=lambda: (self.pull_btn.setEnabled(True), self.pull_bar.hide()))

        run_job(lambda: tv_apps(True), on_result=chosen,
                on_error=lambda m: (self.pull_btn.setEnabled(True), self.pull_msg.set(m, "bad")))

    def _apk_step(self, done, total, what):
        if total > 0:
            self.apk_bar.setValue(int(1000 * done / total))
        if what == "installing…":
            self.apk_msg.set("Installing on the TV… if the TV asks to confirm or checks the app, answer it there.",
                             "info")
        else:
            self.apk_msg.set(f"Copying {what} to the TV… {done / 1048576:.1f} of {total / 1048576:.1f} MB", "info")

    def _live_switch(self, key, on):
        self.win.settings.setValue(key, "1" if on else "0")
        tp = next((p for p in self.win.page_list if isinstance(p, ThemesPage)), None)
        if tp is not None:
            cb = tp.live_tile if key == "live_tile" else tp.switches.get("live_tv_row")
            if cb is not None and cb.isChecked() != on:
                cb.setChecked(on)

    def report(self):
        self.diag.setEnabled(False)

        def show(text):
            DATA.mkdir(parents=True, exist_ok=True)
            f = DATA / f"launcher-report-{time.strftime('%Y%m%d-%H%M%S')}.txt"
            try:
                f.write_text(text, encoding="utf-8")
            except OSError:
                f = None
            d = Dialog(self, "Launcher report", 820)
            d.lay.addWidget(label("Send this text (or the file) over. The TV's IP is replaced with &lt;tv ip&gt;." +
                                  (f"<br>Saved as {f}" if f else ""), "Muted", wrap=True, rich=True))
            box = QPlainTextEdit(text)
            box.setObjectName("Box")
            box.setReadOnly(True)
            box.setMinimumHeight(420)
            d.lay.addWidget(box)
            copy = button("Copy", None, "save")
            copy.clicked.connect(lambda: QApplication.clipboard().setText(text))
            d.lay.addWidget(hbox(copy, None))
            d.buttons("Close", None)
            d.exec()

        run_job(launcher_report, on_result=show, on_done=lambda: self.diag.setEnabled(True))

    def _run_build(self, jdk, sdk):
        """Wake the TV and check it answers, then build. A long first download can leave it asleep."""
        self._say("Checking the TV is awake and answers…")
        run_job(lambda: tv_preflight() and tv_stamp(), on_result=lambda st: self._start_build(jdk, sdk, st),
                on_error=lambda m: (self._say(m), self.build.setEnabled(TV.info.get("sdk_int", 0) >= 26),
                                    inform(self, "The TV does not answer", m, "warn")))

    def _start_build(self, jdk, sdk, stamp=""):
        jdk, sdk = Path(jdk), Path(sdk)
        started = time.time()
        if self.clean.isChecked():
            gone = clean_launcher_build(LAUNCHER)
            self._say("Clean build: removed " + (", ".join(gone) if gone else "nothing (no earlier build)"))
        # Point the build at this SDK; an older local.properties may name one that does not exist.
        try:
            (LAUNCHER / "local.properties").write_text(f"sdk.dir={sdk.as_posix()}\n", encoding="ascii")
        except OSError as e:
            self._say(f"Could not write launcher/local.properties: {e}")
        env = {"TV_HOST": TV.host, "TV_PORT": str(TV.port), "JAVA_HOME": str(jdk), "ANDROID_HOME": str(sdk),
               "ANDROID_SDK_ROOT": str(sdk),
               "PATH": str(jdk / "bin") + os.pathsep + os.environ.get("PATH", "")}
        try:
            ok, why = apply_livetv(LAUNCHER, LIVETV_EDITS, LIVETV_FILES)
        except Exception as e:
            ok, why = False, str(e)
        self.livetv_built = ok
        self._say("Live TV row: " + ("included" if ok else f"left out, {why}"))
        if not ok and (self.live_row_b.isChecked() or self.tile_menu_b.isChecked()):
            inform(self, "Built without this app's additions",
                   "The toolkit's launcher changed in a way this version of the app does not know yet, so this build "
                   "has no Live TV channels row and no Open in the hold-OK menu. Everything else is installed as usual."
                   "<br><br>Get the newest CleanYourTV (github.com/nikkpap/CleanYourTV-App) and build again.", "warn")
        want_tile, want_row = self.live_tile_b.isChecked(), self.live_row_b.isChecked()
        want_icon, want_pos = self.live_icon.currentData(), self.live_pos.currentData()
        want_tv_key = False
        want_menu = self.tile_menu_b.isChecked()
        live_pkg = ""
        try:
            live_pkg, _ = launcher_hidden_defaults()
            if TV.info.get("live_tv_app") and set_config_string(LAUNCHER, "live_tv_package", live_pkg):
                self._say(f"Live TV app on this TV: {live_pkg}")
            if ok:
                set_config_bool(LAUNCHER, "live_tv_row", want_row)
                set_config_string(LAUNCHER, "live_tv_row_position", want_pos)
                # Our Greek strings for the menu step aside when the toolkit ships its own Greek translation.
                el = LAUNCHER / "app" / "src" / "main" / "res" / "values-el"
                if (el / "strings.xml").is_file() and (el / "strings_cleanyourtv.xml").is_file():
                    (el / "strings_cleanyourtv.xml").unlink()
            set_config_bool(LAUNCHER, "tile_menu", want_menu)
            want_tv_key = self.tv_key_b.isChecked() and self.input_svc.isChecked() and bool(live_pkg) \
                and bool(TV.info.get("live_tv_app"))
            apply_tv_key(LAUNCHER, live_pkg, want_tv_key)
            if want_tv_key:
                self._say(f"TV button: opens {live_pkg}")
            self._say("Hold-OK menu: " + ("on" if want_menu else "off"))
            self._say("Live TV row: " + (f"on, {want_pos}" if want_row and ok else "off") + " in this build")
            # banner_tv_blue comes with this app's launcher additions; without them, the launcher's own banner_tv.
            note = apply_live_tile(LAUNCHER, live_pkg, want_tile,
                                   live_banner(want_icon) if ok or want_icon != "blue" else "banner_tv")
            self._say("Live TV app: " + (f"tile, icon {want_icon}" if want_tile else "hidden, under Inputs") +
                      (f" ({note})" if note else ""))
        except Exception as e:
            self._say(f"Live TV: config.xml left as it was ({e})")
        self._say(f"{APP_NAME} {APP_VERSION} · building with Java at {jdk}\n")

        def after(code):
            if code == 0:
                apk = LAUNCHER / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
                try:
                    fresh = apk.stat().st_mtime >= started - 5
                except OSError:
                    fresh = False
                if not fresh and not DEMO:
                    self._say("WARNING: the APK in app/build is older than this build. Tick Clean build and run "
                              "Build & install again.")

                def check():
                    if ok:
                        grant_livetv()
                        # The launcher started before the grant and found no channels: Home again reads them.
                        TV.sh("input keyevent KEYCODE_HOME", quiet=True)
                    notes = sync_live_on_tv(want_row and ok, want_tile, live_pkg, live_banner(want_icon), want_pos,
                                            {"tile_menu": want_menu}, want_tv_key)
                    time.sleep(0 if DEMO else 4)
                    return launcher_update_age(), launcher_crash_since(stamp), notes

                def checked(res):
                    age, crash, notes = res
                    for n in notes:
                        self._say("Live TV: " + n)
                    if ok:
                        log("Live TV row: channel access granted to the launcher", "ok")
                    if age is not None:
                        self._say(f"On the TV: launcher installed {int(age)} s ago" +
                                  (" (this build)" if age < 900 else ": that is an OLD install, this build did not "
                                   "reach the TV"))
                    if crash:
                        self._say("The launcher CRASHED on the TV:\n" + crash)
                        inform(self, "The launcher crashed", "The new launcher stopped with an error on the TV. "
                               "The details are in the build log: send them over.", "warn")
                run_job(check, on_result=checked)
            self.refresh()
            BUS.packages_changed.emit()
            hook = getattr(self, "on_build_finished", None)   # a bundle set-up waits for the launcher
            if hook:
                self.on_build_finished = None
                QTimer.singleShot(5000 if code == 0 else 0, lambda: hook(code))

        cvte = bool(TV.info.get("cvte"))
        if cvte:
            # A CVTE board keeps its stock launcher (#741): the new one only becomes Home.
            self._say("CVTE board: the stock launcher stays enabled; the new launcher only becomes Home.")
            first_after = after

            def after(code):
                first_after(code)
                if code == 0:
                    inform(self, "CVTE board: reboot once now",
                           "On a CVTE board, reboot the TV once (Finish → Reboot &amp; compare) and check that Home "
                           "and the connection come back before changing anything else (#741).", "warn")

        if os.name == "nt":
            args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(LAUNCHER / "build-and-install.ps1"),
                    "-TvHost", TV.host]
            if cvte:
                args += ["-StockLauncher", "none"]
            if self.input_svc.isChecked():
                args.append("-InputKeyService")
            if self.home_svc.isChecked():
                args.append("-HomeKeyService")
            self._stream("powershell", args, env=env, cwd=LAUNCHER, after=after, keep=True)
        else:
            if cvte:
                env["STOCK_LAUNCHER"] = "none"
            if self.input_svc.isChecked():
                env["INPUT_KEY_SERVICE"] = "1"
            if self.home_svc.isChecked():
                env["HOME_KEY_SERVICE"] = "1"
            self._stream("bash", [str(LAUNCHER / "build-and-install.sh")], env=env, cwd=LAUNCHER, after=after,
                         keep=True)


# ----------------------------------------------------------------------------------------------
# Themes: the launcher's look, pushed the way tools/theme.sh does it
# ----------------------------------------------------------------------------------------------
THEME_PKG = OUR_LAUNCHER
DREAM_COMPONENT = f"{OUR_LAUNCHER}/.ClockDream"
THEME_DIR = f"/sdcard/Android/data/{THEME_PKG}/files"
THEME_URI = f"content://{THEME_PKG}.theme"
THEME_TMP = "/data/local/tmp/cyt-theme"
USER_THEMES = cyt_home() / "themes"   # themes you add or save; a toolkit update never touches them
MY_THEME = USER_THEMES / "my-theme"   # the My theme editor's working copy
WALL_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
REMOTE_PATH_RE = re.compile(r"/[A-Za-z0-9._/-]+")
# Same restart as theme.sh: force-stop the launcher, bring Home back the right way, and put the remote's
# accessibility helpers back on, since a force-stop drops them.
THEME_RESTART = (
    f"a=$(settings get secure enabled_accessibility_services); am force-stop {THEME_PKG}; "
    f"case \"$(cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME "
    f"| tail -n 1)\" in {THEME_PKG}/*) am start -a android.intent.action.MAIN -c android.intent.category.HOME "
    f">/dev/null ;; *) am start -n {THEME_PKG}/.MainActivity >/dev/null ;; esac; case \"$a\" in *{THEME_PKG}*) "
    "sleep 1; settings put secure enabled_accessibility_services \"$a\"; settings put secure accessibility_enabled 1; "
    "sleep 1; settings put secure enabled_accessibility_services ''; settings put secure accessibility_enabled 0; "
    "sleep 1; settings put secure enabled_accessibility_services \"$a\"; settings put secure accessibility_enabled 1 ;; esac")


def _stage(name):
    return f"{THEME_TMP}-{name.replace('/', '-')}"


def _put(name):
    # Through the launcher's ThemeProvider first (files then belong to the launcher), cp as the fallback;
    # Android 8/9 print "Unsupported operation" for content write and still exit 0 (theme.sh).
    t = _stage(name)
    return (f"rm -f {THEME_DIR}/{name} 2>/dev/null; {{ o=$(content write --uri {THEME_URI}/{name} < {t} 2>&1) && "
            f"case \"$o\" in *'Unsupported operation'*) false ;; esac; }} || cp {t} {THEME_DIR}/{name} 2>/dev/null; "
            f"rm -f {t}")


def _drop(name):
    return f"rm -f {THEME_DIR}/{name} 2>/dev/null; content delete --uri {THEME_URI}/{name} 2>/dev/null"


def push_file(local, remote, progress=None):
    """tools/b64push.py over the open connection: base64 chunks, md5 check, then move into place."""
    import base64
    import hashlib
    if not REMOTE_PATH_RE.fullmatch(remote) or ".." in remote:
        raise RuntimeError(f"refusing remote path {remote!r}")
    data = Path(local).read_bytes()
    if DEMO:
        time.sleep(0.15)
        return
    want = hashlib.md5(data).hexdigest()
    b64, part = remote + ".b64.part", remote + ".part"
    with TV.lock:
        chunk = min(48 * 1024, getattr(TV.dev, "max_chunk_size", 4096) * 3 // 4 - 64)
        chunk -= chunk % 3
        TV.sh(f"rm -f '{b64}' '{part}' && : > '{b64}'", quiet=True)
        n = (len(data) + chunk - 1) // chunk
        try:
            for i in range(n):
                piece = base64.b64encode(data[i * chunk:(i + 1) * chunk]).decode()
                out = TV.dev.shell(f"echo '{piece}' >> '{b64}' && echo ok{i}", read_timeout_s=60.0)
                if f"ok{i}" not in out:
                    raise RuntimeError(f"upload of {Path(local).name} failed at chunk {i + 1}/{n}")
                if progress:
                    progress(i + 1, n)
            out = TV.sh(f"base64 -d < '{b64}' > '{part}' && md5sum '{part}'; rm -f '{b64}'", quiet=True)
            got = out.split()[0] if out.strip() else ""
            if got != want:
                raise RuntimeError(f"{Path(local).name} arrived damaged (md5 mismatch); nothing was changed")
            if "moved" not in TV.sh(f"mv -f '{part}' '{remote}' && echo moved", quiet=True):
                raise RuntimeError(f"could not move {Path(local).name} into place")
        finally:
            TV.sh(f"rm -f '{b64}' '{part}'", quiet=True, retry=False)


def launcher_installed():
    return THEME_PKG in TV.packages(THEME_PKG)


THEME_NOTES = []   # what the last apply_theme() wants the Themes page to say


def apply_theme(folder):
    folder = Path(folder)
    cfg = folder / "config.json"
    json.loads(cfg.read_text(encoding="utf-8"))   # refuse broken JSON before touching the TV
    if not launcher_installed():
        raise RuntimeError("The CleanYourTV launcher is not installed on this TV. Install it on the Extras page first.")
    TV.sh(f"mkdir -p {THEME_DIR} 2>/dev/null; true", quiet=True)
    log(f"pushing theme {folder.name}", "info")
    push_file(cfg, _stage("config.json"))
    TV.sh(_put("config.json"), quiet=True)
    wall = folder / "wallpaper.jpg"
    if wall.is_file():
        push_file(wall, _stage("wallpaper.jpg"))
        TV.sh(_put("wallpaper.jpg"), quiet=True)
    else:
        TV.sh(_drop("wallpaper.jpg"), quiet=True)
    exts = ("jpg", "jpeg", "png", "webp", "JPG", "JPEG", "PNG", "WEBP")
    TV.sh(f"mkdir -p {THEME_DIR}/wallpapers 2>/dev/null; rm -f " +
          " ".join(f"{THEME_DIR}/wallpapers/*.{e}" for e in exts) +
          f" 2>/dev/null; content delete --uri {THEME_URI}/wallpapers 2>/dev/null; true", quiet=True)
    walls = folder / "wallpapers"
    if walls.is_dir():
        imgs = sorted(p for p in walls.iterdir() if p.is_file() and p.suffix.lstrip(".") in exts)
        for i, img in enumerate(imgs, 1):
            if not WALL_NAME_RE.match(img.name):
                raise RuntimeError(f"unsupported wallpaper filename: {img.name}")
            log(f"wallpaper {i}/{len(imgs)}: {img.name}", "info")
            push_file(img, _stage(f"wallpapers/{img.name}"))
            TV.sh(_put(f"wallpapers/{img.name}"), quiet=True)
    if (walls / "captions.txt").is_file():
        push_file(walls / "captions.txt", _stage("wallpapers/captions.txt"))
        TV.sh(_put("wallpapers/captions.txt"), quiet=True)
    else:
        TV.sh(_drop("wallpapers/captions.txt"), quiet=True)
    THEME_NOTES.clear()
    try:
        wants_livetv = bool(json.loads(cfg.read_text(encoding="utf-8")).get("live_tv_row"))
    except (OSError, ValueError, AttributeError):
        wants_livetv = False
    if wants_livetv:
        # Granted before the restart, so the launcher finds its channels as it comes back.
        if launcher_has_livetv():
            grant_livetv()
        else:
            THEME_NOTES.append("livetv_rebuild")
            log("this theme turns on the Live TV row, but the launcher on the TV was built without it", "warn")
    stamp = tv_stamp() if not DEMO else ""
    _revision_and_restart()
    verify_theme(cfg)
    crash = launcher_crash_since(stamp) if stamp else ""
    if crash:
        raise RuntimeError("the theme reached the TV, but the launcher crashed while loading it:<br><br>" +
                           crash.replace("&", "&amp;").replace("<", "&lt;").replace("\n", "<br>"))
    log(f"theme {folder.name} is on the TV", "ok")
    time.sleep(2.5)
    return TV.screenshot()


def _remote_md5(name):
    """md5 of a theme file as the launcher sees it: through its provider first, then the folder itself."""
    for cmd in (f"content read --uri {THEME_URI}/{name} 2>/dev/null | md5sum",
                f"md5sum {THEME_DIR}/{name} 2>/dev/null"):
        out = TV.sh(cmd, quiet=True).strip().split()
        if out and re.fullmatch(r"[0-9a-f]{32}", out[0]) and out[0] != "d41d8cd98f00b204e9800998ecf8427e":  # not ""
            return out[0]
    return None


def verify_theme(cfg):
    """Check that config.json really is where the launcher reads it, and that the launcher came back."""
    import hashlib
    if DEMO:
        return
    want = hashlib.md5(Path(cfg).read_bytes()).hexdigest()
    got = _remote_md5("config.json")
    time.sleep(1.5)
    running = bool(TV.sh(f"pidof {THEME_PKG} || ps -A | grep {THEME_PKG}", quiet=True).strip())
    home, _ = TV.home_owner()
    if got == want and running and home and home != THEME_PKG:
        raise RuntimeError(f"the theme is on the CleanYourTV launcher, but Home now opens <b>{home}</b>, so the TV "
                           "shows that one. The firmware probably brought its own launcher back after a reboot. "
                           "Run <b>Build &amp; install</b> on the Extras page again to make the new launcher Home.")
    if got == want and running:
        log("verified: config.json on the TV matches, launcher restarted, Home is the new launcher", "ok")
        return
    sdk = TV.prop("ro.build.version.sdk")
    listing = TV.sh(f"ls -la {THEME_DIR} 2>&1 | head -12", quiet=True).strip()
    provider = TV.sh(f"content read --uri {THEME_URI}/config.json 2>&1 | head -c 200", quiet=True).strip()
    staged = TV.sh(f"ls -la {THEME_TMP}* 2>&1 | head -5", quiet=True).strip()
    logs = TV.sh(f"logcat -d -t 300 2>/dev/null | grep -iE 'TvHome|{THEME_PKG}' | tail -8", quiet=True).strip()
    diag = (f"Android SDK {sdk}\n\nTheme folder ({THEME_DIR}):\n{listing or '(nothing)'}\n\n"
            f"Read through the launcher's provider:\n{provider or '(nothing)'}\n\nStaging files:\n{staged}"
            + (f"\n\nLauncher log:\n{logs}" if logs else ""))
    log("theme check failed:\n" + diag, "error")
    if got != want:
        why = ("config.json did not arrive where the launcher reads it" if got is None
               else "config.json on the TV differs from the theme's")
    else:
        why = "the launcher did not come back after the restart"
    raise RuntimeError(f"{why}. Details are in the Activity log (bottom left); send them to me and I'll fix it.")


def _revision_and_restart():
    import uuid
    rev = uuid.uuid4().hex
    TV.sh(f"printf '%s' '{rev}' > {_stage('theme_revision')}; {_put('theme_revision')}", quiet=True)
    TV.sh(THEME_RESTART + "; echo applied", quiet=True, timeout=60)


def reset_theme():
    if not launcher_installed():
        raise RuntimeError("The CleanYourTV launcher is not installed on this TV.")
    TV.sh(f"mkdir -p {THEME_DIR} 2>/dev/null; {_drop('config.json')}; {_drop('wallpaper.jpg')}; true", quiet=True)
    _revision_and_restart()
    log("theme reset to the launcher's built-in config", "ok")
    time.sleep(2.5)
    return TV.screenshot()


def leanback_apps():
    out = TV.sh("cmd package query-activities --brief -a android.intent.action.MAIN "
                "-c android.intent.category.LEANBACK_LAUNCHER", quiet=True)
    pkgs = sorted({m.group(1) for m in (COMPONENT_RE.match(l.strip()) for l in out.splitlines()) if m})
    return pkgs or sorted(TV.packages("-3"))


def load_themes():
    """Theme folders from the toolkit, with the one-line description from themes/README.md."""
    root = REPO / "themes"
    desc = {}
    try:
        for line in (root / "README.md").read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*`([\w.-]+)/`\s*\|\s*(.+?)\s*\|", line)
            if m:
                desc[m.group(1)] = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", m.group(2)).replace("`", "")
    except OSError:
        pass
    themes = []
    for base, mine in ((USER_THEMES, True), (root, False)):
        if not base.is_dir():
            continue
        for d in sorted(base.iterdir(), key=lambda x: x.name.lower()):
            if not (d / "config.json").is_file():
                continue
            text = desc.get(d.name, "") if not mine else ""
            try:
                text = (d / "about.txt").read_text(encoding="utf-8").strip().splitlines()[0]
            except (OSError, IndexError):
                pass
            shot = next((d / n for n in ("screenshot.jpg", "preview.jpg", "wallpaper.jpg") if (d / n).is_file()),
                        d / "screenshot.jpg")
            themes.append({"name": d.name, "path": d, "desc": text, "shot": shot, "mine": mine})
    return themes


def import_themes(src):
    """Copies the theme folders in a .zip (or a folder) into USER_THEMES; returns their names."""
    import tempfile
    import zipfile
    src = Path(src)
    tmp = None
    try:
        if src.is_file():
            tmp = Path(tempfile.mkdtemp(prefix="cyt-theme-"))
            with zipfile.ZipFile(src) as z:
                for n in z.namelist():
                    if n.startswith("/") or ".." in Path(n).parts:
                        raise RuntimeError(f"unsafe path in the zip: {n}")
                z.extractall(tmp)
            base = tmp
        else:
            base = src
        found = sorted({c.parent for c in base.rglob("config.json")
                        if not any(p.startswith(("_", ".")) for p in c.relative_to(base).parts)})
        if not found:
            raise RuntimeError("no theme in it (a theme is a folder with a config.json)")
        names = []
        USER_THEMES.mkdir(parents=True, exist_ok=True)
        for d in found:
            json.loads((d / "config.json").read_text(encoding="utf-8"))   # refuse broken JSON
            name = d.name if d != base else src.stem
            name = re.sub(r"[^A-Za-z0-9_.-]+", "-", name).strip("-") or "theme"
            dest = USER_THEMES / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(d, dest)
            names.append(name)
        return names
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


class ThemeCard(QFrame):
    clicked = pyqtSignal(object)

    def __init__(self, theme):
        super().__init__()
        self.theme = theme
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedWidth(262)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 10, 10, 12)
        lay.setSpacing(6)
        self.view = ShotView("No preview")
        self.view.setFixedSize(242, 136)
        if theme["shot"].is_file():
            self.view.set_path(str(theme["shot"]))
        lay.addWidget(self.view)
        name = theme["name"].replace("-", " ").title()
        until = ""
        try:
            until = json.loads((theme["path"] / "config.json").read_text(encoding="utf-8")).get("festival_until", "")
        except (OSError, ValueError, AttributeError):
            pass
        ended = bool(until) and until < time.strftime("%Y-%m-%d")
        title = label(name, "H2")
        row = QHBoxLayout()
        row.addWidget(title)
        row.addStretch(1)
        if theme.get("mine"):
            row.addWidget(Pill("mine", C["accent"]))
            self.setToolTip(str(theme["path"]))
        if ended:
            row.addWidget(Pill("ended", C["muted"]))
            self.setToolTip(f"Its festive skin switched itself off after {until}.")
        lay.addLayout(row)
        text = theme["desc"] or ""
        short = text if len(text) <= 105 else text[:102].rsplit(" ", 1)[0] + "…"
        d = label(short, "Muted", wrap=True)
        d.setToolTip(text)
        lay.addWidget(d)
        lay.addStretch(1)
        self.set_selected(False)

    def set_selected(self, on):
        border = C["accent"] if on else C["line"]
        bg = "#182032" if on else C["card"]
        self.setStyleSheet(f"ThemeCard {{ background: {bg}; border: {2 if on else 1}px solid {border}; "
                           "border-radius: 14px; } ThemeCard QLabel { background: transparent; }")

    def mousePressEvent(self, e):
        self.clicked.emit(self.theme)


class ThemesPage(Page):
    title = "Themes"
    subtitle = "Change how the launcher looks: pick a theme or make your own"

    def __init__(self, win):
        super().__init__(win)
        self.selected = None
        self.apps = []
        self.status = Banner("Themes need the CleanYourTV launcher on the TV (Extras → Build & install).", "info")
        self.body.addWidget(self.status)

        # gallery
        c, lay = card()
        top = QHBoxLayout()
        top.addWidget(label("Themes", "H2"))
        top.addStretch(1)
        self.reset_btn = button("Reset to default", None, "undo", "Remove the theme; back to the launcher's own config")
        self.apply_btn = button("Apply to TV", "Primary", "check")
        self.apply_btn.setEnabled(False)
        self.import_btn = button("Add themes…", "Ghost", "palette", "Add themes from a .zip into " + str(USER_THEMES))
        self.folder_btn = button("Folder", "Ghost", "folder", "Open " + str(USER_THEMES))
        top.addWidget(self.import_btn)
        top.addWidget(self.folder_btn)
        top.addWidget(self.reset_btn)
        top.addWidget(self.apply_btn)
        lay.addLayout(top)
        strip = QWidget()
        strip.setObjectName("Clear")
        self.grid = QGridLayout(strip)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(12)
        self.cards = []
        self.none_lbl = label("No themes folder found in the toolkit.", "Muted")
        lay.addWidget(self.none_lbl)
        self.fill_gallery()
        lay.addWidget(strip)
        lay.addWidget(label("Previews are the theme authors' own screenshots; your apps and wallpaper may differ. "
                            "Applying restarts the launcher, which takes a few seconds.", "Dim", wrap=True))
        self.body.addWidget(c)

        # my theme editor
        c, lay = card(spacing=12)
        top = QHBoxLayout()
        top.addWidget(label("My theme", "H2"))
        top.addStretch(1)
        self.from_sel = button("Start from selected", "Ghost", "list", "Load the selected theme's settings below")
        self.json_btn = button("Edit JSON…", "Ghost", "keyboard")
        self.my_apply = button("Save & apply", "Primary", "check")
        top.addWidget(self.from_sel)
        top.addWidget(self.json_btn)
        top.addWidget(self.my_apply)
        lay.addLayout(top)
        lay.addWidget(label(f"Saved in {MY_THEME}. Only the settings below are changed; anything else the theme "
                            "had stays as it was.", "Dim", wrap=True))
        cols = QHBoxLayout()
        cols.setSpacing(16)

        # dock
        left = QVBoxLayout()
        left.addWidget(label("Dock apps (drag to reorder)", "Key"))
        self.dock = QListWidget()
        self.dock.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.dock.setMinimumHeight(190)
        left.addWidget(self.dock)
        self.app_pick = QComboBox()
        self.app_pick.setEditable(True)
        self.app_pick.lineEdit().setPlaceholderText("Connect to list the TV's apps…")
        self.app_pick.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.app_pick.setMinimumContentsLength(10)
        add = button("Add", None, None)
        rem = button("Remove", "Ghost")
        left.addWidget(hbox(self.app_pick, add, rem))
        left.addWidget(label("4 to 7 apps fit nicely. Apps that are not installed are skipped by the launcher.",
                             "Dim", wrap=True))
        cols.addLayout(left, 1)

        # look
        form = QGridLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)
        r = 0

        def row(title, w, tip=""):
            nonlocal r
            l = label(title, "Key")
            if tip:
                l.setToolTip(tip)
                w.setToolTip(tip)
            form.addWidget(l, r, 0)
            form.addWidget(w, r, 1)
            r += 1

        self.columns = QSpinBox()
        self.columns.setRange(1, 8)
        row("Columns", self.columns, "Tiles per row; tiles shrink to fit from 5 up")
        self.rows = QSpinBox()
        self.rows.setRange(0, 3)
        row("Grid rows under dock", self.rows, "Grid rows left visible under the dock")
        self.bg = QPushButton("#000000")
        self.bg.clicked.connect(self.pick_color)
        row("Background colour", self.bg)
        self.wall_btn = button("Choose picture…", None, "folder")
        self.wall_clear = button("None", "Ghost")
        self.wall_view = ShotView("No wallpaper")
        self.wall_view.setFixedSize(144, 81)
        wb = QWidget()
        wb.setObjectName("Clear")
        wl = QVBoxLayout(wb)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(hbox(self.wall_btn, self.wall_clear, None))
        wl.addWidget(self.wall_view)
        row("Wallpaper", wb, "Any picture; it is cropped to 1920×1080 and saved as a light JPEG")
        self.dim = QSpinBox()
        self.dim.setRange(0, 90)
        self.dim.setSuffix(" %")
        row("Darken wallpaper", self.dim, "Black overlay over the wallpaper")
        self.opacity = QSpinBox()
        self.opacity.setRange(30, 100)
        self.opacity.setSuffix(" %")
        row("Dock opacity", self.opacity, "Lower lets a wallpaper show through the dock band")
        self.greet = QLineEdit()
        self.greet.setPlaceholderText("e.g. Nikos")
        row("Greeting name", self.greet, "Shown after GOOD MORNING / EVENING")
        self.clock = QSpinBox()
        self.clock.setRange(0, 1440)
        self.clock.setSuffix(" min")
        self.clock.setSpecialValueText("off")
        row("Clock screensaver after", self.clock, "Minutes Home may sit idle before the clock screensaver")
        form.setColumnStretch(1, 1)
        cols.addLayout(form, 1)

        # switches
        sw = QVBoxLayout()
        sw.addWidget(label("Options", "Key"))
        self.switches = {}
        for key, text, tip in [
            ("reduced_motion", "Reduced motion", "Calmer animations for weak TVs"),
            ("always_show_names", "Always show app names", "Names under every tile, dimmed until focused"),
            ("cinematic_home", "Cinematic top shelf", "The focused dock app's artwork fills the top of the screen"),
            ("dock_glass", "Frosted-glass dock", "Suits a wallpaper"),
            ("app_glow", "Glow in the app's colour", "The focus highlight glows in each app's colour"),
            ("icon_only_buttons", "Icon-only top buttons", "Wi-Fi and Settings as round icons"),
            ("app_library", "App library", "An App library pill to add or remove apps from Home"),
            ("show_stats", "CPU / memory line", "One line under the clock with CPU, free memory and storage"),
            ("live_tv_row", "Live TV channels row", "A row of the tuner's channels after the apps, like the stock "
                                                     "launcher's; OK tunes the channel. Needs the launcher built by "
                                                     "this app (Extras → Build & install)."),
        ]:
            cb = Toggle(text)
            cb.setToolTip(tip)
            self.switches[key] = cb
            sw.addWidget(cb)
        self.live_tile = Toggle("Live TV app as a tile")
        self.live_tile.setToolTip("The launcher hides the Live TV app because the Inputs menu (top right) already has "
                                  "it. Tick to show it among the apps too.")
        sw.addWidget(self.live_tile)
        self.live_tile.toggled.connect(lambda on: self._mirror("live_tile", on))
        self.switches["live_tv_row"].toggled.connect(lambda on: self._mirror("live_row", on))
        sw.addStretch(1)
        cols.addLayout(sw, 1)
        lay.addLayout(cols)
        self.my_msg = Banner("")
        lay.addWidget(self.my_msg)
        self.body.addWidget(c)
        self.body.addStretch(1)

        self.base = {}
        self.wall_src = None   # a QImage-ready path chosen by the user, or "" for none, or None = unchanged
        self._load_my_theme()

        self.apply_btn.clicked.connect(lambda: self.apply(self.selected["path"]) if self.selected else None)
        self.reset_btn.clicked.connect(self.reset)
        self.from_sel.clicked.connect(self.start_from_selected)
        self.json_btn.clicked.connect(self.edit_json)
        self.import_btn.clicked.connect(self.import_themes)
        self.folder_btn.clicked.connect(self.open_theme_folder)
        self.my_apply.clicked.connect(self.save_apply)
        add.clicked.connect(self.add_app)
        rem.clicked.connect(lambda: [self.dock.takeItem(self.dock.row(i)) for i in self.dock.selectedItems()])
        self.wall_btn.clicked.connect(self.choose_wall)
        self.wall_clear.clicked.connect(self.clear_wall)

    # --- gallery ------------------------------------------------------------------------------
    def fill_gallery(self, select=None):
        for cd in self.cards:
            self.grid.removeWidget(cd)
            cd.deleteLater()
        self.cards = []
        themes = load_themes()
        for i, t in enumerate(themes):
            cd = ThemeCard(t)
            cd.clicked.connect(self.pick)
            self.cards.append(cd)
            self.grid.addWidget(cd, i // 3, i % 3, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.none_lbl.setVisible(not themes)
        if select:
            t = next((c.theme for c in self.cards if c.theme.get("mine") and c.theme["name"] == select), None)
            if t:
                self.pick(t)

    def import_themes(self):
        f, _ = QFileDialog.getOpenFileName(self, "Add themes", str(Path.home() / "Downloads"),
                                           "Themes (*.zip);;All files (*)")
        if not f:
            return
        import zipfile
        try:
            names = import_themes(f)
        except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as e:
            self.status.set(f"Could not add themes from <b>{Path(f).name}</b>: {e}", "bad")
            return
        self.fill_gallery(select=names[0] if len(names) == 1 else None)
        self.status.set(f"Added {len(names)} theme{'s' if len(names) != 1 else ''}: <b>{', '.join(names)}</b>. "
                        "Pick one and press Apply.", "ok")

    def open_theme_folder(self):
        USER_THEMES.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(USER_THEMES)))

    def pick(self, theme):
        self.selected = theme
        for cd in self.cards:
            cd.set_selected(cd.theme is theme)
        self.apply_btn.setEnabled(True)
        self.apply_btn.setText(f"Apply “{theme['name']}”")

    def on_connection(self, ok, info):
        if not ok:
            return

        def check():
            return launcher_installed(), leanback_apps()

        def show(res):
            installed, apps = res
            self.apps = apps
            cur = self.app_pick.currentText()
            self.app_pick.clear()
            self.app_pick.addItems(apps)
            self.app_pick.setCurrentText(cur)
            if installed:
                self.status.set("The CleanYourTV launcher is installed. Pick a theme and press Apply; the TV "
                                "restarts Home with the new look.", "ok")
            else:
                self.status.set("The CleanYourTV launcher is <b>not installed</b> on this TV yet. Themes only change "
                                "that launcher: install it on the <b>Extras</b> page first. You can still prepare "
                                "<b>My theme</b> now.", "warn")

        run_job(check, on_result=show)

    def apply(self, folder):
        if not self.need_tv():
            return
        self._busy(True)
        self.status.set(f"Applying <b>{Path(folder).name}</b>… uploading files and restarting the launcher.", "info")
        self._pending = str(folder)
        run_job(apply_theme, folder, on_result=self._applied,
                on_error=lambda m: self.status.set(f"Could not apply the theme: {m}", "bad"),
                on_done=lambda: self._busy(False))

    def _applied(self, shot):
        self.win.settings.setValue(f"theme_applied/{TV.host}", getattr(self, "_pending", ""))
        BUS.shot.emit(shot)
        if "livetv_rebuild" in THEME_NOTES:
            self.status.set("Theme applied, but the launcher on the TV was built without the <b>Live TV channels "
                            "row</b>. Build &amp; install it once from this app to add the row.", "warn")
            if ask(self, "Add the Live TV row?",
                   "The theme turns the Live TV channels row on, but the launcher on your TV was built before this "
                   "app could add it. Build and install the launcher now? It keeps your theme; the first build "
                   "takes a few minutes.", "Build & install"):
                self.win.go("Extras")
                ex = next(p for p in self.win.page_list if isinstance(p, ExtrasPage))
                QTimer.singleShot(200, ex.build_install)
            return
        self.status.set("Theme applied. The TV screen is shown on the Remote page; press Home on the remote if the "
                        "old look is still there.", "ok")

    def reset(self):
        if not self.need_tv():
            return
        self._busy(True)
        run_job(reset_theme, on_result=lambda s: (self.win.settings.setValue(f"theme_applied/{TV.host}", ""),
                                                  BUS.shot.emit(s), self.status.set(
            "Theme removed: the launcher is back to its built-in look.", "ok")),
                on_error=lambda m: self.status.set(f"Reset failed: {m}", "bad"), on_done=lambda: self._busy(False))

    def _busy(self, on):
        for b in (self.apply_btn, self.reset_btn, self.my_apply):
            b.setEnabled(not on)
        if not on and not self.selected:
            self.apply_btn.setEnabled(False)

    # --- my theme -----------------------------------------------------------------------------
    def _load_my_theme(self):
        cfg = MY_THEME / "config.json"
        base = {}
        if cfg.is_file():
            try:
                base = json.loads(cfg.read_text(encoding="utf-8"))
            except ValueError:
                base = {}
        else:
            d = REPO / "themes" / "default" / "config.json"
            try:
                base = json.loads(d.read_text(encoding="utf-8")) if d.is_file() else {}
            except ValueError:
                base = {}
            base.pop("hidden_apps", None)
        self._fill(base, MY_THEME / "wallpaper.jpg")

    def _fill(self, cfg, wall_path=None):
        self.base = dict(cfg)
        self.dock.clear()
        for p in cfg.get("dock_apps", []):
            self.dock.addItem(p)
        self.columns.setValue(int(cfg.get("columns", 4) or 4))
        self.rows.setValue(int(cfg.get("rows_below_dock", 0) or 0))
        self._set_bg(cfg.get("background_color", "#000000"))
        self.dim.setValue(int(cfg.get("wallpaper_dim", 0) or 0))
        self.opacity.setValue(int(cfg.get("dock_opacity", 100) or 100))
        self.greet.setText(cfg.get("greeting_name", "") or "")
        self.clock.setValue(int(cfg.get("home_idle_clock_minutes", 0) or 0))
        for k, cb in self.switches.items():
            cb.setChecked(bool(cfg.get(k, False)))
        live_pkg, _defaults = launcher_hidden_defaults()
        in_theme = isinstance(cfg.get("hidden_apps"), list)
        self.live_tile.setChecked(bool(live_pkg) and (live_pkg not in cfg["hidden_apps"] if in_theme
                                                      else self.win.settings.value("live_tile", "") == "1"))
        self.wall_src = None
        if wall_path and Path(wall_path).is_file() and cfg.get("wallpaper", False):
            self.wall_src = str(wall_path)
            self.wall_view.set_path(str(wall_path))
        else:
            self.wall_view.pix = None
            self.wall_view.update()

    def _set_bg(self, color):
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(color)):
            color = "#000000"
        self.bg.setText(color.upper())
        q = QColor(color)
        fg = "#000" if q.lightness() > 140 else "#fff"
        self.bg.setStyleSheet(f"background: {color}; color: {fg}; border: 1px solid {C['line2']};")

    def pick_color(self):
        from PyQt6.QtWidgets import QColorDialog
        c = QColorDialog.getColor(QColor(self.bg.text()), self, "Background colour")
        if c.isValid():
            self._set_bg(c.name())

    def choose_wall(self):
        f, _ = QFileDialog.getOpenFileName(self, "Wallpaper", str(Path.home() / "Pictures"),
                                           "Images (*.jpg *.jpeg *.png *.webp *.bmp)")
        if f:
            self.wall_src = f
            self.wall_view.set_path(f)

    def clear_wall(self):
        self.wall_src = ""
        self.wall_view.pix = None
        self.wall_view.update()

    def start_from_selected(self):
        if not self.selected:
            inform(self, "Pick a theme", "Click a theme above first, then load it here to change it.", "info")
            return
        try:
            cfg = json.loads((self.selected["path"] / "config.json").read_text(encoding="utf-8"))
        except ValueError as e:
            inform(self, "Broken theme", str(e), "bad")
            return
        cfg.pop("hidden_apps", None)   # another person's TV; your hidden apps differ
        self._fill(cfg, self.selected["path"] / "wallpaper.jpg")
        self._copy_walls = self.selected["path"] / "wallpapers"
        self.my_msg.set(f"Loaded <b>{self.selected['name']}</b>. Change what you like, then Save & apply.", "info")

    def add_app(self):
        p = self.app_pick.currentText().strip()
        if not PACKAGE_RE.fullmatch(p):
            return
        if p not in [self.dock.item(i).text() for i in range(self.dock.count())]:
            self.dock.addItem(p)

    def _collect(self):
        cfg = dict(self.base)
        cfg["dock_apps"] = [self.dock.item(i).text() for i in range(self.dock.count())]
        cfg["columns"] = self.columns.value()
        cfg["rows_below_dock"] = self.rows.value()
        cfg["background_color"] = self.bg.text()
        for key, val, default in [("wallpaper_dim", self.dim.value(), 0), ("dock_opacity", self.opacity.value(), 100),
                                  ("home_idle_clock_minutes", self.clock.value(), 0)]:
            if val != default or key in cfg:
                cfg[key] = val
        name = self.greet.text().strip()
        if name or "greeting_name" in cfg:
            cfg["greeting_name"] = name
        for k, cb in self.switches.items():
            if cb.isChecked() or k in cfg:
                cfg[k] = cb.isChecked()
        cfg["wallpaper"] = bool(self.wall_src)
        if cfg.get("live_tv_row"):
            cfg["live_tv_row_position"] = self.win.settings.value("live_pos", "top")
        live_pkg, defaults = launcher_hidden_defaults()
        if live_pkg:
            if self.live_tile.isChecked():
                # The launcher's own hidden apps, minus the Live TV app, and the tile named and drawn as Live TV.
                cfg["hidden_apps"] = [p for p in cfg.get("hidden_apps", defaults) if p != live_pkg]
                own = config_xml_arrays()
                cfg["app_labels"], cfg["app_banners"] = live_tile_extras(
                    live_pkg, cfg.get("app_labels", own.get("app_labels", [])),
                    cfg.get("app_banners", own.get("app_banners", [])),
                    live_banner(self.win.settings.value("live_icon", "blue")))
            elif "hidden_apps" in cfg and live_pkg not in cfg["hidden_apps"]:
                cfg["hidden_apps"] = list(cfg["hidden_apps"]) + [live_pkg]
                for k in ("app_labels", "app_banners"):
                    if isinstance(cfg.get(k), list):
                        cfg[k] = [x for x in cfg[k] if not str(x).startswith(live_pkg + "=")]
        return cfg

    def _mirror(self, key, on):
        self.win.settings.setValue(key, "1" if on else "0")
        ex = next((p for p in self.win.page_list if isinstance(p, ExtrasPage)), None)
        if ex is not None:
            cb = ex.live_tile_b if key == "live_tile" else ex.live_row_b
            if cb.isChecked() != on:
                cb.setChecked(on)

    def edit_json(self):
        d = Dialog(self, "My theme – config.json", 700)
        d.lay.addWidget(label("Every key is documented in themes/README.md in the toolkit. Changes here replace "
                              "the form.", "Muted", wrap=True))
        box = QPlainTextEdit(json.dumps(self._collect(), indent=2, ensure_ascii=False))
        box.setObjectName("Box")
        box.setMinimumHeight(380)
        d.lay.addWidget(box)
        d.buttons("Use this", "Cancel")
        if d.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            cfg = json.loads(box.toPlainText())
            if not isinstance(cfg, dict):
                raise ValueError("the top level must be an object { … }")
        except ValueError as e:
            inform(self, "Not valid JSON", str(e), "bad")
            return
        keep = self.wall_src
        self._fill(cfg)
        self.wall_src = keep if cfg.get("wallpaper") else ""

    def save_apply(self):
        cfg = self._collect()
        MY_THEME.mkdir(parents=True, exist_ok=True)
        wall = MY_THEME / "wallpaper.jpg"
        try:
            if self.wall_src and Path(self.wall_src).resolve() != wall.resolve():
                save_wallpaper(self.wall_src, wall)
            elif self.wall_src == "" and wall.exists():
                wall.unlink()
            src_walls = getattr(self, "_copy_walls", None)
            dst_walls = MY_THEME / "wallpapers"
            if src_walls is not None:
                shutil.rmtree(dst_walls, ignore_errors=True)
                if src_walls.is_dir():
                    shutil.copytree(src_walls, dst_walls)
                self._copy_walls = None
        except Exception as e:
            self.my_msg.set(f"Could not prepare the wallpaper: {e}", "bad")
            return
        (MY_THEME / "config.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        self.base = cfg
        self.my_msg.set(f"Saved to {MY_THEME}.", "ok")
        name = ask_name(self, "Keep it as a theme?",
                        f"My theme is saved. Keep a copy under a name of its own in <b>{USER_THEMES}</b>, so it stays "
                        "in the gallery after you change My theme again?",
                        self.win.settings.value("my_theme_name", ""), "Keep a copy", "Not now")
        if name:
            safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", name).strip("-.") or "my-theme-copy"
            dest = USER_THEMES / safe
            if safe == MY_THEME.name or not dest.exists() or ask(
                    self, "Replace theme?", f"A theme called <b>{safe}</b> exists. Replace it?", "Replace"):
                if dest != MY_THEME:
                    shutil.rmtree(dest, ignore_errors=True)
                    shutil.copytree(MY_THEME, dest)
                self.win.settings.setValue("my_theme_name", name)
                self.my_msg.set(f"Saved to {MY_THEME} and kept as <b>{safe}</b> in {USER_THEMES}.", "ok")
        self.fill_gallery(select=safe if name else None)
        if TV.connected:
            self.apply(MY_THEME)


# ----------------------------------------------------------------------------------------------
# Profiles: a TV's whole setup in one .cytv file (packages, theme, settings), to apply again later
# ----------------------------------------------------------------------------------------------
PROFILE_DIR = cyt_home() / "profile"
PROFILE_CACHE = APPDATA / "profile-cache"
PROFILE_VERSION = 1
PROFILE_SETTINGS = [
    ("dns", "global", "private_dns_mode"), ("dns", "global", "private_dns_specifier"),
    ("anim", "global", "window_animation_scale"), ("anim", "global", "transition_animation_scale"),
    ("anim", "global", "animator_duration_scale"),
    ("dream", "secure", "screensaver_components"), ("dream", "secure", "screensaver_enabled"),
    ("dream", "secure", "screensaver_activate_on_sleep"), ("dream", "system", "screen_off_timeout"),
]
# Every value goes into a shell command on the TV, so only plain characters get through.
SETTING_VALUE_RE = re.compile(r"[A-Za-z0-9_.,:/\-]+")
THEME_FILE_RE = re.compile(r"(config\.json|wallpaper\.jpg|wallpapers/[A-Za-z0-9_.-]+)")


def _safe_name(name):
    return re.sub(r"[^\w\- .()]+", "_", name, flags=re.UNICODE).strip(" .") or "profile"


def save_profile(name, theme_folder):
    """Read the TV and write <name>.cytv (a zip: profile.json + theme/)."""
    import zipfile
    info = TV.info or {}
    disabled = sorted(n for n in TV.packages("-d") if not is_core(n))
    settings = {}
    for _group, ns, key in PROFILE_SETTINGS:
        settings[f"{ns}/{key}"] = TV.sh(f"settings get {ns} {key}", quiet=True).strip()
    home, _ = TV.home_owner()
    prof = {
        "format": "cleanyourtv-profile", "version": PROFILE_VERSION, "name": name,
        "created": time.strftime("%Y-%m-%d %H:%M"), "app_version": APP_VERSION,
        "tv": {"model": info.get("model"), "device": info.get("device"), "manufacturer": info.get("manufacturer"),
               "android": info.get("release"), "sdk": info.get("sdk"), "board": info.get("board"),
               "platform": info.get("platform"), "hardware": info.get("hardware"), "brand": info.get("brand"),
               "build": info.get("build")},
        "disabled_packages": disabled, "settings": settings,
        "launcher": {"installed": launcher_installed(), "home": home},
        "theme": None,
    }
    files = {}
    folder = Path(theme_folder) if theme_folder else None
    if folder and (folder / "config.json").is_file():
        files["config.json"] = folder / "config.json"
        if (folder / "wallpaper.jpg").is_file():
            files["wallpaper.jpg"] = folder / "wallpaper.jpg"
        walls = folder / "wallpapers"
        if walls.is_dir():
            for f in sorted(walls.iterdir()):
                if f.is_file() and WALL_NAME_RE.match(f.name):
                    files[f"wallpapers/{f.name}"] = f
        prof["theme"] = {"from": folder.name, "files": sorted(files)}
    elif prof["launcher"]["installed"]:
        # No record of what was applied from here: take what the launcher holds now, wallpaper included.
        text = TV.sh(f"content read --uri {THEME_URI}/config.json 2>/dev/null", quiet=True)
        try:
            json.loads(text)
            prof["theme"] = {"from": "read from the TV", "files": ["config.json"], "config_text": text}
        except ValueError:
            text = None
        if text is not None:
            pulled = _pull_theme_file("wallpaper.jpg")
            if pulled:
                tmpdir = PROFILE_CACHE / "_pulled"
                tmpdir.mkdir(parents=True, exist_ok=True)
                (tmpdir / "wallpaper.jpg").write_bytes(pulled)
                files["wallpaper.jpg"] = tmpdir / "wallpaper.jpg"
                prof["theme"]["files"].append("wallpaper.jpg")
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    dest = PROFILE_DIR / f"{_safe_name(name)}.cytv"
    tmp = dest.with_suffix(".cytv.tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        text = (prof["theme"] or {}).pop("config_text", None) if prof["theme"] else None
        z.writestr("profile.json", json.dumps(prof, indent=2, ensure_ascii=False))
        if text is not None:
            z.writestr("theme/config.json", text)
        for rel, src in files.items():
            z.write(src, f"theme/{rel}")
    os.replace(tmp, dest)
    log(f"profile saved: {dest} ({len(disabled)} disabled packages)", "ok")
    return dest


def _pull_theme_file(name):
    """A theme file's bytes from the TV, through base64 so the text-only shell can carry it; None if absent."""
    import base64
    import hashlib
    for src in (f"content read --uri {THEME_URI}/{name} 2>/dev/null", f"cat {THEME_DIR}/{name} 2>/dev/null"):
        out = TV.sh(f"{src} | base64 | tr -d '\\n'; echo; {src} | md5sum", quiet=True, timeout=180).strip().splitlines()
        if len(out) < 2:
            continue
        try:
            data = base64.b64decode(out[0].strip(), validate=False)
        except Exception:
            continue
        if data and hashlib.md5(data).hexdigest() == out[-1].split()[0]:
            return data
    return None


def read_profile(path):
    """Unpack a .cytv into the cache and return (profile dict, theme folder or None)."""
    import zipfile
    path = Path(path)
    out = PROFILE_CACHE / _safe_name(path.stem)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "profile.json" not in names:
            raise RuntimeError("not a CleanYourTV profile (no profile.json inside)")
        prof = json.loads(z.read("profile.json").decode("utf-8"))
        if prof.get("format") != "cleanyourtv-profile":
            raise RuntimeError("not a CleanYourTV profile")
        for n in names:
            if n.startswith("theme/") and THEME_FILE_RE.fullmatch(n[len("theme/"):]):
                target = out / n
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(n))
    pk = [p for p in prof.get("disabled_packages", []) if isinstance(p, str) and PACKAGE_RE.fullmatch(p)
          and not is_core(p)]
    prof["disabled_packages"] = pk
    theme = out / "theme"
    return prof, (theme if (theme / "config.json").is_file() else None)


# A profile bundle: <name>.zip = profile.cytv + apps/*.apk|*.apks + bundle.json (what is inside, and the launcher
# switches for that model), so a second box of the same kind is set up from one file.
BUNDLE_APP_RE = re.compile(r"apps/[A-Za-z0-9_.()+-]+\.apks?")


def read_bundle(path):
    """(bundle.json, profile dict) of a bundle, without unpacking it."""
    import zipfile
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "bundle.json" not in names or "profile.cytv" not in names:
            raise RuntimeError("not a CleanYourTV profile bundle (bundle.json and profile.cytv)")
        meta = json.loads(z.read("bundle.json").decode("utf-8"))
        with zipfile.ZipFile(io.BytesIO(z.read("profile.cytv"))) as inner:
            prof = json.loads(inner.read("profile.json").decode("utf-8"))
    meta["apps"] = [a for a in meta.get("apps", []) if BUNDLE_APP_RE.fullmatch("apps/" + str(a))]
    return meta, prof


def make_bundle(cytv, apps, dest, extras=None):
    """Writes <dest>.zip from a .cytv, the app files and the launcher switches."""
    import zipfile
    dest = Path(dest)
    tmp = dest.with_suffix(".zip.part")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_STORED) as z:   # .apk files are compressed already
        z.write(cytv, "profile.cytv")
        names = []
        for f in apps:
            f = Path(f)
            if BUNDLE_APP_RE.fullmatch("apps/" + f.name):
                z.write(f, "apps/" + f.name)
                names.append(f.name)
        z.writestr("bundle.json", json.dumps({
            "format": "cleanyourtv-bundle", "app": f"{APP_NAME} {APP_VERSION}",
            "created": time.strftime("%Y-%m-%d %H:%M"), "apps": names, "extras": extras or {}}, indent=2))
    tmp.replace(dest)
    return dest


def unpack_bundle(path, out):
    """profile.cytv and the app files into out; returns (cytv path, app files)."""
    import zipfile
    out = Path(out)
    shutil.rmtree(out, ignore_errors=True)
    (out / "apps").mkdir(parents=True, exist_ok=True)
    apps = []
    with zipfile.ZipFile(path) as z:
        (out / "profile.cytv").write_bytes(z.read("profile.cytv"))
        for n in z.namelist():
            if BUNDLE_APP_RE.fullmatch(n):
                t = out / n
                t.write_bytes(z.read(n))
                apps.append(t)
    return out / "profile.cytv", apps


def install_bundle_apps(files, sig=None):
    """Installs each app of a bundle on its own, so one that the TV refuses does not stop the others."""
    results = []
    for i, f in enumerate(files):
        if sig:
            sig.step.emit(i, len(files), Path(f).name)
        try:
            install_apks([str(f)])
            results.append((Path(f).name, ""))
        except Exception as e:
            results.append((Path(f).name, str(e)))
    if sig:
        sig.step.emit(len(files), len(files), "")
    return results


def apply_profile_settings(prof, groups):
    """Put the profile's settings back, for the groups the user ticked (dns, anim, dream)."""
    done = []
    has_launcher = launcher_installed()
    remember_settings([f"{ns}/{key}" for group, ns, key in PROFILE_SETTINGS if group in groups])
    for group, ns, key in PROFILE_SETTINGS:
        if group not in groups:
            continue
        value = str(prof.get("settings", {}).get(f"{ns}/{key}", "")).strip()
        if key == "screensaver_components" and OUR_LAUNCHER in value and not has_launcher:
            log("skipping the clock screensaver: the CleanYourTV launcher is not installed", "warn")
            continue
        if value in ("", "null"):
            TV.sh(f"settings delete {ns} {key}")
        elif SETTING_VALUE_RE.fullmatch(value):
            TV.sh(f"settings put {ns} {key} {value}")
        else:
            log(f"skipping {key}: unexpected value {value!r}", "warn")
            continue
        done.append(key)
    return done


class ProfileApplyDialog(Dialog):
    def __init__(self, parent, prof, theme, installed, disabled_now, has_launcher):
        super().__init__(parent, f"Apply profile “{prof.get('name')}”", 620)
        tv = prof.get("tv", {})
        self.lay.addWidget(label(f"Saved {prof.get('created')} from {tv.get('model') or 'a TV'} "
                                 f"(Android {tv.get('android') or '?'}).", "Muted"))
        if TV.info and tv.get("model") and tv.get("model") != TV.info.get("model"):
            self.lay.addWidget(Banner(f"This profile comes from a different model (<b>{tv.get('model')}</b>, this TV "
                                      f"is <b>{TV.info.get('model')}</b>). Package names can differ; the app skips "
                                      "what isn't installed and still runs every safety check.", "warn"))
        pk = prof.get("disabled_packages", [])
        todo = [p for p in pk if p in installed and p not in disabled_now]
        self.todo = todo
        s = prof.get("settings", {})
        self.checks = {}

        def add(key, text, enabled=True, tip=""):
            cb = Toggle(text)
            cb.setChecked(enabled)
            cb.setEnabled(enabled)
            cb.setToolTip(tip)
            self.checks[key] = cb
            self.lay.addWidget(cb)

        add("packages", f"Packages: disable {len(todo)}  ({len(pk) - len(todo)} already off or not on this TV)",
            bool(todo), "Goes through the Debloat page: same checks, batches and screenshots")
        if theme:
            tfiles = (prof.get("theme") or {}).get("files", [])
            walls = sum(1 for f in tfiles if f.startswith("wallpaper"))
            add("theme", f"Theme: {(prof.get('theme') or {}).get('from', 'saved theme')}"
                         + (f" with {walls} wallpaper{'s' if walls != 1 else ''}" if walls else ""),
                has_launcher, "" if has_launcher else "Install the launcher first (Extras → Build & install)")
            if not has_launcher:
                self.lay.addWidget(label("    The theme needs the CleanYourTV launcher: install it on the Extras page, "
                                         "then apply the profile again.", "Dim", wrap=True))
        dns = s.get("global/private_dns_mode", "")
        add("dns", "Private DNS: " + (s.get("global/private_dns_specifier", "") if dns == "hostname"
                                      else "automatic"))
        add("anim", f"Animations: {s.get('global/window_animation_scale') or '1.0'}×".replace("null×", "1×"))
        dream = s.get("secure/screensaver_components", "")
        add("dream", "Screensaver: " + ("CleanYourTV clock" if OUR_LAUNCHER in dream else "the TV's own")
            + (f", after {int(s.get('system/screen_off_timeout')) // 60000} min"
               if str(s.get("system/screen_off_timeout", "")).isdigit() else ""))
        self.buttons("Apply")

    def chosen(self):
        return {k for k, cb in self.checks.items() if cb.isChecked() and cb.isEnabled()}



TILE_ADDED = "<!--cyt-live-tile-->"       # after an item this app added
TILE_OFF = ("<!--cyt-live-tile ", " -->")  # around a hidden_apps item this app took out


# The Live TV tile's artwork: (setting, label, launcher drawable; "" keeps the TV app's own banner).
LIVE_ICONS = [("blue", "Blue, like the stock launcher", "banner_tv_blue"),
              ("own", "The Live TV app's own icon", ""),
              ("magenta", "Magenta", "banner_tv")]
# Where the channels row sits (live_tv_row_position).
LIVE_POSITIONS = [("top", "Top, above the apps"), ("bottom", "Bottom, after the apps")]


def live_banner(icon):
    return next((d for k, _, d in LIVE_ICONS if k == icon), "banner_tv_blue")


def live_tile_extras(pkg, labels=(), banners=(), banner="banner_tv_blue"):
    """app_labels and app_banners with the Live TV app named "Live TV" and drawn with banner (a launcher drawable;
    "" leaves the app's own artwork)."""
    labels = [x for x in labels if not x.startswith(pkg + "=")] + [f"{pkg}=Live TV"]
    banners = [x for x in banners if not x.startswith(pkg + "=")] + ([f"{pkg}={banner}"] if banner else [])
    return labels, banners


def config_xml_arrays():
    """{array name: [items]} for hidden_apps, app_labels and app_banners in the toolkit's config.xml (comments,
    such as an item this app took out, do not count)."""
    try:
        xml = (LAUNCHER / "app" / "src" / "main" / "res" / "values" / "config.xml").read_text(encoding="utf-8")
    except OSError:
        return {}
    xml = re.sub(r"<!--.*?-->", "", xml, flags=re.S)
    out = {}
    for name in ("hidden_apps", "app_labels", "app_banners"):
        m = re.search(rf'<string-array name="{name}"[^>]*>(.*?)</string-array>', xml, re.S)
        out[name] = [i.strip() for i in re.findall(r"<item>(.*?)</item>", m.group(1))] if m else []
    return out


def apply_live_tile(launcher, pkg, on, banner="banner_tv_blue"):
    """Shows (on) the Live TV app as a tile, named "Live TV" with the launcher's TV banner, in the launcher's own
    config.xml, so the build itself carries it; off puts back exactly what this app changed. Returns a short note,
    or "" when the file did not change."""
    path = Path(launcher) / "app" / "src" / "main" / "res" / "values" / "config.xml"
    if not pkg or not PACKAGE_RE.fullmatch(pkg):
        return ""
    t = orig = _read_raw(path)
    nl = "\r\n" if "\r\n" in t else "\n"
    # Start from the toolkit's own file: drop the items this app added, un-comment the one it took out.
    t = re.sub(rf"\r?\n[ \t]*<item>[^<]*</item>[ \t]*{re.escape(TILE_ADDED)}", "", t)
    t = re.sub(rf"{re.escape(TILE_OFF[0])}(<item>[^<]*</item>){re.escape(TILE_OFF[1])}", r"\1", t)
    if on:
        m = re.search(r'<string-array name="hidden_apps"[^>]*>(.*?)</string-array>', t, re.S)
        item = f"<item>{pkg}</item>"
        if m and item in m.group(1):
            body = m.group(1).replace(item, TILE_OFF[0] + item + TILE_OFF[1], 1)
            t = t[:m.start(1)] + body + t[m.end(1):]
        for name, val in (("app_labels", f"{pkg}=Live TV"), ("app_banners", f"{pkg}={banner}" if banner else "")):
            if not val:
                continue
            m = re.search(rf'<string-array name="{name}"[^>]*>(.*?)</string-array>', t, re.S)
            if m and f"<item>{pkg}=" not in re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S):
                t = t[:m.start(1)] + f"{nl}        <item>{val}</item> {TILE_ADDED}" + t[m.start(1):]
    if t == orig:
        return ""
    path.write_text(t, encoding="utf-8", newline="")
    return "shown as a tile, named Live TV" if on else "hidden again, as the launcher ships"


TV_KEY_ADDED = "<!--cyt-tv-key-->"


def apply_tv_key(launcher, pkg, on):
    """The remote's TV button opens the Live TV app (pkg): a KEYCODE_TV entry in config.xml's app_keys, which
    InputKeyService and HomeKeyService check before anything else. Off takes back only the entry this app added.
    Returns True when the file changed."""
    path = Path(launcher) / "app" / "src" / "main" / "res" / "values" / "config.xml"
    t = orig = _read_raw(path)
    nl = "\r\n" if "\r\n" in t else "\n"
    t = re.sub(rf"\r?\n[ \t]*<item>[^<]*</item>[ \t]*{re.escape(TV_KEY_ADDED)}", "", t)
    if on and pkg and PACKAGE_RE.fullmatch(pkg):
        m = re.search(r'<string-array name="app_keys"[^>]*>(.*?)</string-array>', t, re.S)
        own = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S) if m else ""
        # The person's own TV-button entry wins.
        if m and not re.search(r"<item>\s*(KEYCODE_TV|170):", own):
            t = t[:m.start(1)] + f"{nl}        <item>KEYCODE_TV:{pkg}</item> {TV_KEY_ADDED}" + t[m.start(1):]
    if t == orig:
        return False
    path.write_text(t, encoding="utf-8", newline="")
    return True


def set_config_string(launcher, name, value):
    """Sets <string name="name"> in the launcher's config.xml; True when the file changed."""
    path = Path(launcher) / "app" / "src" / "main" / "res" / "values" / "config.xml"
    t = _read_raw(path)
    new = re.sub(rf'(<string name="{name}"[^>]*>)[^<]*(</string>)', lambda m: m.group(1) + value + m.group(2), t, count=1)
    if new == t:
        return False
    path.write_text(new, encoding="utf-8", newline="")
    return True


def set_config_bool(launcher, name, value):
    """Sets <bool name="name"> in the launcher's config.xml; True when the file changed."""
    path = Path(launcher) / "app" / "src" / "main" / "res" / "values" / "config.xml"
    t = _read_raw(path)
    new = re.sub(rf'(<bool name="{name}">)\s*(true|false)\s*(</bool>)', rf"\g<1>{'true' if value else 'false'}\3",
                 t, count=1)
    if new == t:
        return False
    path.write_text(new, encoding="utf-8", newline="")
    return True


def sync_live_on_tv(row, tile, pkg, banner="banner_tv_blue", position="top", switches=None, tv_key=None):
    """Makes the theme already on the TV agree with the Live TV switches: a theme pushed earlier can switch the
    row off or hide the Live TV app, and it wins over the launcher's own config.xml. Only those keys change.
    Returns notes for the log."""
    notes = []
    raw = TV.sh(f"content read --uri {THEME_URI}/config.json 2>/dev/null", quiet=True)
    try:
        cfg = json.loads(raw) if raw.strip().startswith("{") else None
    except ValueError:
        cfg = None
    if isinstance(cfg, dict):
        changed = False
        if "live_tv_row" in cfg and cfg["live_tv_row"] != row:
            cfg["live_tv_row"] = row
            changed = True
        if "live_tv_row_position" in cfg and cfg["live_tv_row_position"] != position:
            cfg["live_tv_row_position"] = position
            changed = True
        if tv_key is not None and isinstance(cfg.get("app_keys"), list):
            ours = f"KEYCODE_TV:{pkg}"
            has_tv = any(str(k).startswith(("KEYCODE_TV:", "170:")) for k in cfg["app_keys"])
            if tv_key:
                want = cfg["app_keys"] + ([] if has_tv or not pkg else [ours])   # a TV entry of their own wins
            else:
                want = [k for k in cfg["app_keys"] if k != ours]
            if want != cfg["app_keys"]:
                cfg["app_keys"] = want
                changed = True
        for k, v in (switches or {}).items():   # other switches the build set, when the theme overrides them
            if k in cfg and cfg[k] != v:
                cfg[k] = v
                changed = True
        if pkg and isinstance(cfg.get("hidden_apps"), list):
            hidden = [x for x in cfg["hidden_apps"] if x != pkg] + ([] if tile else [pkg])
            if hidden != cfg["hidden_apps"]:
                cfg["hidden_apps"] = hidden
                changed = True
        if pkg and tile:
            own = config_xml_arrays()
            labels, banners = live_tile_extras(pkg, cfg.get("app_labels", own.get("app_labels", [])),
                                               cfg.get("app_banners", own.get("app_banners", [])), banner)
            if cfg.get("app_labels") != labels or cfg.get("app_banners") != banners:
                cfg["app_labels"], cfg["app_banners"] = labels, banners
                changed = True
        if changed:
            DATA.mkdir(parents=True, exist_ok=True)
            local = DATA / "tv-theme-config.json"
            local.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
            push_file(local, _stage("config.json"))
            TV.sh(_put("config.json"), quiet=True)
            _revision_and_restart()
            notes.append("the theme on the TV is updated to match (row " + ("on" if row else "off") + ", app " +
                         ("shown" if tile else "hidden") + "), Home restarted")
    if pkg and tile:
        entry = TV.sh("cmd package query-activities --brief -a android.intent.action.MAIN -c "
                      f"android.intent.category.LEANBACK_LAUNCHER | grep -c '^{pkg}/'", quiet=True).strip()
        if entry == "0":
            notes.append(f"{pkg} has no TV app icon of its own, so Android offers no tile for it; it stays under "
                         "Inputs → Live TV")
    return notes


def launcher_hidden_defaults():
    """(Live TV package, hidden_apps): the connected TV's own Live TV app when one was found (TV.info), else
    config.xml's live_tv_package; hidden_apps from config.xml. ("", []) when config.xml is unreadable."""
    try:
        xml = (LAUNCHER / "app" / "src" / "main" / "res" / "values" / "config.xml").read_text(encoding="utf-8")
    except OSError:
        return "", []
    live = re.search(r'<string name="live_tv_package"[^>]*>\s*([A-Za-z0-9_.]*)\s*</string>', xml)
    found = (TV.info or {}).get("live_tv_app") if TV.connected else ""
    xml = re.sub(r"<!--.*?-->", "", xml, flags=re.S)
    block = re.search(r'<string-array name="hidden_apps"[^>]*>(.*?)</string-array>', xml, re.S)
    hidden = re.findall(r"<item>\s*([A-Za-z0-9_.]+)\s*</item>", block.group(1)) if block else []
    return found or (live.group(1) if live else ""), hidden


def save_wallpaper(src, dest):
    """Crop to 16:9, scale to 1920×1080 and save as a JPEG under about 300 KB (themes/README.md)."""
    img = QImage(str(src))
    if img.isNull():
        raise RuntimeError("that file is not a picture this app can read")
    w, h = img.width(), img.height()
    if w / h > 16 / 9:
        nw = int(h * 16 / 9)
        img = img.copy((w - nw) // 2, 0, nw, h)
    else:
        nh = int(w * 9 / 16)
        img = img.copy(0, (h - nh) // 2, w, nh)
    img = img.scaled(1920, 1080, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
    for q in (88, 80, 72, 64, 56, 48):
        img.save(str(dest), "JPG", q)
        if dest.stat().st_size <= 300_000:
            break


def recorded_home(host):
    """The Home component an undo record found on this TV before anything changed, if it was not ours."""
    if not DATA.is_dir():
        return ""
    for p in sorted(DATA.glob("recovery-*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            rec = json.loads(p.read_text())
        except Exception:
            continue
        home = rec.get("home") or ""
        if rec.get("host", "").split(":")[0] == host and COMPONENT_RE.match(home) \
                and not home.startswith(OUR_LAUNCHER + "/"):
            return home
    return ""


def remove_new_launcher(stock_hint, dream_prev=""):
    """Gives Home back to the stock launcher, then uninstalls com.gathin.tvhome (the one app this tool installed).

    The debloat is left exactly as it is. Nothing is uninstalled until the stock launcher is enabled, set as Home
    and confirmed as Home, so the TV is never left without a Home screen. Returns a list of what was done.
    """
    done = []
    if OUR_LAUNCHER not in TV.packages():
        raise RuntimeError("The new launcher is not installed on this TV, so there is nothing to remove.")
    installed = TV.packages()
    # Which launcher to bring back: the Home the undo record saw, then the one picked on this page, then the
    # known stock launchers that are on this TV (CVTE boards keep theirs enabled all along, #741).
    cands = []
    rec = recorded_home(TV.host)
    if rec:
        cands.append(rec.split("/", 1)[0])
    if stock_hint and PACKAGE_RE.fullmatch(stock_hint):
        cands.append(stock_hint)
    cands += KNOWN_STOCK + sorted(n for n in installed if n.startswith("com.cvte.tv.launcher"))
    cands = [c for i, c in enumerate(cands) if c in installed and c != OUR_LAUNCHER and c not in cands[:i]]
    if not cands:
        raise RuntimeError("No stock launcher was found on this TV, so the new launcher stays: without it the TV "
                           "would have no Home screen. Type the stock launcher's package in 'Stock launcher' and "
                           "try again.")
    stock = comp = ""
    for c in cands:
        TV.sh(f"pm enable --user 0 {c}")
        lines = [l.strip() for l in TV.sh(f"{HOME_QUERY} {c}", quiet=True).splitlines() if l.strip()]
        found = rec if rec and rec.startswith(c + "/") else (lines[-1] if lines else "")
        if COMPONENT_RE.match(found) and found.startswith(c + "/"):
            stock, comp = c, found
            break
    if not comp:
        raise RuntimeError(f"None of these answer as a Home screen: {', '.join(cands)}. The new launcher stays.")
    done.append(f"{stock} enabled")
    TV.sh(f"cmd package set-home-activity --user 0 {comp}")
    TV.sh("input keyevent KEYCODE_HOME", quiet=True)
    time.sleep(0 if DEMO else 2.5)
    owner, _ = TV.home_owner()
    if owner != stock:
        raise RuntimeError(f"Home did not move to {stock} (it is {owner or 'nothing'}), so the new launcher was "
                           f"left installed. Nothing else was changed apart from {stock} being enabled.")
    done.append(f"Home is {stock} again")
    # Settings that point at the launcher would point at nothing once it is gone.
    dream = TV.sh("settings get secure screensaver_components", quiet=True).strip()
    if OUR_LAUNCHER in dream:
        if dream_prev and dream_prev != "null" and OUR_LAUNCHER not in dream_prev \
                and all(COMPONENT_RE.match(x) for x in dream_prev.split(",")):
            TV.sh(f"settings put secure screensaver_components {dream_prev}")
        else:
            TV.sh("settings delete secure screensaver_components")
        done.append("screensaver back to the TV's own")
    acc = TV.sh("settings get secure enabled_accessibility_services", quiet=True).strip()
    if OUR_LAUNCHER in acc:
        keep = [a for a in acc.split(":") if a and a != "null" and not a.startswith(OUR_LAUNCHER + "/")]
        if keep and all(COMPONENT_RE.match(a) for a in keep):
            TV.sh(f"settings put secure enabled_accessibility_services {':'.join(keep)}")
        else:
            TV.sh("settings put secure enabled_accessibility_services ''")
            TV.sh("settings put secure accessibility_enabled 0")
        done.append("remote-key helpers switched off")
    TV.sh(f"am force-stop {OUR_LAUNCHER}")
    out = TV.sh(f"pm uninstall {OUR_LAUNCHER}")
    if "Success" not in out or OUR_LAUNCHER in TV.packages():
        raise RuntimeError(f"Home is {stock} again, but uninstalling the new launcher failed: {out.strip()[:200]}")
    done.append("new launcher uninstalled")
    TV.sh("input keyevent KEYCODE_HOME", quiet=True)
    return stock, done


class FinishPage(Page):
    title = "Finish"
    subtitle = "Check what stuck, undo if needed, and close network ADB"

    def __init__(self, win):
        super().__init__(win)
        # Reboot & verify
        c, lay = card()
        lay.addWidget(label("1 · Reboot once and check", "H2"))
        lay.addWidget(label("Some firmware re-enables packages at every boot from its own list (TCL Android 9 "
                            "does this for its user centre). Reboot once and compare: those are noted, not fought.",
                            "Muted", wrap=True))
        self.reboot = button("Reboot & compare", "Primary", "refresh")
        lay.addWidget(hbox(self.reboot, None))
        self.reboot_msg = Banner("")
        lay.addWidget(self.reboot_msg)
        self.body.addWidget(c)

        # Restore
        c, lay = card()
        lay.addWidget(label("Undo: restore", "H2"))
        lay.addWidget(label("Puts the TV back the way the undo record found it: packages that were already "
                            "disabled before stay disabled, Home and the animation scales go back to their recorded "
                            "values. Uses tools/recovery.py.", "Muted", wrap=True))
        self.list_path = QLineEdit()
        self.list_path.setPlaceholderText("The app's own list for this TV is used by default")
        pick = button("Other list…", None, "folder", "A list you used with tools/disable.ps1 or disable.sh")
        pick.clicked.connect(self.pick_list)
        lay.addWidget(hbox(self.list_path, pick))
        self.stock = QComboBox()
        self.stock.setEditable(True)
        self.stock.addItems(KNOWN_STOCK)
        self.stock.setToolTip("The stock launcher to bring back if Home has nothing recorded")
        self.restore = button("Preview & restore", "Danger", "undo")
        lay.addWidget(hbox(label("Stock launcher", "Muted"), self.stock, None, self.restore))
        self.restore_msg = Banner("")
        lay.addWidget(self.restore_msg)
        self.body.addWidget(c)

        # Remove the new launcher only
        c, lay = card()
        lay.addWidget(label("Back to the original launcher", "H2"))
        lay.addWidget(label("Gives Home back to the TV's own launcher and uninstalls the new launcher "
                            "(com.gathin.tvhome, the one app this tool installed). The debloat stays as it is: "
                            "no package is enabled again apart from the stock launcher. The new launcher is "
                            "removed only after the stock one is confirmed as Home. Build & install on Extras "
                            "puts it back at any time.", "Muted", wrap=True))
        self.unlaunch = button("Restore original launcher & remove the new one", "Danger", "undo")
        lay.addWidget(hbox(self.unlaunch, None))
        self.unlaunch_msg = Banner("")
        lay.addWidget(self.unlaunch_msg)
        self.body.addWidget(c)

        # Lock down
        c, lay = card()
        lay.addWidget(label("2 · Close network ADB", "H2"))
        lay.addWidget(label("Port 5555 is plaintext. When you're done, close it on the TV:", "Muted"))
        self.steps = []
        for text in ["Developer options → switch off USB debugging and Network/ADB debugging",
                     "Developer options → Revoke USB debugging authorisations",
                     "Restart the TV",
                     "If the network runs over a USB Ethernet adapter: unplug and replug it, and check the TV is on "
                     "Ethernet again (not Wi-Fi)"]:
            cb = Toggle(text)
            self.steps.append(cb)
            lay.addWidget(cb)
        self.check_port = button("Check the port is closed", "Primary", "lock")
        self.check_host = QLineEdit(win.settings.value("host", ""))
        self.check_host.setPlaceholderText("TV IP")
        self.check_host.setFixedWidth(180)
        lay.addWidget(hbox(self.check_host, self.check_port, None))
        self.port_msg = Banner("")
        lay.addWidget(self.port_msg)
        self.body.addWidget(c)
        self.body.addStretch(1)

        self.reboot.clicked.connect(self.do_reboot)
        self.restore.clicked.connect(self.do_restore)
        self.unlaunch.clicked.connect(self.do_unlaunch)
        self.check_port.clicked.connect(self.do_check_port)

    def on_connection(self, ok, info):
        if ok:
            self.check_host.setText(TV.host)
            home = info.get("home", "")
            if home and home not in (OUR_LAUNCHER, "android") and self.stock.findText(home) < 0:
                self.stock.insertItem(0, home)
            if home in KNOWN_STOCK or (home and home not in (OUR_LAUNCHER, "android")):
                self.stock.setCurrentText(home)
            if not self.list_path.text():
                self.list_path.setPlaceholderText(str(gui_list_path()))

    def pick_list(self):
        f, _ = QFileDialog.getOpenFileName(self, "Debloat list", str(EXAMPLES), "Lists (*.txt)")
        if f:
            self.list_path.setText(f)

    def do_reboot(self):
        if not self.need_tv():
            return
        path = gui_list_path()
        ours = []
        if path.exists():
            ours = [l.split("#", 1)[0].strip() for l in path.read_text(encoding="utf-8").splitlines()]
            ours = [l for l in ours if PACKAGE_RE.fullmatch(l)]
        if not ask(self, "Reboot the TV?", "The TV restarts; the app reconnects when it is back (up to 4 minutes)."):
            return
        self.reboot.setEnabled(False)
        self.reboot_msg.set("Rebooting… waiting for the TV to come back.", "info")
        run_job(reboot_and_compare, ours, on_result=self.rebooted,
                on_error=lambda m: (self.reboot_msg.set(f"{m}", "bad"),
                                    None if TV.connected else BUS.connection.emit(False, {})),
                on_done=lambda: self.reboot.setEnabled(True))

    def rebooted(self, res):
        back, still, home = res
        BUS.packages_changed.emit()
        txt = f"The TV is back. Home: <b>{home or '?'}</b>. {len(still)} of your packages stayed disabled."
        if back:
            txt += ("<br><b>Re-enabled by the firmware at boot</b> (note them, don't fight them): " + ", ".join(back))
            self.reboot_msg.set(txt, "warn")
        else:
            self.reboot_msg.set(txt, "ok")

    def do_restore(self):
        if not self.need_tv():
            return
        path = Path(self.list_path.text().strip() or gui_list_path())
        extra = settings_restore_commands(TV.host)
        if not path.exists() and not extra:
            self.restore_msg.set(f"Nothing to restore for {TV.host}: no packages were disabled and no settings "
                                 "were changed from this app.", "warn")
            return
        stock = self.stock.currentText().strip()
        if stock and not PACKAGE_RE.fullmatch(stock):
            self.restore_msg.set("The stock launcher must be a package name.", "bad")
            return
        cmds, notes = [], ""
        if path.exists():
            try:
                if recmod is None:
                    raise RuntimeError("tools/recovery.py could not be loaded")
                buf = io.StringIO()
                with contextlib.redirect_stderr(buf):
                    cmds = recmod.restore_commands(str(path), stock, TV.host)
                notes = buf.getvalue().strip()
            except SystemExit as e:
                self.restore_msg.set(str(e.code), "bad")
                return
            except Exception as e:
                self.restore_msg.set(str(e), "bad")
                return
        if extra:
            # The TV's own values from before the app changed them (DNS, animations, screensaver); they come
            # after the package record, so they win over its animation scales.
            cmds = [c for c in cmds if c != "pm list packages -d"] + ["# the TV's own settings"] + extra + \
                (["pm list packages -d"] if path.exists() else [])
        d = Dialog(self, "Restore plan", 760)
        if notes:
            d.lay.addWidget(Banner(notes.replace("\n", "<br>"), "info"))
        box = QPlainTextEdit("\n".join(cmds))
        box.setObjectName("Box")
        box.setReadOnly(True)
        box.setMinimumHeight(260)
        d.lay.addWidget(box)
        d.buttons("Run these on the TV", "Cancel", "Danger")
        if d.exec() != QDialog.DialogCode.Accepted:
            return
        self.restore.setEnabled(False)
        self.restore_msg.set("Restoring…", "info")

        def go():
            for c in cmds:
                if not c.startswith("#"):
                    TV.sh(c)
            return True

        run_job(go, on_result=lambda _: (self.restore_msg.set("Restored. Press Home on the remote; reboot if "
                                                              "something still looks off.", "ok"),
                                         BUS.packages_changed.emit()),
                on_error=lambda m: self.restore_msg.set(f"Restore stopped: {m}", "bad"),
                on_done=lambda: self.restore.setEnabled(True))

    def do_unlaunch(self):
        if not self.need_tv():
            return
        stock = self.stock.currentText().strip()
        if stock and not PACKAGE_RE.fullmatch(stock):
            self.unlaunch_msg.set("The stock launcher must be a package name.", "bad")
            return
        if not ask(self, "Remove the new launcher?",
                   "The TV's own launcher becomes Home again and the new launcher is uninstalled, together with its "
                   "theme and clock screensaver. Your debloat stays as it is.<br><br>Keep the TV awake until this "
                   "finishes.", "Restore & remove", "Danger"):
            return
        prev = self.win.settings.value(f"dream_prev/{TV.host}", "") or ""
        self.unlaunch.setEnabled(False)
        self.unlaunch_msg.set("Working…", "info")

        def ok(res):
            stock, done = res
            for d in done:
                log(d, "ok")
            self.unlaunch_msg.set(f"Done: Home is <b>{stock}</b> and the new launcher is gone. The debloat was not "
                                  "touched, so rows that relied on disabled recommendation apps may stay empty.",
                                  "ok")
            BUS.packages_changed.emit()

        run_job(remove_new_launcher, stock, prev, on_result=ok,
                on_error=lambda m: self.unlaunch_msg.set(f"{m}", "bad"),
                on_done=lambda: self.unlaunch.setEnabled(True))

    def do_check_port(self):
        host = self.check_host.text().strip()
        if not host:
            return
        self.port_msg.set("Checking…", "info")

        def check():
            run_job(port_closed, host, 5555, pool=NET_POOL, on_result=lambda r: self.port_msg.set(*r))

        if TV.connected and TV.host == host:
            # Our own connection would keep the port busy: close it first (on the TV thread), then check.
            run_job(TV.close, on_done=lambda: (BUS.connection.emit(False, {}), check()))
        else:
            check()


def reboot_and_compare(ours):
    host, port = TV.host, TV.port
    try:
        TV.sh("reboot", timeout=10, retry=False)
    except Exception:
        pass
    TV.close()
    if DEMO:
        TV.connect(host, port)
    else:
        time.sleep(25)
        deadline = time.time() + 240
        last = None
        while time.time() < deadline:
            try:
                TV.connect(host, port, timeout=10)
                if TV.prop("sys.boot_completed") == "1":
                    break
            except Exception as e:
                last = e
                TV.close()
            time.sleep(5)
        else:
            raise RuntimeError(f"The TV did not come back within 4 minutes ({last}). Check it on screen, then "
                               "Connect again.")
    log("TV is back after reboot", "ok")
    disabled = TV.packages("-d")
    home, _ = TV.home_owner()
    back = [n for n in ours if n not in disabled]
    still = [n for n in ours if n in disabled]
    return back, still, home


def port_closed(host, port):
    if DEMO:
        time.sleep(0.6)
        return (f"{host}:{port} is closed: the TV refused the connection. All done.", "ok")
    try:
        with socket.create_connection((host, port), timeout=3):
            pass
    except ConnectionRefusedError:
        return (f"{host}:{port} is <b>closed</b>: the TV refused the connection. All done.", "ok")
    except socket.timeout:
        return (f"{host}:{port} did not answer in 3 s: closed, unless the TV is off or not at this address.", "ok")
    except OSError as e:
        return (f"Could not check {host}:{port} ({e}). Is the TV on and on this network? (On macOS, “No route to "
                "host” proves nothing.)", "warn")
    return (f"{host}:{port} is <b>still open</b>: network ADB is on. Switch USB debugging and Network/ADB debugging "
            "off on the TV, reboot it, and check again.", "bad")


def open_path(path):
    QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))


# ----------------------------------------------------------------------------------------------
# Main window
# ----------------------------------------------------------------------------------------------

AUTHOR = {"name": "Nikolaos K. Paridis", "handle": "nikkpap", "team": "ALU DEV TEAM",
          "email": "nikkpap@gmail.com"}
UPSTREAM = {"name": "Gathin", "github": "https://github.com/Gathin23", "repo": "https://github.com/Gathin23/cleanyourtv",
            "site": "https://cleanyour.tv", "x": "https://x.com/gathint", "coffee": "https://buymeacoffee.com/gathint"}


def make_icon_file():
    """A Windows .ico of the app's logo for the shortcuts, drawn with Qt (256 px down to 16 px)."""
    ico = APPDATA / "CleanYourTV.ico"
    try:
        APPDATA.mkdir(parents=True, exist_ok=True)
        img = QImage(256, 256, QImage.Format.Format_ARGB32)
        img.fill(Qt.GlobalColor.transparent)
        p = QPainter(img)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(8, 8, 240, 240), 54, 54)
        p.fillPath(path, QColor("#111216"))
        p.setPen(QPen(QColor("#2e313b"), 4))
        p.drawPath(path)
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4f7cff" '
               'stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" '
               'height="14" rx="2.5"/><polyline points="17 2 12 7 7 2"/></svg>')
        QSvgRenderer(QByteArray(svg.encode())).render(p, QRectF(48, 44, 160, 160))
        p.end()
        if img.save(str(ico), "ICO"):
            return ico
    except Exception:
        pass
    return None


def make_shortcuts(force=False):
    """Desktop and Start menu shortcuts that start the app with pythonw.exe: never a console window."""
    if os.name != "nt":
        return False
    script = str(Path(__file__).resolve())
    settings = QSettings("CleanYourTV", "CleanYourTV")
    if not force and settings.value("shortcut_for", "") == script:
        return True
    ico = make_icon_file()
    ps = ("$sh = New-Object -ComObject WScript.Shell; "
          "foreach ($dir in @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs'))) { "
          "if (-not $dir) { continue }; $l = $sh.CreateShortcut((Join-Path $dir 'CleanYourTV.lnk')); "
          "$l.TargetPath = $env:CYT_PYW; $l.Arguments = '\"' + $env:CYT_SCRIPT + '\"'; "
          "$l.WorkingDirectory = $env:CYT_DIR; $l.Description = 'CleanYourTV - Android TV debloat'; "
          "if ($env:CYT_ICO) { $l.IconLocation = $env:CYT_ICO + ',0' }; $l.Save() }")
    env = dict(os.environ, CYT_PYW=_gui_python(), CYT_SCRIPT=script, CYT_DIR=str(Path(script).parent),
               CYT_ICO=str(ico) if ico else "")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden", "-Command", ps],
                           env=env, capture_output=True, text=True, timeout=30, creationflags=NO_WINDOW)
        ok = r.returncode == 0
    except Exception:
        ok = False
    if ok:
        settings.setValue("shortcut_for", script)
    return ok


class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")
        self.setFixedWidth(640)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(26, 24, 26, 20)
        lay.setSpacing(14)

        head = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(icon("tv", C["accent"], 52).pixmap(52, 52))
        head.addWidget(logo)
        t = QLabel(f"<span style='font-size:18pt;font-weight:700'>{APP_NAME}</span><br>"
                   f"<span style='color:{C['muted']}'>Version {APP_VERSION} · Android TV debloat &amp; launcher "
                   "desktop app</span>")
        head.addWidget(t, 1)
        lay.addLayout(head)

        def link(url, text=None):
            return f"<a style='color:{C['accent2']};text-decoration:none' href='{url}'>{text or url}</a>"

        def person(title, body, colour):
            f = QFrame()
            q = QColor(colour)
            f.setStyleSheet(f"QFrame {{ background: rgba({q.red()},{q.green()},{q.blue()},18); "
                            f"border: 1px solid rgba({q.red()},{q.green()},{q.blue()},70); border-radius: 14px; }}"
                            " QLabel { background: transparent; border: none; }")
            fl = QVBoxLayout(f)
            fl.setContentsMargins(18, 14, 18, 16)
            fl.setSpacing(4)
            fl.addWidget(label(title, "Key"))
            b = QLabel(body)
            b.setTextFormat(Qt.TextFormat.RichText)
            b.setOpenExternalLinks(True)
            b.setWordWrap(True)
            # Wrapped rich text: give it the height it needs at this dialog's fixed width, or it gets clipped.
            b.setMinimumHeight(b.heightForWidth(640 - 52 - 36) + 4)
            fl.addWidget(b)
            return f

        a = AUTHOR
        lay.addWidget(person(
            "DESKTOP APP",
            f"<span style='font-size:13pt;font-weight:650'>{a['name']}</span>"
            f"&nbsp;&nbsp;<span style='color:{C['muted']}'>@{a['handle']} · {a['team']}</span><br>"
            f"<span style='color:{C['muted']}'>Design and development of this Windows app.</span><br>"
            + link(f"mailto:{a['email']}", a["email"]), C["accent"]))

        u = UPSTREAM
        lay.addWidget(person(
            "TOOLKIT, LAUNCHER & TV LISTS",
            f"<span style='font-size:13pt;font-weight:650'>{u['name']}</span>"
            f"&nbsp;&nbsp;<span style='color:{C['muted']}'>@Gathin23</span><br>"
            f"<span style='color:{C['muted']}'>All the backend work this app runs on: the ADB tools, the safety "
            "checks and undo records, the Apple TV style launcher, the themes, and the tested debloat lists "
            "gathered with the CleanYourTV community.</span><br>"
            + link(u["repo"], "github.com/Gathin23/cleanyourtv") + " · " + link(u["site"], "cleanyour.tv")
            + " · " + link(u["x"], "@gathint") + " · " + link(u["coffee"], "Buy him a coffee ☕"), C["ok"]))

        lic = QLabel(
            f"<span style='color:{C['muted']}'>The cleanyourtv toolkit is © 2026 Gathin, released under the "
            f"MIT License ({link(u['repo'] + '/blob/main/LICENSE', 'read it')}). This app uses it unmodified "
            "and fetches it from GitHub. Built with Python, PyQt6 (GPL v3) and adb-shell (Apache 2.0).<br>"
            "Packages are disabled, never uninstalled: every change can be undone from the Finish page.</span>")
        lic.setTextFormat(Qt.TextFormat.RichText)
        lic.setOpenExternalLinks(True)
        lic.setWordWrap(True)
        lic.setMinimumHeight(lic.heightForWidth(640 - 52) + 4)
        lay.addWidget(lic)

        st = QSettings("CleanYourTV", "CleanYourTV")
        auto = Toggle("Connect to my TV by itself when the app starts")
        auto.setToolTip("Tries the last TV, or the only one a network scan finds. Untick it when you work on a TV "
                        "other than your usual one.")
        auto.setChecked(st.value("auto_connect", "true") == "true")
        auto.toggled.connect(lambda v: st.setValue("auto_connect", "true" if v else "false"))
        lay.addWidget(auto)

        # Toolkit zips: the newest for use and the one before as a backup
        keep = Toggle("Keep the toolkit as zip files on this PC: the newest and the one before")
        keep.setToolTip(f"Every toolkit download is also saved as toolkit.<date>.<version>.zip in "
                        f"{toolkit_archive_dir()}. Only the last {TOOLKIT_ZIPS_KEEP} are kept.")
        keep.setChecked(st.value("keep_toolkit_zips", "false") == "true")
        lay.addWidget(keep)
        self.zips = QLabel()
        self.zips.setWordWrap(True)
        self.zips.setTextFormat(Qt.TextFormat.RichText)
        lay.addWidget(self.zips)
        zrow = QHBoxLayout()
        self.zip_open = button("Open folder", None, "folder")
        self.zip_open.clicked.connect(lambda: (toolkit_archive_dir().mkdir(parents=True, exist_ok=True),
                                               open_path(toolkit_archive_dir())))
        self.zip_prev = button("Use the previous one", None, "undo",
                               "Puts the older kept toolkit in place and pauses toolkit updates until you resume them")
        self.zip_prev.clicked.connect(self.use_previous)
        self.zip_resume = button("Resume updates", None, "refresh", "The newest toolkit comes back at the next start")
        self.zip_resume.clicked.connect(self.resume_updates)
        zrow.addWidget(self.zip_open)
        zrow.addWidget(self.zip_prev)
        zrow.addWidget(self.zip_resume)
        zrow.addStretch(1)
        lay.addLayout(zrow)

        def keep_toggled(v):
            st.setValue("keep_toolkit_zips", "true" if v else "false")
            if v and not toolkit_zips() and _is_toolkit(TOOLKIT_MANAGED):
                self.zips.setText(f"<span style='color:{C['muted']}'>Saving the toolkit in use…</span>")
                run_job(zip_current_toolkit, pool=NET_POOL, on_result=lambda _: self.show_zips(),
                        on_error=lambda m: self.zips.setText(f"<span style='color:{C['bad']}'>{m}</span>"))
            else:
                self.show_zips()

        keep.toggled.connect(keep_toggled)
        self.show_zips()

        row = QHBoxLayout()
        where = QLabel(f"<span style='color:{C['dim']}'>Toolkit in use: {REPO}</span>")
        where.setWordWrap(True)
        row.addWidget(where, 1)
        if os.name == "nt":
            sc = button("Desktop shortcut", None, "tv", "Make the Desktop and Start menu shortcuts again "
                                                        "(they start the app without a console window)")
            sc.clicked.connect(lambda: run_job(make_shortcuts, True, pool=NET_POOL,
                                               on_result=lambda ok: sc.setText("Shortcut made ✓" if ok
                                                                               else "Could not make it")))
            row.addWidget(sc)
        ok = button("Close", "Primary")
        ok.clicked.connect(self.accept)
        row.addWidget(ok)
        lay.addLayout(row)


    # (AboutDialog) kept toolkit zips
    def show_zips(self):
        st = QSettings("CleanYourTV", "CleanYourTV")
        zips = toolkit_zips()
        held = st.value("toolkit_hold", "")
        on = st.value("keep_toolkit_zips", "false") == "true"
        lines = [f"{'▶ ' if i == 0 else '◦ '}{z.name}  <span style='color:{C['dim']}'>"
                 f"{z.stat().st_size / 1048576:.1f} MB{' · newest' if i == 0 else ' · backup'}</span>"
                 for i, z in enumerate(zips)]
        txt = "<br>".join(lines) if lines else ("No toolkit zip yet: the next download is saved." if on else
                                                 "Off: toolkit downloads are not kept.")
        if held:
            txt += f"<br><span style='color:{C['warn']}'>Using the previous toolkit ({held[:7]}): updates paused.</span>"
        self.zips.setText(f"<span style='color:{C['muted']}'>{txt}</span>")
        self.zip_prev.setEnabled(len(zips) >= 2 and not held)
        self.zip_resume.setVisible(bool(held))

    def use_previous(self):
        zips = toolkit_zips()
        if len(zips) < 2:
            return
        prev = zips[1]
        if not ask(self, "Use the previous toolkit?",
                   f"<b>{prev.name}</b> replaces the toolkit in use. Your ADB key, the build tools and the launcher "
                   "build state stay. Toolkit updates pause until you press Resume updates here.<br><br>Then build "
                   "the launcher again on Extras if you want it from this toolkit.", "Use it"):
            return
        self.zip_prev.setEnabled(False)
        sha = toolkit_zip_sha(prev) or "previous"

        def done(_):
            QSettings("CleanYourTV", "CleanYourTV").setValue("toolkit_hold", sha)
            self.show_zips()

        run_job(install_toolkit_zip, prev, sha, pool=NET_POOL, on_result=done,
                on_error=lambda m: (self.zips.setText(f"<span style='color:{C['bad']}'>{m}</span>"),
                                    self.zip_prev.setEnabled(True)))

    def resume_updates(self):
        st = QSettings("CleanYourTV", "CleanYourTV")
        st.remove("toolkit_hold")
        try:   # forget the held version, so the next start sees the newest as new
            TOOLKIT_VERSION.write_text(json.dumps({"sha": "", "updated": time.strftime("%Y-%m-%d %H:%M")}))
        except OSError:
            pass
        self.show_zips()
        self.zips.setText(self.zips.text() + f"<br><span style='color:{C['ok']}'>The newest toolkit is downloaded "
                                             "at the next start.</span>")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("CleanYourTV", "CleanYourTV")
        self.backup_done = False
        self.matched_profile = None
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}{' — demo' if DEMO else ''}")
        self.setWindowIcon(icon("tv", C["accent"], 64))
        self.resize(1320, 880)
        self.setMinimumSize(1060, 700)

        root = QWidget()
        rl = QHBoxLayout(root)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        # sidebar
        side = QFrame()
        side.setObjectName("Sidebar")
        side.setFixedWidth(224)
        sl = QVBoxLayout(side)
        sl.setContentsMargins(14, 18, 14, 14)
        sl.setSpacing(4)
        brand = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(icon("tv", C["accent"], 28).pixmap(28, 28))
        brand.addWidget(logo)
        name = QLabel(f"<span style='font-size:13pt;font-weight:700'>CleanYourTV</span><br>"
                      f"<span style='color:{C['dim']};font-size:8.5pt'>Android TV debloat</span>")
        brand.addWidget(name)
        brand.addStretch(1)
        sl.addLayout(brand)
        sl.addSpacing(18)

        self.pages = QStackedWidget()
        self.nav = {}
        entries = [("tv", ConnectPage), ("backup", BackupPage), ("box", DebloatPage),
                   ("remote", RemotePage), ("spark", ExtrasPage), ("palette", ThemesPage),
                   ("shield", FinishPage)]
        self.page_list = []
        for i, (ico_name, cls) in enumerate(entries):
            page = cls(self)
            self.pages.addWidget(page)
            self.page_list.append(page)
            b = QPushButton(f"  {cls.title}".replace("&", "&&"))
            b.setObjectName("Nav")
            b.setCheckable(True)
            b.setIcon(icon(ico_name, C["muted"], 20))
            b.setIconSize(QSize(19, 19))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _, n=i: self.show_page(n))
            b._ico = ico_name
            sl.addWidget(b)
            self.nav[cls.title] = b
        sl.addStretch(1)
        self.conn_pill = Pill("Not connected", C["muted"])
        self.conn_pill.setWordWrap(True)
        sl.addWidget(self.conn_pill)
        sl.addSpacing(6)
        self.about_btn = QPushButton("  About")
        self.about_btn.setObjectName("Nav")
        self.about_btn.setIcon(icon("info", C["muted"], 20))
        self.about_btn.setIconSize(QSize(18, 18))
        self.about_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.about_btn.clicked.connect(lambda: AboutDialog(self).exec())
        sl.addWidget(self.about_btn)
        self.log_btn = QPushButton("  Activity log")
        self.log_btn.setObjectName("Nav")
        self.log_btn.setCheckable(True)
        self.log_btn.setIcon(icon("log", C["muted"], 20))
        self.log_btn.setIconSize(QSize(18, 18))
        sl.addWidget(self.log_btn)
        sl.addWidget(label(f"v{APP_VERSION} · by {AUTHOR['name']}", "Dim"))
        rl.addWidget(side)

        # content
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)
        head = QWidget()
        hl = QVBoxLayout(head)
        hl.setContentsMargins(28, 22, 28, 8)
        hl.setSpacing(2)
        self.h_title = label("", "H1")
        self.h_sub = label("", "Muted")
        hl.addWidget(self.h_title)
        hl.addWidget(self.h_sub)
        cl.addWidget(head)

        split = QSplitter(Qt.Orientation.Vertical)
        split.setHandleWidth(1)
        split.addWidget(self.pages)
        self.logbox = QPlainTextEdit()
        self.logbox.setReadOnly(True)
        self.logbox.setMaximumBlockCount(6000)
        self.logbox.hide()
        split.addWidget(self.logbox)
        split.setSizes([700, 200])
        cl.addWidget(split, 1)
        rl.addWidget(content, 1)
        self.setCentralWidget(root)

        self.log_btn.toggled.connect(self.logbox.setVisible)
        BUS.log.connect(self.append_log)
        BUS.connection.connect(self.on_connection)
        self.show_page(0)
        for n, i in [("Ctrl+1", 0), ("Ctrl+2", 1), ("Ctrl+3", 2), ("Ctrl+4", 3), ("Ctrl+5", 4), ("Ctrl+6", 5),
                     ("Ctrl+7", 6)]:
            QShortcut(QKeySequence(n), self, activated=lambda i=i: self.show_page(i))
        if DEMO:
            log("demo mode: a simulated TV, nothing leaves this computer", "warn")

    def show_page(self, i):
        page = self.page_list[i]
        self.pages.setCurrentIndex(i)
        self.h_title.setText(page.title)
        self.h_sub.setText(page.subtitle)
        for title, b in self.nav.items():
            on = title == page.title
            b.setChecked(on)
            b.setIcon(icon(b._ico, "white" if on else C["muted"], 20))
        if isinstance(page, RemotePage):
            page.setFocus()

    def go(self, title):
        for i, p in enumerate(self.page_list):
            if p.title == title:
                self.show_page(i)

    def on_connection(self, ok, info):
        if ok:
            self.conn_pill.set(f"●  {info.get('model', 'TV')}\n    {TV.host}", C["ok"])
        else:
            self.conn_pill.set("Not connected", C["muted"])
        for p in self.page_list:
            p.on_connection(ok, info)
        if ok:
            self.capture()

    def append_log(self, level, text):
        col = {"cmd": C["sky"], "out": "#9aa1ad", "ok": C["ok"], "warn": C["warn"], "error": C["bad"],
               "info": C["text"]}.get(level, C["text"])
        stamp = time.strftime("%H:%M:%S")
        esc = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
               .replace("  ", "&nbsp; "))
        self.logbox.appendHtml(f"<span style='color:{C['dim']}'>{stamp}</span>&nbsp; "
                               f"<span style='color:{col}'>{esc}</span>")
        if level == "error":
            self.log_btn.setChecked(True)

    def capture(self, on_done=None):
        if not TV.connected:
            if on_done:
                on_done()
            return
        run_job(TV.screenshot, on_result=lambda p: (BUS.shot.emit(p), self.page_list[3].msg.set("")),
                on_error=lambda m: (log(m, "warn"), self.page_list[3].msg.set(m.replace("\n", "<br>"), "warn")),
                on_done=lambda: on_done and on_done())

    def closeEvent(self, e):
        self.settings.sync()
        # Close the connection unless a command holds it (a reboot wait can take minutes): then just leave.
        if TV.lock.acquire(blocking=False):
            try:
                TV.close()
            finally:
                TV.lock.release()
        super().closeEvent(e)


def main():
    global BUS
    app = make_app()
    app.setStyleSheet(stylesheet())
    BUS = Bus()
    if not DEMO:
        try:
            moved = migrate_documents(QSettings("CleanYourTV", "CleanYourTV"))
            for old, new in moved:
                log(f"moved {old} to {new}", "ok")
        except Exception as e:   # never stop the app over tidying folders
            log(f"folder move: {e}", "warn")
    win = MainWindow()
    win.show()
    bring_to_front(win)
    if not DEMO:   # the toolkit update check: in the background, used at the next start
        QTimer.singleShot(4000, lambda: run_job(
            download_toolkit_update, pool=NET_POOL, on_error=lambda m: log(f"toolkit update check: {m}", "warn"),
            on_result=lambda sha: sha and log(f"a toolkit update ({sha[:7]}) was downloaded; it is used from the "
                                              "next start of the app", "ok")))
    if win.settings.value("auto_connect", "true") == "true" or DEMO:
        QTimer.singleShot(500, win.page_list[0].auto_connect)
    if not DEMO:   # once per location of this file; quietly, in the background
        run_job(make_shortcuts, pool=NET_POOL, on_error=lambda m: None)
    if DEMO and "--autoconnect" in sys.argv:
        QTimer.singleShot(200, win.page_list[0].do_connect)
    code = app.exec()
    # Work still running on the TV or the network (a reboot wait, a scan) would hold the process open after the
    # window is gone; settings are already saved, so leave at once instead.
    TV_POOL.clear()
    NET_POOL.clear()
    if TV_POOL.activeThreadCount() or NET_POOL.activeThreadCount():
        QSettings("CleanYourTV", "CleanYourTV").sync()
        os._exit(code)
    return code


if __name__ == "__main__":
    sys.exit(main())
