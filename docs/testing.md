# Testing Guide

## Unit Tests

Run:

```bash
python -m unittest discover -s tests
```

The tests verify:

- engineered feature ranges stay between 0 and 1;
- high-risk samples produce critical recommendations;
- low-risk samples stay in the safe zone.

## Manual API Test

Start the API:

```bash
uvicorn backend.tactifit.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/dashboard
http://127.0.0.1:8000/docs
```

## Manual Frontend Test

Open:

```text
frontend/index.html
```

Check that:

- all 11 players appear on the pitch;
- fatigue colors update when changing match minute;
- the right panel shows the selected player's explanation.

