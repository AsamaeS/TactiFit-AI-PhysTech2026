from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PlayerSample:
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

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class PredictionResult:
    player_id: str
    fatigue_score: float
    energy_remaining: float
    zone: str
    recommendation: str
    reasons: list[dict]

    def to_dict(self) -> dict:
        return asdict(self)

