import pandas as pd
import streamlit as st
import io
from datetime import datetime

def generate_csv_bytes(df: pd.DataFrame) -> bytes:
    """Helper to convert DF to CSV bytes for download."""
    if df is None or df.empty:
        return b""
    return df.to_csv(index=False).encode('utf-8')

def generate_excel_bytes(sheets_dict: dict) -> bytes:
    """Helper to convert multiple DFs to multi-sheet Excel bytes."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in sheets_dict.items():
            if df is not None and not df.empty:
                # Limit sheet name to 31 chars (Excel limit)
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    return output.getvalue()

def get_executive_summary_text(df, audit_score, fatal_rate, top_muni, top_make, health_score) -> str:
    """Generates a text-based executive summary briefing."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary = f"""NATIONAL DATA ASSESSMENT 2024 - EXECUTIVE BRIEFING
Generated: {now}
--------------------------------------------------

1. DATA QUALITY STANDARDS
- Data Health Score: {health_score}%
- Audit Integrity: {audit_score}%
- Total Records Analyzed: {len(df):,}

2. RISK & SAFETY INTELLIGENCE
- Overall Fatal Rate: {fatal_rate:.2f}%
- Primary Risk Zone: {top_muni}
- Vehicle Risk Profile: {top_make}

3. STRATEGIC RECOMMENDATION
Based on current patterns, immediate preventive measures are 
recommended in {top_muni} region, specifically targeting 
high-risk temporal windows identified in Phase 7-8 analysis.

--------------------------------------------------
END OF BRIEFING
"""
    return summary

def check_deployment_readiness(df, geo_quality):
    """Verifies system stability for national deployment."""
    checks = []
    
    # 1. Data Integrity
    if not df.empty:
        checks.append(("🟢 Master Dataset Loaded", True))
    else:
        checks.append(("🔴 Master Dataset Missing", False))
        
    # 2. Geo Quality
    if geo_quality >= 80:
        checks.append((f"🟢 High-Quality Geo Data ({geo_quality}%)", True))
    elif geo_quality > 50:
        checks.append((f"🟡 Moderate Geo Data ({geo_quality}%)", True))
    else:
        checks.append((f"🔴 Critical Geo Issues ({geo_quality}%)", False))
        
    # 3. Required Columns
    needed = ['Latitude', 'Longitude', 'Municipality', 'Injury Severity']
    missing = [c for c in needed if c not in df.columns]
    if not missing:
        checks.append(("🟢 All Critical Schema Validated", True))
    else:
        checks.append((f"🔴 Schema Missing: {', '.join(missing)}", False))
        
    return checks
