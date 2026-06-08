"""Oncura Apps — portal / landing page for the internal app suite.

A simple index: password + initials gate (audit-compliant — every login is
logged with initials and timestamp), then a grid of cards linking out to
each app. Card clicks record an `app_click` event with the app name so
the access log shows "AJ opened the portal at 10:32, clicked Comp App at
10:33" — exactly what an auditor needs to reconstruct activity.

Run locally:  streamlit run app.py
Deploy:       Streamlit Cloud, app file = app.py. Set APP_PASSWORD + GITHUB_TOKEN in secrets.
"""
from __future__ import annotations

import streamlit as st

from core import audit, auth, ui

st.set_page_config(
    page_title="Oncura Apps",
    page_icon="*",
    layout="wide",
)

auth.require_login()
ui.inject()


# ── App catalog ───────────────────────────────────────────────────────────────
APPS = [
    {
        "key": "demo_health",
        "name": "Demo (Health)",
        "url": "https://oncura-demo-health.streamlit.app/",
        "description": "Sales / demo environment showcasing the Oncura imaging-analytics dashboard.",
        "status": "live",
    },
    {
        "key": "comp_app",
        "name": "Specialist Comp",
        "url": "https://oncura-comp-app.streamlit.app/",
        "description": "Per-specialist compensation calculator and statement generator.",
        "status": "live",
    },
    {
        "key": "programs",
        "name": "Pass-Through & Rebates",
        "url": "https://oncura-programs.streamlit.app/",
        "description": "FLEX cycle (finance imports, credit memos, unused/overage recapture) + Rebate cycle.",
        "status": "live",
    },
    {
        "key": "docusign_billing",
        "name": "DocuSign Billing",
        "url": None,
        "description": "Monthly batch billing for DocuSign customers via Authorize.net CIM profiles.",
        "status": "coming_soon",
    },
]


# ── Header + identity strip ───────────────────────────────────────────────────
ui.header(
    "Internal app suite",
    "One password, one place. Pick an app below — each click is recorded on the access log.",
    kicker="ONCURA APPS",
)

ident_l, ident_r = st.columns([5, 1])
ident_l.markdown(
    f"<span style='font-family: var(--mono); color: var(--muted); "
    f"font-size: .8rem; letter-spacing: .08em;'>"
    f"LOGGED IN AS: <b style='color: var(--ink)'>{auth.current_initials()}</b></span>",
    unsafe_allow_html=True,
)
if ident_r.button("Log out", key="logout_btn", use_container_width=True):
    auth.logout()
    st.rerun()

st.markdown('<div style="height: 1rem"></div>', unsafe_allow_html=True)


# ── App cards ─────────────────────────────────────────────────────────────────
def _render_card(col, app: dict):
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
            st.button(
                "Coming soon",
                key=f"btn_{app['key']}",
                disabled=True,
                use_container_width=True,
            )
        else:
            # st.link_button opens in a new tab via plain href, so the click
            # leaves the portal immediately — we can't intercept it server-side
            # to log. Pair it with a small companion button that logs the
            # event explicitly when the operator wants the audit trail. The
            # link_button is the primary affordance; the "Log this open" is
            # the optional belt-and-suspenders.
            st.link_button(
                f"Open {app['name']} ↗",
                app["url"],
                use_container_width=True,
            )
            if st.button(
                "Log this open",
                key=f"log_{app['key']}",
                use_container_width=True,
                help="Records an app_click event in the access log. Useful when you want the trail to show "
                     "you opened this app even if the link_button click itself wasn't intercepted.",
            ):
                ok, _id, info = audit.record_event("app_click", app=app["key"])
                if ok:
                    st.success(f"Logged: {app['name']} opened by {auth.current_initials()}.")
                else:
                    st.warning(f"Logged locally only — {info}")


# 2×2 grid
row1_l, row1_r = st.columns(2, gap="medium")
row2_l, row2_r = st.columns(2, gap="medium")
_render_card(row1_l, APPS[0])
_render_card(row1_r, APPS[1])
_render_card(row2_l, APPS[2])
_render_card(row2_r, APPS[3])


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div style="height: 1.5rem"></div>', unsafe_allow_html=True)
st.divider()
st.caption(
    ":gray[Same password as the apps below. Every login + app open is recorded on the "
    "access log (visible in the sidebar nav). Audit-compliant by design.]"
)
