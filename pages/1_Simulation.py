
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from engine.sim_core import Params, run_mc

st.set_page_config(page_title="Simulation", layout="wide")
st.title("Simulation")

with st.sidebar:
    st.header("Run Settings")
    seed = st.number_input("Random Seed", min_value=0, max_value=2**31-1, value=42, step=1)
    n_runs = st.slider("Monte Carlo runs", min_value=100, max_value=5000, value=1000, step=100)

left, right = st.columns([1, 1])
with left:
    st.subheader("Market & Pricing")
    tam0 = st.number_input("TAM start (units)", min_value=10000, value=2_500_000, step=10000)
    tam_mu = st.slider("TAM growth mu", 0.00, 0.20, 0.06, 0.01)
    tam_sigma = st.slider("TAM growth sigma", 0.00, 0.10, 0.02, 0.01)

    price_baseline = st.number_input("Baseline price (€)", min_value=100.0, value=1500.0, step=50.0)
    price_delta_pct = st.slider("Price delta % vs. baseline", -0.5, 0.5, 0.0, 0.01)
    eps_mu = st.slider("Price elasticity mu", 0.2, 3.0, 1.4, 0.1)
    eps_sigma = st.slider("Price elasticity sigma", 0.0, 1.0, 0.2, 0.05)

with right:
    st.subheader("Spend & Costs")
    sm_pct = st.slider("S&M % of revenue", 0.00, 0.40, 0.10, 0.01)
    rd_pct = st.slider("R&D % of revenue", 0.00, 0.20, 0.04, 0.01)
    ga_pct = st.slider("G&A % of revenue", 0.00, 0.25, 0.06, 0.01)

    st.subheader("Investments & Strategy")
    capex_auto = st.number_input("Capex: Automation (€)", min_value=0.0, value=600_000.0, step=50_000.0)
    auto_year = st.slider("Automation year", 1, 8, 1, 1)
    capex_integ = st.number_input("Capex: Vertical integration (€)", min_value=0.0, value=800_000.0, step=50_000.0)
    integ_year = st.slider("Integration year", 1, 8, 3, 1)

    prod_year = st.slider("Product development launch year", 1, 8, 3, 1)
    market_year = st.slider("Market development start year", 1, 8, 3, 1)

st.divider()

p = Params(
    years=8,
    tam0=float(tam0),
    tam_growth_mu=float(tam_mu),
    tam_growth_sigma=float(tam_sigma),
    price_baseline=float(price_baseline),
    price_delta_pct=float(price_delta_pct),
    epsilon_mu=float(eps_mu),
    epsilon_sigma=float(eps_sigma),
    sm_pct_rev=float(sm_pct),
    rd_pct_rev=float(rd_pct),
    ga_pct_rev=float(ga_pct),
    capex_automation=float(capex_auto),
    invest_auto_year=int(auto_year),
    capex_integration=float(capex_integ),
    invest_integ_year=int(integ_year),
    product_dev_year=int(prod_year),
    market_dev_year=int(market_year),
)

left2, right2 = st.columns([1, 1])
with left2:
    st.subheader("Preview (100 quick runs)")
    quick = run_mc(p, n=100, seed=seed)
    q = quick['quantiles']
    st.line_chart(q.set_index('Year')[['Revenue_p10','Revenue_p50','Revenue_p90']])

with right2:
    st.subheader("Parameters")
    dfp = pd.DataFrame({
        'Parameter': [
            'TAM0','TAM mu','TAM sigma','Price baseline','Price d%','eps mu','eps sigma','S&M %','R&D %','G&A %',
            'Capex Auto','Auto Year','Capex Integr','Integr Year','Prod Dev Year','Market Dev Year'
        ],
        'Value': [
            p.tam0, p.tam_growth_mu, p.tam_growth_sigma, p.price_baseline, p.price_delta_pct, p.epsilon_mu, p.epsilon_sigma,
            p.sm_pct_rev, p.rd_pct_rev, p.ga_pct_rev, p.capex_automation, p.invest_auto_year, p.capex_integration, p.invest_integ_year,
            p.product_dev_year, p.market_dev_year
        ]
    })
    st.dataframe(dfp, use_container_width=True)

st.divider()

if st.button("Run full simulation"):
    res = run_mc(p, n=n_runs, seed=seed)
    st.session_state['results'] = res
    st.session_state['params'] = p
    st.success("Simulation completed. Open the Results page.")
    st.switch_page("pages/2_Results.py")
