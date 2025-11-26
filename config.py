# config.py

class AppConfig:
    """Central configuration for column names, settings, and constants."""
    
    # App Settings
    APP_TITLE = "Strategic Research Intelligence"
    DEFAULT_FILE = 'publications.csv'
    
    # Dataset Column Mappings
    COL_NAME = 'Name'
    COL_YEAR = 'year'
    COL_DOCS = 'Web of Science Documents'
    COL_CITES = 'Times Cited'
    COL_CNCI = 'Category Normalized Citation Impact'
    COL_COLLAB_CNCI = 'Collab-CNCI'
    
    # Aggregation Strategy
    # Columns to SUM (Volume metrics)
    SUM_COLS = [COL_DOCS, COL_CITES, 'Documents in Top 1%', 'Documents in Top 10%']
    
    # Columns to AVERAGE (Quality/Ratio metrics)
    MEAN_COLS = [COL_COLLAB_CNCI, 'Rank', '% Docs Cited', COL_CNCI, 
                 '% Documents in Top 1%', '% Documents in Top 10%']