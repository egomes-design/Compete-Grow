
# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="VoltCycle Simulator", layout="wide")

# Background image via CSS
hero_path = Path('assets/hero.jpg')
if hero_path.exists():
    st.markdown(
        """
        <style>
        .stApp {
            background: url('assets/hero.jpg') no-repeat center center fixed;
            background-size: cover;
        }
        .overlay {
            background: rgba(0,0,0,0.55);
            padding: 3rem 2rem;
            border-radius: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Logo
st.image('assets/logo.png', width=96)

st.markdown(
    """
    <div class="overlay">
      <h1 style="color:white; font-size: 3rem; margin-bottom:0.5rem;">VoltCycle Strategy Simulator</h1>
      <p style="color:white; font-size: 1.1rem;">
        Model demand, pricing, costs, uncertainty & cash — then compare strategies with Monte Carlo bands.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Start Simulation"):
        st.switch_page("pages/1_Simulation.py")

with col2:
    st.write("")
    st.write("**How it works**: Choose a strategy + inputs, run N simulations, then open Results to see P10/P50/P90 bands and KPIs.")

st.caption("Tip: swap the background in assets/hero.jpg and your logo in assets/logo.png")
