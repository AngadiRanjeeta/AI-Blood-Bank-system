# 🩸 AI Emergency Blood Allocation System (AI Blood Bank)

Blood Bank Allocation System built with FastAPI and MySQL that finds the most suitable hospital for a blood request using geospatial distance (Haversine SQL), stock availability, and urgency-based scoring. Includes an analytics dashboard and ML-based demand forecasting to analyze and predict blood demand trends.

## 🚀 Features
- Distance (Haversine SQL)
- Blood stock availability (MySQL aggregation)
- Urgency weighting + ranking score
- Analytics dashboard (Chart.js)
- ML demand forecasting (Ridge Regression)

### ✅ Allocation Engine
- Finds top hospitals matching blood group
- Computes distance using **Haversine formula inside MySQL**
- Ranks hospitals using a weighted score:
  - Urgency weight
  - Distance score (normalized)
  - Stock score (scaled)

![image alt](https://github.com/AngadiRanjeeta/AI-Blood-Bank-system/blob/4573e1fdf6e6992e1c44d545306ca696eb91b723/blood.png)

### 🗺️ Map UI (Web)
- Receiver location marker
- Hospital markers
- Route line (straight-line demo)
- Clean responsive Bootstrap interface

### 📊 Analytics Dashboard
- KPI Cards (Total blood units, Requests received, Requests fulfilled)
- Blood inventory by hospital
- Blood group distribution
- Request fulfillment by urgency
- 14-Day ML demand forecast (Ridge Regression)
- **Power BI Dashboard** with city-level cross filtering

### 🤖 ML Demand Forecasting
- Uses request history from `bloodrequest`
- Trains a regression model (Ridge)
- Predicts demand for next N days
- Stores model in `ml/forecast_model.pkl`

![image alt](https://github.com/AngadiRanjeeta/AI-Blood-Bank-system/blob/477afb2308f0e480d7dcd358fc033dc039560b50/1.png)
![image alt](https://github.com/AngadiRanjeeta/AI-Blood-Bank-system/blob/569874cae1de1f0a75484e65b5a8f59ea70090bc/2.png)
---

## 🧱 Tech Stack
- **Backend:** FastAPI, SQLAlchemy, PyMySQL
- **Database:** MySQL
- **Frontend:** HTML, Bootstrap, Leaflet Map
- **Analytics:** Power BI (interactive dashboard), Chart.js
- **ML:** scikit-learn (Ridge Regression), joblib
- **Server:** Uvicorn

---

## ✅ Setup Instructions (Windows)

1) Clone Repository  
git clone https://github.com/AngadiRanjeeta/AI-Blood-Bank-system.git  
cd AI-Blood-Bank-system  

2) Create Virtual Environment  
python -m venv venv  
venv\Scripts\activate  

3) Install Dependencies  
pip install -r requirements.txt  

4) Configure MySQL Connection  
Create a file named .env in the project root and add:  
DB_HOST=127.0.0.1  
DB_PORT=3306  
DB_USER=root  
DB_PASSWORD=YOUR_PASSWORD  
DB_NAME=ai_blood_bank  

5) Create Database + Tables  
Run in MySQL Workbench:  
CREATE DATABASE ai_blood_bank;  
USE ai_blood_bank;  
Then run: app/models/tables.sql  

6) Run Server  
python -m uvicorn app.main:app --reload  

## 🌐 Open in Browser
### localhost
Main UI: http://127.0.0.1:8000/  
Swagger Docs: http://127.0.0.1:8000/docs  
Analytics Dashboard: http://127.0.0.1:8000/analytics  
