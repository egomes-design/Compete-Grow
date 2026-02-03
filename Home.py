

# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st

# ---------- Page config ----------
st.set_page_config(
    page_title="VoltCycle Strategy Simulator",
    page_icon="⚡",
    layout="wide",
)

# ---------- Lightweight cached bits ----------
@st.cache_data(show_spinner=False, ttl=3600)
def app_meta():
    """Tiny cached payload to demo a non-blocking cache layer."""
    return {
        "name": "VoltCycle Strategy Simulator",
        "version": "0.1.0",
        "features": ["Benchmark", "Pricing", "Uncertainty", "Cashflow"],
    }

meta = app_meta()  # Safe and instant, just a placeholder

# ---------- Assets & styles ----------
ASSETS = Path("assets")
LOGO = ASSETS / "logo.png"
HERO = ASSETS / "hero.jpg"

# Base CSS: subtle typography, container width, hero styling
hero_css = f"""
<style>
/* Tighten the page’s max width for better line length */
.main > div {{ padding-top: 1.5rem; }}

/* Hero block */
.hero {{
  position: relative;
  border-radius: 16px;
  padding: 3.2rem 2.4rem;
  color: white;
  overflow: hidden;
  background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
  min-height: 240px;
  display: flex;
  align-items: center;
}}
.hero .content {{
  position: relative;
  z-index: 2;
  max-width: 900px;
}}
.hero h1 {{
  font-size: 2.1rem;
  line-height: 1.2;
  margin: 0 0 .4rem 0;
}}
.hero p {{
  font-size: 1.05rem;
  opacity: 0.95;
  margin: 0.2rem 0 1.2rem 0;
}}
.hero .cta-row {{
  display: flex;
  gap: .75rem;
  flex-wrap: wrap;
}}
/* Background image overlay if present */
.hero::before {{
  content: "";
  position: absolute;
  inset: 0;
  background: url('{HERO.as_posix()}') center/cover no-repeat;
  opacity: {0.28 if HERO.exists() else 0}; /* fade image if exists */
  filter: saturate(110%) contrast(105%);
}}
/* Frosted overlay for text readability */
.hero::after {{
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(2,6,23,.75), rgba(15,23,42,.35));
}}
/* Section spacing */
.section {{ margin-top: 1.25rem; }}
.metrics .stMetric {{ background: rgba(148,163,184,0.08); border-radius: 12px; padding: .75rem; }}
</style>
"""
st.markdown(hero_css, unsafe_allow_html=True)

# ---------- Header (logo + brand) ----------
cols = st.columns([1, 6])
with cols[0]:
    if LOGO.exists():
        st.image(str(LOGO), width=72)
with cols[1]:
    st.caption("Strategy • Benchmark • Pricing • Uncertainty • Cashflow")

# ---------- HERO ----------
with st.container():
    st.markdown(
        """
<div class="hero">
  <div class="content">
    <h1>VoltCycle Strategy Simulator</h1>
    <p>Model demand, pricing, costs, uncertainty & cash — then compare
       strategies with Monte Carlo bands and decision‑ready KPIs.</p>
    <div class="cta-row">
      <!-- We’ll render the real buttons below to keep state/logic in Streamlit -->
    </div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

# Real Streamlit buttons directly below (ensure keyboard focus & state)
cta_col1, cta_col2, cta_col3 = st.columns([1.2, 1.2, 1.4])
with cta_col1:
    if st.button("🚀 Start Simulation", use_container_width=True):
        try:
            st.switch_page("pages/1_Simulation.py")
        except Exception:
            st.warning("Simulation page not found. Create `pages/1_Simulation.py`.")
with cta_col2:
    if st.button("👀 Try Demo Run", use_container_width=True):
        st.session_state["use_demo"] = True
        try:
            st.switch_page("pages/1_Simulation.py")
        except Exception:
            st.info("Demo mode set. Create `pages/1_Simulation.py` to proceed.")
with cta_col3:
    if st.button("📊 Overview", use_container_width=True):
        # Optional page; see snippet below
        try:
            st.switch_page("pages/2_Overview.py")
        except Exception:
            st.info("Overview page not found (optional). See code snippet below.")

st.divider()

# ---------- “What you can do” (responsive two-column) ----------
left, right = st.columns([2, 1], vertical_alignment="center")
with left:
    st.subheader("What you can do here")
    st.markdown(
        "- **Benchmark** strategies under uncertainty\n"
        "- **Price** and **cost** scenarios with sensitivity bands\n"
        "- **Forecast cash** and KPIs (P10/P50/P90)\n"
        "- Export decisions as a concise **playbook**"
    )
with right:
    st.subheader("Quick stats")
    m1, m2 = st.columns(2)
    m1.metric("Sim runs", "1,000", "baseline")
    m2.metric("Scenarios", "9", "common")
    st.caption(f"App version: {meta['version']}")

st.divider()

# ---------- How it works ----------
with st.expander("How it works", expanded=False):
    st.markdown(
        """
1. Pick a strategy and set inputs (demand, price, costs).
2. Run **N** simulations to capture uncertainty.
3. Review **P10 / P50 / P90** bands and key KPIs in *Results*.
4. Export a **Playbook** to align decisions with stakeholders.
        """
    )

st.caption("Tip: swap the background in `assets/hero.jpg` and your logo in `assets/logo.png`.")
``
