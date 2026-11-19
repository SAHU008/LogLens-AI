# 🚀 LogLens AI — Intelligent Cloud Monitoring & Anomaly Detection System

An AI-powered cloud monitoring platform that analyzes server performance metrics, detects unusual behavior, and helps identify potential infrastructure incidents.

**Built with Python, Machine Learning, FastAPI, Streamlit, and SQLite.**

---

## 🌟 Project Overview

LogLens AI is an intelligent monitoring and anomaly detection system designed to identify unusual server behavior using machine learning.

The system analyzes server performance metrics, detects anomalies using an Isolation Forest model, and provides an interactive dashboard for monitoring predictions and reviewing historical results.

The project demonstrates how machine learning can be integrated with backend APIs and cloud deployment to build a practical monitoring solution.

## ✨ Key Features

- 🤖 **AI-Powered Anomaly Detection:** Uses an Isolation Forest machine learning algorithm.
- 📊 **Real-Time Monitoring Interface:** Interactive Streamlit dashboard.
- ⚡ **FastAPI Backend:** REST API for processing monitoring data and generating predictions.
- 🗄️ **Prediction History:** Stores previous predictions using SQLite.
- 🚨 **Incident Detection:** Identifies unusual server behavior and potential incidents.
- 📈 **Performance Metrics:** Analyzes CPU usage, memory usage, response time, and network traffic.
- ☁️ **Cloud Deployment:** Backend deployed on Render and dashboard deployed on Streamlit Community Cloud.
- 🧪 **API Testing:** Automated tests for verifying API functionality.

## 🧠 Machine Learning

LogLens AI uses the **Isolation Forest** algorithm for unsupervised anomaly detection.

The model identifies unusual patterns in server performance metrics without requiring manually labeled anomaly data.

### Dataset

- 5,000 synthetic server log records.
- Normal and anomalous server behavior.
- Multiple performance metrics.
- Used for model training and evaluation.

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| Algorithm | Isolation Forest |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| API Testing | Pytest |
| Deployment | Render |
| Dashboard Hosting | Streamlit Community Cloud |
| Version Control | Git & GitHub |

## 🏗️ System Architecture

```text
        Server Performance Metrics
                    |
                    v
             Data Processing
                    |
                    v
          Isolation Forest Model
                    |
                    v
             Anomaly Detection
                    |
                    v
               FastAPI
                    |
          -------------------
          |                 |
          v                 v
    Streamlit Dashboard   SQLite
          |                 |
          v                 v
    Visual Results    Prediction History
```

## 📊 Performance Metrics

The system analyzes:

- CPU Usage
- Memory Usage
- Response Time
- Network Traffic

These metrics are processed by the machine learning model to identify abnormal patterns.

## 🖥️ Application Screenshots

Screenshots of the deployed dashboard, prediction results, and monitoring interface can be added here.

## ☁️ Live Deployment

**Backend API:**

https://loglens-ai-api.onrender.com

**API Documentation:**

https://loglens-ai-api.onrender.com/docs

**Streamlit Dashboard:**

[Add your deployed Streamlit application URL here]

## ⚙️ Installation and Setup

Follow these steps to run LogLens AI locally.

### 1. Clone the Repository

```bash
git clone https://github.com/SAHU008/LogLens-AI.git
```

### 2. Navigate to the Project

```bash
cd LogLens-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the FastAPI Backend

```bash
python -m uvicorn src.api:app --reload
```

Backend documentation:

http://127.0.0.1:8000/docs

### 7. Start the Streamlit Dashboard

Open another terminal and execute:

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser.

## 🧪 Testing

Run the automated tests using:

```bash
pytest -v
```

## 🔮 Future Improvements

- Advanced anomaly classification.
- Automated incident alerts.
- Email and notification integration.
- Advanced monitoring visualizations.
- Support for real-world server log ingestion.
- Predictive infrastructure health analysis.
- More advanced incident severity analysis.

## 🎯 Project Objective

The objective of LogLens AI is to demonstrate the practical application of machine learning in cloud infrastructure monitoring, anomaly detection, and intelligent incident analysis.

It combines machine learning, backend development, database management, and cloud deployment into one integrated project.

## 👨‍💻 Developer

**Govinda Sahu**

Computer Science & Engineering — AI & ML

GitHub: https://github.com/SAHU008

---

⭐ If you find this project interesting, consider giving the repository a star!

**LogLens AI — Making Cloud Monitoring Smarter with Machine Learning.**