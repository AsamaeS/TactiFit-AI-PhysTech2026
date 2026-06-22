from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from .model import predict_fatigue
from .schemas import PlayerSample
from .sensor_simulator import simulate_player_sample

app = FastAPI(title="TactiFit AI API", version="0.1.0")


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
    path = Path(__file__).resolve().parents[2] / "data" / "sample_players.json"
    return {"players": json.loads(path.read_text(encoding="utf-8"))}

