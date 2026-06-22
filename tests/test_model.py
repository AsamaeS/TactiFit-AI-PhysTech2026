import unittest

from backend.tactifit.model import predict_fatigue
from backend.tactifit.schemas import PlayerSample


class ModelTest(unittest.TestCase):
    def test_high_risk_sample_triggers_substitution(self):
        sample = PlayerSample(
            player_id="P7",
            heart_rate=198,
            hrv=18,
            body_temp=39.1,
            spo2=92,
            total_distance_m=10500,
            sprint_distance_m=1800,
            accelerations=70,
            decelerations=70,
            cod_count=90,
            high_intensity_distance_m=3600,
            match_minute=105,
            days_rest=0,
            temperature_c=34,
            humidity_pct=80,
            aqi=180,
        )

        result = predict_fatigue(sample)

        self.assertEqual(result.zone, "critical")
        self.assertEqual(result.recommendation, "SUB_NOW")
        self.assertGreaterEqual(result.fatigue_score, 75)
        self.assertGreater(len(result.reasons), 0)

    def test_low_risk_sample_stays_safe(self):
        sample = PlayerSample(
            player_id="P4",
            heart_rate=112,
            hrv=70,
            body_temp=37.1,
            spo2=99,
            total_distance_m=1800,
            sprint_distance_m=80,
            accelerations=8,
            decelerations=8,
            cod_count=10,
            high_intensity_distance_m=150,
            match_minute=15,
            days_rest=4,
            temperature_c=18,
            humidity_pct=35,
            aqi=25,
        )

        result = predict_fatigue(sample)

        self.assertEqual(result.zone, "fresh")
        self.assertEqual(result.recommendation, "KEEP")
        self.assertLess(result.fatigue_score, 35)


if __name__ == "__main__":
    unittest.main()

