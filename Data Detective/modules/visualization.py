import plotly.express as px
import pandas as pd
import streamlit as st

def plot_trend(df, date_col, value_col=None, rolling=False):
    """
    Plots a time-series trend.
    """
    df_plot = df.copy()
    df_plot[date_col] = pd.to_datetime(df_plot[date_col], errors='coerce')
    df_plot = df_plot.dropna(subset=[date_col])
    
    # Aggregate by day
    df_trend = df_plot.resample('D', on=date_col).size().reset_index(name='Crash Count')
    
    fig = px.line(df_trend, x=date_col, y='Crash Count', title=f"Trend Analysis: {date_col}")
    
    if rolling:
        df_trend['Rolling Mean'] = df_trend['Crash Count'].rolling(window=7).mean()
        fig.add_scatter(x=df_trend[date_col], y=df_trend['Rolling Mean'], name='7-Day Rolling Mean')
        
    fig.update_layout(hovermode='x unified', template='plotly_white')
    return fig

def plot_distribution(df, column, show_outliers=True):
    """
    Plots distribution as a boxplot or histogram.
    """
    # Sample if too large for performance
    if len(df) > 50000:
        df_sample = df.sample(10000)
        title_suffix = " (Sampled 10k rows)"
    else:
        df_sample = df
        title_suffix = ""

    if show_outliers:
        fig = px.box(df_sample, y=column, title=f"Distribution: {column}{title_suffix}")
    else:
        # Filter outliers using IQR
        Q1 = df_sample[column].quantile(0.25)
        Q3 = df_sample[column].quantile(0.75)
        IQR = Q3 - Q1
        filtered_df = df_sample[(df_sample[column] >= Q1 - 1.5 * IQR) & (df_sample[column] <= Q3 + 1.5 * IQR)]
        fig = px.box(filtered_df, y=column, title=f"Distribution: {column}{title_suffix} (Outliers Hidden)")
        
    fig.update_layout(template='plotly_white')
    return fig

def plot_comparison(df, column, top_n=10):
    """
    Plots top categories by count.
    """
    counts = df[column].value_counts().head(top_n).reset_index()
    counts.columns = [column, 'Count']
    
    fig = px.bar(counts, x=column, y='Count', color='Count',
                 title=f"Top {top_n} {column}", 
                 color_continuous_scale='Blues')
    
    fig.update_layout(xaxis={'categoryorder':'total descending'}, template='plotly_white')
    return fig
