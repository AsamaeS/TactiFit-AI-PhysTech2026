# TactiFit AI - PhysTech 2026

TactiFit AI is a real-time football fatigue monitoring prototype. It combines lightweight wearable data, contextual conditions, physics-inspired features, and explainable recommendations for coaches.

The goal is simple: detect when a player is moving from normal effort to risky fatigue before performance drops or injury risk rises.

## Why This Project

Most simple fatigue models use only speed, cadence, and heart rate. TactiFit AI uses a richer signal:

| Area | Examples |
| --- | --- |
| Physiological | heart rate, HRV, body temperature, SpO2 |
| Kinematic | distance, sprint distance, accelerations, decelerations, change of direction |
| Contextual | temperature, humidity, air quality, heat stress |
| Temporal | match minute, match phase, days of rest |
| Engineered | sprint ratio, cardiovascular load, recovery deficit, heat effort |

The production target is an XGBoost model with calibration and SHAP explanations. This repository starts with a deterministic baseline that is easy to test, explain, and replace later.

## Repository Architecture

```text
TactiFit-AI-PhysTech2026/
  backend/
    tactifit/
      api.py                # FastAPI endpoints for predictions and dashboard data
      features.py           # Feature engineering from sensor/context data
      model.py              # Baseline fatigue model and recommendation rules
      schemas.py            # Dataclasses used across the backend
      sensor_simulator.py   # Lightweight wearable data simulator
  data/
    sample_players.json     # Demo squad data
  docs/
    architecture.md         # Technical architecture and real-time pipeline
    testing.md              # How to run and validate the project
  frontend/
    index.html              # Coach dashboard UI
    style.css               # Dashboard styling
    app.js                  # Demo dashboard logic
  tests/
    test_features.py
    test_model.py
  pyproject.toml
  requirements.txt
```

## Quick Start

### 1. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run tests

```bash
python -m unittest discover -s tests
```

### 4. Run the API

```bash
uvicorn backend.tactifit.api:app --reload
```

Open:

- API health check: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs
- Dashboard payload: http://127.0.0.1:8000/dashboard

### 5. Open the dashboard

Open `frontend/index.html` in a browser. The dashboard works with local demo data, so it remains usable even if the API is not running.

## Example Prediction

```json
{
  "player_id": "P7",
  "heart_rate": 178,
  "hrv": 31,
  "body_temp": 38.3,
  "spo2": 95,
  "total_distance_m": 9200,
  "sprint_distance_m": 1180,
  "accelerations": 44,
  "decelerations": 41,
  "cod_count": 58,
  "high_intensity_distance_m": 2400,
  "match_minute": 78,
  "days_rest": 1,
  "temperature_c": 28,
  "humidity_pct": 65,
  "aqi": 90
}
```

The API returns a fatigue score, a risk zone, a coach recommendation, and the top reasons behind the decision.

## Scientific Positioning

TactiFit AI is designed around three technical improvements:

1. More complete features than basic TIPE-style models.
2. Real-time explainability through ranked feature contributions.
3. A lightweight sensor constraint: target weight under 50 g, wireless transmission, and no disturbance during match play.

## Next Technical Milestones

- Train an XGBoost model on real match sessions.
- Add TimeSeriesSplit validation to avoid temporal leakage.
- Add probability calibration with isotonic regression.
- Replace heuristic explanations with SHAP values.
- Stream live wearable data through WebSocket or Server-Sent Events.

