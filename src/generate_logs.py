
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUTPUT = Path("data/raw/server_logs.csv")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

SERVICES = [
    "api-server",
    "auth-service",
    "database",
    "payment-service"
]

LEVELS = ["INFO", "WARNING", "ERROR", "CRITICAL"]

MESSAGES = {
    "INFO": [
        "Request processed successfully",
        "Health check passed",
        "User session created",
        "Database query completed"
    ],
    "WARNING": [
        "Response time above threshold",
        "Memory usage increasing",
        "Multiple login attempts detected",
        "Connection pool nearly full"
    ],
    "ERROR": [
        "Database connection failed",
        "Request timeout",
        "Authentication failed",
        "Service unavailable"
    ],
    "CRITICAL": [
        "CPU usage critically high",
        "Database server unreachable",
        "Memory limit exceeded",
        "Payment service crashed"
    ]
}

records = []
start_time = datetime.now() - timedelta(days=7)

for i in range(5000):
    timestamp = start_time + timedelta(seconds=i * 120)
    service = random.choice(SERVICES)

    level = random.choices(
        LEVELS,
        weights=[80, 12, 6, 2],
        k=1
    )[0]

    if level == "INFO":
        cpu = random.uniform(5, 55)
        memory = random.uniform(20, 65)
        response_time = random.uniform(20, 250)
        network_traffic = random.uniform(10, 150)

    elif level == "WARNING":
        cpu = random.uniform(45, 80)
        memory = random.uniform(55, 85)
        response_time = random.uniform(200, 900)
        network_traffic = random.uniform(100, 350)

    elif level == "ERROR":
        cpu = random.uniform(60, 95)
        memory = random.uniform(65, 92)
        response_time = random.uniform(500, 2000)
        network_traffic = random.uniform(150, 500)

    else:
        cpu = random.uniform(90, 100)
        memory = random.uniform(90, 100)
        response_time = random.uniform(1500, 5000)
        network_traffic = random.uniform(400, 1000)

    records.append({
        "timestamp": timestamp.isoformat(timespec="seconds"),
        "service": service,
        "level": level,
        "message": random.choice(MESSAGES[level]),
        "cpu_usage": round(cpu, 2),
        "memory_usage": round(memory, 2),
        "response_time_ms": round(response_time, 2),
        "network_traffic_mb": round(network_traffic, 2)
    })

with OUTPUT.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

print("Log dataset generated successfully!")
print(f"Total records: {len(records)}")
print(f"Output file: {OUTPUT}")
