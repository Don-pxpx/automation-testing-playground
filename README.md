👋🏽 Hi, I'm Sizwe

**QA Engineer | Automation Architect-in-the-Making | AI Agent Explorer**

---

🌿 **This repo is my sandbox.**

It's where I sharpen my automation skills and prototype clean, intelligent, and maintainable test strategies — not just scripts that "pass."

**Personal experimentation playground** for exploring functional testing, AI-assisted test automation, and upskilling myself by learning how to use AI to run manual and automated tests for **functional**, **penetration**, and **performance** testing.

I treat testing like engineering. My questions aren't just:
> "Does it work?"  
but:  
- 🧱 *How clean is the test architecture?*  
- 🔁 *Can it scale and repeat reliably?*  
- 🚨 *How early can I detect failures — and why?*  
- 🔮 *Can I design for change, not just for now?*
- 🤖 *How can AI assist in test generation and execution?*

---

🚀 **On this repo, you'll find me focusing on:**

- ✅ Building maintainable test frameworks (modular locators, configs, data-driven patterns)
- 🤖 Exploring AI-assisted testing agents (self-healing tests, adaptive test flows)
- 📘 Crafting expressive, human-readable test reports (emoji logs, clean assertions, visibility)
- 🔐 Experimenting with early security validation (auth flows, form guards, boundary checks)
- 🧠 Automating with intention — *not just speed, but clarity and strategy*

---

🌱 **What I'm currently building:**

- [`automation-testing-playground`](https://github.com/Don-pxpx/automation-testing-playground)  
  My structured test lab: login, cart logic, flexible checkout flows, test cleanup.  
  Built with **Playwright** and pytest, featuring reusable Page Object Model components, data-layer flexibility, and emoji-powered reporting.

- `Bots-sandbox` *(private)*  
  Where I explore AI/LLM-powered testing agents and smart automation tools.

---

## 🎯 Recent Updates

### Migration from SeleniumBase to Playwright ✅

I've successfully migrated the entire test suite from **SeleniumBase** to **Playwright** to leverage:
- ⚡ **Faster execution** - Playwright's architecture delivers significantly better performance
- 🎯 **Better reliability** - Built-in auto-waiting and retry mechanisms reduce flakiness
- 🔧 **Modern API** - Cleaner, more intuitive syntax for element interactions
- 🌐 **Cross-browser support** - Easy testing across Chromium, Firefox, and WebKit

**What changed:**
- Refactored all Page Object Models to use Playwright's `page` fixture
- Converted all test files from SeleniumBase's `BaseCase` to Playwright's pytest integration
- Updated CI/CD pipeline to install Playwright browsers
- All tests verified and passing ✅

This migration demonstrates my commitment to staying current with testing best practices and continuously improving test infrastructure.

---

## 📁 Repository Structure

```
automation-testing-playground/
├── README.md
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── pytest.ini
├── src/
│   └── automation_testing_playground/  # Production code
│       ├── pages/                      # Page Object Models
│       ├── helpers/                    # Helper utilities
│       ├── config/                     # Configuration
│       ├── performance/                # Performance testing tools
│       └── security/                   # Security testing tools
├── tests/                              # Test suites
│   ├── unit/                          # Unit tests
│   ├── integration/                   # Integration tests
│   └── e2e/                           # End-to-end tests
│       ├── saucedemo/                 # SauceDemo tests
│       └── blazedemo/                 # BlazeDemo tests
├── scripts/                            # Utility scripts
│   └── run_tests.py                   # Test runner CLI
├── artifacts/                          # Test artifacts
│   └── reports/                       # HTML test reports
├── docs/                               # Documentation
└── .github/workflows/                  # CI/CD workflows
```

> **Note:** This repository is currently being refactored to comply with Personal GitHub Repository Rules. See `REFACTORING_STATUS.md` for migration progress. Run `python scripts/migrate_structure.py` to complete the migration.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/e2e/saucedemo/

# Run with HTML report
pytest --html=artifacts/reports/test_report.html --self-contained-html

# Use the test runner script
python scripts/run_tests.py targets  # List available targets
```

---

## 🧪 Test Coverage

### SauceDemo Tests
- ✅ Login functionality
- ✅ Cart operations
- ✅ Cart removal
- ✅ Checkout flow

### BlazeDemo Tests
- ✅ Flight booking flow
- ✅ Flight selection
- ✅ Purchase confirmation

---

## 🔄 CI/CD Pipeline

The repository includes automated CI/CD workflows:

- **Sanity Tests** - Quick validation of critical paths
- **Regression Tests** - Full test suite execution
- **Code Quality** - Linting and code quality checks

Workflows run automatically on:
- Push to `main` or `master` branches
- Pull requests
- Manual trigger via workflow_dispatch

---

## 📈 Progress & Milestones

### ✅ Completed

- **Migration to Playwright** (Latest)
  - Successfully migrated entire test suite from SeleniumBase to Playwright
  - Refactored all Page Object Models to use Playwright's `page` fixture
  - Updated CI/CD pipeline for Playwright browsers
  - All tests verified and passing ✅

- **Test Framework Architecture**
  - Built maintainable test framework with modular Page Object Models
  - Implemented reusable components for SauceDemo and BlazeDemo
  - Created data-driven test patterns
  - Established coding standards and best practices

- **Test Coverage**
  - SauceDemo: Login, cart operations, cart removal, checkout flow
  - BlazeDemo: Flight booking flow, flight selection, purchase confirmation
  - OrangeHRM: Employee management, login, job titles, employee search

- **CI/CD Pipeline**
  - Automated sanity tests for critical paths
  - Regression test suite execution
  - Code quality checks and linting
  - Automated workflows on push, PR, and manual triggers

- **Reporting & Visualization**
  - Emoji-powered test reports
  - HTML test reports with rich formatting
  - Dashboard for test results visualization

- **Additional Features**
  - API testing with JSONPlaceholder
  - Performance testing with Locust
  - Security vulnerability scanning
  - Form validation testing

### 🔄 In Progress

- Expanding test coverage for OrangeHRM
- Adding more API endpoint tests
- Improving test reliability and flakiness reduction
- Exploring AI-assisted functional testing workflows
- **Repository Structure Refactoring** - Migrating to standard structure (see `REFACTORING_STATUS.md`)

### 📋 Planned

- AI-assisted testing agents exploration
- Self-healing test capabilities
- Advanced security validation tests
- Cross-browser testing expansion
- Mobile testing capabilities
- **Performance Testing** - Load testing, stress testing, performance monitoring (Not Started)
- **Penetration Testing** - Security testing integration (Not Started)

---

⚙️ **Why I build this way**

Because test automation should help you test faster — but also make it fun, challenging, and meaningful.
This playground isn't just about passing checks — it's where I explore smarter workflows, AI tooling, and early security testing strategies.

---

📎 **Let's connect**  
[LinkedIn →](https://linkedin.com/in/sizwe-lethuli-59274919)
