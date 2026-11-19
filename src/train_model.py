
import joblib
import pandas as pd

from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Project paths
DATA_PATH = Path("data/raw/server_logs.csv")
MODEL_PATH = Path("models/isolation_forest.joblib")
OUTPUT_PATH = Path("data/processed/anomaly_results.csv")

# Create output folders if necessary
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# Load dataset
print("Loading server logs...")
df = pd.read_csv(DATA_PATH)

# Select numerical features
features = [
    "cpu_usage",
    "memory_usage",
    "response_time_ms",
    "network_traffic_mb"
]

X = df[features]

# Build machine learning pipeline
print("Training Isolation Forest model...")

model = Pipeline([
    ("scaler", StandardScaler()),
    ("detector", IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42,
        n_jobs=-1
    ))
])

# Train model
model.fit(X)

# Predict anomalies
predictions = model.predict(X)
scores = model.decision_function(X)

# Save results
df["anomaly_prediction"] = predictions
df["anomaly_score"] = scores
df["is_anomaly"] = predictions == -1

df.to_csv(OUTPUT_PATH, index=False)

# Save trained model
joblib.dump(model, MODEL_PATH)

# Display summary
anomalies = int(df["is_anomaly"].sum())
normal = len(df) - anomalies

print("\nMODEL TRAINING COMPLETED!")
print("-------------------------")
print(f"Total logs: {len(df)}")
print(f"Normal logs: {normal}")
print(f"Anomalies detected: {anomalies}")
print(f"Anomaly percentage: {anomalies / len(df) * 100:.2f}%")
print(f"\nModel saved: {MODEL_PATH}")
print(f"Results saved: {OUTPUT_PATH}")
