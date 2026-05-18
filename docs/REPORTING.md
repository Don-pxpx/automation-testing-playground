# Test reporting metrics (TypeScript)

Automated runs write **`reports/metrics-latest.json`** (Python pytest hook). The dashboard uses **TypeScript** to aggregate and display metrics.

> **Note:** Test execution remains **Python + Playwright**. Reporting logic lives in `ui/reporting/` (TypeScript), not Ruby.

## Flow

1. `pytest tests/e2e/` runs (optionally `-m smoke` for a quick check).
2. `tests/conftest.py` exports pass/fail, suites, requirement IDs, duration.
3. Flask API serves `GET /api/metrics`.
4. React dashboard (`ui/react_dashboard`) uses `@reporting` TypeScript helpers.

## Local dashboard

```powershell
# Terminal 1 — API
cd ui/flask_api
pip install -r requirements.txt
python app.py

# Terminal 2 — run tests (generates metrics)
cd ../..
pytest tests/e2e/ --browser chromium

# Terminal 3 — dashboard
cd ui/react_dashboard
npm install
npm run dev
```

Open http://localhost:3001

## TypeScript package

```bash
cd ui/reporting
npm install
npm run typecheck
```
