# LogLens AI – Intelligent Cloud Monitoring & Incident Detection

LogLens AI is a machine-learning-powered cloud monitoring prototype that analyzes server logs, detects unusual system behavior, and generates incident reports to help identify potential operational issues.

## Key Features

- Synthetic server log generation with 5,000 records.
- Machine learning anomaly detection using Isolation Forest.
- Rule-based incident severity classification.
- FastAPI backend for real-time predictions.
- Interactive Streamlit monitoring dashboard.
- SQLite database for prediction history.
- CSV export for anomaly and incident reports.
- Automated API tests using pytest.

## Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- FastAPI
- Streamlit
- SQLAlchemy and SQLite
- Matplotlib and Seaborn
- Pytest

## Project Structure

```text
LogLens_AI/
├── dashboard.py
├── requirements.txt
├── README.md
├── src/
├── data/
├── models/
└── tests/
```

## Installation and Setup

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd LogLens_AI
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

Generate synthetic logs:

```bash
python -m src.generate_logs
```

Train the anomaly detection model:

```bash
python -m src.train_model
```

Generate incident reports:

```bash
python -m src.incident_analyzer
```

Start the API:

```bash
python -m uvicorn src.api:app --reload
```

Start the dashboard in another terminal:

```bash
python -m streamlit run dashboard.py
```

API documentation:

`http://127.0.0.1:8000/docs`

Dashboard:

`http://localhost:8501`

## Run Automated Tests

```bash
python -m pytest tests/ -v
```

## Machine Learning Approach

The project uses the Isolation Forest algorithm to identify unusual patterns in server performance metrics such as CPU usage, memory usage, response time, and network traffic.

The current prototype uses synthetic data and a configured anomaly contamination rate of 5%. Its predictions are intended for demonstration and experimentation, not production incident diagnosis.

## Future Improvements

- Real cloud monitoring integrations.
- Advanced incident correlation.
- Model performance evaluation on real-world datasets.
- Docker-based deployment.
- Cloud hosting and monitoring integrations.

## Author

Developed as an AI/ML learning and portfolio project.