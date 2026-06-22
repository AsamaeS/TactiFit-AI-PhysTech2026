# Technical Architecture

## Real-Time Pipeline

```text
Lightweight sensor or sports watch
  -> phone/tablet via Bluetooth Low Energy
  -> feature engineering
  -> FastAPI fatigue prediction
  -> coach dashboard
```

## Sensor Constraint

The hardware target is a small match-safe wearable:

| Constraint | Target |
| --- | --- |
| Weight | Under 50 g |
| Size | Small enough for vest pocket or armband |
| Battery | More than 90 minutes |
| Transmission | Bluetooth Low Energy or local relay |
| Data | GPS, IMU, heart rate, optional temperature and SpO2 |

## Backend

The backend contains three layers:

1. `schemas.py`: shared data structures.
2. `features.py`: raw data to engineered features.
3. `model.py`: fatigue score, risk zone, recommendation, and explanations.

The baseline model is deterministic by design. It makes the prototype transparent and testable before real training data is available.

## Future ML Upgrade

The model layer can later be replaced by:

- XGBoost classifier or regressor.
- TimeSeriesSplit validation.
- Optuna hyperparameter tuning.
- Isotonic regression calibration.
- SHAP explanations per prediction.

