import streamlit as st
import pandas as pd
from utils.data_loader import load_data, get_data_summary
import os
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="National Data Assessment 2024",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session State
if 'cleaning_log' not in st.session_state:
    st.session_state['cleaning_log'] = []
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'original_df' not in st.session_state:
    st.session_state['original_df'] = None
if 'drill_down' not in st.session_state:
    st.session_state['drill_down'] = {"level": "Country", "value": None}

# Load Custom CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles/main.css")

# Breadcrumb Navigation
def show_breadcrumb():
    level = st.session_state['drill_down']['level']
    val = st.session_state['drill_down']['value']
    
    st.markdown(f"**📍 Filter Tier:** `Country` {' > `' + val + '`' if val else ''}")
    if st.button("⬅️ Reset Drill-Down"):
        st.session_state['drill_down'] = {"level": "Country", "value": None}
        st.rerun()

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: #3b82f6; font-size: 2.2rem; margin-bottom: 0;">🏆</h1>
            <h2 style="color: white; font-size: 1.2rem; margin-top: 0;">Data Intel 2024</h2>
            <p style="color: #94a3b8; font-size: 0.8rem;">National Level Assessment</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "Main Menu",
        ["🏠 Dashboard Home", "🔍 Quality Audit", "🧹 Data Cleaning", "📊 Detailed VIZ", 
         "📍 Geo Mapping", "🚨 Risk Analysis", "🧪 Pattern Forensics", "💡 Business Insights", "📤 Export Center"]
    )

# Load Data logic
DATA_PATH = "1_crash_reports.csv"

if st.session_state['df'] is None:
    with st.spinner("Initializing high-performance cache..."):
        df = load_data(DATA_PATH)
        if not df.empty:
            st.session_state['original_df'] = df.copy()
            st.session_state['df'] = df.copy()
            st.sidebar.success(f"✓ {len(df):,} records ready")
        else:
            st.sidebar.error("Error: Dataset missing.")

# Sidebar Master Filters
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Global Controls")
if st.session_state['df'] is not None:
    selected_agency = st.sidebar.multiselect("Federal Agency", options=st.session_state['df']['Agency Name'].unique())
    selected_weather = st.sidebar.multiselect("Filter by Weather", options=st.session_state['df']['Weather'].unique())

# Apply Master Filters
filtered_df = st.session_state['df']
if filtered_df is not None:
    # 1. Apply Drill-Down
    if st.session_state['drill_down']['level'] == 'State':
        filtered_df = filtered_df[filtered_df['Drivers License State'] == st.session_state['drill_down']['value']]
    elif st.session_state['drill_down']['level'] == 'Municipality':
        filtered_df = filtered_df[filtered_df['Municipality'] == st.session_state['drill_down']['value']]
        
    # 2. Apply Sidebar Filters
    if selected_agency:
        filtered_df = filtered_df[filtered_df['Agency Name'].isin(selected_agency)]
    if selected_weather:
        filtered_df = filtered_df[filtered_df['Weather'].isin(selected_weather)]

# Sidebar Master Controls
st.sidebar.markdown("---")
with st.sidebar:
    st.subheader("⚙️ System Deployment")
    if filtered_df is not None:
        # Avoid circular imports by using local or utility calls
        from modules.geo_intelligence import analyze_geospatial
        geo_data = analyze_geospatial(filtered_df)
        geo_q = geo_data['quality_pct'] if geo_data else 0
        
        from modules.export_center import check_deployment_readiness
        readiness = check_deployment_readiness(filtered_df, geo_q)
        
        ready_score = sum(1 for _, ok in readiness if ok)
        if ready_score == len(readiness):
            st.success("🟢 System Deployment: READY")
        else:
            st.warning("🟡 System Deployment: WARNING")
        
        with st.expander("View Readiness Log"):
            for msg, ok in readiness:
                st.write(f"{'✅' if ok else '❌'} {msg}")

# Master Dashboard Summary Logic
def show_master_dashboard(df):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 60px; border-radius: 20px; color: white; margin-bottom: 40px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="display: flex; align-items: centre; gap: 20px;">
                <div style="background: rgba(59, 130, 246, 0.2); padding: 20px; border-radius: 15px;">
                    <h1 style="margin: 0; font-size: 3rem;">📊</h1>
                </div>
                <div>
                    <h1 style="color: white; font-size: 3rem; margin: 0; letter-spacing: -0.05em;">National Intelligence <span style="color: #3b82f6;">Premium</span></h1>
                    <p style="font-size: 1.25rem; opacity: 0.8; font-weight: 300; margin-top: 10px;">Integrated Crash Risk & Geo-Spatial Assessment 2024</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if df is not None and not df.empty:
        show_breadcrumb()
        
        # Performance optimized summary
        from modules.data_audit import run_audit
        audit = run_audit(df)
        
        from modules.risk_scoring import calculate_risk_scores
        scored_df = calculate_risk_scores(df)
        avg_risk = scored_df['Crash_Risk_Score'].mean()
        high_risk_rows = scored_df[scored_df['Risk_Level'].isin(['High Risk', 'Critical Risk'])]
        high_risk_pct = (len(high_risk_rows) / len(scored_df)) * 100
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-card"><div class="metric-value">{audit['score']}%</div><div class="metric-label">Health Score</div></div>
            <div class="metric-card"><div class="metric-value">{avg_risk:.2f}</div><div class="metric-label">Avg Risk Score</div></div>
            <div class="metric-card"><div class="metric-value">{high_risk_pct:.1f}%</div><div class="metric-label">High Risk Rate</div></div>
            <div class="metric-card"><div class="metric-value">{len(df):,}</div><div class="metric-label">Active Records</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Unified Visuals
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("📍 Risk Hotspot Concentration")
            from modules.geo_intelligence import analyze_geospatial, plot_crash_map
            geo = analyze_geospatial(df)
            if geo: st.plotly_chart(plot_crash_map(geo['df_valid'], mode="Density"), use_container_width=True)
        with c2:
            st.subheader("🚨 Risk Severity Profile")
            import plotly.express as px
            risk_fig = px.pie(scored_df, names="Risk_Level", color="Risk_Level", hole=0.5,
                        color_discrete_map={"Low Risk": "#10b981", "Medium Risk": "#f59e0b", "High Risk": "#ef4444", "Critical Risk": "#7f1d1d"})
            st.plotly_chart(risk_fig, use_container_width=True)
            
        st.markdown("---")
        st.subheader("📋 Top Strategic Risk Areas")
        st.dataframe(geo['m_stats'].head(10), use_container_width=True)

# Sidebar History Log
st.sidebar.markdown("---")
st.sidebar.subheader("📜 Transformation Steps")
if st.session_state['cleaning_log']:
    for log in st.session_state['cleaning_log']:
        st.sidebar.info(log)
else:
    st.sidebar.write("No transformations recorded.")

# Page Routing
if menu == "🏠 Dashboard Home":
    if filtered_df is not None:
        show_master_dashboard(filtered_df)
    else:
        st.info("Dataset initialization required. Please check data source.")

elif menu == "🔍 Quality Audit":
    st.markdown('<h1 style="font-size: 2.5rem; margin-bottom: 30px;">🔍 Data Quality Audit</h1>', unsafe_allow_html=True)
    if filtered_df is not None:
        from modules.data_audit import run_audit
        with st.spinner("Running high-performance audit..."):
            audit_results = run_audit(filtered_df)
        if audit_results:
            st.markdown(f'<div class="metric-container"><div class="metric-card"><div class="metric-value">{audit_results["score"]}%</div><div class="metric-label">Data Health Score</div></div><div class="metric-card"><div class="metric-value">{audit_results["duplicate_rate"]}%</div><div class="metric-label">Duplicate Rate</div></div><div class="metric-card"><div class="metric-value">{audit_results["timeliness"]}</div><div class="metric-label">Latest Data Entry</div></div></div>', unsafe_allow_html=True)
            st.subheader("💡 Audit Summary")
            for note in audit_results['summary']: st.info(note)
            st.subheader("📋 Column Meta-Analysis")
            audit_df = pd.DataFrame(audit_results['table'])
            def color_status(val): color = 'green' if val == 'Valid' else 'orange' if val == 'Warning' else 'red'; return f'color: {color}; font-weight: bold'
            st.dataframe(audit_df.style.applymap(color_status, subset=['Status']), use_container_width=True, height=400)
    else: st.info("Please load data on the Home page first.")

elif menu == "🧹 Data Cleaning":
    st.markdown('<h1 style="font-size: 2.5rem; margin-bottom: 30px;">🧹 Interactive Data Cleaning</h1>', unsafe_allow_html=True)
    if st.session_state['df'] is not None:
        from modules.cleaning import impute_missing, standardize_dates, remove_duplicates, get_cleaning_metrics
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("🧹 Missing Value Handling")
            target_col = st.selectbox("Select Column to Clean", st.session_state['df'].columns)
            strategy = st.radio("Imputation Strategy", ["Mean", "Median", "Mode", "Drop"], horizontal=True)
            if st.button("Apply Imputation"):
                new_df, log_msg = impute_missing(st.session_state['df'], target_col, strategy); st.session_state['df'] = new_df; st.session_state['cleaning_log'].append(log_msg); st.success(log_msg); st.rerun()
        with col2:
            st.subheader("📅 Standardization & Consistency")
            date_cols = [c for c in st.session_state['df'].columns if 'Date' in c or 'Time' in c]
            date_col = st.selectbox("Select Date Column", date_cols if date_cols else st.session_state['df'].columns)
            if st.button("Fix Date Formats"):
                new_df, log_msg = standardize_dates(st.session_state['df'], date_col); st.session_state['df'] = new_df; st.session_state['cleaning_log'].append(log_msg); st.success(log_msg); st.rerun()
            st.markdown("---")
            if st.button("🚨 Remove All Duplicates"):
                new_df, log_msg = remove_duplicates(st.session_state['df']); st.session_state['df'] = new_df; st.session_state['cleaning_log'].append(log_msg); st.success(log_msg); st.rerun()
        st.markdown("---"); st.subheader("📈 Cleaning Impact")
        if st.session_state['original_df'] is not None:
            metrics = get_cleaning_metrics(st.session_state['original_df'], st.session_state['df'])
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric("Initial Rows", f"{metrics['Rows Before']:,}"); m_col2.metric("Current Rows", f"{metrics['Rows After']:,}", delta=metrics['Rows After'] - metrics['Rows Before']); m_col3.metric("Initial Missing", f"{metrics['Missing Before']:,}"); m_col4.metric("Current Missing", f"{metrics['Missing After']:,}", delta=metrics['Missing After'] - metrics['Missing Before'], delta_color="inverse")
        if st.button("🔄 Reset to Original Data"): st.session_state['df'] = st.session_state['original_df'].copy(); st.session_state['cleaning_log'] = ["Reset to original data."]; st.rerun()
    else: st.info("Please load data on the Home page first.")

elif menu == "📊 Detailed VIZ":
    st.markdown('<h1 style="font-size: 2.5rem; margin-bottom: 30px;">📊 Detailed Analytics Visualization</h1>', unsafe_allow_html=True)
    if filtered_df is not None:
        if filtered_df.empty: st.warning("⚠️ No data matches filters.")
        else:
            from modules.visualization import plot_trend, plot_distribution, plot_comparison
            tab1, tab2, tab3 = st.tabs(["📈 Trend Analysis", "📦 Distribution", "📊 Comparisons"])
            with tab1:
                col_t, col_r = st.columns([3, 1]); date_cols = [c for c in filtered_df.columns if 'Date' in c or 'Time' in c]
                date_col = col_t.selectbox("Date Column to Plot", date_cols if date_cols else [filtered_df.columns[0]])
                use_rolling = col_r.checkbox("Show 7-Day Rolling Mean", key="rolling_chk")
                st.plotly_chart(plot_trend(filtered_df, date_col, rolling=use_rolling), use_container_width=True)
            with tab2:
                col_d, col_o = st.columns([3, 1]); num_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
                dist_col = col_d.selectbox("Numeric Column to Inspect", num_cols if num_cols else filtered_df.columns); show_o = col_o.checkbox("Show Outliers", value=True, key="outlier_chk")
                st.plotly_chart(plot_distribution(filtered_df, dist_col, show_outliers=show_o), use_container_width=True)
            with tab3:
                comp_cols = [c for c in filtered_df.columns if filtered_df[c].nunique() < 50]; comp_col = st.selectbox("Categorical Column to Compare", comp_cols if comp_cols else filtered_df.columns)
                st.plotly_chart(plot_comparison(filtered_df, comp_col), use_container_width=True)
    else: st.info("Please load data on the Home page first.")

elif menu == "📍 Geo Mapping":
    st.markdown('<h1 style="font-size: 2.5rem; margin-bottom: 30px;">📍 Geo-Spatial Risk Mapping</h1>', unsafe_allow_html=True)
    if filtered_df is not None:
        show_breadcrumb()
        from modules.geo_intelligence import analyze_geospatial, plot_crash_map
        geo_data = analyze_geospatial(filtered_df)
        if geo_data:
            st.metric("Geo Data Quality", f"{geo_data['quality_pct']}%")
            col_m, col_s = st.columns([2, 1])
            with col_s:
                view_mode = st.radio("Map Mode", ["Scatter", "Density", "Cluster"], horizontal=True)
                st.subheader("🏙 High Risk Municipalities")
                st.dataframe(geo_data['m_stats'].head(10), use_container_width=True)
                selected_m = st.selectbox("Drill-Down to Municipality", ["None"] + list(geo_data['m_stats']['Municipality'].unique()))
                if selected_m != "None" and st.button("📍 Focus on Area"):
                    st.session_state['drill_down'] = {"level": "Municipality", "value": selected_m}; st.rerun()
            with col_m:
                st.plotly_chart(plot_crash_map(geo_data['df_valid'], mode=view_mode), use_container_width=True)
    else: st.info("Load data first.")

elif menu == "🚨 Risk Analysis":
    st.markdown('<h1 style="font-size: 2.5rem; margin-bottom: 30px;">🚨 Multi-Factor Risk Assessment</h1>', unsafe_allow_html=True)
    if filtered_df is not None:
        from modules.risk_scoring import get_risk_aggregations
        df_scored, m_risk, make_risk, hour_risk = get_risk_aggregations(filtered_df)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Risk Score Distribution")
            fig = px.histogram(df_scored, x="Crash_Risk_Score", color="Risk_Level", barmode="overlay")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("🔝 Top 10 High Risk Areas")
            st.dataframe(m_risk.head(10), use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("🏎 High Risk Vehicle Makes")
            st.bar_chart(make_risk.set_index('Vehicle Make'))
        with col4:
            st.subheader("⏰ Risk by Hour of Day")
            if not hour_risk.empty: st.line_chart(hour_risk.set_index('Hour'))
    else: st.info("Load data first.")

elif menu == "🧪 Pattern Forensics":
    st.markdown('<h1 style="font-size: 2.5rem; margin-bottom: 30px;">🧪 Advanced Data Forensics</h1>', unsafe_allow_html=True)
    if filtered_df is not None:
        from modules.forensics import run_forensics_analysis, get_vehicle_age_pattern
        results = run_forensics_analysis(filtered_df)
        if results:
            st.subheader("🔍 Statistical Anomalies (Z-Score > 2)")
            if 'anomalies' in results:
                for anomaly in results['anomalies']:
                    with st.expander(f"Anomaly: {anomaly['id']}"):
                        st.write(f"Observed Fatal Rate: **{anomaly['observed']}** (Expected: {anomaly['expected']})")
                        st.write(f"Deviation: **{anomaly['deviation']}** | Z-Score: **{anomaly['z_score']}**")
            else: st.info("No significant statistical anomalies detected.")
            st.subheader("🚗 Vehicle Age Impact")
            age_data = get_vehicle_age_pattern(filtered_df)
            if age_data is not None: st.bar_chart(age_data.set_index('Age_Group'))
    else: st.info("Load data first.")

elif menu == "💡 Business Insights":
    st.markdown('<h1 style="font-size: 2.5rem; margin-bottom: 30px;">💡 Strategic Business Insights</h1>', unsafe_allow_html=True)
    if filtered_df is not None:
        from modules.insights import generate_insights
        with st.spinner("Generating..."):
            insights_list = generate_insights(filtered_df)
        if insights_list:
            for item in insights_list:
                with st.expander(f"{item['title']}", expanded=True):
                    st.markdown(f'<div class="insight-box"><div class="insight-title">💡 Key Insight</div><ul><li><strong>What:</strong> {item["what"]}</li><li><strong>Why:</strong> {item["why"]}</li><li><strong>So What:</strong> {item["so_what"]}</li><li><strong>Now What:</strong> {item["now_what"]}</li></ul></div>', unsafe_allow_html=True)
    else: st.info("Load data first.")

elif menu == "📤 Export Center":
    st.markdown('<h1 style="font-size: 2.5rem; margin-bottom: 30px;">📤 Professional Export & Reporting</h1>', unsafe_allow_html=True)
    if filtered_df is not None:
        from modules.export_center import generate_csv_bytes, generate_excel_bytes, get_executive_summary_text
        from modules.data_audit import run_audit
        from modules.risk_scoring import calculate_risk_scores
        from modules.geo_intelligence import analyze_geospatial

        with st.spinner("Preparing export bundles..."):
            audit_data = run_audit(filtered_df)
            scored_data = calculate_risk_scores(filtered_df)
            geo_data = analyze_geospatial(filtered_df)

        # Performance Safeguards
        if len(filtered_df) > 150000:
            st.warning("⚠️ Large Dataset: Full export may be slow. Sampling recommended.")
            use_sample = st.toggle("Use 10k Sample for Export", value=True)
            export_df = filtered_df.sample(10000) if use_sample else filtered_df
        else:
            export_df = filtered_df

        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.subheader("📄 Intelligence Reports")
            xls = generate_excel_bytes({
                "Cleaned_Data": export_df.head(50000), 
                "Risk_Ranking": geo_data['m_stats'],
                "Audit_Report": pd.DataFrame(audit_data['table'])
            })
            st.download_button("Excel: Comprehensive Report (.xlsx)", data=xls, 
                            file_name=f"Intel_Report_{datetime.now().strftime('%Y%m%d')}.xlsx")
            
            summary_txt = get_executive_summary_text(filtered_df, audit_data['score'], scored_data['Crash_Risk_Score'].mean(), 
                                                   geo_data['m_stats']['Municipality'].iloc[0], "Fleet Profile", audit_data['score'])
            st.download_button("Text: Executive Briefing Summary", data=summary_txt, file_name="Executive_Summary.txt")
            
        with col_ex2:
            st.subheader("💾 Raw Data Access")
            st.download_button("CSV: Export Current View", data=generate_csv_bytes(export_df), file_name="exported_data.csv")
            
        st.markdown("---")
        st.subheader("📊 Live Executive Summary")
        st.code(summary_txt)
    else:
        st.info("Load data first.")
