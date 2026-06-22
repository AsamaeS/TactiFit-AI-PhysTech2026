from __future__ import annotations

from .features import engineer_features
from .schemas import PlayerSample, PredictionResult


FEATURE_WEIGHTS = {
    "heart_rate_norm": 0.14,
    "hrv_drop": 0.10,
    "body_temp_elevation": 0.08,
    "spo2_drop": 0.05,
    "sprint_ratio": 0.10,
    "hi_ratio": 0.08,
    "accel_decel_load": 0.07,
    "cod_load": 0.06,
    "temp_humidity_stress": 0.08,
    "aqi_impact": 0.04,
    "minutes_load": 0.10,
    "recovery_deficit": 0.06,
    "cv_load": 0.08,
    "heat_effort": 0.06,
}

FEATURE_LABELS = {
    "heart_rate_norm": "Heart rate is high for match intensity",
    "hrv_drop": "HRV is low, suggesting reduced recovery",
    "body_temp_elevation": "Body temperature is elevated",
    "spo2_drop": "SpO2 is lower than optimal",
    "sprint_ratio": "Sprint distance is high relative to total distance",
    "hi_ratio": "High-intensity running load is high",
    "accel_decel_load": "Acceleration/deceleration load is elevated",
    "cod_load": "Change-of-direction load is elevated",
    "temp_humidity_stress": "Heat and humidity increase physiological stress",
    "aqi_impact": "Air quality adds cardiovascular load",
    "minutes_load": "Cumulative match minutes are high",
    "recovery_deficit": "Days of rest are below target",
    "cv_load": "Cumulative cardiovascular load is high",
    "heat_effort": "Heat combined with intense effort increases risk",
}


def predict_fatigue(sample: PlayerSample) -> PredictionResult:
    features = engineer_features(sample)
    contributions = {
        name: value * FEATURE_WEIGHTS[name] for name, value in features.items()
    }
    score = round(min(100.0, sum(contributions.values()) * 100), 1)
    energy = round(max(0.0, 100.0 - score), 1)
    zone = classify_zone(score)
    recommendation = recommend_action(score)
    reasons = explain(contributions)

    return PredictionResult(
        player_id=sample.player_id,
        fatigue_score=score,
        energy_remaining=energy,
        zone=zone,
        recommendation=recommendation,
        reasons=reasons,
    )


def classify_zone(score: float) -> str:
    if score >= 75:
        return "critical"
    if score >= 55:
        return "fatigued"
    if score >= 35:
        return "moderate"
    return "fresh"


def recommend_action(score: float) -> str:
    if score >= 75:
        return "SUB_NOW"
    if score >= 55:
        return "PREPARE_SUB"
    if score >= 35:
        return "WATCH"
    return "KEEP"


def explain(contributions: dict[str, float], limit: int = 5) -> list[dict]:
    ranked = sorted(contributions.items(), key=lambda item: item[1], reverse=True)
    return [
        {
            "feature": name,
            "impact_pct": round(value * 100, 1),
            "message": FEATURE_LABELS[name],
        }
        for name, value in ranked[:limit]
        if value > 0
    ]

