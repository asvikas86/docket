# Docket — Desktop App (Python + pywebview)

This is a lighter-weight alternative to the Electron build: same interface,
same features, but wrapped with [pywebview](https://pywebview.flowrl.com/)
instead of Electron.

## Why this is smaller

Electron ships an entire copy of Chromium and Node.js inside every app it
builds — that's why Electron installers commonly land in the 150–250MB
range even for a simple app like this one.

pywebview does not bundle a browser. It hands the page to the operating
system's **own** web renderer that's already installed on the machine:

- Windows → Microsoft Edge WebView2 (present on virtually all Windows 10/11
  machines already; if missing, it's a ~2MB installer, not something we
  bundle)
- macOS → WKWebView (built into macOS)
- Linux → WebKitGTK (usually already installed, or a normal package)

So the `.exe` PyInstaller produces is mostly just the Python interpreter
and a thin bridge — typically **20–40MB**, versus Electron's 150MB+.

The interface itself (`index.html`) is the exact same design you already
reviewed — the same look, dashboard, calendar, categories, and reminders.
Only the storage layer changed: instead of the browser's local storage,
the page now talks to a tiny Python API (`window.pywebview.api`) that reads
and writes a plain JSON file at `~/.docket/data.json`.

## What you need first

On the Windows PC you'll build on:

1. **Python 3.9+** — download from https://python.org and run the
   installer. On the first screen, tick **"Add Python to PATH"**.

## Build steps

**Easiest way:** double-click **`build.bat`** in this folder. It installs
dependencies and builds `dist\Docket.exe` for you. Then skip to "Get a
clickable icon" below.

**Manual way**, if you'd rather run the commands yourself:

1. Copy this whole `docket-pywebview` folder onto your Windows PC.
2. Open a terminal (Command Prompt or PowerShell) **inside this folder**.
3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. (Optional) Try it first without packaging:

   ```
   python app.py
   ```

   A window titled "Docket" should open with the app.

5. Build the `.exe`:

   ```
   pyinstaller --onefile --windowed --name Docket --icon assets/icon.ico --add-data "index.html;." app.py
   ```

6. Find your app at `dist\Docket.exe` — a single portable file. Copy it
   anywhere, including other Windows PCs; no Python install needed on the
   machines you copy it to.

## Get a clickable icon (like a normal Windows app)

Once `dist\Docket.exe` exists, you never need Python, a terminal, or
`py app.py`/`python app.py` again — that command was only ever for testing
before packaging.

1. (Recommended) Move `Docket.exe` somewhere permanent, e.g.
   `C:\Programs\Docket\Docket.exe`, so it doesn't get lost if you clean
   out the `dist` folder later.
2. Right-click it → **Show more options** → **Send to** →
   **Desktop (create shortcut)**.
3. Optionally, right-click that new desktop shortcut → **Pin to Start**,
   or **Pin to taskbar**.

From then on, double-clicking the icon opens Docket directly — with the
icon you built in, no console window, no typing anything. Exactly like
any other installed Windows app.

## Notes

- Your tasks are saved to `%USERPROFILE%\.docket\data.json` on whichever
  PC runs the app. Export/Import inside the app still work exactly as
  before, for moving data between machines or into a future version.
- If Windows ever complains it can't find WebView2, install the small
  official redistributable from Microsoft (search "WebView2 Runtime") —
  it's a couple MB, not a browser bundle.
- To rebuild after editing `index.html`, just re-run the `pyinstaller`
  command in step 5.
- To use your own app icon, replace `assets/icon.ico` with your own
  `.ico` file (containing 16–256px sizes) before building.
- Building a **macOS** app: same steps on a Mac (Apple requires builds to
  happen on macOS), using `--add-data "index.html:."` (colon, not
  semicolon, on macOS/Linux).

## Upgrading: your data survives, by design

Rebuilding `Docket.exe` from an updated `app.py`/`index.html` — and
replacing the old `.exe` (or shortcut) with the new one — keeps all your
tasks and categories automatically. No export/import needed for a normal
upgrade. That's because of three things working together:

1. **Data lives outside the app.** `data.json` sits in your Windows user
   folder (`~/.docket/`), never inside the `.exe` or the `dist` folder.
   A new build reads from that same fixed spot — it has no idea, and
   doesn't need to know, which build wrote the file.
2. **Loading is forgiving.** Every task and category is passed through a
   normalizer on load, on both the Python and JavaScript side. If a
   future version adds a new field, older saved data just gets sensible
   defaults for it instead of breaking.
3. **There's a version + migration hook.** `app.py` stores a `_version`
   number inside `data.json` and has a `_migrate()` function ready for
   the day a future change needs more than "just fill in a default" —
   e.g. renaming a field or restructuring something. You (or I, in a
   future session) add a migration step there when that happens; old
   files upgrade themselves the first time the new app opens them.
4. **There's a backup.** Every save keeps the previous save as
   `data.backup.json`. If a write is ever interrupted, the app falls
   back to that instead of losing everything.

Exporting a `.json` backup from the app every so often is still a good
habit for peace of mind (or for moving data to a different computer),
but it's no longer a required step for a routine upgrade.

## Troubleshooting

### "'pip' is not recognized as an internal or external command"

Python's installer either didn't add itself to your PATH, or your
terminal was opened before the install finished (Windows only picks up
PATH changes in *new* terminal windows).

1. **Close and reopen your terminal completely**, then retry. This fixes
   it most of the time on its own.
2. Still failing? Use the Python **launcher** instead — it registers
   itself separately from PATH and almost always works:
   ```
   py -m pip install -r requirements.txt
   py app.py
   py -m PyInstaller --onefile --windowed --name Docket --icon assets/icon.ico --add-data "index.html;." app.py
   ```
3. If `py` isn't recognized either, Python isn't installed yet, or was
   installed without the PATH option. Reinstall from
   https://python.org and tick **"Add python.exe to PATH"** on the very
   first screen of the installer before clicking Install.

### "'pyinstaller' is not recognized"

Same cause/fix as above — use `py -m PyInstaller ...` instead of
`pyinstaller ...` if the bare command isn't found.

### Something isn't working and you want to see the error

Normal use never shows a DevTools window — the app should look and
behave like any other plain desktop app. If something seems broken and
you want to peek at what JavaScript is complaining about:

- Double-click **`debug.bat`** instead of the app's usual shortcut. It
  launches the already-built `Docket.exe` with DevTools available for
  that one session — right-click anywhere inside the app window and
  choose **Inspect**, then check the **Console** tab for red error text.
- This doesn't change your normal shortcut or icon at all — it's a
  separate, one-off way to launch the app for troubleshooting only.

## Trade-offs versus the Electron build

| | Electron | pywebview |
|---|---|---|
| Typical installed size | 150–250MB | 20–40MB |
| Bundles its own browser | Yes (Chromium) | No (uses the OS's) |
| Build tool needed | Node.js | Python |
| Rendering consistency | Identical on every OS | Depends slightly on each OS's webview (minor, rarely noticeable for an app this simple) |
| Startup memory use | Higher | Lower |

If you want the absolute smallest, most consistent build and don't mind
the larger download, Electron is still a reasonable choice. For most
people, this pywebview version is the better trade — same app, a
fraction of the size.
