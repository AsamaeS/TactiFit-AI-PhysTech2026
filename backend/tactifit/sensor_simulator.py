from __future__ import annotations

import random

from .schemas import PlayerSample


def simulate_player_sample(player_id: str, match_minute: int = 78) -> PlayerSample:
    """Generate realistic demo data for a lightweight football wearable."""
    fatigue_pressure = match_minute / 90
    return PlayerSample(
        player_id=player_id,
        heart_rate=random.uniform(120, 175 + 15 * fatigue_pressure),
        hrv=random.uniform(25, 70 - 15 * fatigue_pressure),
        body_temp=random.uniform(37.0, 38.6),
        spo2=random.uniform(94, 99),
        total_distance_m=random.uniform(4500, 10500),
        sprint_distance_m=random.uniform(250, 1300),
        accelerations=random.randint(12, 55),
        decelerations=random.randint(12, 55),
        cod_count=random.randint(18, 70),
        high_intensity_distance_m=random.uniform(600, 2600),
        match_minute=match_minute,
        days_rest=random.choice([1, 2, 3, 4]),
        temperature_c=random.uniform(18, 32),
        humidity_pct=random.uniform(35, 75),
        aqi=random.uniform(25, 120),
    )

