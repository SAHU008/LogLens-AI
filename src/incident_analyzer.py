
import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/processed/anomaly_results.csv")
OUTPUT_PATH = Path("data/processed/incident_reports.csv")


def analyze_incident(row):
    cpu = row["cpu_usage"]
    memory = row["memory_usage"]
    response = row["response_time_ms"]
    message = str(row["message"]).lower()

    reasons = []
    actions = []

    if cpu >= 90:
        reasons.append("Critically high CPU usage")
        actions.append("Inspect CPU-intensive processes and workload spikes.")

    if memory >= 90:
        reasons.append("Critical memory pressure")
        actions.append("Inspect memory consumption and possible memory leaks.")

    if response >= 1500:
        reasons.append("Very high response time")
        actions.append("Check application latency, database queries and network delays.")

    if "database" in message:
        reasons.append("Possible database connectivity issue")
        actions.append("Check database availability and connection pool health.")

    if "authentication" in message or "login" in message:
        reasons.append("Possible authentication issue")
        actions.append("Review authentication logs and failed login patterns.")

    if "payment" in message:
        reasons.append("Possible payment service failure")
        actions.append("Inspect payment service health and transaction errors.")

    if "network" in message or row["network_traffic_mb"] > 700:
        reasons.append("Unusual network activity")
        actions.append("Inspect network traffic and request patterns.")

    if not reasons:
        reasons.append("Unusual combination of server metrics")
        actions.append("Review recent logs and compare metrics with normal baselines.")

    if cpu >= 90 or memory >= 90 or "critical" in message:
        severity = "CRITICAL"
    elif "ERROR" == row["level"] or response >= 1500:
        severity = "HIGH"
    elif row["level"] == "WARNING":
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return pd.Series({
        "severity": severity,
        "possible_causes": "; ".join(reasons),
        "recommended_actions": "; ".join(actions)
    })


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            "Anomaly results not found. Run train_model.py first."
        )

    df = pd.read_csv(INPUT_PATH)

    anomalies = df[df["is_anomaly"] == True].copy()

    if anomalies.empty:
        print("No anomalies found.")
        return

    analysis = anomalies.apply(analyze_incident, axis=1)

    reports = pd.concat(
        [anomalies.reset_index(drop=True),
         analysis.reset_index(drop=True)],
        axis=1
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    reports.to_csv(OUTPUT_PATH, index=False)

    print("INCIDENT ANALYSIS COMPLETED!")
    print("--------------------------------")
    print(f"Incidents analyzed: {len(reports)}")
    print("\nSeverity distribution:")
    print(reports["severity"].value_counts().to_string())
    print(f"\nReports saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
