from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .model import predict_fatigue
from .schemas import PlayerSample
from .sensor_simulator import simulate_player_sample

app = FastAPI(title="TactiFit AI API", version="0.1.0")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class PlayerSampleIn(BaseModel):
    player_id: str
    heart_rate: float
    hrv: float
    body_temp: float
    spo2: float
    total_distance_m: float
    sprint_distance_m: float
    accelerations: int
    decelerations: int
    cod_count: int
    high_intensity_distance_m: float
    match_minute: int
    days_rest: int
    temperature_c: float
    humidity_pct: float
    aqi: float


@app.get("/")
def root() -> dict:
    return {
        "message": "Welcome to TactiFit AI API",
        "app": "/app",
        "docs": "/docs",
        "health": "/health",
        "dashboard": "/dashboard",
    }


@app.get("/app", response_class=FileResponse)
def coach_app() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/style.css", response_class=FileResponse)
def frontend_styles() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "style.css", media_type="text/css")


@app.get("/app.js", response_class=FileResponse)
def frontend_script() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "app.js", media_type="text/javascript")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "tactifit-ai"}


@app.post("/predict")
def predict(payload: PlayerSampleIn) -> dict:
    sample = PlayerSample(**payload.model_dump())
    return predict_fatigue(sample).to_dict()


@app.get("/dashboard")
def dashboard(match_minute: int = 78) -> dict:
    players = [simulate_player_sample(f"P{i}", match_minute) for i in range(1, 12)]
    predictions = [predict_fatigue(player).to_dict() for player in players]
    team_avg = round(sum(item["energy_remaining"] for item in predictions) / len(predictions), 1)

    return {
        "match_minute": match_minute,
        "team_energy_avg": team_avg,
        "weather": {"temperature_c": 28, "humidity_pct": 65, "aqi": 90},
        "players": predictions,
    }


@app.get("/demo-players")
def demo_players() -> dict:
    path = PROJECT_ROOT / "data" / "sample_players.json"
    return {"players": json.loads(path.read_text(encoding="utf-8"))}
