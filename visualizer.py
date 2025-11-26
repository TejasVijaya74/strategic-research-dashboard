# visualizer.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import AppConfig

class ChartBuilder:
    """Factory class for generating Plotly visualization objects."""

    @staticmethod
    def plot_temporal_trends(df: pd.DataFrame) -> go.Figure:
        """Generates line chart for document volume over time."""
        fig = px.line(
            df, 
            x=AppConfig.COL_YEAR, 
            y=AppConfig.COL_DOCS, 
            color=AppConfig.COL_NAME,
            markers=True, 
            title="Research Output Growth over Time"
        )
        fig.update_layout(hovermode="x unified")
        return fig

    @staticmethod
    def plot_strategic_matrix(df: pd.DataFrame) -> go.Figure:
        """Generates scatter plot for Quality vs Quantity."""
        # Aggregate to country level for the scatter plot
        scatter_df = df.groupby(AppConfig.COL_NAME).agg({
            AppConfig.COL_DOCS: 'sum',
            AppConfig.COL_CNCI: 'mean'
        }).reset_index()

        fig = px.scatter(
            scatter_df,
            x=AppConfig.COL_DOCS,
            y=AppConfig.COL_CNCI,
            size=AppConfig.COL_DOCS,
            color=AppConfig.COL_NAME,
            text=AppConfig.COL_NAME,
            title="Strategic Matrix: Quality (Impact) vs. Quantity (Volume)",
            labels={
                AppConfig.COL_CNCI: 'Impact (CNCI)', 
                AppConfig.COL_DOCS: 'Volume (Documents)'
            }
        )
        
        # Add quadrants/reference lines
        avg_x = scatter_df[AppConfig.COL_DOCS].mean()
        avg_y = scatter_df[AppConfig.COL_CNCI].mean()
        
        fig.add_hline(y=avg_y, line_dash="dash", line_color="grey", annotation_text="Avg Quality")
        fig.add_vline(x=avg_x, line_dash="dash", line_color="grey", annotation_text="Avg Volume")
        fig.update_traces(textposition='top center')
        return fig

    @staticmethod
    def plot_leaderboard(df: pd.DataFrame) -> go.Figure:
        """Generates horizontal bar chart for weighted impact."""
        df_temp = df.copy()
        df_temp['Weighted_Impact'] = df_temp[AppConfig.COL_CNCI] * df_temp[AppConfig.COL_DOCS]
        
        leaderboard = df_temp.groupby(AppConfig.COL_NAME).agg({
            'Weighted_Impact': 'sum',
            AppConfig.COL_DOCS: 'sum'
        })
        
        leaderboard['Weighted_CNCI'] = leaderboard['Weighted_Impact'] / leaderboard[AppConfig.COL_DOCS]
        leaderboard = leaderboard.sort_values('Weighted_CNCI', ascending=False).head(10).reset_index()

        fig = px.bar(
            leaderboard, 
            x='Weighted_CNCI', 
            y=AppConfig.COL_NAME, 
            orientation='h',
            title="Top 10 Performers (Weighted Citation Impact)",
            color='Weighted_CNCI',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        return fig