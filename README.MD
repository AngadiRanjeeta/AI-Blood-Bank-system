# 🩸 AI Emergency Blood Allocation System (AI Blood Bank)

A full-stack **FastAPI + MySQL + Strong SQL + Map + Analytics + ML Forecasting** project that finds the best hospital for a blood request based on:

✅ Distance (Haversine SQL)  
✅ Blood stock availability (MySQL aggregation)  
✅ Urgency weighting  
✅ Built-in analytics dashboard (Chart.js)  
✅ ML demand forecasting (Ridge Regression)  

---

## 🚀 Features

### ✅ Allocation Engine
- Finds top hospitals matching blood group
- Computes distance using **Haversine formula inside MySQL**
- Ranks hospitals using a weighted score:
  - Urgency weight
  - Distance score (normalized)
  - Stock score (scaled)

### 🗺️ Map UI (Web)
- Receiver location marker
- Hospital markers
- Route line (straight-line demo)
- Clean responsive Bootstrap interface

### 📊 Analytics Dashboard
- KPI Cards (Hospitals, Stock rows, Requests today)
- Stock by blood group
- Requests by blood group
- Requests by urgency
- Requests trend (last 14 days)

### 🤖 ML Demand Forecasting
- Uses request history from `bloodrequest`
- Trains a regression model (Ridge)
- Predicts demand for next N days
- Stores model in `ml/forecast_model.pkl`

---

## 🧱 Tech Stack
- **Backend:** FastAPI, SQLAlchemy, PyMySQL
- **Database:** MySQL
- **Frontend:** HTML, Bootstrap, Leaflet Map
- **Charts:** Chart.js
- **ML:** scikit-learn (Ridge Regression), joblib
- **Server:** Uvicorn

---

## 📂 Project Structure
