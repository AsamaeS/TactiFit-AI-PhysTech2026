import unittest

from backend.tactifit.features import engineer_features
from backend.tactifit.schemas import PlayerSample


class FeatureEngineeringTest(unittest.TestCase):
    def test_engineered_features_are_normalized(self):
        sample = PlayerSample(
            player_id="P7",
            heart_rate=178,
            hrv=31,
            body_temp=38.3,
            spo2=95,
            total_distance_m=9200,
            sprint_distance_m=1180,
            accelerations=44,
            decelerations=41,
            cod_count=58,
            high_intensity_distance_m=2400,
            match_minute=78,
            days_rest=1,
            temperature_c=28,
            humidity_pct=65,
            aqi=90,
        )

        features = engineer_features(sample)

        self.assertGreaterEqual(len(features), 10)
        for value in features.values():
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1)


if __name__ == "__main__":
    unittest.main()

