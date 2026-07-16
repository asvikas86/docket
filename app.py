"""
Docket — desktop app entry point.

Uses pywebview to host the same HTML/CSS/JS interface inside the operating
system's own web renderer (WebView2 on Windows, WebKit on macOS, GTK
WebKit on Linux) instead of bundling an entire Chromium browser the way
Electron does. That's what keeps the packaged .exe small.

All data is persisted to a small JSON file in the user's home folder, via
the Api class below, which is exposed to the page's JavaScript as
`window.pywebview.api`.
"""

import json
import os
import shutil
import sys
from pathlib import Path

import webview

APP_DIR = Path.home() / '.docket'
DATA_FILE = APP_DIR / 'data.json'
BACKUP_FILE = APP_DIR / 'data.backup.json'

# Bump this whenever the shape of data.json changes in a way that needs
# a migration step below. This lets a newer build of the app recognize
# and upgrade data written by an older build, automatically.
DATA_VERSION = 1

DEFAULT_CATEGORIES = [
    {'id': 'personal', 'name': 'Personal', 'color': '#3E7454'},
    {'id': 'professional', 'name': 'Professional', 'color': '#2F4B7C'},
]

DEFAULT_SETTINGS = {
    'autoClearDays': 30,  # 0 means never auto-clear Done items
}

DEFAULT_DATA = {
    'tasks': [],
    'theme': 'light',
    'categories': DEFAULT_CATEGORIES,
    'settings': DEFAULT_SETTINGS,
}


def _migrate(data):
    """Upgrade an older data.json (from a previous build of the app) to
    the current shape. Add a new `if version < N:` block here each time
    DATA_VERSION is bumped, so old data keeps working after an upgrade."""
    version = data.get('_version', 0)

    # Example pattern for the future:
    # if version < 2:
    #     for t in data.get('tasks', []):
    #         t.setdefault('newField', 'someDefault')

    data['_version'] = DATA_VERSION
    return data


def _load_data():
    for source in (DATA_FILE, BACKUP_FILE):
        if not source.exists():
            continue
        try:
            with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for key, default_value in DEFAULT_DATA.items():
                data.setdefault(key, default_value)
            if not data.get('categories'):
                data['categories'] = list(DEFAULT_CATEGORIES)
            return _migrate(data)
        except (json.JSONDecodeError, OSError):
            continue  # this copy is unreadable; try the backup, then give up
    fresh = dict(DEFAULT_DATA)
    fresh['_version'] = DATA_VERSION
    return fresh


def _save_data(data):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    # Keep a copy of the last known-good save. If a future write is ever
    # interrupted (crash, power loss) or a future version writes something
    # broken, the app can fall back to this instead of losing everything.
    if DATA_FILE.exists():
        try:
            shutil.copyfile(DATA_FILE, BACKUP_FILE)
        except OSError:
            pass
    tmp_path = DATA_FILE.with_suffix('.tmp')
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    tmp_path.replace(DATA_FILE)


class Api:
    """Exposed to the page as window.pywebview.api.<method>(...)"""

    def __init__(self):
        self.data = _load_data()

    def get_state(self):
        return self.data

    def save_tasks(self, tasks):
        self.data['tasks'] = tasks
        _save_data(self.data)
        return True

    def save_theme(self, theme):
        self.data['theme'] = theme
        _save_data(self.data)
        return True

    def save_categories(self, categories):
        self.data['categories'] = categories
        _save_data(self.data)
        return True

    def save_settings(self, settings):
        self.data['settings'] = settings
        _save_data(self.data)
        return True


def _resource_path(rel_path):
    """Resolve a path that works both when run directly and when frozen
    into a single-file PyInstaller executable."""
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)


def main():
    api = Api()
    webview.create_window(
        'Docket',
        _resource_path('index.html'),
        js_api=api,
        width=1050,
        height=820,
        min_size=(640, 560),
        background_color='#F3F1EA',
        text_select=True,
    )
    # Debug/DevTools mode is OFF by default so the app opens cleanly like
    # a normal program. Turn it on temporarily for troubleshooting by
    # setting the DOCKET_DEBUG environment variable to 1 before launching
    # (see debug.bat, or run `set DOCKET_DEBUG=1` in a terminal first).
    debug = os.environ.get('DOCKET_DEBUG') == '1'
    webview.start(debug=debug)


if __name__ == '__main__':
    main()
