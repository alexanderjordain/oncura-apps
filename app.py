"""Oncura Apps — portal / landing page for the internal app suite.

Categorized 2x2 grid of cards, Material Symbols icons, no gate. Each linked
app has its own password and audit log; this page is pure navigation.

Run locally:  streamlit run app.py
Deploy:       Streamlit Cloud, app file = app.py. No secrets required.
"""
from __future__ import annotations

import streamlit as st

from core import ui

st.set_page_config(
    page_title="Oncura Apps",
    page_icon=None,
    layout="wide",
)
ui.inject()


# App catalog — grouped by section. Adding a new app = appending an entry
# here. The 2x2 grid below auto-fills rows of two.
SECTIONS = [
    {
        "label": "Sales & analytics",
        "apps": [
            {
                "name": "Demo (Health)",
                "url": "https://oncura-demo-health.streamlit.app/",
                "description": "Sales / demo environment showcasing the Oncura imaging-analytics dashboard.",
                "icon": "monitor_heart",
                "accent": "blue",
                "status": "live",
            },
            {
                "name": "Specialist Comp",
                "url": "https://oncura-comp-app.streamlit.app/",
                "description": "Per-specialist compensation calculator and statement generator.",
                "icon": "payments",
                "accent": "green",
                "status": "live",
            },
        ],
    },
    {
        "label": "Accounting operations",
        "apps": [
            {
                "name": "Pass-Through & Rebates",
                "url": "https://oncura-programs.streamlit.app/",
                "description": "FLEX cycle (finance imports, credit memos, unused/overage recapture) plus the multi-month rebate report.",
                "icon": "receipt_long",
                "accent": "blue",
                "status": "live",
            },
            {
                "name": "DocuSign Billing",
                "url": None,
                "description": "Monthly batch billing for DocuSign customers via Authorize.net CIM profiles. In development.",
                "icon": "credit_card",
                "accent": "muted",
                "status": "coming_soon",
            },
        ],
    },
]


ui.header(
    "Internal app suite",
    "Pick an app to open. Each app has its own password.",
    kicker="ONCURA APPS",
)


for section in SECTIONS:
    ui.section_label(section["label"])
    apps = section["apps"]
    # Lay out two columns per row; works for 1, 2, or 3+ apps per section.
    for i in range(0, len(apps), 2):
        cols = st.columns(2, gap="medium")
        for col, app in zip(cols, apps[i:i + 2]):
            with col:
                ui.app_card(**app)
