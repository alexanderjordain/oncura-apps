# CLAUDE.md — oncura-apps

## What this is

Streamlit landing page for the Oncura internal app suite. Pure navigation: 4 cards in a 2×2 grid, each linking to a separate Streamlit Cloud app. **No password gate, no audit log, no persistence.** Each linked app handles its own auth.

Earlier iteration had a password + initials gate and a GitHub-backed access log. Removed 2026-06-08 — for a navigation-only portal it was overkill, and the linked apps already log their own activity.

## Stack

- Streamlit only (entry: `app.py`)
- `core/ui.py` — theme/CSS matched to `UI_STYLE_GUIDE.md` from `oncura-programs`

## Deploy

- **Repo**: github.com/alexanderjordain/oncura-apps
- **Live**: https://oncura.streamlit.app/
- **Sharing**: must be set to **Public** in the Streamlit Cloud dashboard. Default-private makes Streamlit show its own auth wall, which is wrong for a portal.
- **Secrets**: none required.

## Adding a new card

Edit `APPS` in `app.py`. 2×2 grid currently; add more rows by extending the `_render_card` calls.

## Pre-push checks

```bash
python scripts/smoke_test.py
```

CI runs the same on every push.
