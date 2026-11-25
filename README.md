🏆 Data Detective — National Data Assessment 2024

เว็บแอปพลิเคชันวิเคราะห์ข้อมูลรายงานอุบัติเหตุจราจรแบบ Interactive พัฒนาด้วย Python และ Streamlit ครอบคลุมตั้งแต่การตรวจสอบคุณภาพข้อมูล (Data Quality Audit), การทำความสะอาดข้อมูล (Data Cleaning), การวิเคราะห์เชิงพื้นที่และพฤติกรรมความเสี่ยง ไปจนถึงการส่งออกรายงานสำหรับผู้บริหาร

✨ ฟีเจอร์หลัก (Key Features)

🏠 Dashboard Home

แสดงตัวชี้วัดภาพรวม: Health Score, Avg Risk Score, High Risk Rate และ Active Records
แสดงแผนที่ความหนาแน่นของจุดเกิดเหตุ (Risk Hotspot Concentration) และสัดส่วนระดับความเสี่ยง (Low, Medium, High, Critical Risk)
ตาราง Top 10 พื้นที่เสี่ยงสูง พร้อมระบบ Breadcrumb สำหรับการเจาะข้อมูลเฉพาะพื้นที่ (Drill-Down)

🔍 Quality Audit (modules/data_audit.py)

ประเมินคุณภาพข้อมูล 4 มิติ ได้แก่
Completeness: ตรวจสอบเปอร์เซ็นต์ค่าว่างรายคอลัมน์และสถานะ (Valid, Warning, Critical)
Consistency: ตรวจสอบข้อมูลซ้ำจากคอลัมน์ Report Number
Accuracy: ตรวจสอบค่าผิดปกติทางตรรกะ เช่น Speed Limit < 0 หรือ Vehicle Year ที่เกินปีอนาคต
Timeliness: ตรวจสอบวันเวลาล่าสุดของข้อมูลจาก Crash Date/Time

🧹 Data Cleaning (modules/cleaning.py)

จัดการ Missing Values รายคอลัมน์ด้วยกลยุทธ์ Mean, Median, Mode หรือ Drop
แปลงและจัดมาตรฐานรูปแบบวันที่ (pd.to_datetime) และลบข้อมูลซ้ำ
แสดงผลเปรียบเทียบจำนวนแถวและค่าว่างก่อน–หลังทำความสะอาด พร้อมบันทึกประวัติการแก้ไข (Transformation Steps) และปุ่ม Reset กลับเป็นข้อมูลต้นฉบับ

📊 Detailed VIZ (modules/visualization.py)

Trend Analysis: กราฟแนวโน้มจำนวนอุบัติเหตุรายวัน พร้อมตัวเลือกแสดง 7-Day Rolling Mean
Distribution: Boxplot สำหรับคอลัมน์ตัวเลข พร้อมตัวเลือกซ่อน/แสดง Outliers ด้วยวิธี IQR (และสุ่มตัวอย่างอัตโนมัติเมื่อข้อมูลเกิน 50,000 แถว)
Comparisons: กราฟแท่งเปรียบเทียบ Top 10 หมวดหมู่

📍 Geo Mapping (modules/geo_intelligence.py)

ตรวจสอบความถูกต้องของพิกัด Latitude / Longitude และคำนวณ % คุณภาพข้อมูลเชิงพื้นที่
แสดงแผนที่ Interactive 3 โหมด: Scatter, Density และ Cluster (จัดกลุ่ม Hotspot ด้วยอัลกอริทึม DBSCAN)
จัดอันดับ Municipality ที่มี Fatal Rate % สูงสุด และกด Focus on Area เพื่อ Drill-Down ทั้งแดชบอร์ดได้

🚨 Risk Analysis (modules/risk_scoring.py)

คำนวณคะแนนความเสี่ยงรวม (Crash_Risk_Score) จากปัจจัยแวดล้อมและพฤติกรรม:
ความรุนแรงของการบาดเจ็บ (Injury Severity: Fatal +5, Suspected Serious +3)
การใช้แอลกอฮอล์/สารเสพติด (Driver Substance Abuse: +3)
สภาพอากาศ (Weather: Rain/Snow/Sleet +2)
สภาพแสง (Light: Dark +2)
เขตจำกัดความเร็ว (Speed Limit > 60: +2)
จำแนกเป็น Low Risk, Medium Risk, High Risk และ Critical Risk พร้อมกราฟวิเคราะห์ตามพื้นที่ ยี่ห้อรถ และชั่วโมงเกิดเหตุ

🧪 Pattern Forensics (modules/forensics.py)

ตรวจจับความผิดปกติทางสถิติ (Statistical Anomalies) ของอัตราการเสียชีวิตในแต่ละพื้นที่ด้วยเกณฑ์ Z-Score > 2 (เฉพาะพื้นที่ที่มีเหตุการณ์มากกว่า 50 ครั้ง)
วิเคราะห์ความสัมพันธ์ระหว่างอายุยานพาหนะ (0-5 yrs ถึง 20+ yrs) กับอัตราการเสียชีวิต

💡 Business Insights (modules/insights.py)

สรุปข้อค้นพบเชิงกลยุทธ์อัตโนมัติในรูปแบบ What / Why / So What / Now What ครอบคลุมหน่วยงานที่รายงานสูงสุด ปัจจัยสภาพอากาศ และความสมบูรณ์ของข้อมูล

📤 Export Center (modules/export_center.py)

ส่งออกรายงาน Excel (.xlsx) แบบหลายชีต (Cleaned_Data, Risk_Ranking, Audit_Report)
ส่งออก CSV ตามข้อมูลที่กรองอยู่ในปัจจุบัน (มีตัวเลือก Sample 10,000 แถวอัตโนมัติหากข้อมูลเกิน 150,000 แถว)
สร้างและดาวน์โหลด Executive Summary (.txt)

🎯 Global Controls & System Readiness (Sidebar)

ตัวกรองข้อมูลส่วนกลางตามหน่วยงาน (Agency Name) และสภาพอากาศ (Weather)
ตรวจสอบความพร้อมของระบบ (System Deployment: READY / WARNING) จากความสมบูรณ์ของชุดข้อมูล คุณภาพพิกัด และคอลัมน์สำคัญ
🛠️ เทคโนโลยีที่ใช้ (Tech Stack)
Python 3.13
Streamlit (1.54.0) — Web Application Framework & Caching (@st.cache_data)
Pandas (2.3.3) & NumPy (2.4.2) — Data Processing
Plotly (6.5.2) — Interactive Charts & Mapbox Visualizations
Scikit-learn — DBSCAN Spatial Clustering
XlsxWriter — Multi-sheet Excel Report Generation
📁 โครงสร้างโปรเจกต์ (Project Structure)
text
Data Detective/
├── app.py                      # ไฟล์หลักสำหรับ UI, Routing และ Global Filters
├── 1_crash_reports.csv         # ชุดข้อมูลรายงานอุบัติเหตุ
├── requirements.txt            # รายการ dependencies
├── styles/
│   └── main.css                # Custom CSS สำหรับตกแต่งหน้า Dashboard
├── utils/
│   └── data_loader.py          # โหลดข้อมูล CSV พร้อม @st.cache_data
└── modules/
    ├── data_audit.py           # ตรวจสอบคุณภาพข้อมูล 4 มิติ
    ├── cleaning.py             # ทำความสะอาดข้อมูลและติดตาม Metrics
    ├── visualization.py        # กราฟ Trend, Distribution และ Comparison
    ├── geo_intelligence.py     # วิเคราะห์พิกัด แผนที่ และ DBSCAN Clustering
    ├── risk_scoring.py         # คำนวณคะแนนและระดับความเสี่ยง
    ├── forensics.py            # ตรวจจับ Anomaly ด้วย Z-Score และวิเคราะห์อายุรถ
    ├── insights.py             # สร้าง Strategic Business Insights
    └── export_center.py        # ส่งออกไฟล์ Excel, CSV, Summary และเช็กความพร้อม
🚀 วิธีติดตั้งและรันใช้งาน (Getting Started)
1. สร้าง Virtual Environment และติดตั้ง Dependencies
bash
cd "Data Detective"
python -m venv .venv
Windows (PowerShell):
powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
macOS / Linux:
bash
source .venv/bin/activate
pip install -r requirements.txt
2. รันเว็บแอปพลิเคชัน
bash
streamlit run app.py
จากนั้นเปิดเบราว์เซอร์ไปที่ http://localhost:8501
