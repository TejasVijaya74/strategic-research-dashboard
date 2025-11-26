# Strategic Research Intelligence Dashboard

An interactive dashboard for analyzing global research trends, quality vs. quantity metrics, and statistical anomalies in publication data.

🔗 **Live Demo:** [Click Here ](https://eda-publish.streamlit.app/) 

---

## Project Structure

This project follows a **modular software engineering architecture**:

- **app.py** – Main entry point and UI layout  
- **config.py** – Central configuration for constants and settings  
- **data_processor.py** – Logic for data ingestion, cleaning, and aggregation  
- **visualizer.py** – Factory class for generating Plotly charts  

---

## Setup Instructions

### 1. Prerequisites

Ensure you have **Python 3.8+** installed. 

### 2. Installation

Install all required dependencies:

**pip install -r requirements.txt**


### 3. Running the Application

Navigate to your project directory and start the Streamlit app:

**streamlit run app.py**


---

## Features

### 1. Data Pipeline

- Automatically aggregates duplicate country–year entries for accurate analysis.  

### 2. Anomaly Detection

- Uses Z-score–based statistical analysis to detect unusual citation patterns and outliers in research output. 

### 3. Interactive Visualizations

- Time-series research trend analysis.  
- Strategic quadrant matrix for quality vs. quantity insights.  
- Interactive charts with hover tooltips and filters for exploratory analysis. 

