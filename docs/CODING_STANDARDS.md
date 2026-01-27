## Coding Standards for automation-testing-playground

These standards codify the conventions used in this repository so contributors can write code that blends in immediately.

### Tooling and versions

- **Python**: target 3.10+ (CI uses 3.10).
- **Formatter**: Black with line length 88.
- **Import sorter**: isort with Black profile.
- **Linter**: Ruff (or flake8/pylint in CI); rules aligned with E,F,I,UP,B,SIM,PL,TID,C90,PYI; ignore E203.
- **Testing**: pytest with pytest-playwright; `tests/` is the test root; default addopts `-ra -q --strict-markers`.

### Project structure

- **Production code** lives under `src/automation_testing_playground/`:
  - **Config**: `config/` — credentials and URLs; small data-holder classes (e.g. `TestData`, `OrangeHRMData`). Read from `os.environ.get(...)` with public-demo fallbacks only.
  - **Page objects**: `pages/<app>_pages/` — one class per file, named `<Thing>Page` (e.g. `CartPage`, `LoginPage`).
  - **Helpers**: `helpers/` — e.g. `InlineLogger`, shared logging/utilities.
  - **Models**: `models/` — Pydantic or dataclass models for test data.
- **Tests** live under `tests/`:
  - `tests/e2e/<app>/` — end-to-end (Playwright) tests per app (saucedemo, blazedemo, OrangeHRM).
  - `tests/integration/` — API/integration tests.
  - `tests/unit/` — unit tests.
- **No sensitive data in repo.** Config modules use environment variables when set; fallbacks are public-demo values only. Real credentials must never be committed; use `.env` (gitignored) locally and CI secrets in automation.

### Page Object Model (POM)

- Each page module defines a single class whose name matches the file (e.g. `purchase_page.py` → `PurchasePage`).
- The constructor receives the Playwright `page` (and optionally a logger) and stores `self.page`.
- Use **config** for all URLs and credentials — no inline URLs or passwords in page classes. Import `TestData`, `OrangeHRMData`, or other config classes and use their `BASE_URL` / credentials.
- Expose high-level intent methods (verbs) such as `open_login`, `login`, `go_to_checkout`, `fill_checkout_form`, `complete_checkout`.
- Prefer CSS selectors; use Playwright’s built-in waits and locators.
- Methods should return meaningful data when appropriate (e.g. lists of names) and otherwise perform actions/assertions.

### Tests

- Tests use pytest and the Playwright `page` fixture (pytest-playwright). No SeleniumBase.
- Use expressive test function names that describe behavior, e.g. `test_checkout_missing_info_shows_error`.
- Instantiate page objects within tests and drive flows through page methods.
- Assertions use Playwright’s `expect(...)` or standard `assert`.
- Use **config** for URLs and credentials — no inline URLs or passwords in tests. Use `TestData`, `OrangeHRMData`, etc.
- Generate data via **faker** where randomized input is useful; avoid hard-coding unless required. Mask sensitive outputs in logs.

### Logging and reporting

- Use `helpers.log_helpers.InlineLogger` within tests to provide step-oriented, emoji-enhanced logs:
  - `step`, `note`, `success`, `warning`, `error`, `divider`, `summary(passed, failed, skipped)`.
- Start each test with a clear `step` and end with `summary`; keep logs action-focused and concise.

### Naming conventions

- Files: `snake_case.py`.
- Classes: `PascalCase` (e.g. `LoginPage`, `CheckoutPage`).
- Functions/methods: `snake_case` with verb-first names that express intent.
- Variables: `snake_case` with descriptive names; avoid 1–2 letter identifiers.
- Constants / test data classes: `PascalCase` class names (e.g. `TestData`, `OrangeHRMData`).

### Imports and style

- Group imports as: stdlib, third-party, local; isort will enforce with Black profile.
- Avoid wildcard imports.
- Keep lines ≤ 88 chars; let Black handle wrapping.
- Add type hints for public method parameters where helpful; keep private internals lightweight.

### Control flow and errors

- Prefer guard clauses and early returns over deep nesting.
- Raise precise exceptions (e.g. `IndexError` for out-of-range selection) when a method cannot complete its action.
- Avoid silent `try/except`; handle meaningfully or let errors propagate to fail the test.

### Selectors and waits

- Prefer CSS selectors; keep them specific but resilient.
- Use Playwright’s auto-waiting and `wait_for_*` where needed for stability.
- Centralize frequently used selectors as attributes in page objects when reused within that class.

### Test data and randomness

- Use **faker** for dynamic values and mask sensitive outputs in logs.
- When randomness is involved (e.g. selecting items or flights), consider logging the chosen values for diagnosability.

### Pytest configuration

- Put new tests under `tests/` to be auto-discovered.
- Use markers defined in `pyproject.toml` (e.g. `smoke`, `e2e`, `integration`) for suite selection. Example: `pytest -m smoke`.

### Documentation and readability

- Keep methods short and single-purpose.
- Name methods/variables to explain “why”; avoid redundant comments.
- Update this file when conventions evolve so newcomers can align quickly.
