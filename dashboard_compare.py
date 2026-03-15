import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os

st.set_page_config(page_title="RAG Comparison Dashboard", layout="wide")

st.title("⚖️ RAG Comparison: Baseline vs Optimized")

# 1. Pobieranie listy plików
all_files = sorted([f for f in os.listdir('.') if f.endswith('.json') and 'report' in f])

if len(all_files) < 1:
    st.error("❌ Nie znaleziono plików raportów .json w katalogu!")
    st.stop()

# 2. Wybór plików do porównania
col_a, col_b = st.columns(2)
with col_a:
    file_1 = st.selectbox("Wybierz Raport A (Baseline):", all_files, index=0)
with col_b:
    file_2 = st.selectbox("Wybierz Raport B (Eksperyment):", all_files, index=min(len(all_files)-1, 1))

def load_data(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

data_a = load_data(file_1)
data_b = load_data(file_2)

df_a = pd.DataFrame(data_a['details'])
df_b = pd.DataFrame(data_b['details'])

# 3. Metryki KPI (Porównanie)
st.header("📊 Porównanie Kluczowych Metryk")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

def get_delta(val_a, val_b, inverse=False):
    diff = val_b - val_a
    return f"{diff:+.3f}"

kpi1.metric("Avg Score", f"{data_b['summary']['avg_relevance_score']}/5", 
            get_delta(data_a['summary']['avg_relevance_score'], data_b['summary']['avg_relevance_score']))

kpi2.metric("Hit Rate", f"{data_b['summary']['hit_rate_percent']}%", 
            f"{data_b['summary']['hit_rate_percent'] - data_a['summary']['hit_rate_percent']:+.2f}%")

kpi3.metric("Avg Latency", f"{data_b['summary']['avg_latency_sec']}s", 
            get_delta(data_a['summary']['avg_latency_sec'], data_b['summary']['avg_latency_sec']), delta_color="inverse")

kpi4.metric("Total Cost", f"${data_b['summary']['total_audit_cost_usd']}", 
            get_delta(data_a['summary']['total_audit_cost_usd'], data_b['summary']['total_audit_cost_usd']), delta_color="inverse")

st.markdown("---")

# 4. Wykresy
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Rozkład ocen")
    df_a['Source'] = file_1
    df_b['Source'] = file_2
    combined_df = pd.concat([df_a, df_b])
    fig = px.histogram(combined_df, x="score", color="Source", barmode="group",
                       color_discrete_sequence=['#1f77b4', '#ff7f0e'])
    st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    st.subheader("Latencja vs Koszt (Raport B)")
    fig2 = px.scatter(df_b, x="latency", y="cost_usd", color="score", size="score",
                      hover_data=['query'], title=f"Analiza wydajności: {file_2}")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 5. Tabela Porównawcza i EKSPORT CSV
st.subheader("🔍 Szczegółowe zestawienie i Eksport")

# Łączymy dane do jednej tabeli eksportowej
full_comp = df_a[['id', 'query', 'score', 'latency']].merge(
    df_b[['id', 'score', 'latency', 'cost_usd']], 
    on='id', 
    suffixes=(f'_{file_1}', f'_{file_2}')
)

# Przycisk eksportu CSV
csv = full_comp.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 Pobierz pełny raport porównawczy (CSV)",
    data=csv,
    file_name=f"comparison_{file_1}_vs_{file_2}.csv",
    mime="text/csv",
)

# Wyświetlanie tabeli w dashboardzie
st.dataframe(full_comp, use_container_width=True)

# 6. Analiza regresji (gdzie pogorszyliśmy wyniki?)
st.subheader("⚠️ Regresje (gdzie wynik spadł)")
regression = full_comp[full_comp[f'score_{file_2}'] < full_comp[f'score_{file_1}']]
if not regression.empty:
    st.table(regression)
else:
    st.success("Brak regresji! Wersja B jest równa lub lepsza od Wersji A we wszystkich przypadkach.")