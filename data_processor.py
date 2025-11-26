# data_processor.py
import pandas as pd
import streamlit as st
from config import AppConfig

class DataProcessor:
    """Handles data loading, aggregation, and feature engineering."""

    @staticmethod
    @st.cache_data(ttl=3600)  # Cache data to prevent reloading on every interaction
    def load_and_process(file_source) -> pd.DataFrame:
        """
        Loads CSV, aggregates duplicates, and flags anomalies.
        Returns None if loading fails.
        """
        try:
            # 1. Load Data
            raw_df = pd.read_csv(file_source)
        except Exception as e:
            st.error(f"Critical Error loading file: {e}")
            return None

        # 2. Define Aggregation Logic
        agg_dict = {c: 'sum' for c in AppConfig.SUM_COLS}
        agg_dict.update({c: 'mean' for c in AppConfig.MEAN_COLS})

        try:
            # 3. Aggregate to remove duplicates (Country + Year)
            df_processed = raw_df.groupby(
                [AppConfig.COL_NAME, AppConfig.COL_YEAR], as_index=False
            ).agg(agg_dict)
            
            # 4. Feature Engineering
            df_processed = DataProcessor._detect_anomalies(df_processed)
            return df_processed
            
        except KeyError as e:
            st.error(f"Schema Error: Missing column {e} in the dataset.")
            return None

    @staticmethod
    def _detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
        """
        Internal method to calculate Z-scores for citations.
        Marks a row as 'Is_Anomaly' if Z-score > 2.
        """
        if df[AppConfig.COL_CITES].std() > 0:
            mean_val = df[AppConfig.COL_CITES].mean()
            std_val = df[AppConfig.COL_CITES].std()
            
            df['z_score'] = (df[AppConfig.COL_CITES] - mean_val) / std_val
            df['Is_Anomaly'] = df['z_score'].abs() > 2
        else:
            df['Is_Anomaly'] = False
        
        return df