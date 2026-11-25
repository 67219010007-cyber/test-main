import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def run_forensics_analysis(df):
    """
    Performs anomaly detection and pattern analysis on the crash dataset.
    """
    if df.empty:
        return None

    results = {}
    
    # 1. Time Pattern Analysis
    if 'Crash Date/Time' in df.columns:
        df['datetime'] = pd.to_datetime(df['Crash Date/Time'], errors='coerce')
        df['Hour'] = df['datetime'].dt.hour
        df['Is_Weekend'] = df['datetime'].dt.dayofweek >= 5
        
        peak_hour = df['Hour'].value_counts().idxmax()
        weekend_risk = len(df[df['Is_Weekend']]) / len(df) if len(df) > 0 else 0
        results['time_pattern'] = {
            "peak_hour": f"{peak_hour}:00",
            "weekend_share": f"{weekend_risk*100:.1f}%"
        }

    # 2. Environmental Pattern (Combinations)
    if 'Weather' in df.columns and 'Surface Condition' in df.columns:
        env_combo = df.groupby(['Weather', 'Surface Condition']).size().idxmax()
        results['dangerous_env'] = f"{env_combo[0]} + {env_combo[1]}"

    # 3. Anomaly Detection: Z-Score for Fatal Rates per Municipality
    if 'Municipality' in df.columns and 'Injury Severity' in df.columns:
        m_counts = df['Municipality'].value_counts()
        # Only consider municipalities with significant data (>50 crashes)
        m_list = m_counts[m_counts > 50].index
        
        m_stats = []
        overall_fatal_rate = len(df[df['Injury Severity'].str.contains('FATAL', na=False, case=False)]) / len(df)
        
        for m in m_list:
            m_df = df[df['Municipality'] == m]
            fatal_count = len(m_df[m_df['Injury Severity'].str.contains('FATAL', na=False, case=False)])
            fatal_rate = fatal_count / len(m_df)
            m_stats.append({"Municipality": m, "Fatal_Rate": fatal_rate, "Count": len(m_df)})
            
        m_stats_df = pd.DataFrame(m_stats)
        if not m_stats_df.empty:
            mean_fr = m_stats_df['Fatal_Rate'].mean()
            std_fr = m_stats_df['Fatal_Rate'].std()
            
            # Avoid division by zero
            if std_fr > 0:
                m_stats_df['Z-Score'] = (m_stats_df['Fatal_Rate'] - mean_fr) / std_fr
                anomalies = m_stats_df[m_stats_df['Z-Score'] > 2].sort_values(by='Z-Score', ascending=False)
                
                anomaly_findings = []
                for _, row in anomalies.iterrows():
                    anomaly_findings.append({
                        "id": row['Municipality'],
                        "observed": f"{row['Fatal_Rate']*100:.2f}%",
                        "expected": f"{mean_fr*100:.2f}%",
                        "deviation": f"{((row['Fatal_Rate']-mean_fr)/mean_fr)*100:.1f}%",
                        "z_score": round(row['Z-Score'], 2)
                    })
                results['anomalies'] = anomaly_findings

    return results

def get_vehicle_age_pattern(df):
    """
    Analyzes the impact of vehicle age on injury severity.
    """
    if 'Vehicle Year' not in df.columns or 'Injury Severity' not in df.columns:
        return None
        
    df_v = df.dropna(subset=['Vehicle Year'])
    current_year = pd.Timestamp.now().year
    df_v['Vehicle_Age'] = current_year - df_v['Vehicle Year']
    
    # Simple bins
    df_v['Age_Group'] = pd.cut(df_v['Vehicle_Age'], bins=[0, 5, 10, 15, 20, 100], 
                                labels=['0-5 yrs', '6-10 yrs', '11-15 yrs', '16-20 yrs', '20+ yrs'])
    
    age_fatal = df_v.groupby('Age_Group')['Injury Severity'].apply(lambda x: (x.str.contains('FATAL', case=False, na=False).sum() / len(x)) * 100).reset_index(name='Fatal Rate %')
    return age_fatal
