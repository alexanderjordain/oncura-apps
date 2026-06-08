# Oncura Apps

Landing page for the Oncura internal app suite. Just navigation — no gate, no audit log. Each linked app has its own password.

**Live:** https://oncura.streamlit.app/

## What's here

| App | URL | Status |
|---|---|---|
| Demo (Health) | https://oncura-demo-health.streamlit.app/ | Live |
| Specialist Comp | https://oncura-comp-app.streamlit.app/ | Live |
| Pass-Through & Rebates | https://oncura-programs.streamlit.app/ | Live |
| DocuSign Billing | — | Coming soon |

## Local dev

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Streamlit Cloud, app file = `app.py`. **No secrets required.** Set the app's Sharing setting to **Public** in the Streamlit Cloud dashboard.

## Adding a card

Edit `APPS` in `app.py`:

```python
{
    "name": "Human-friendly name",
    "url": "https://...",         # or None for coming-soon
    "description": "One-line description.",
    "status": "live",              # or "coming_soon"
},
```

Grid currently fits 4 cards (2×2). Expand the row layout in `app.py` for more.
