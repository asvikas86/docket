# Docket

A personal to-do & reminder app that keeps **Personal** and
**Professional** tasks separate — with a dashboard, calendar, reminders,
categories you can customize, search, and more.

This runs as a real desktop app on Windows (double-click an icon, just
like any other program) — no browser tab, no account, no internet
connection required to use it. Your data stays on your own computer.

> **New here and not very technical?** That's exactly who this guide is
> for. Follow the steps below in order and you'll have your own working
> app. Nothing here requires knowing how to code.

---

## What this app does

- **Dashboard** — see what's overdue, due today, and coming up in the
  next 7 days, plus quick stats (completed this week/month, completion
  rate)
- **List view** — every task, filterable by category, priority, and
  status
- **Calendar view** — a month grid showing what's due on each day
- **Done tab** — everything you've completed, with a one-click "clear"
  option
- **Archived tab** — set tasks aside without deleting them
- **Search** — find a task by title or notes instantly
- **Categories** — start with Personal/Professional, or add your own
  (Family, Freelance, Health...), each with its own color
- **Reminders** — a pop-up with a soft ping sound 30 minutes before
  something's due
- **Recurring tasks, subtasks, priorities, due dates/times, links**
- **Light/dark mode**
- **Export/Import** — back up your data to a file, or move it to
  another computer
- **Settings** — e.g. auto-clear old completed items after N days

---

## Quick start (for the impatient)

If someone already built `Docket.exe` for you and handed it to you
directly: just double-click it. That's it — skip everything below.

Otherwise, keep reading — you're going to build it yourself. It sounds
scarier than it is; it's mostly clicking "Next" and "Yes."

---

## Step 1 — Get the project onto your computer

If you're reading this on GitHub, click the green **Code** button near
the top of the page, then **Download ZIP**. Once it downloads, right-click
the ZIP file and choose **Extract All**, and remember where you put the
extracted folder (e.g. your Desktop).

## Step 2 — Install Python

This app is built using Python, a free programming language. You need it
installed once.

1. Go to https://python.org/downloads and click the big "Download
   Python" button.
2. Run the installer you downloaded.
3. **Important:** on the very first screen of the installer, tick the
   checkbox that says **"Add python.exe to PATH"** before clicking
   Install. This one checkbox is the most common thing people miss.
4. Click through the rest with the default options.

## Step 3 — Build the app

1. Open the `docket-pywebview` folder you extracted in Step 1.
2. Double-click **`build.bat`**.
3. A black window will pop up and show progress text for a minute or two
   (it's downloading a couple of things the first time, and then
   building your app). Just let it run.
4. When it says **"Done!"**, you're finished. A new `dist` folder now
   exists inside `docket-pywebview`, containing **`Docket.exe`**.

If this window shows an error instead of "Done!", see
[Troubleshooting](BUILD_DETAILS.md#troubleshooting) in `BUILD_DETAILS.md`
— the most common issues (like Python not being found) are covered there
with exact fixes.

## Step 4 — Make it feel like a normal app

Right now `Docket.exe` is buried inside a `dist` folder. Let's fix that:

1. Open the `dist` folder.
2. Right-click `Docket.exe` → **Show more options** → **Send to** →
   **Desktop (create shortcut)**.
3. (Optional) Right-click that new desktop shortcut → **Pin to Start**
   or **Pin to taskbar**, so it's always one click away.

From now on, double-click that icon whenever you want to open Docket.
No Python, no terminal, no folders to hunt through.

---

## Using the app

- **Add a task:** click **+ New entry** (top right). Give it a title,
  pick a category and priority, optionally a due date/time, and save.
- **Switch views:** the row of tabs (Dashboard / List / Calendar / Done
  / Archived) changes what you're looking at.
- **Personal vs. Professional (or your own categories):** click a
  category tab to filter, or the small **⚙** next to the tabs to add,
  rename, recolor, reorder, or delete categories.
- **Mark something done:** click the circle on the left of any task.
- **Set a reminder:** just give a task a due date *and* time — you'll
  get a pop-up with a soft ping 30 minutes beforehand.
- **Search:** type into the search box under the tabs — it filters as
  you type.
- **Settings:** click **⚙ Settings** (top right) to control things like
  how long completed items stick around before auto-clearing.
- **Back up your data:** click **⬇ Export** to save a `.json` file
  anywhere you like. Click **⬆ Import** later to bring it back (handy
  if you get a new computer, or after rebuilding the app — see
  `HOW_TO_UPDATE.md`).

Your data is saved automatically as you go — there's no "Save" button
to remember, and nothing is lost if you close the app.

---

## Updating to a newer version later

If you ever get updated files for this app, see **`HOW_TO_UPDATE.md`** —
it walks through replacing the files and rebuilding without losing any
of your existing tasks.

## The technical details

If you're curious how this actually works under the hood (why it's much
smaller than a typical desktop app, how the data is stored, troubleshooting
specific error messages, building on Mac/Linux, etc.), see
**`BUILD_DETAILS.md`**.

## Questions or something broken?

Open an "Issue" on this GitHub page (there's an **Issues** tab near the
top) and describe what happened. Screenshots help a lot.
