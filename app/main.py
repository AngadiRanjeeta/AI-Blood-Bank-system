import math
from datetime import datetime
from fastapi import FastAPI, Depends, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.db import get_db
from app.api.schemas import FindBestRequest
from app.services.forecasting import ForecastModel

app = FastAPI(title="AI Blood Bank System")

# UI setup
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ML forecast model wrapper
forecast_model = ForecastModel(model_path="ml/forecast_model.pkl")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/analytics", response_class=HTMLResponse)
def analytics_page(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})


@app.get("/api/analytics")
def analytics_api(db: Session = Depends(get_db)):
    # Totals
    totals_sql = text("""
        SELECT
          (SELECT COUNT(*) FROM hospitals) AS hospitals_count,
          (SELECT COUNT(*) FROM receivers) AS receivers_count,
          (SELECT COUNT(*) FROM bloodinfo) AS total_stock_rows,
          (SELECT COUNT(*) FROM bloodrequest) AS total_requests,
          (SELECT COUNT(*) FROM bloodrequest WHERE request_date = CURDATE()) AS requests_today
    """)
    totals = db.execute(totals_sql).mappings().one()

    # Stock by blood group
    stock_sql = text("""
        SELECT bg, COUNT(*) AS units
        FROM bloodinfo
        GROUP BY bg
        ORDER BY units DESC
    """)
    stock = [dict(r) for r in db.execute(stock_sql).mappings().all()]

    # Requests by blood group
    req_sql = text("""
        SELECT bg, COUNT(*) AS requests
        FROM bloodrequest
        GROUP BY bg
        ORDER BY requests DESC
    """)
    reqs = [dict(r) for r in db.execute(req_sql).mappings().all()]

    # Requests by urgency
    urg_sql = text("""
        SELECT urgency, COUNT(*) AS requests
        FROM bloodrequest
        GROUP BY urgency
        ORDER BY requests DESC
    """)
    urg = [dict(r) for r in db.execute(urg_sql).mappings().all()]

    # Last 14 days trend
    trend_sql = text("""
        SELECT request_date AS day, COUNT(*) AS requests
        FROM bloodrequest
        WHERE request_date >= (CURDATE() - INTERVAL 13 DAY)
        GROUP BY request_date
        ORDER BY request_date
    """)
    trend = [dict(r) for r in db.execute(trend_sql).mappings().all()]

    return {
        "totals": totals,
        "stock_by_bg": stock,
        "requests_by_bg": reqs,
        "requests_by_urgency": urg,
        "requests_trend_14d": trend,
    }


@app.post("/find-best")
def find_best(payload: FindBestRequest, db: Session = Depends(get_db)):
    urgency_weights = {
        "critical": 1.0,
        "high": 0.8,
        "medium": 0.5,
        "low": 0.2,
    }
    urgency = payload.urgency.lower().strip()
    urgency_w = urgency_weights.get(urgency, 0.5)

    # Strong SQL: distance + stock count + lat/lon for map markers
    query = text("""
        SELECT 
            h.id,
            h.hname,
            h.hcity,
            h.latitude,
            h.longitude,
            (
                6371 * ACOS(
                    COS(RADIANS(:lat)) *
                    COS(RADIANS(h.latitude)) *
                    COS(RADIANS(h.longitude) - RADIANS(:lon)) +
                    SIN(RADIANS(:lat)) *
                    SIN(RADIANS(h.latitude))
                )
            ) AS distance_km,
            COUNT(b.bid) AS stock_units
        FROM hospitals h
        JOIN bloodinfo b ON h.id = b.hid
        WHERE b.bg = :bg
        GROUP BY h.id, h.hname, h.hcity, h.latitude, h.longitude
        ORDER BY distance_km ASC
        LIMIT 10;
    """)

    rows = db.execute(query, {"lat": payload.lat, "lon": payload.lon, "bg": payload.bg}).fetchall()
    if not rows:
        return {"message": "No hospital found with required blood group"}

    # ✅ FIX: normalize distance among returned candidates so distance_score is meaningful
    distances = [float(r.distance_km) for r in rows if r.distance_km is not None]
    min_d = min(distances)
    max_d = max(distances)

    candidates = []
    for r in rows:
        distance = float(r.distance_km) if r.distance_km is not None else 9999.0
        stock = int(r.stock_units) if r.stock_units is not None else 0

        # 0..1 (closest = 1, farthest = 0)
        if max_d == min_d:
            distance_score = 1.0
        else:
            distance_score = 1.0 - ((distance - min_d) / (max_d - min_d))

        # stock score (0..1)
        stock_score = min(1.0, stock / 10.0)

        # final score
        score = (urgency_w * 0.40) + (distance_score * 0.40) + (stock_score * 0.20)

        candidates.append({
            "hospital_id": int(r.id),
            "hospital_name": r.hname,
            "city": r.hcity,
            "latitude": float(r.latitude),
            "longitude": float(r.longitude),
            "distance_km": round(distance, 2),
            "stock_units": stock,
            "score": round(score, 4),
            "score_parts": {
                "urgency_weight": round(urgency_w, 2),
                "distance_score": round(distance_score, 4),
                "stock_score": round(stock_score, 4),
            }
        })

    # best = highest score
    candidates.sort(key=lambda x: x["score"], reverse=True)

    return {"best": candidates[0], "top5": candidates[:5]}


@app.get("/forecast")
def forecast(
    bg: str = Query(..., description="Blood group like A+, O-, AB+"),
    days: int = Query(14, ge=1, le=60),
    db: Session = Depends(get_db),
):
    """
    ML forecast of demand (requests/day) for the next N days for a blood group.
    Uses bloodrequest history.
    """
    hist_sql = text("""
        SELECT request_date AS day, COUNT(*) AS requests
        FROM bloodrequest
        WHERE bg = :bg
        GROUP BY request_date
        ORDER BY request_date
    """)
    hist = [dict(r) for r in db.execute(hist_sql, {"bg": bg}).mappings().all()]

    if len(hist) < 7:
        return JSONResponse(
            {"message": "Not enough history to forecast. Add more rows to bloodrequest (>= 7 days).", "history": hist},
            status_code=200,
        )

    if not forecast_model.exists():
        forecast_model.train_from_history(hist)

    preds = forecast_model.predict_next_days(hist, days=days)

    return {
        "bg": bg,
        "days": days,
        "history": hist[-30:],
        "forecast": preds
    }