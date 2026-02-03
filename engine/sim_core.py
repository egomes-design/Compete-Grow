
# -*- coding: utf-8 -*-
"""
Simulation core for VoltCycle Strategy Simulator (ASCII-safe build)
- Monte Carlo engine with demand, price elasticity, share response, cost learning, and cash flow
- Pure Python + numpy/pandas
"""
from dataclasses import dataclass
from typing import Dict, Any
import numpy as np
import pandas as pd

@dataclass
class Params:
    years: int = 8
    # Market
    tam0: float = 2_500_000.0
    tam_growth_mu: float = 0.06
    tam_growth_sigma: float = 0.02
    # Pricing
    price_baseline: float = 1500.0
    price_delta_pct: float = 0.0
    epsilon_mu: float = 1.4
    epsilon_sigma: float = 0.2
    # Share response (logistic on S&M spend % of revenue)
    smax: float = 0.35
    k_spend: float = 16.0
    m0: float = 0.10
    sm_pct_rev: float = 0.10
    quality_factor: float = 1.00
    availability_factor: float = 1.00
    # Unit economics
    cogs0: float = 900.0
    learning_b: float = 0.08
    rd_pct_rev: float = 0.04
    ga_pct_rev: float = 0.06
    # Finance
    tax_rate: float = 0.20
    wc_ratio: float = 0.10
    start_cash: float = 1_500_000.0
    # Strategy toggles / investments
    capex_automation: float = 0.0
    invest_auto_year: int = 1
    capex_integration: float = 0.0
    invest_integ_year: int = 3
    product_dev_year: int = 3
    market_dev_year: int = 3
    # Effects magnitudes
    quality_boost: float = 0.12
    availability_boost: float = 0.08
    tam_access_boost: float = 0.20


def run_path(p: Params, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    years = p.years
    tam = np.zeros(years)
    price = np.zeros(years)
    units = np.zeros(years)
    revenue = np.zeros(years)
    cogs_unit = np.zeros(years)
    cogs = np.zeros(years)
    gp = np.zeros(years)
    sm = np.zeros(years)
    rd = np.zeros(years)
    ga = np.zeros(years)
    depreciation = np.zeros(years)
    ebit = np.zeros(years)
    tax = np.zeros(years)
    net_income = np.zeros(years)
    cash = np.zeros(years)
    share = np.zeros(years)

    cum_units = 1.0
    cash_prev = p.start_cash
    revenue_prev = 0.0

    epsilon = max(0.2, rng.normal(p.epsilon_mu, p.epsilon_sigma))

    invested_auto = False
    invested_integ = False

    for t in range(years):
        if t == 0:
            tam[t] = p.tam0 * (1.0 + rng.normal(p.tam_growth_mu, p.tam_growth_sigma))
        else:
            tam[t] = tam[t-1] * (1.0 + rng.normal(p.tam_growth_mu, p.tam_growth_sigma))

        tam_access = 1.0
        if t + 1 >= p.market_dev_year:
            tam_access += p.tam_access_boost

        price[t] = p.price_baseline * (1.0 + p.price_delta_pct)
        price_effect = (price[t] / p.price_baseline) ** (-epsilon)

        qfactor = p.quality_factor
        afactor = p.availability_factor
        if t + 1 >= p.product_dev_year:
            qfactor *= (1.0 + p.quality_boost)
        if t + 1 >= p.invest_integ_year and p.capex_integration > 0.0:
            afactor *= (1.0 + p.availability_boost)

        sm_frac = max(0.0, p.sm_pct_rev)
        share_potential = p.smax / (1.0 + np.exp(-p.k_spend * (sm_frac - p.m0)))
        share[t] = np.clip(share_potential * qfactor * afactor, 0.0, 0.95)

        units[t] = tam[t] * tam_access * share[t] * price_effect

        cogs_shock = rng.lognormal(mean=0.0, sigma=0.06)
        cum_units = max(1.0, cum_units + units[t])
        cogs_unit[t] = p.cogs0 * (cum_units ** (-p.learning_b)) * cogs_shock
        cogs[t] = cogs_unit[t] * units[t]

        revenue[t] = price[t] * units[t]
        gp[t] = max(0.0, revenue[t] - cogs[t])

        rd[t] = max(0.0, p.rd_pct_rev * revenue[t])
        ga[t] = max(0.0, p.ga_pct_rev * revenue[t])
        sm[t] = max(0.0, p.sm_pct_rev * revenue[t])

        capex = 0.0
        if (t + 1 == p.invest_auto_year) and (not invested_auto) and p.capex_automation > 0.0:
            invested_auto = True
            capex += p.capex_automation
            depreciation[t: min(years, t + 4)] += p.capex_automation / 4.0
        if (t + 1 == p.invest_integ_year) and (not invested_integ) and p.capex_integration > 0.0:
            invested_integ = True
            capex += p.capex_integration
            depreciation[t: min(years, t + 4)] += p.capex_integration / 4.0

        ebit[t] = gp[t] - (sm[t] + rd[t] + ga[t]) - depreciation[t]
        tax[t] = max(0.0, ebit[t]) * p.tax_rate
        net_income[t] = ebit[t] - tax[t]

        wc_change = p.wc_ratio * (revenue[t] - revenue_prev)
        cash[t] = cash_prev + net_income[t] - capex - wc_change

        cash_prev = cash[t]
        revenue_prev = revenue[t]

    return {
        'Year': np.arange(1, years + 1),
        'TAM': tam,
        'Price': price,
        'Units': units,
        'Revenue': revenue,
        'COGS_unit': cogs_unit,
        'COGS': cogs,
        'GrossProfit': gp,
        'SM': sm,
        'RD': rd,
        'GA': ga,
        'Depreciation': depreciation,
        'EBIT': ebit,
        'Tax': tax,
        'NetIncome': net_income,
        'Cash': cash,
        'Share': share,
    }


def run_mc(p: Params, n: int = 1000, seed: int = 42) -> Dict[str, Any]:
    rng = np.random.default_rng(seed)
    series_keys = ['Revenue','Cash','EBIT','Units','Share','COGS_unit','GrossProfit']
    paths = []
    for i in range(n):
        prng = np.random.default_rng(rng.integers(0, 2**31-1))
        out = run_path(p, prng)
        df = pd.DataFrame(out)
        df['run'] = i
        paths.append(df)
    all_df = pd.concat(paths, ignore_index=True)
    q = all_df.groupby('Year')[series_keys].quantile([0.10, 0.50, 0.90]).unstack(level=-1)
    q.columns = [f"{m}_p{int(q*100):02d}" for m, q in q.columns]
    q = q.reset_index()
    med = all_df.groupby('Year').median(numeric_only=True).reset_index()
    return {'samples': all_df, 'quantiles': q, 'median': med}
