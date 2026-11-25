import pandas as pd

def generate_insights(df):
    """
    Generates automated strategic insights from the dataset.
    """
    if df.empty:
        return None

    insights = []

    # 1. Top Performer (Agency or Route)
    if 'Agency Name' in df.columns:
        top_agency = df['Agency Name'].value_counts().idxmax()
        count = df['Agency Name'].value_counts().max()
        insights.append({
            "title": "🏆 Dominant Agency",
            "what": f"'{top_agency}' reports the highest number of incidents ({count:,}).",
            "why": "Higher traffic volume or more rigorous reporting protocols in this agency's jurisdiction.",
            "so_what": f"This agency manages { (count/len(df))*100:.1f}% of all incidents in the current selection.",
            "now_what": "Evaluate if additional resources or specialized safety programs are needed for this specific agency."
        })

    # 2. Main Pain Point (Weather or Collision Type)
    if 'Weather' in df.columns:
        worst_weather = df['Weather'].value_counts().idxmax()
        if worst_weather != 'CLEAR':
            insights.append({
                "title": "⚠️ Environmental Risk",
                "what": f"'{worst_weather}' conditions are significantly present in incident reports.",
                "why": "Reduced visibility and compromised road surface conditions lead to higher accident rates.",
                "so_what": "Weather-related factors are a primary contributor to safety incidents.",
                "now_what": "Implement weather-responsive traffic management and public safety alerts for these specific conditions."
            })
    
    # 3. Data Integrity Insight
    missing_pct = df.isna().mean().mean() * 100
    if missing_pct > 5:
        insights.append({
            "title": "📉 Data Quality Alert",
            "what": f"Dataset has a total missingness rate of {missing_pct:.2f}%.",
            "why": "Inconsistent field entry or lack of mandatory field enforcement in the reporting system.",
            "so_what": "Missing data can skew analysis results and lead to inaccurate policy decisions.",
            "now_what": "Audit the data entry process and implement stricter validation rules at the source of collection."
        })
    else:
        insights.append({
            "title": "✨ Data Reliability",
            "what": "The dataset shows high completeness with minimal missing values.",
            "why": "Effective reporting standards and data validation early in the pipeline.",
            "so_what": "High-confidence decisions can be made based on this reliable data source.",
            "now_what": "Maintain current standards and focus on advanced predictive modeling."
        })

    return insights
