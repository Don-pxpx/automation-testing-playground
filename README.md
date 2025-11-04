👋🏽 Hi, I'm Sizwe

**QA Engineer | Automation Architect-in-the-Making | AI Agent Explorer**

---

🌿 **This repo is my sandbox.**

It's where I sharpen my automation skills and prototype clean, intelligent, and maintainable test strategies — not just scripts that "pass."

I treat testing like engineering. My questions aren't just:
> "Does it work?"  
but:  
- 🧱 *How clean is the test architecture?*  
- 🔁 *Can it scale and repeat reliably?*  
- 🚨 *How early can I detect failures — and why?*  
- 🔮 *Can I design for change, not just for now?*

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
├── pages/                    # Page Object Models
│   ├── saucedemo_pages/     # SauceDemo page objects
│   └── blazedemo_pages/     # BlazeDemo page objects
├── tests/                    # Test suites
│   ├── saucedemo/           # SauceDemo tests
│   └── blazedemo/           # BlazeDemo tests
├── config/                   # Configuration files
├── .github/workflows/        # CI/CD workflows
└── requirements.txt          # Python dependencies
```

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
pytest tests/saucedemo/

# Run with HTML report
pytest --html=Artifacts/Reports/test_report.html --self-contained-html
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

⚙️ **Why I build this way**

Because test automation should help you test faster — but also make it fun, challenging, and meaningful.
This playground isn't just about passing checks — it's where I explore smarter workflows, AI tooling, and early security testing strategies.

---

📎 **Let's connect**  
[LinkedIn →](https://linkedin.com/in/sizwe-lethuli-59274919)
