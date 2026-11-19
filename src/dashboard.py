
import streamlit as st
import pandas as pd
import requests
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
ANOMALY_PATH = BASE_DIR / "data" / "processed" / "anomaly_results.csv"
INCIDENT_PATH = BASE_DIR / "data" / "processed" / "incident_reports.csv"

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LogLens AI",
    page_icon="🔍",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("🔍 LogLens AI")
st.subheader("Intelligent Cloud Monitoring & Incident Detection")

st.markdown(
    "Monitor server activity, detect anomalies and analyze "
    "potential incidents using Machine Learning."
)

# ==========================================
# LOAD DATA
# ==========================================

if not ANOMALY_PATH.exists() or not INCIDENT_PATH.exists():
    st.error("Required CSV files are missing. Please generate the logs and incident reports first.")
    st.stop()

logs = pd.read_csv(ANOMALY_PATH)
incidents = pd.read_csv(INCIDENT_PATH)

if "is_anomaly" not in logs.columns:
    st.error("The anomaly_results.csv file is missing the is_anomaly column.")
    st.stop()

logs["is_anomaly"] = (
    logs["is_anomaly"].astype(str).str.lower().isin(["true", "1", "yes"])
)

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Dashboard Filters")

if "service" in logs.columns:
    services = ["ALL"] + sorted(logs["service"].dropna().unique().tolist())
    service = st.sidebar.selectbox("Select Service", services)

    if service != "ALL":
        logs = logs[logs["service"] == service]
        if "service" in incidents.columns:
            incidents = incidents[incidents["service"] == service]

# ==========================================
# OVERVIEW
# ==========================================

st.divider()
st.header("System Overview")

total = len(logs)
anomalies = int(logs["is_anomaly"].sum())
normal = total - anomalies

c1, c2, c3 = st.columns(3)
c1.metric("Total Logs", f"{total:,}")
c2.metric("Anomalies Detected", f"{anomalies:,}")
c3.metric("Normal Logs", f"{normal:,}")

# ==========================================
# ANOMALY ANALYTICS
# ==========================================

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
    if not incidents.empty and "severity" in incidents.columns:
        st.bar_chart(incidents["severity"].value_counts())
    else:
        st.info("No incidents available.")

# ==========================================
# SERVER PERFORMANCE
# ==========================================

st.divider()
st.header("⚙️ Server Performance")

available_metrics = [
    metric for metric in [
        "cpu_usage",
        "memory_usage",
        "response_time_ms",
        "network_traffic_mb"
    ]
    if metric in logs.columns
]

if available_metrics and not logs.empty:
    metric = st.selectbox("Choose server metric", available_metrics)
    st.line_chart(logs[metric])
else:
    st.info("No performance metrics available.")

# ==========================================
# INCIDENT REPORTS
# ==========================================

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

    available_columns = [
        column for column in columns if column in incidents.columns
    ]

    st.dataframe(
        incidents[available_columns],
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

# ==========================================
# PREDICTION HISTORY
# ==========================================

st.divider()
st.header("📋 Prediction History")

st.write(
    "Previously saved AI predictions retrieved "
    "from the LogLens AI SQLite database."
)

if st.button("🔄 Refresh Prediction History"):
    st.rerun()

try:
    history_response = requests.get(
        f"{API_URL}/history",
        params={"limit": 100},
        timeout=10
    )

    history_response.raise_for_status()
    history_data = history_response.json()
    history_records = history_data.get("history", [])

    st.metric(
        "Total Saved Predictions",
        history_data.get("total_records", len(history_records))
    )

    if history_records:
        history_df = pd.DataFrame(history_records)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Prediction History CSV",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="loglens_prediction_history.csv",
            mime="text/csv"
        )
    else:
        st.info("No saved predictions yet. Run a live AI prediction below.")

except requests.exceptions.RequestException as error:
    st.error(f"Cannot retrieve prediction history. Check that FastAPI is running. Details: {error}")

except (ValueError, KeyError) as error:
    st.error(f"Invalid prediction history response: {error}")

# ==========================================
# SERVER LOGS
# ==========================================

st.divider()
st.header("📄 Server Logs")

show_anomalies = st.checkbox("Show only anomalies")

display_logs = logs.copy()

if show_anomalies:
    display_logs = display_logs[display_logs["is_anomaly"]]

st.dataframe(
    display_logs,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download Server Logs CSV",
    data=display_logs.to_csv(index=False).encode("utf-8"),
    file_name="loglens_server_logs.csv",
    mime="text/csv"
)

# ==========================================
# LIVE AI ANOMALY PREDICTION
# ==========================================

st.divider()
st.header("🤖 Live AI Anomaly Prediction")

st.write(
    "Enter server metrics to check whether the server "
    "is behaving normally."
)

with st.form("live_prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        cpu = st.number_input(
            "CPU Usage (%)",
            min_value=0.0,
            max_value=100.0,
            value=25.0
        )

        memory = st.number_input(
            "Memory Usage (%)",
            min_value=0.0,
            max_value=100.0,
            value=40.0
        )

    with col2:
        response_time = st.number_input(
            "Response Time (ms)",
            min_value=0.0,
            value=120.0
        )

        network = st.number_input(
            "Network Traffic (MB)",
            min_value=0.0,
            value=30.0
        )

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
            f"{API_URL}/predict",
            json=payload,
            timeout=10
        )

        api_response.raise_for_status()
        result = api_response.json()

        st.subheader("Prediction Result")

        if result["is_anomaly"]:
            st.error("🚨 ANOMALY DETECTED")
        else:
            st.success("SERVER STATUS: NORMAL")

        st.metric(
            "Anomaly Score",
            result["anomaly_score"]
        )

        st.write("Prediction ID:", result["prediction_id"])
        st.write("Database Status:", result["database_status"])
        st.json(result)

        st.info("Refresh the Prediction History section to see this saved prediction.")

    except requests.exceptions.RequestException as error:
        st.error(f"Could not connect to FastAPI: {error}")

    except (ValueError, KeyError) as error:
        st.error(f"Unexpected prediction response: {error}")

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "LogLens AI | Machine Learning Based Cloud Monitoring"
)

st.caption(
    "Demonstration project using synthetic server logs."
)
