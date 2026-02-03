# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(page_title="Overview • VoltCycle", page_icon="📊", layout="wide")

st.title("Overview")
st.caption("Key concepts, assumptions, and where to start.")

# --- Intro ---
left, right = st.columns([2, 1], vertical_alignment="center")
with left:
    st.subheader("What is VoltCycle?")
    st.markdown(
        """
VoltCycle helps you compare strategies under uncertainty. Configure demand, price,
and cost assumptions, run Monte Carlo simulations, and read decision‑ready KPIs
(e.g., **P10 / P50 / P90**), not just point estimates.
        """
    )
    st.subheader("When to use it")
    st.markdown(
        "- Pricing or discount decisions with volatile demand\n"
        "- Cost and margin planning with supply risk\n"
        "- Evaluating go‑to‑market plays under uncertainty"
    )

with right:
    st.metric("Typical runs", "1,000–10,000")
    st.metric("Outputs", "P10 / P50 / P90")
    st.info("Tip: Start with the demo run, then tune assumptions.")

st.divider()

# --- How it works ---
st.subheader("How it works")
st.markdown(
    """
1) Choose a **strategy** and set inputs.  
2) Run **N** simulations to capture uncertainty.  
3) Review **bands** (P10 / P50 / P90) and **KPIs**.  
4) Export a concise **playbook** for stakeholders.
"""
)

# --- Next steps ---
st.divider()
st.subheader("Next steps")
c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 Start Simulation", use_container_width=True):
        try:
            st.switch_page("pages/1_Simulation.py")
        except Exception:
            st.warning("Simulation page not found. Create `pages/1_Simulation.py`.")
with c2:
    if st.button("👀 Try Demo Run", use_container_width=True):
        st.session_state["use_demo"] = True
        try:
            st.switch_page("pages/1_Simulation.py")
        except Exception:
            st.info("Demo mode set. Create `pages/1_Simulation.py` to proceed.")
