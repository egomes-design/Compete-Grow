
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Results", layout="wide")
st.title("Results")

if 'results' not in st.session_state:
    st.info("No results yet. Go to the Simulation page and run the model.")
    st.stop()

res = st.session_state['results']
q = res['quantiles'].copy()
med = res['median'].copy()

# Fan chart helper

def fan_chart(df_q: pd.DataFrame, y_base: str, title: str):
    y10 = f"{y_base}_p10"; y50 = f"{y_base}_p50"; y90 = f"{y_base}_p90"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_q['Year'], y=df_q[y90], line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=df_q['Year'], y=df_q[y10], fill='tonexty', name='P10–P90',
                             line=dict(width=0), fillcolor='rgba(37,99,235,0.25)'))
    fig.add_trace(go.Scatter(x=df_q['Year'], y=df_q[y50], name='Median', line=dict(color='rgb(37,99,235)', width=2)))
    fig.update_layout(title=title, xaxis_title='Year', yaxis_title=y_base, template='plotly_white',
                      legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return fig

colA, colB = st.columns(2)
with colA:
    st.plotly_chart(fan_chart(q, 'Revenue', 'Revenue (P10/P50/P90)'), use_container_width=True)
with colB:
    st.plotly_chart(fan_chart(q, 'Cash', 'Cash (P10/P50/P90)'), use_container_width=True)

colC, colD = st.columns(2)
with colC:
    st.plotly_chart(fan_chart(q, 'EBIT', 'EBIT (P10/P50/P90)'), use_container_width=True)
with colD:
    st.plotly_chart(fan_chart(q, 'Units', 'Units (P10/P50/P90)'), use_container_width=True)

st.subheader("KPIs (Median path)")
last = med.iloc[-1]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Revenue (Y8)", f"€{last['Revenue']:,.0f}")
col2.metric("Cash (Y8)", f"€{last['Cash']:,.0f}")
col3.metric("EBIT (Y8)", f"€{last['EBIT']:,.0f}")
col4.metric("Share (Y8)", f"{last['Share']*100:.1f}%")

st.subheader("Downloads")
colx, coly = st.columns(2)
with colx:
    csv_q = q.to_csv(index=False).encode('utf-8')
    st.download_button("Download Quantiles (CSV)", csv_q, file_name='quantiles.csv', mime='text/csv')
with coly:
    csv_m = med.to_csv(index=False).encode('utf-8')
    st.download_button("Download Median Path (CSV)", csv_m, file_name='median.csv', mime='text/csv')

st.caption("Tip: rerun with different strategies and compare CSVs offline or extend this page to overlay runs.")
