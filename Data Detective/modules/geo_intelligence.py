import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from sklearn.cluster import DBSCAN

@st.cache_data
def analyze_geospatial(df):
    """
    Validates coordinates and performs spatial aggregations.
    """
    if df.empty:
        return None

    df_geo = df.copy()
    
    # 1. Validate Coordinates
    # Drop rows with missing lat/lon for spatial analysis
    initial_count = len(df_geo)
    df_geo = df_geo.dropna(subset=['Latitude', 'Longitude'])
    
    # Range check
    valid_mask = (df_geo['Latitude'].between(-90, 90)) & (df_geo['Longitude'].between(-180, 180))
    df_valid = df_geo[valid_mask].copy()
    
    valid_count = len(df_valid)
    quality_pct = (valid_count / initial_count) * 100 if initial_count > 0 else 0
    
    # 2. Spatial Aggregations
    municipality_agg = df_valid['Municipality'].value_counts().reset_index()
    municipality_agg.columns = ['Municipality', 'Crash Count']
    
    state_agg = df_valid['Drivers License State'].value_counts().reset_index()
    state_agg.columns = ['Drivers License State', 'Crash Count']
    
    # Fatal Rate per Municipality
    if 'Injury Severity' in df_valid.columns:
        fatal_counts = df_valid[df_valid['Injury Severity'].str.contains('FATAL', na=False, case=False)]
        fatal_agg = fatal_counts['Municipality'].value_counts().reset_index()
        fatal_agg.columns = ['Municipality', 'Fatal Count']
        
        m_stats = municipality_agg.merge(fatal_agg, on='Municipality', how='left').fillna(0)
        m_stats['Fatal Rate %'] = (m_stats['Fatal Count'] / m_stats['Crash Count']) * 100
    else:
        m_stats = municipality_agg
        m_stats['Fatal Rate %'] = 0

    return {
        "df_valid": df_valid,
        "quality_pct": round(quality_pct, 2),
        "m_stats": m_stats.sort_values(by='Fatal Rate %', ascending=False),
        "state_agg": state_agg
    }

def get_geo_clusters(df, eps_km=5, min_samples=10):
    """
    Performs simple DBSCAN clustering to identify hotspots.
    eps_km is approximate (0.01 degrees ~ 1.1km)
    """
    if len(df) < min_samples:
        return df.assign(Cluster=-1)
    
    # Convert km to approximate degrees
    eps_deg = eps_km / 111.0
    
    coords = df[['Latitude', 'Longitude']].values
    db = DBSCAN(eps=eps_deg, min_samples=min_samples).fit(coords)
    
    df_clustered = df.copy()
    df_clustered['Cluster'] = db.labels_
    return df_clustered

def plot_crash_map(df, mode="Scatter", sample_limit=None):
    """
    Generates mapping visualizations with performance optimization.
    """
    if df.empty:
        return None
        
    # Standardize sample limits for performance
    if sample_limit is None:
        if mode == "Scatter":
            sample_limit = 5000  # Scatter is heaviest
        elif mode == "Cluster":
            sample_limit = 8000
        else:
            sample_limit = 20000 # Density is lighter
            
    # Sampling for performance
    if len(df) > sample_limit:
        df_plot = df.sample(sample_limit, random_state=42)
        note = f" (Optimized View: {sample_limit:,} points)"
    else:
        df_plot = df
        note = " (All valid points)"

    # Mapbox configuration
    map_style = "carto-positron"
    
    if mode == "Scatter":
        fig = px.scatter_mapbox(df_plot, lat="Latitude", lon="Longitude", 
                                color="Injury Severity" if "Injury Severity" in df_plot.columns else None,
                                size_max=12, zoom=9,
                                mapbox_style=map_style,
                                title=f"Crash Distribution{note}",
                                opacity=0.6)
    elif mode == "Density":
        fig = px.density_mapbox(df_plot, lat="Latitude", lon="Longitude", 
                                radius=8, zoom=9,
                                mapbox_style=map_style,
                                title=f"High-Density Crash Intensity{note}",
                                color_continuous_scale="Viridis")
    elif mode == "Cluster":
        # Hotspot detection on original data, then sample for visual
        # or just sample for speed if extremely large
        df_clu = get_geo_clusters(df_plot)
        df_clu_clean = df_clu[df_clu['Cluster'] != -1]
        fig = px.scatter_mapbox(df_clu_clean, lat="Latitude", lon="Longitude", 
                                color="Cluster", zoom=9,
                                mapbox_style=map_style,
                                title=f"Identified High-Risk Hotspots{note}",
                                color_discrete_sequence=px.colors.qualitative.Bold)
        if df_clu_clean.empty:
            st.warning("No significant clusters found in the current sample.")

    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, hovermode='closest')
    return fig
