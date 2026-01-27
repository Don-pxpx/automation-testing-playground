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

```
automation-testing-playground/
├── README.md
├── CONTRIBUTING.md
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── src/automation_testing_playground/
│   ├── pages/           # Page Object Models (SauceDemo, BlazeDemo, OrangeHRM)
│   ├── models/          # Pydantic models for test data
│   ├── config/          # Settings, credentials, API config
│   ├── helpers/         # Logging, utilities
│   ├── performance/     # Load testing (Locust)
│   └── security/        # Basic security checks
├── tests/
│   ├── e2e/             # End-to-end tests
│   │   ├── saucedemo/   # Login, cart, checkout
│   │   ├── blazedemo/   # Flight booking
│   │   └── OrangeHRM/   # HR flows
│   ├── integration/     # API tests (e.g. JSONPlaceholder)
│   └── unit/
├── scripts/             # run_tests.py, etc.
├── docs/                # Coding standards, structure notes
└── .github/workflows/   # CI/CD
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

# Run all tests
pytest

# Run a subset
pytest tests/e2e/saucedemo/
pytest tests/e2e/blazedemo/

# With HTML report
pytest --html=reports/report.html --self-contained-html
```

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

---

## Author

**Sizwe** · QA Engineer · Gauteng, South Africa  

- [LinkedIn](https://linkedin.com/in/sizwe-lethuli-59274919)  
- [GitHub](https://github.com/Don-pxpx)

---

*This repo is a portfolio POC. It is read-only; see [CONTRIBUTING.md](CONTRIBUTING.md) for details.*
