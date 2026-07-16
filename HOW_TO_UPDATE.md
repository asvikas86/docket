# How to update Docket without losing your data

Short version: your tasks live in a completely separate place from the
app itself, so a normal update is just "swap the app files, rebuild."
Nothing below touches your data on purpose.

## Where things live

| What | Where | Touched by an update? |
|---|---|---|
| App code (`app.py`, `index.html`, etc.) | wherever you put the `docket-pywebview` folder | Yes — this is what you're replacing |
| Your actual data (tasks, categories, settings) | `%USERPROFILE%\.docket\data.json` | No — a different folder entirely |
| Backup of your data | `%USERPROFILE%\.docket\data.backup.json` | No |

Because those are separate folders, replacing the app files and
rebuilding the `.exe` has no way to reach into `.docket\` and change
anything — the new build just reads the same `data.json` next time it
opens, the same way the old build did.

## Steps

1. **(Optional but recommended) Back up first.**
   Open your current Docket app → click **⬇ Export** → save the
   `.json` file somewhere safe. This costs nothing and means you're
   covered even in a freak scenario.

2. **Get the new files.**
   Take the updated `app.py` / `index.html` (and anything else that
   changed) and drop them into your existing `docket-pywebview` folder,
   overwriting the old ones. Leave `build.bat`, `requirements.txt`, and
   the `build` folder alone unless you were told to change those too.

3. **Rebuild.**
   Double-click `build.bat` (or run the `pyinstaller` command from
   `README.md` yourself). This produces a fresh `dist\Docket.exe`.

4. **Swap the executable.**
   - Easiest: copy the new `dist\Docket.exe` over the old one, using
     the exact same file path/name it had before. Any existing desktop
     shortcut or Start Menu pin keeps working automatically, since
     shortcuts point at a path, not a specific file version.
   - Alternative: put the new `.exe` somewhere new and re-create the
     shortcut (right-click → **Send to** → **Desktop (create
     shortcut)**), then delete the old one.

5. **Open it and check.**
   Launch Docket as usual. Your tasks, categories, theme, and settings
   should all be exactly as you left them — nothing to import, nothing
   to reconfigure.

## If something ever looks wrong after an update

- Check `%USERPROFILE%\.docket\data.json` still exists and isn't empty
  (right-click → Open with → Notepad, if you want to peek).
- If it looks damaged, the app automatically tries
  `data.backup.json` next time it starts — that's a copy of your data
  from just before the last save.
- Worst case, re-import the `.json` you exported in step 1 via the
  app's **⬆ Import** button.
