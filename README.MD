# 🩸 AI Emergency Blood Allocation System (AI Blood Bank)

A full-stack FastAPI + MySQL + Strong SQL + Map + Analytics + ML Forecasting project.

## 🚀 Features
- Distance (Haversine SQL)
- Blood stock availability (MySQL aggregation)
- Urgency weighting + ranking score
- Analytics dashboard (Chart.js)
- ML demand forecasting (Ridge Regression)

## 🧱 Tech Stack
- Backend: FastAPI, SQLAlchemy, PyMySQL
- Database: MySQL
- Frontend: HTML, Bootstrap, Leaflet
- Charts: Chart.js
- ML: scikit-learn (Ridge), joblib
- Server: Uvicorn

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
Main UI: http://127.0.0.1:8000/  
Swagger Docs: http://127.0.0.1:8000/docs  
Analytics Dashboard: http://127.0.0.1:8000/analytics  
