"""Visual identity for the Oncura Apps portal.

Aesthetic: professional productivity app — Linear / Notion / Stripe Dashboard.
Restrained palette (steel blue, leaf green, amber on cool grey), Fraunces
serif for display, Hanken Grotesk for body, IBM Plex Mono for the kicker.
Material Symbols Rounded for icons (loaded via Google Fonts CSS import).
No emojis anywhere.
"""
from __future__ import annotations

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

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

/* ── Page header ───────────────────────────────────────────────────────── */
.oncura-head { margin:.2rem 0 1.8rem 0; padding:.1rem 0 1rem 1rem; border-bottom:1px solid var(--line); border-left:4px solid var(--green); }
.oncura-head .kicker { font-family:var(--mono); text-transform:uppercase; letter-spacing:.28em; font-size:.7rem; color:var(--amber); margin-bottom:.5rem; }
.oncura-head h1 { font-size:2.4rem; line-height:1.05; margin:0; color:var(--blue) !important; }
.oncura-head .sub { font-family:var(--sans); color:var(--muted); font-size:1rem; margin:.5rem 0 0 0; max-width:62ch; }

/* ── Section header (between card groups) ─────────────────────────────── */
.oncura-section {
  font-family: var(--mono); text-transform: uppercase; letter-spacing: .18em;
  font-size: .72rem; color: var(--muted); font-weight: 600;
  margin: 1.4rem 0 .85rem 0; padding-bottom: .5rem;
  border-bottom: 1px solid var(--line);
}

/* ── App card ──────────────────────────────────────────────────────────── */
.oncura-app-card {
  position: relative;
  padding: 1.55rem 1.7rem 1.3rem 1.7rem;
  border-radius: 12px;
  background: var(--surface);
  border: 1px solid var(--line);
  height: 100%;
  transition: transform .15s ease, box-shadow .2s ease, border-color .15s ease;
  overflow: hidden;
}
.oncura-app-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(31, 61, 92, .09);
  border-color: rgba(58, 106, 154, .32);
}
.oncura-app-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--blue);
}
.oncura-app-card.accent-blue::before  { background: var(--blue); }
.oncura-app-card.accent-green::before { background: var(--green); }
.oncura-app-card.accent-amber::before { background: var(--amber); }
.oncura-app-card.accent-muted::before { background: var(--muted); }
.oncura-app-card.coming-soon          { opacity: .9; }
.oncura-app-card.coming-soon:hover    { transform: none; box-shadow: none; }

.oncura-app-card .icon-wrap {
  display: flex; align-items: center; justify-content: center;
  width: 44px; height: 44px;
  border-radius: 10px;
  background: rgba(58, 106, 154, .08);
  margin-bottom: 1rem;
}
.oncura-app-card.accent-green  .icon-wrap { background: rgba(70, 155, 104, .10); }
.oncura-app-card.accent-amber  .icon-wrap { background: rgba(227, 160, 51, .12); }
.oncura-app-card.accent-muted  .icon-wrap { background: rgba(107, 119, 133, .10); }

.oncura-app-card .icon {
  font-family: 'Material Symbols Rounded';
  font-size: 1.55rem;
  color: var(--blue);
  font-weight: 400;
  line-height: 1;
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
.oncura-app-card.accent-green  .icon { color: var(--green); }
.oncura-app-card.accent-amber  .icon { color: var(--amber); }
.oncura-app-card.accent-muted  .icon { color: var(--muted); }

.oncura-app-card .title {
  font-family: var(--serif);
  font-size: 1.28rem;
  color: var(--ink);
  font-weight: 600;
  line-height: 1.2;
  margin: 0 0 .55rem 0;
}

.oncura-app-card .status {
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  font-family: var(--mono);
  font-size: .65rem;
  text-transform: uppercase;
  letter-spacing: .15em;
  font-weight: 600;
  color: var(--green);
  margin-bottom: .9rem;
}
.oncura-app-card .status::before {
  content: '';
  display: inline-block;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 0 3px rgba(70, 155, 104, .15);
}
.oncura-app-card.coming-soon .status { color: var(--muted); }
.oncura-app-card.coming-soon .status::before { box-shadow: 0 0 0 3px rgba(107, 119, 133, .12); }

.oncura-app-card .desc {
  font-family: var(--sans);
  font-size: .9rem;
  color: var(--muted);
  line-height: 1.45;
  margin: 0 0 1rem 0 !important;
  max-width: 38ch;
}

/* ── Streamlit button + link-button restyling for the cards ───────────── */
.stButton > button, .stDownloadButton > button, .stLinkButton > a, .stLinkButton > a:visited {
  background: #FFFFFF !important; color: var(--blue-deep) !important;
  border: 1.5px solid var(--blue-deep) !important;
  font-family: var(--sans) !important; font-weight: 600 !important;
  border-radius: 8px; text-decoration: none !important;
  transition: transform .1s ease, background .15s ease, border-color .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stLinkButton > a:hover {
  background: var(--blue-deep) !important; color: #FFFFFF !important;
  border-color: var(--blue-deep) !important;
}
.stButton > button:disabled, .stDownloadButton > button:disabled, .stLinkButton > a[aria-disabled="true"] {
  background: #F3F4F6 !important; border-color: #D1D5DB !important;
  color: #9CA3AF !important; cursor: not-allowed;
}

section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
[data-testid="stHeader"] { background: var(--surface) !important; border-bottom: 1px solid var(--line); }
[data-testid="stDecoration"] { display:none; }
footer { visibility:hidden; }
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


def section_label(text: str):
    st.markdown(f'<div class="oncura-section">{text}</div>', unsafe_allow_html=True)


def app_card(*, name: str, description: str, icon: str, accent: str,
             status: str, url: str | None):
    """Render an app card. `icon` is a Material Symbols Rounded identifier
    (e.g. 'monitor_heart'). `accent` ∈ {'blue', 'green', 'amber', 'muted'}.
    `status` ∈ {'live', 'coming_soon'}.
    """
    coming_soon = status == "coming_soon"
    classes = ["oncura-app-card", f"accent-{accent}"]
    if coming_soon:
        classes.append("coming-soon")
    status_label = "COMING SOON" if coming_soon else "LIVE"
    st.markdown(
        f'<div class="{" ".join(classes)}">'
        f'<div class="icon-wrap"><span class="icon">{icon}</span></div>'
        f'<p class="title">{name}</p>'
        f'<div class="status">{status_label}</div>'
        f'<p class="desc">{description}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if coming_soon:
        st.button("In development", key=f"btn_{name}", disabled=True,
                  use_container_width=True)
    else:
        st.link_button(f"Open  →", url, use_container_width=True)
