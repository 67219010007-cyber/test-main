import pandas as pd
import numpy as np
from datetime import datetime

def run_audit(df):
    """
    Performs a 4-dimension Data Quality Audit.
    Returns:
        dict: Audit results including scores, table data, and summary.
    """
    if df.empty:
        return None

    # 1. Completeness Check
    completeness_records = []
    key_fields = ['Report Number', 'Crash Date/Time', 'Vehicle ID', 'Person ID']
    critical_missing = False
    
    total_rows = len(df)
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_pct = (missing_count / total_rows) * 100
        unique_count = df[col].nunique()
        
        status = "Valid"
        if missing_pct > 10:
            status = "Critical"
        elif missing_pct > 1:
            status = "Warning"
            
        if col in key_fields and missing_pct > 1:
            critical_missing = True
            
        completeness_records.append({
            "Column Name": col,
            "Type": str(df[col].dtype),
            "% Missing": round(missing_pct, 2),
            "Unique Values": unique_count,
            "Status": status
        })

    # 2. Consistency Check (Duplicates)
    # Using 'Report Number' as Primary Key candidate for this check
    dup_pk_count = df.duplicated(subset=['Report Number']).sum() if 'Report Number' in df.columns else 0
    duplicate_rate = (dup_pk_count / total_rows) * 100

    # 3. Accuracy Check (Logical Errors)
    accuracy_issues = []
    # Check for Speed Limit (usually 0-100+)
    if 'Speed Limit' in df.columns:
        speed_errors = (df['Speed Limit'] < 0).sum()
        if speed_errors > 0:
            accuracy_issues.append(f"Found {speed_errors} negative speed limits.")
            
    # Check for Vehicle Year (should not be in the far future)
    if 'Vehicle Year' in df.columns:
        future_year = datetime.now().year + 1
        year_errors = (df['Vehicle Year'] > future_year).sum()
        if year_errors > 0:
            accuracy_issues.append(f"Found {year_errors} vehicles with future model years.")

    # 4. Timeliness Check
    timeliness_info = "Unknown"
    if 'Crash Date/Time' in df.columns:
        try:
            temp_dates = pd.to_datetime(df['Crash Date/Time'], errors='coerce')
            latest_date = temp_dates.max()
            if pd.notnull(latest_date):
                timeliness_info = latest_date.strftime('%Y-%m-%d %H:%M')
        except:
            timeliness_info = "Formatting Error"

    # Calculate Overall Health Score
    # Simple weighted formula
    completeness_score = max(0, 100 - (df.isna().mean().mean() * 100))
    consistency_score = max(0, 100 - (duplicate_rate * 2))
    accuracy_score = max(0, 100 - (len(accuracy_issues) * 5))
    
    overall_score = (completeness_score * 0.4) + (consistency_score * 0.4) + (accuracy_score * 0.2)

    # Textual Summary
    summary_notes = []
    if critical_missing:
        summary_notes.append("⚠️ Critical: Key fields have more than 1% missing data.")
    if duplicate_rate > 5:
        summary_notes.append(f"⚠️ High Duplicate Rate: {duplicate_rate:.2f}% duplicates detected.")
    if accuracy_issues:
        summary_notes.extend(accuracy_issues)
    
    if not summary_notes:
        summary_notes.append("✅ Data looks clean and consistent across all dimensions.")

    return {
        "score": round(overall_score),
        "table": completeness_records,
        "duplicate_rate": round(duplicate_rate, 2),
        "timeliness": timeliness_info,
        "summary": summary_notes
    }
