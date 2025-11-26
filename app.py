# app.py
import streamlit as st
import pandas as pd

# Import our custom modules
from config import AppConfig
from data_processor import DataProcessor
from visualizer import ChartBuilder

# UI HELPER FUNCTIONS
def inject_custom_css():
    """Injects CSS for KPI cards and ensures Dark Mode compatibility."""
    st.markdown("""
        <style>
        [data-testid="stMetric"] {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #dcdcdc;
        }
        /* Force text to be black so it is visible in Dark Mode */
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] {
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Renders filters and returns the filtered DataFrame."""
    st.sidebar.header("⚙️ Data Pipeline")
    
    # Pre-select top 5 volume leaders
    top_volume = df.groupby(AppConfig.COL_NAME)[AppConfig.COL_DOCS].sum().nlargest(5).index.tolist()
    all_countries = sorted(df[AppConfig.COL_NAME].unique())
    
    st.sidebar.subheader("🔍 Filters")
    selected_countries = st.sidebar.multiselect(
        "Select Entities", 
        all_countries, 
        default=top_volume
    )
    
    if selected_countries:
        return df[df[AppConfig.COL_NAME].isin(selected_countries)]
    return df

def render_kpi_section(df: pd.DataFrame):
    """Renders the top KPI cards."""
    st.subheader("📊 Executive Summary")
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric("Total Documents", f"{df[AppConfig.COL_DOCS].sum():,.0f}")
    c2.metric("Total Citations", f"{df[AppConfig.COL_CITES].sum():,.0f}")
    c3.metric("Avg Impact (CNCI)", f"{df[AppConfig.COL_CNCI].mean():.2f}")
    c4.metric("Anomalies Detected", f"{df['Is_Anomaly'].sum()}", delta_color="inverse")


# MAIN APP LOOP
def main():
    st.set_page_config(page_title=AppConfig.APP_TITLE, layout="wide", page_icon="📈")
    inject_custom_css()
    
    st.title(f"🌍 {AppConfig.APP_TITLE}")
    st.markdown("Automated insights into global research trends, quality vs. quantity, and anomaly detection.")

    # 1. File Upload / Ingestion
    uploaded_file = st.sidebar.file_uploader("Upload Dataset (CSV)", type=['csv'])
    file_path = uploaded_file if uploaded_file else AppConfig.DEFAULT_FILE
    
    if not uploaded_file:
        st.sidebar.info(f"Using default dataset: `{AppConfig.DEFAULT_FILE}`")

    # 2. Data Processing (via data_processor module)
    df = DataProcessor.load_and_process(file_path)
    if df is None:
        st.stop()

    # 3. Filtering
    df_filtered = render_sidebar(df)

    # 4. KPI Display
    render_kpi_section(df_filtered)

    # 5. Visualizations (via visualizer module)
    tab_trends, tab_matrix, tab_details = st.tabs(["📈 Trends", "🧩 Strategy Matrix", "🏆 Leaderboard & Details"])

    with tab_trends:
        st.plotly_chart(ChartBuilder.plot_temporal_trends(df_filtered), use_container_width=True)
        st.info("💡 **Insight:** Steep upward slopes indicate rapid R&D scaling (common in emerging economies).")

    with tab_matrix:
        st.plotly_chart(ChartBuilder.plot_strategic_matrix(df_filtered), use_container_width=True)
        st.markdown("**Matrix Guide:** Top-Right = Strategic Leaders (High Vol/High Impact). Top-Left = Efficiency Players.")

    with tab_details:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(ChartBuilder.plot_leaderboard(df), use_container_width=True)
        with c2:
            st.subheader("⚠️ Anomaly Detection Log")
            st.caption("Years with statistically significant deviation (>2 Z-Scores) in citation counts.")
            anomalies = df[df['Is_Anomaly']].sort_values(AppConfig.COL_YEAR, ascending=False)
            cols_to_show = [AppConfig.COL_NAME, AppConfig.COL_YEAR, AppConfig.COL_DOCS, AppConfig.COL_CITES]
            st.dataframe(anomalies[cols_to_show], use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()