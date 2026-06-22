from __future__ import annotations

from .schemas import PlayerSample


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def engineer_features(sample: PlayerSample) -> dict[str, float]:
    """Convert raw wearable/context values into normalized fatigue features."""
    total_distance = max(sample.total_distance_m, 1.0)

    sprint_ratio = sample.sprint_distance_m / total_distance
    hi_ratio = sample.high_intensity_distance_m / total_distance
    accel_decel_load = (sample.accelerations + sample.decelerations) / 120
    cod_load = sample.cod_count / 90

    heart_rate_norm = clamp((sample.heart_rate - 90) / 115)
    hrv_drop = clamp((65 - sample.hrv) / 45)
    body_temp_elevation = clamp((sample.body_temp - 37.0) / 2.0)
    spo2_drop = clamp((98 - sample.spo2) / 8)

    temp_humidity_stress = clamp((sample.temperature_c * sample.humidity_pct / 100) / 35)
    aqi_impact = clamp(sample.aqi / 200)
    minutes_load = clamp(sample.match_minute / 120)
    recovery_deficit = clamp((3 - sample.days_rest) / 3)
    cv_load = clamp((sample.heart_rate * sample.match_minute) / 18000)
    heat_effort = clamp(temp_humidity_stress * (sprint_ratio * 4 + hi_ratio * 2))

    return {
        "heart_rate_norm": heart_rate_norm,
        "hrv_drop": hrv_drop,
        "body_temp_elevation": body_temp_elevation,
        "spo2_drop": spo2_drop,
        "sprint_ratio": clamp(sprint_ratio * 4),
        "hi_ratio": clamp(hi_ratio * 3),
        "accel_decel_load": clamp(accel_decel_load),
        "cod_load": clamp(cod_load),
        "temp_humidity_stress": temp_humidity_stress,
        "aqi_impact": aqi_impact,
        "minutes_load": minutes_load,
        "recovery_deficit": recovery_deficit,
        "cv_load": cv_load,
        "heat_effort": heat_effort,
    }

