import pandas as pd
import streamlit as st

def impute_missing(df, column, strategy):
    """
    Imputes missing values in a specified column.
    """
    df_clean = df.copy()
    initial_missing = df_clean[column].isna().sum()
    
    if strategy == "Mean":
        val = df_clean[column].mean()
        df_clean[column] = df_clean[column].fillna(val)
    elif strategy == "Median":
        val = df_clean[column].median()
        df_clean[column] = df_clean[column].fillna(val)
    elif strategy == "Mode":
        val = df_clean[column].mode()[0]
        df_clean[column] = df_clean[column].fillna(val)
    elif strategy == "Drop":
        df_clean = df_clean.dropna(subset=[column])
        val = "Dropped Rows"
        
    log_msg = f"Imputed '{column}' using {strategy}. Fixed {initial_missing} missing values."
    return df_clean, log_msg

def standardize_dates(df, column):
    """
    Standardizes date formats for a column.
    """
    df_clean = df.copy()
    df_clean[column] = pd.to_datetime(df_clean[column], errors='coerce')
    
    invalid_dates = df_clean[column].isna().sum()
    log_msg = f"Standardized dates in '{column}'. {invalid_dates} invalid entries coerced to NaT."
    return df_clean, log_msg

def remove_duplicates(df, subset=None):
    """
    Removes duplicate records.
    """
    df_clean = df.copy()
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=subset)
    dropped_count = initial_rows - len(df_clean)
    
    log_msg = f"Removed {dropped_count} duplicate rows."
    return df_clean, log_msg

def get_cleaning_metrics(old_df, new_df):
    """
    Returns before/after metrics.
    """
    return {
        "Rows Before": len(old_df),
        "Rows After": len(new_df),
        "Missing Before": old_df.isna().sum().sum(),
        "Missing After": new_df.isna().sum().sum()
    }
