# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(page_title="Overview • VoltCycle", page_icon="📊", layout="wide")

st.title("Overview")
st.caption("Key concepts, assumptions, and where to start.")

st.subheader("What is VoltCycle?")
st.markdown(
    """
VoltCycle helps you compare strategies under uncertainty. Configure demand, price,
and cost assumptions, run Monte Carlo simulations, and read decision‑ready KPIs
(e.g., **P10 / P50 / P90**), not just point estimates.
"""
)

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
