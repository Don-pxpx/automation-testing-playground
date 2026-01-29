# Automation Testing Playground

**Playwright + Python + pytest** — End-to-end and API test automation with Page Object Model.  
*Portfolio POC · Read-only*

---

## About

This repository is a **proof-of-concept** for test automation using **Playwright**, **Python**, and **pytest**. It demonstrates:

- **Page Object Model (POM)** — Reusable page objects for SauceDemo, BlazeDemo, and OrangeHRM
- **E2E & API tests** — Functional flows, cart/checkout, login, and REST API checks
- **Structured framework** — Clear separation of pages, tests, config, and helpers
- **CI/CD-ready** — GitHub Actions for sanity, regression, and code quality

Built for clarity, maintainability, and LinkedIn/portfolio visibility. **No direct contributions** — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Tech Stack

| Layer        | Stack                          |
|-------------|---------------------------------|
| **Runtime** | Python 3.10+                   |
| **E2E**     | Playwright (Chromium / Firefox / WebKit) |
| **Test**    | pytest, pytest-playwright       |
| **Data**    | Pydantic, dotenv, YAML          |
| **Reports** | pytest-html, custom logging      |

---

## Repository Structure

This is the **public automation testing POC** — no other repositories are linked or required.

```
automation-testing-playground/
├── src/automation_testing_playground/   # Production code
│   ├── config/              # Credentials & URLs (env + demo fallbacks)
│   ├── helpers/             # InlineLogger, utilities
│   ├── models/              # Pydantic/dataclass test data models
│   ├── pages/               # Page Object Models
│   │   ├── saucedemo_pages/
│   │   ├── blazedemo_pages/
│   │   ├── orangeHRM_pages/
│   │   └── api/             # API clients
│   ├── performance/         # Load testing (Locust)
│   └── security/            # Vulnerability scan helpers
├── tests/
│   ├── e2e/                 # Playwright E2E tests
│   │   ├── saucedemo/
│   │   ├── blazedemo/
│   │   └── OrangeHRM/
│   ├── integration/         # API integration tests
│   └── unit/
├── ui/                      # React dashboard + Flask API
│   ├── react_dashboard/
│   └── flask_api/
├── scripts/                 # run_tests.py, etc.
├── docs/                    # CODING_STANDARDS.md, DOCKER.md
├── .github/workflows/       # CI (sanity, regression, code quality)
├── reports/                 # Test report output (gitkept)
├── pytest.ini
├── pyproject.toml
└── requirements.txt
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Install & run

```bash
# Clone (read-only portfolio — no PRs)
git clone https://github.com/Don-pxpx/automation-testing-playground.git
cd automation-testing-playground

# Dependencies
pip install -r requirements.txt
playwright install chromium
# playwright install firefox webkit   # optional: multi-browser
```

### Running tests

```bash
# Run all tests (default: Chromium)
pytest

# Run a subset
pytest tests/e2e/saucedemo/
pytest tests/e2e/blazedemo/

# Run on a specific browser (Chromium, Firefox, or WebKit)
pytest tests/e2e/saucedemo/ --browser firefox
pytest tests/e2e/saucedemo/ --browser webkit

# With HTML report
pytest --html=reports/report.html --self-contained-html
```

### Run with Docker (Windows)

To avoid host sandbox, proxy, or plugin conflicts, run tests in a Linux container:

```powershell
docker compose build
docker compose run --rm tests
```

See [docs/DOCKER.md](docs/DOCKER.md) for prerequisites (Docker Desktop + WSL2) and options.

**Cross-OS and cross-browser:** The app and tests are supported on Windows, macOS, and Linux. Playwright runs the same tests on Chromium, Firefox, and WebKit; use `--browser <name>` as above. CI runs sanity and regression on **Ubuntu and macOS** across **Chromium, Firefox, and WebKit**.

---

## Test Coverage

| Target      | Flows covered |
|------------|----------------|
| **SauceDemo** | Login, cart, cart removal, checkout |
| **BlazeDemo** | Flight search, booking, payment confirmation |
| **OrangeHRM** | Login, job titles, employee search, PIM, My Info |
| **API**       | JSONPlaceholder (HTTP methods, endpoints) |

---

## CI/CD

- **Sanity** — Critical paths on push/PR  
- **Regression** — Full suite on push/PR  
- **Code quality** — Linting and style checks  

Triggers: push to `main`, pull requests, `workflow_dispatch`.

**Security & standards:** No sensitive data (credentials, API keys, tokens) is stored in the repo. All real credentials use environment variables; config uses public-demo fallbacks only (e.g. SauceDemo, OrangeHRM demo). CI secrets (e.g. email notifications) live in GitHub Actions secrets only. See `.cursor/rules/no-secrets-and-standards.mdc` and `docs/CODING_STANDARDS.md`.

---

## Author

**Sizwe** · QA Engineer · Gauteng, South Africa  

- [LinkedIn](https://linkedin.com/in/sizwe-lethuli-59274919)  

---

*This repo is a portfolio POC. It is read-only; see [CONTRIBUTING.md](CONTRIBUTING.md) for details.*
