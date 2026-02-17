import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="SEO Analytics Dashboard",
    layout="wide"
)

# ------------------ TITLE ------------------
st.title("📊 Real-Time SEO-Based Virtual Marketing Analytics & Alert System")

st.markdown(
    "This dashboard allows users to upload their own SEO dataset and analyze "
    "website performance in real time using KPIs, alerts, and visualizations."
)

# ------------------ SIDEBAR HELP ------------------
st.sidebar.title("⚙ Dashboard Settings")
st.sidebar.markdown(
    "ℹ **Instructions**  \n"
    "- Upload a CSV file containing SEO data  \n"
    "- Required columns: Time, Traffic, CTR, Keyword_Rank  \n"
    "- Adjust thresholds to trigger alerts"
)

# ------------------ DATASET UPLOAD ------------------
st.subheader("📤 Upload Your SEO Dataset")

uploaded_file = st.file_uploader(
    "Upload SEO CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("✅ Dataset uploaded successfully!")
else:
    data = pd.read_csv("data/seo_data.csv")
    st.info("ℹ Using default SEO dataset")

# ------------------ DATA VALIDATION ------------------
required_columns = {"Time", "Traffic", "CTR", "Keyword_Rank"}

if not required_columns.issubset(data.columns):
    st.error(
        "❌ Invalid dataset format.\n\n"
        "Your file must contain these columns:\n"
        "Time, Traffic, CTR, Keyword_Rank"
    )
    st.stop()

# ------------------ DATA PREVIEW ------------------
st.subheader("🔍 Dataset Preview")
st.dataframe(data.head())

latest = data.iloc[-1]

# ------------------ SIDEBAR THRESHOLDS ------------------
TRAFFIC_THRESHOLD = st.sidebar.slider(
    "🚦 Traffic Threshold",
    min_value=100,
    max_value=5000,
    value=500
)

CTR_THRESHOLD = st.sidebar.slider(
    "🎯 CTR Threshold (%)",
    min_value=0.5,
    max_value=10.0,
    value=2.0
)

RANK_THRESHOLD = st.sidebar.slider(
    "🔎 Keyword Rank Limit",
    min_value=1,
    max_value=50,
    value=10
)

# ------------------ KPI SECTION ------------------
st.subheader("📌 Key Performance Indicators (Auto-Detected)")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("🚦 Current Traffic", int(latest["Traffic"]))
kpi2.metric("🎯 Current CTR (%)", latest["CTR"])
kpi3.metric("🔎 Current Rank", int(latest["Keyword_Rank"]))
kpi4.metric("📈 Avg Traffic", int(data["Traffic"].mean()))

# ------------------ ALERT SYSTEM ------------------
st.subheader("🚨 Live Alerts")

alert_triggered = False

if latest["Traffic"] < TRAFFIC_THRESHOLD:
    st.error(f"⚠ Traffic dropped to {latest['Traffic']} visitors")
    alert_triggered = True

if latest["CTR"] < CTR_THRESHOLD:
    st.warning(f"⚠ Low CTR detected: {latest['CTR']}%")
    alert_triggered = True

if latest["Keyword_Rank"] > RANK_THRESHOLD:
    st.info(f"ℹ Keyword rank dropped to position {latest['Keyword_Rank']}")
    alert_triggered = True

# ------------------ STATUS INDICATOR ------------------
if alert_triggered:
    st.markdown("🔴 **System Status: ALERT MODE**")
else:
    st.success("🟢 System Status: NORMAL")

# ------------------ GRAPHS SECTION ------------------
st.subheader("📈 SEO Performance Trends")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Website Traffic Trend")
    plt.figure(figsize=(6, 4))
    plt.plot(data["Time"], data["Traffic"], marker="o")
    plt.xlabel("Time")
    plt.ylabel("Traffic")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

with col2:
    st.markdown("### CTR Trend")
    plt.figure(figsize=(6, 4))
    plt.plot(data["Time"], data["CTR"], marker="o")
    plt.xlabel("Time")
    plt.ylabel("CTR (%)")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

st.markdown("### Keyword Ranking Trend")
plt.figure(figsize=(12, 4))
plt.plot(data["Time"], data["Keyword_Rank"], marker="o")
plt.xlabel("Time")
plt.ylabel("Keyword Rank")
plt.gca().invert_yaxis()
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)

# ------------------ DOWNLOAD REPORT ------------------
st.subheader("⬇ Download SEO Report")

st.download_button(
    label="Download CSV Report",
    data=data.to_csv(index=False),
    file_name="seo_analytics_report.csv",
    mime="text/csv"
)

# ------------------ FOOTER ------------------
footer = st.empty()

footer.caption(f"🕒 Last updated at: {time.strftime('%H:%M:%S')}")
time.sleep(5)
st.rerun()

# ------------------ AUTO REFRESH ------------------
st.caption(f"🕒 Last updated at: {time.strftime('%H:%M:%S')}")
st.autorefresh(interval=5000, key="refresh")

