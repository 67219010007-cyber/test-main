import pandas as pd
import numpy as np
import streamlit as st

def calculate_risk_scores(df):
    """
    Calculates composite risk scores based on domain-weighted logic.
    """
    if df.empty:
        return df

    df_risk = df.copy()
    
    # Initialize Score
    df_risk['Crash_Risk_Score'] = 0
    
    # 1. Injury Severity Weighting
    if 'Injury Severity' in df_risk.columns:
        df_risk.loc[df_risk['Injury Severity'].str.contains('FATAL', na=False, case=False), 'Crash_Risk_Score'] += 5
        df_risk.loc[df_risk['Injury Severity'].str.contains('SUSPECTED SERIOUS', na=False, case=False), 'Crash_Risk_Score'] += 3
        
    # 2. Driver Substance Abuse
    if 'Driver Substance Abuse' in df_risk.columns:
        abuse_mask = df_risk['Driver Substance Abuse'].str.contains('ALCOHOL|DRUGS', na=False, case=False)
        df_risk.loc[abuse_mask, 'Crash_Risk_Score'] += 3
        
    # 3. Weather Indicators
    if 'Weather' in df_risk.columns:
        weather_mask = df_risk['Weather'].str.contains('RAIN|SNOW|SLEET', na=False, case=False)
        df_risk.loc[weather_mask, 'Crash_Risk_Score'] += 2
        
    # 4. Night Time Indicators (Light column)
    if 'Light' in df_risk.columns:
        night_mask = df_risk['Light'].str.contains('DARK', na=False, case=False)
        df_risk.loc[night_mask, 'Crash_Risk_Score'] += 2
        
    # 5. Speed Limit Indicators
    if 'Speed Limit' in df_risk.columns:
        # Ensure Speed Limit is numeric
        speed_vals = pd.to_numeric(df_risk['Speed Limit'], errors='coerce').fillna(0)
        df_risk.loc[speed_vals > 60, 'Crash_Risk_Score'] += 2

    # Risk Classification
    def classify_risk(score):
        if score >= 8: return "Critical Risk"
        if score >= 5: return "High Risk"
        if score >= 3: return "Medium Risk"
        return "Low Risk"
        
    df_risk['Risk_Level'] = df_risk['Crash_Risk_Score'].apply(classify_risk)
    
    return df_risk

@st.cache_data
def get_risk_aggregations(df):
    """
    Aggregates risk levels by various dimensions.
    """
    df_scored = calculate_risk_scores(df)
    
    # Avg Risk per Municipality
    muni_risk = df_scored.groupby('Municipality')['Crash_Risk_Score'].mean().sort_values(ascending=False).reset_index()
    
    # Risk per Vehicle Make
    make_risk = df_scored.groupby('Vehicle Make')['Crash_Risk_Score'].mean().sort_values(ascending=False).head(10).reset_index()
    
    # Risk per Hour of Day
    if 'Crash Date/Time' in df_scored.columns:
        df_scored['Hour'] = pd.to_datetime(df_scored['Crash Date/Time'], errors='coerce').dt.hour
        hour_risk = df_scored.groupby('Hour')['Crash_Risk_Score'].mean().reset_index()
    else:
        hour_risk = pd.DataFrame()
        
    return df_scored, muni_risk, make_risk, hour_risk
