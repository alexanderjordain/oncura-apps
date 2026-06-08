# CLAUDE.md — oncura-apps

## What this app is

A minimal Streamlit landing page / portal for the Oncura internal app suite. One password (same as `oncura-programs`) plus initials capture, then a 2×2 grid of cards linking to each app. Every login and app-click is recorded to a GitHub-backed access log so the operator's activity is auditable.

This is a **deliberate minimal sibling** of `oncura-flex-rebate-app`. The `core/` modules are simplified adaptations — same shape, less surface area.

## Stack

- Streamlit (entry: `app.py`)
- `core/auth.py` — combined password + initials login gate
- `core/store.py` — GitHub Contents API + local-file fallback (same as oncura-programs)
- `core/audit.py` — append-only access log with per-entry SHA-256 hash
- `core/ui.py` — theme/CSS matched to UI_STYLE_GUIDE.md from oncura-programs
- `pages/access_log.py` — admin view of recent entries + integrity check

## Audit model

Two event types:
- `portal_login` — fired on successful gate entry
- `app_click` — fired when operator clicks "Log this open" on a card (the `st.link_button` itself opens in a new tab and can't be intercepted server-side, so the explicit log button is the belt-and-suspenders)

Each entry: `{id, timestamp, initials, event, app?, note, entry_hash}`. Hash is sha256 of canonical JSON minus the hash field; the GitHub commit history on `data/access_log.json` is the tamper trail.

## Deploy

- **Repo**: github.com/alexanderjordain/oncura-apps
- **Live**: https://oncura.streamlit.app/
- **Secrets** (Streamlit Cloud → Settings → Secrets):
  ```toml
  APP_PASSWORD = "..."   # same as oncura-programs
  GITHUB_TOKEN = "..."   # Contents:write on this repo
  ```

## Adding a new app card

Edit `APPS` in `app.py`:
```python
{
    "key": "new_app_slug",
    "name": "Human-friendly name",
    "url": "https://...",       # or None for coming-soon
    "description": "One-line description.",
    "status": "live",            # or "coming_soon"
},
```
The grid currently fits 4 cards (2×2). For more, expand the grid layout in `app.py`.

## Pre-push checks

```bash
python scripts/smoke_test.py    # syntax + cross-module reference check
```

CI runs the same smoke test on every push/PR (`.github/workflows/smoke.yml`).
