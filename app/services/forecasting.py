from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import List, Dict

import joblib
import numpy as np
from sklearn.linear_model import Ridge


@dataclass
class ForecastModel:
    model_path: str = "ml/forecast_model.pkl"

    def exists(self) -> bool:
        return Path(self.model_path).exists()

    def _to_xy(self, history: List[Dict]) -> tuple[np.ndarray, np.ndarray, date]:
        """
        history: [{"day": <date>, "requests": <int>}]
        Converts to X = day_index, y = requests.
        """
        # Parse days
        days = []
        y = []
        for r in history:
            d = r["day"]
            if isinstance(d, str):
                d = datetime.fromisoformat(d).date()
            days.append(d)
            y.append(float(r["requests"]))

        start = min(days)
        x = np.array([(d - start).days for d in days], dtype=float).reshape(-1, 1)
        y = np.array(y, dtype=float)
        return x, y, start

    def train_from_history(self, history: List[Dict]) -> None:
        Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)

        X, y, start = self._to_xy(history)

        # Ridge regression = simple, stable baseline for time trend
        model = Ridge(alpha=1.0)
        model.fit(X, y)

        joblib.dump({"model": model, "start_date": start.isoformat()}, self.model_path)

    def predict_next_days(self, history: List[Dict], days: int = 14) -> List[Dict]:
        if not self.exists():
            self.train_from_history(history)

        data = joblib.load(self.model_path)
        model: Ridge = data["model"]
        start = datetime.fromisoformat(data["start_date"]).date()

        # Determine last date in history
        last_day = history[-1]["day"]
        if isinstance(last_day, str):
            last_day = datetime.fromisoformat(last_day).date()

        last_idx = (last_day - start).days

        future = []
        for i in range(1, days + 1):
            idx = last_idx + i
            pred = float(model.predict(np.array([[idx]], dtype=float))[0])
            pred = max(0.0, pred)  # no negative demand

            future.append({
                "day": (last_day + timedelta(days=i)).isoformat(),
                "predicted_requests": round(pred, 2)
            })

        return future