import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data(file_path):
    """
    Loads data from a CSV file with caching for performance.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: The loaded dataset.
    """
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    # Using low_memory=False for better type inference on large datasets
    try:
        df = pd.read_csv(file_path, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def get_data_summary(df):
    """
    Returns a basic summary of the dataframe.
    """
    if df.empty:
        return "No data available."
    return f"Rows: {len(df):,}, Columns: {len(df.columns)}"
