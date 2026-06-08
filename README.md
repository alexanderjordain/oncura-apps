# Oncura Apps

Internal portal / landing page for the Oncura app suite. One password, one place — pick an app and go.

**Live:** https://oncura.streamlit.app/

## What's here

| App | URL | Status |
|---|---|---|
| Demo (Health) | https://oncura-demo-health.streamlit.app/ | Live |
| Specialist Comp | https://oncura-comp-app.streamlit.app/ | Live |
| Pass-Through & Rebates | https://oncura-programs.streamlit.app/ | Live |
| DocuSign Billing | — | Coming soon |

## How it works

- **Combined login**: password + initials. Initials are captured on the access log so every event is attributable to a person.
- **Access log**: every `portal_login` and `app_click` is appended to `data/access_log.json`, persisted via the GitHub Contents API. Tamper-evident via per-entry SHA-256 hashes; the GitHub commit history is the authoritative trail.
- **Same password as `oncura-programs`** so the operator has one credential across the suite.

## Local dev

```bash
pip install -r requirements.txt
ONCURA_APPS_LOCAL=1 streamlit run app.py
```

`ONCURA_APPS_LOCAL=1` bypasses the password gate for local development. Don't set this in Cloud secrets.

## Deploy on Streamlit Cloud

1. Connect this repo on https://share.streamlit.io
2. App file: `app.py`
3. Secrets:
   ```toml
   APP_PASSWORD = "..."
   GITHUB_TOKEN = "..."  # Contents:write scope on this repo
   ```
4. Hard-refresh after the first deploy to bust JS cache.

## Reusing the FLEX/Rebate patterns

This app is a deliberate minimal sibling of [`oncura-programs`](https://github.com/alexanderjordain/oncura-flex-rebate-app). The `core/auth.py`, `core/store.py`, `core/audit.py`, and `core/ui.py` modules are adapted versions of that app's equivalents — same shape, simpler content. If you change auth or persistence behavior here, mirror it in `oncura-programs` (and vice versa).

UI patterns follow [`UI_STYLE_GUIDE.md`](https://github.com/alexanderjordain/oncura-flex-rebate-app/blob/main/docs/UI_STYLE_GUIDE.md) in the FLEX repo.
