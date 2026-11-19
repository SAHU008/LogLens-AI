import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="LogLens AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 LogLens AI")
st.subheader("Intelligent Cloud Monitoring & Incident Detection")

st.write(
    "Monitor server activity, detect anomalies and analyze "
    "potential incidents using Machine Learning."
)

ANOMALY_PATH = Path("data/processed/anomaly_results.csv")
INCIDENT_PATH = Path("data/processed/incident_reports.csv")

if not ANOMALY_PATH.exists() or not INCIDENT_PATH.exists():
    st.error("Required CSV files are missing.")
    st.stop()

logs = pd.read_csv(ANOMALY_PATH)
incidents = pd.read_csv(INCIDENT_PATH)

st.sidebar.header("Dashboard Filters")

services = ["ALL"] + sorted(logs["service"].dropna().unique().tolist())
service = st.sidebar.selectbox("Select Service", services)

if service != "ALL":
    logs = logs[logs["service"] == service]
    incidents = incidents[incidents["service"] == service]

st.divider()

total = len(logs)
anomalies = int(logs["is_anomaly"].sum())
normal = total - anomalies

c1, c2, c3 = st.columns(3)
c1.metric("Total Logs", f"{total:,}")
c2.metric("Anomalies Detected", f"{anomalies:,}")
c3.metric("Normal Logs", f"{normal:,}")

st.divider()
st.header("📊 Anomaly Analytics")

chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Normal vs Anomalous Logs")
    st.bar_chart(pd.Series({
        "Normal": normal,
        "Anomalies": anomalies
    }))

with chart2:
    st.subheader("Incident Severity")
    if not incidents.empty:
        st.bar_chart(incidents["severity"].value_counts())
    else:
        st.info("No incidents available.")

st.divider()
st.header("⚙️ Server Performance")

metric = st.selectbox(
    "Choose server metric",
    [
        "cpu_usage",
        "memory_usage",
        "response_time_ms",
        "network_traffic_mb"
    ]
)

st.line_chart(logs[metric])

st.divider()
st.header("🚨 Incident Reports")

if not incidents.empty:
    columns = [
        "timestamp",
        "service",
        "severity",
        "possible_causes",
        "recommended_actions"
    ]

    available = [c for c in columns if c in incidents.columns]

    st.dataframe(
        incidents[available],
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Incident Reports",
        incidents.to_csv(index=False).encode("utf-8"),
        "incident_reports.csv",
        "text/csv"
    )
else:
    st.info("No incidents found.")

st.divider()
st.header("📋 Server Logs")

show_anomalies = st.checkbox("Show only anomalies")

if show_anomalies:
    logs = logs[logs["is_anomaly"] == True]

st.dataframe(
    logs,
    use_container_width=True,
    hide_index=True
)

st.divider()
st.caption("LogLens AI | Machine Learning Based Cloud Monitoring")
st.caption("Demo project using synthetic server logs.")

# ==========================================
# LIVE AI ANOMALY PREDICTION
# ==========================================

import requests

st.divider()
st.header("Live AI Anomaly Prediction")
st.write("Enter server metrics to check whether the server is behaving normally.")

with st.form("live_prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        cpu = st.number_input("CPU Usage (%)", min_value=0.0, max_value=100.0, value=25.0)
        memory = st.number_input("Memory Usage (%)", min_value=0.0, max_value=100.0, value=40.0)

    with col2:
        response_time = st.number_input("Response Time (ms)", min_value=0.0, value=120.0)
        network = st.number_input("Network Traffic (MB)", min_value=0.0, value=30.0)

    submitted = st.form_submit_button("Run AI Prediction")

if submitted:
    payload = {
        "cpu_usage": cpu,
        "memory_usage": memory,
        "response_time_ms": response_time,
        "network_traffic_mb": network
    }

    try:
        api_response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload,
            timeout=10
        )

        if api_response.status_code == 200:
            result = api_response.json()
            st.subheader("Prediction Result")

            if result["is_anomaly"]:
                st.error("ANOMALY DETECTED")
            else:
                st.success("SERVER STATUS: NORMAL")

            st.metric("Anomaly Score", result["anomaly_score"])
            st.json(result)

        else:
            st.error(f"API Error: {api_response.status_code}")
            st.write(api_response.text)

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FastAPI. Make sure the API server is running on port 8000.")

    except requests.exceptions.RequestException as error:
        st.error(f"Request failed: {error}")

# ==========================================
# LOG LENS AI - PREDICTION HISTORY
# ==========================================

import requests

st.divider()
st.header("📋 Prediction History")
st.write("Previously saved AI predictions from the SQLite database.")

if st.button("Refresh Prediction History"):
    st.rerun()

try:
    response = requests.get(
        "http://127.0.0.1:8000/history",
        params={"limit": 100},
        timeout=10
    )
    response.raise_for_status()

    data = response.json()
    records = data.get("history", [])

    st.metric("Total Saved Predictions", data.get("total_records", 0))

    if records:
        history_df = pd.DataFrame(records)

        st.dataframe(
            history_df,
            width="stretch",
            hide_index=True
        )

        st.download_button(
            "Download Prediction History CSV",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="loglens_prediction_history.csv",
            mime="text/csv"
        )
    else:
        st.info("No saved predictions yet. Run a live AI prediction first.")

except requests.exceptions.RequestException as error:
    st.error(f"API connection failed: {error}")

