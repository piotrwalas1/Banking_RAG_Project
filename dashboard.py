import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Konfiguracja strony
st.set_page_config(
    page_title="RAG Evaluation Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RAG Evaluation Dashboard - Santander Bank Bot")
st.markdown("""
Ten dashboard wizualizuje wyniki testów automatycznych systemu RAG. 
Dane pochodzą z audytu przeprowadzonego przez model **Gemini 1.5 Pro**.
""")
st.markdown("---")

#  Wczytywanie danych
try:
    with open('advanced_report.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['details'])
    summary = data['summary']


    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Średnia Ocena", f"{summary['avg_relevance_score']} / 5")
    with col2:
        st.metric("Hit Rate (Retrieval)", f"{summary['hit_rate_percent']}%")
    with col3:
        st.metric("Średnie Opóźnienie", f"{summary['avg_latency_sec']}s")
    with col4:
        st.metric("Całkowity Koszt Audytu", f"${summary['total_audit_cost_usd']}")

    st.markdown("---")

    #  Sekcja wykresów
    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.subheader("📈 Rozkład Ocen (Merytoryka)")
       
        fig_score = px.histogram(
            df, 
            x="score", 
            nbins=5, 
            color="score",
            color_discrete_sequence=px.colors.qualitative.G10,
            labels={'score': 'Ocena (1-5)', 'count': 'Liczba pytań'}
        )
        st.plotly_chart(fig_score, width='stretch')

    with right_chart:
        st.subheader("⏱️ Latency vs 💰 Cost per Query")
        fig_scatter = px.scatter(
            df, 
            x="latency", 
            y="cost_usd", 
            color="score",
            size="latency", 
            hover_data=['query'],
            labels={'latency': 'Czas odpowiedzi (s)', 'cost_usd': 'Koszt ($)'},
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_scatter, width='stretch')

    st.markdown("---")

    # Interaktywna tabela wyników
    st.subheader("🔍 Szczegóły Scenariuszy Testowych")
    
    # Filtry
    score_filter = st.multiselect(
        "Filtruj listę według wystawionej oceny:", 
        options=sorted(df['score'].unique()), 
        default=sorted(df['score'].unique())
    )
    
    filtered_df = df[df['score'].isin(score_filter)]
    
    # Wyświetlanie tabeli
    st.dataframe(
        filtered_df[['id', 'query', 'score', 'latency', 'is_hit', 'cost_usd']], 
        width='stretch'
    )

    
    st.markdown("---")
    st.subheader("📥 Eksport Pełnych Danych")
    st.info("Poniższy przycisk pozwala pobrać wszystkie przefiltrowane wiersze do pliku CSV, co zapobiega ucinaniu danych występującym przy eksporcie do PDF.")
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="💾 Pobierz wyniki jako plik .CSV",
        data=csv,
        file_name='rag_evaluation_full_report.csv',
        mime='text/csv',
    )

except FileNotFoundError:
    st.error("❌ Nie znaleziono pliku 'advanced_report.json'. Upewnij się, że najpierw uruchomiłeś skrypt 'test_runner.py'!")
except Exception as e:
    st.error(f"❌ Wystąpił niespodziewany błąd: {e}")

# Stopka
st.markdown("---")
st.caption("BankBot Evaluation System | Wygenerowano za pomocą Streamlit & Plotly")