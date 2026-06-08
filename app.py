"""Oncura Apps — portal / landing page for the internal app suite.

A simple index: 4 cards in a 2x2 grid linking to each app. No gate — each
linked app has its own password + audit. The portal is just navigation.

Run locally:  streamlit run app.py
Deploy:       Streamlit Cloud, app file = app.py. No secrets required.
"""
from __future__ import annotations

import streamlit as st

from core import ui

st.set_page_config(
    page_title="Oncura Apps",
    page_icon="*",
    layout="wide",
)
ui.inject()


APPS = [
    {
        "name": "Demo (Health)",
        "url": "https://oncura-demo-health.streamlit.app/",
        "description": "Sales / demo environment showcasing the Oncura imaging-analytics dashboard.",
        "status": "live",
    },
    {
        "name": "Specialist Comp",
        "url": "https://oncura-comp-app.streamlit.app/",
        "description": "Per-specialist compensation calculator and statement generator.",
        "status": "live",
    },
    {
        "name": "Pass-Through & Rebates",
        "url": "https://oncura-programs.streamlit.app/",
        "description": "FLEX cycle (finance imports, credit memos, unused/overage recapture) + Rebate cycle.",
        "status": "live",
    },
    {
        "name": "DocuSign Billing",
        "url": None,
        "description": "Monthly batch billing for DocuSign customers via Authorize.net CIM profiles.",
        "status": "coming_soon",
    },
]


ui.header(
    "Internal app suite",
    "Pick an app to open. Each app has its own password.",
    kicker="ONCURA APPS",
)


def _render_card(col, app):
    coming_soon = app["status"] == "coming_soon"
    card_class = "oncura-app-card coming-soon" if coming_soon else "oncura-app-card"
    status_label = "COMING SOON" if coming_soon else "LIVE"
    with col:
        st.markdown(
            f'<div class="{card_class}">'
            f'<p class="title">{app["name"]}</p>'
            f'<p class="status">{status_label}</p>'
            f'<p>{app["description"]}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if coming_soon:
            st.button("Coming soon", key=f"btn_{app['name']}",
                      disabled=True, use_container_width=True)
        else:
            st.link_button(f"Open {app['name']} ↗", app["url"],
                           use_container_width=True)


row1_l, row1_r = st.columns(2, gap="medium")
row2_l, row2_r = st.columns(2, gap="medium")
_render_card(row1_l, APPS[0])
_render_card(row1_r, APPS[1])
_render_card(row2_l, APPS[2])
_render_card(row2_r, APPS[3])
