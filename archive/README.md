# Archived code

Archived on **2026-05-18** to keep the active repo focused on **web UI functional automation** (Playwright E2E).

## Contents

| Path | Former location | Reason |
|------|-----------------|--------|
| `non-functional/performance/` | `src/.../performance/` | Load testing (Locust) — ISO 25010 performance efficiency, out of UI scope |
| `non-functional/security/` | `src/.../security/` | Vulnerability scanning — ISO 25010 security, out of UI scope |
| `integration-api/tests/` | `tests/integration/` | REST/API tests — functional but not web UI |
| `integration-api/src/pages/api/` | `src/.../pages/api/` | API clients used only by archived integration tests |
| `integration-api/src/config/api_config.py` | `src/.../config/api_config.py` | API configuration |
| `scripts/run_tests_legacy_perf_sec.py` | `scripts/run_tests.py` | CLI for performance/security/integration |

## Restore

Move folders back to their original paths and reinstall optional dependencies from `archive/requirements-archived.txt`.

## Active test entry point

```bash
pytest tests/e2e/
```

Or: `python scripts/run_tests.py e2e`
