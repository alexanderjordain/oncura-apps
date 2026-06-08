"""Access log for the portal — append-only record of who opened the portal
and which apps they clicked through to.

Each entry: {id, timestamp, initials, event, app?, entry_hash}. The
entry_hash is sha256 of the entry's canonical JSON minus the hash itself;
the GitHub commit history is the authoritative tamper trail.

Persistence model identical to oncura-programs/core/audit.py: GitHub
Contents API when GITHUB_TOKEN is set, local file otherwise. Stored at
`data/access_log.json`.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import uuid

from . import store

LOG_PATH = "access_log.json"

EVENT_TYPES = {
    "portal_login",      # successful login at the portal
    "app_click",         # clicked through to a specific app (app field set)
}


def _empty():
    return {"version": 1, "entries": []}


def _load():
    data, sha = store.load_json(LOG_PATH, default=_empty())
    if not isinstance(data, dict) or "entries" not in data:
        data = _empty()
    return data, sha


def _sha256(s: bytes) -> str:
    return hashlib.sha256(s).hexdigest()


def _entry_hash(entry: dict) -> str:
    content = {k: v for k, v in entry.items() if k != "entry_hash"}
    return _sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def record_event(event: str, *, app: str | None = None, note: str = ""):
    """Append an access-log entry. `event` should be in EVENT_TYPES.

    Pulls initials from session_state — if missing, records 'UNKNOWN' so
    the gap is visible rather than silently dropping the entry.
    """
    import streamlit as st  # local — avoid hard dep at module load
    initials = st.session_state.get("user_initials", "UNKNOWN")

    if event not in EVENT_TYPES:
        note = f"[unknown event {event!r}] {note}".strip()

    data, sha = _load()
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "initials": initials,
        "event": event,
        "app": app,
        "note": note,
    }
    entry["entry_hash"] = _entry_hash(entry)
    data["entries"].append(entry)
    msg = f"Access: {event}" + (f" → {app}" if app else "") + f" ({initials})"
    ok, info = store.save_json(LOG_PATH, data, msg, sha=sha)
    return ok, entry["id"], info


def list_entries(limit: int | None = None):
    """Most-recent-first."""
    data, _ = _load()
    entries = list(data.get("entries", []))
    entries.reverse()
    if limit is not None:
        return entries[:limit]
    return entries


def verify_integrity():
    """Recompute each entry's hash. Returns (ok, [tampered_ids])."""
    data, _ = _load()
    tampered = []
    for entry in data.get("entries", []):
        if "entry_hash" not in entry:
            continue
        if _entry_hash(entry) != entry["entry_hash"]:
            tampered.append(entry["id"])
    return len(tampered) == 0, tampered


def summary():
    data, _ = _load()
    entries = data.get("entries", [])
    by_event = {}
    by_initials = {}
    by_app = {}
    for e in entries:
        by_event[e.get("event", "?")] = by_event.get(e.get("event", "?"), 0) + 1
        by_initials[e.get("initials", "?")] = by_initials.get(e.get("initials", "?"), 0) + 1
        if e.get("app"):
            by_app[e["app"]] = by_app.get(e["app"], 0) + 1
    latest = max((e.get("timestamp", "") for e in entries), default="")
    return {
        "entry_count": len(entries),
        "by_event": by_event,
        "by_initials": by_initials,
        "by_app": by_app,
        "latest_timestamp": latest,
    }
