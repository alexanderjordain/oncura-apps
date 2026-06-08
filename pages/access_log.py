"""Access log — admin view of every portal_login + app_click event.

Read-only. Anyone with the portal password can see this, since the entries
contain no sensitive data (just initials + timestamps + which app was
clicked). The full trail is the GitHub commit history on data/access_log.json.
"""
from __future__ import annotations

import streamlit as st

from core import audit, auth, ui

auth.require_login()
ui.inject()

ui.header(
    "Access log",
    "Every login + app open is recorded here. Tamper-evident: each entry "
    "carries a SHA-256 hash of its content; the GitHub commit history on "
    "data/access_log.json is the authoritative trail.",
    kicker="AUDIT",
)


# ── Summary metrics ──────────────────────────────────────────────────────────
s = audit.summary()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total entries", s["entry_count"])
m2.metric("Distinct users", len(s["by_initials"]))
m3.metric("App clicks", sum(s["by_app"].values()))
m4.metric(
    "Latest event",
    (s["latest_timestamp"] or "—")[:19].replace("T", " "),
)

# ── Integrity check ──────────────────────────────────────────────────────────
ok, tampered = audit.verify_integrity()
if ok:
    st.success(
        f":material/verified: All {s['entry_count']} entry hashes verify cleanly.",
        icon=":material/verified:",
    )
else:
    st.error(
        f":material/error: {len(tampered)} entrie(s) failed hash verification: "
        f"`{', '.join(tampered[:5])}`. The GitHub commit history is authoritative — "
        "compare against `data/access_log.json` on origin/main."
    )


# ── Recent entries table ────────────────────────────────────────────────────
st.markdown("### Recent activity")
limit = st.slider("Entries to show", min_value=10, max_value=500, value=100, step=10)
entries = audit.list_entries(limit=limit)

if not entries:
    st.info("No access-log entries yet — the next login or app-click will be the first.")
else:
    rows = [
        {
            "Timestamp": e.get("timestamp", "")[:19].replace("T", " "),
            "Initials": e.get("initials", ""),
            "Event": e.get("event", ""),
            "App": e.get("app") or "—",
            "Note": e.get("note") or "",
        }
        for e in entries
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True, height=480)


# ── Per-user / per-app breakdown ────────────────────────────────────────────
with st.expander(":gray[Per-user counts]"):
    if not s["by_initials"]:
        st.caption("No entries yet.")
    else:
        st.dataframe(
            [{"Initials": k, "Events": v} for k, v in sorted(s["by_initials"].items(), key=lambda kv: -kv[1])],
            use_container_width=True,
            hide_index=True,
        )

with st.expander(":gray[Per-app click counts]"):
    if not s["by_app"]:
        st.caption("No app clicks recorded yet (use the 'Log this open' button on the portal cards).")
    else:
        st.dataframe(
            [{"App": k, "Clicks": v} for k, v in sorted(s["by_app"].items(), key=lambda kv: -kv[1])],
            use_container_width=True,
            hide_index=True,
        )
