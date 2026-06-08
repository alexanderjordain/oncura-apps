"""Visual identity — matched to oncura-programs (UI_STYLE_GUIDE.md).

Steel blue primary, leaf green accent, amber kicker on a cool grey canvas.
Fraunces serif for display, Hanken Grotesk for body, IBM Plex Mono for
tabular figures. Same patterns as the FLEX/Rebate app so the operator
moves between the apps without visual whiplash.
"""
from __future__ import annotations

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
  --canvas:#F0F2F4; --surface:#FFFFFF; --ink:#2A3742; --blue:#3A6A9A;
  --blue-deep:#2F567E; --green:#469B68; --amber:#E3A033; --muted:#6B7785; --line:#E2E6EA;
  --serif:'Fraunces',Georgia,serif; --sans:'Hanken Grotesk',-apple-system,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,monospace;
}

.stApp {
  background:
    radial-gradient(900px 520px at 90% -10%, rgba(58,106,154,.06), transparent 60%),
    radial-gradient(720px 480px at -6% 6%, rgba(70,155,104,.05), transparent 55%),
    var(--canvas);
}
html, body, [class*="css"], .stApp, p, li, label, .stMarkdown { font-family: var(--sans); color: var(--ink); }
h1, h2, h3, h4 { font-family: var(--serif) !important; color: var(--blue) !important; letter-spacing:-.01em; font-weight:600; }

.oncura-head { margin:.2rem 0 1.4rem 0; padding:.1rem 0 1rem 1rem; border-bottom:1px solid var(--line); border-left:4px solid var(--green); }
.oncura-head .kicker { font-family:var(--mono); text-transform:uppercase; letter-spacing:.28em; font-size:.7rem; color:var(--amber); margin-bottom:.5rem; }
.oncura-head h1 { font-size:2.4rem; line-height:1.05; margin:0; color:var(--blue) !important; }
.oncura-head .sub { font-family:var(--sans); color:var(--muted); font-size:1rem; margin:.5rem 0 0 0; max-width:62ch; }

.stButton > button, .stDownloadButton > button, .stLinkButton > a, .stLinkButton > a:visited {
  background:#FFFFFF !important; color:#1F3D5C !important; border:1.5px solid #1F3D5C !important;
  font-family:var(--sans) !important; font-weight:700 !important; border-radius:6px;
  text-decoration:none !important; transition:transform .08s ease, box-shadow .15s ease, background .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stLinkButton > a:hover {
  background:#EAF2FA !important; border-color:#1F3D5C !important; color:#1F3D5C !important;
  transform:translateY(-1px); box-shadow:0 4px 14px rgba(31,61,92,.18);
}
.stButton > button:disabled, .stDownloadButton > button:disabled, .stLinkButton > a[aria-disabled="true"] {
  background:#F3F4F6 !important; border-color:#D1D5DB !important; color:#9CA3AF !important; cursor:not-allowed;
}
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"], .stLinkButton > a {
  background:#FFFFFF !important; color:#1F3D5C !important; border:1.5px solid #1F3D5C !important;
  font-weight:700 !important; box-shadow:none !important;
}
.stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover {
  background:#EAF2FA !important; color:#1F3D5C !important; border-color:#1F3D5C !important;
  transform:translateY(-1px); box-shadow:0 4px 14px rgba(31,61,92,.18) !important;
}

section[data-testid="stSidebar"] { background:var(--surface); border-right:1px solid var(--line); }
[data-testid="stHeader"] { background: var(--surface) !important; border-bottom:1px solid var(--line); }
[data-testid="stDecoration"] { display:none; }
footer { visibility:hidden; }

/* App-card grid */
.oncura-app-card {
  padding: 1rem 1.1rem;
  border-radius: 10px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-top: 3px solid var(--blue);
  height: 100%;
}
.oncura-app-card.coming-soon { border-top-color: var(--muted); opacity: .85; }
.oncura-app-card .title {
  font-family: var(--serif); font-size: 1.2rem; color: var(--blue);
  font-weight: 600; margin: 0 0 .3rem 0; line-height: 1.2;
}
.oncura-app-card .status {
  font-family: var(--mono); font-size: .65rem; text-transform: uppercase;
  letter-spacing: .15em; color: var(--green); margin-bottom: .6rem;
}
.oncura-app-card.coming-soon .status { color: var(--muted); }
.oncura-app-card p { margin: 0 0 .8rem 0 !important; font-size: .92rem; color: var(--ink); }
</style>
"""


def inject():
    st.markdown(_CSS, unsafe_allow_html=True)


def header(title: str, subtitle: str = "", kicker: str = "ONCURA APPS"):
    sub = f'<p class="sub">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<div class="oncura-head"><div class="kicker">{kicker}</div>'
        f"<h1>{title}</h1>{sub}</div>",
        unsafe_allow_html=True,
    )
