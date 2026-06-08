"""Combined password + initials login gate for the portal.

The portal is a public Streamlit Cloud URL, so a shared password keeps the
app index from being world-readable. Initials are captured at the same
moment so every audit log entry can be attributed to a person — the gate
itself is the audit-trail starting point.

Same APP_PASSWORD as oncura-programs (operator has one password across
the suite). Local dev bypass: set ONCURA_APPS_LOCAL=1 to skip the gate.
"""
from __future__ import annotations

import os

import streamlit as st


def _secret(key, default=None):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default


def require_login():
    """Render the gate. Once authenticated, records portal_login to the
    audit log and returns. On failure, st.stop()s and stays on the gate."""
    if st.session_state.get("auth_ok"):
        return

    app_pw = _secret("APP_PASSWORD")
    if not app_pw:
        if os.environ.get("ONCURA_APPS_LOCAL") == "1":
            st.session_state["auth_ok"] = True
            st.session_state["user_initials"] = "DEV"
            return
        st.error(
            "App password not configured. Set `APP_PASSWORD` in Streamlit secrets. "
            "For local dev, run with env var `ONCURA_APPS_LOCAL=1`."
        )
        st.stop()

    from . import ui

    ui.inject()
    # Hide sidebar on the login screen — the auto-discovered page list
    # leaks into the sidebar before our content renders.
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarCollapsedControl"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        ui.header("Oncura Apps", kicker="Internal Portal")
        st.caption(
            "Enter the shared password and your initials. Initials are recorded on the "
            "access log so we can tell who opened the portal and when."
        )
        with st.form("login_form", clear_on_submit=False):
            entered_pw = st.text_input("Password", type="password")
            entered_initials = st.text_input(
                "Your initials",
                max_chars=4,
                placeholder="e.g. AJ",
                help="2–4 characters. Persists for this session.",
            )
            submitted = st.form_submit_button("Enter", type="primary", use_container_width=True)
        if submitted:
            if entered_pw != app_pw:
                st.error("Incorrect password.")
                st.stop()
            initials = (entered_initials or "").strip().upper()
            if not initials:
                st.error("Initials are required for the access log.")
                st.stop()
            st.session_state["auth_ok"] = True
            st.session_state["user_initials"] = initials
            # Record the login event now — before the landing page renders —
            # so the audit log captures the access even if the user closes
            # the tab without clicking any app.
            from . import audit
            audit.record_event("portal_login")
            st.rerun()
    st.stop()


def current_initials() -> str:
    return st.session_state.get("user_initials", "")


def logout():
    """Drop session auth. Used by the sidebar Log out button."""
    for k in ("auth_ok", "user_initials"):
        st.session_state.pop(k, None)
