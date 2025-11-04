## Coding Standards for automation-testing-playground

These standards codify the conventions already used in this repository so contributors can write code that blends in immediately.

### Tooling and versions
- **Python**: target `py313`.
- **Formatter**: Black with line length 88.
- **Import sorter**: isort with Black profile.
- **Linter**: Ruff with rules `E,F,I,UP,B,SIM,PL,TID,C90,PYI`; ignore `E203`.
- **Testing**: pytest via SeleniumBase; `tests/` is the test root; default addopts `-ra -q`.

### Project structure
- Keep page objects in `pages/<app>_pages/` with one class per file, named `<Thing>Page` (e.g., `CartPage`).
- Put test modules under `tests/<app>/` with `BaseCase` subclasses per feature grouping.
- Shared helpers live in `helpers/` (e.g., `InlineLogger`).
- Configuration and secrets are under `config/`; reference via small data-holder classes.

### Page Object Model (POM)
- Each page module defines a single class whose name matches the file (e.g., `purchase_page.py` → `PurchasePage`).
- The constructor receives the SeleniumBase test instance as `base` or `test` and stores it as `self.base`/`self.test`.
- Expose high-level intent methods (verbs) such as `open_homepage`, `login`, `go_to_checkout`, `fill_checkout_form`, `complete_checkout`.
- Prefer CSS selectors; use Selenium `By` only when necessary (e.g., cell access in tables).
- Methods should return meaningful data when appropriate (e.g., lists of names) and otherwise perform actions/assertions via the provided base.

### Tests
- Test classes subclass `seleniumbase.BaseCase`.
- Use one test class per feature area; name classes `<Feature>Tests`.
- Use expressive test function names that describe behavior, e.g., `test_checkout_missing_info_shows_error`.
- Instantiate page objects within tests and drive flows through page methods.
- Assertions come from SeleniumBase (e.g., `assert_element`, `assert_text`, `assert_true`, `assert_in`).
- Generate data via `faker` where randomized input is useful; avoid hard-coding unless required.

### Logging and reporting
- Use `helpers.log_helpers.InlineLogger` within tests to provide step-oriented, emoji-enhanced logs:
  - `step`, `note`, `success`, `warning`, `error`, `divider`, `summary(passed, failed, skipped)`.
- Start each test with a clear `step` and end with `summary`; keep logs action-focused and concise.

### Naming conventions
- Files: `snake_case.py`.
- Classes: `PascalCase` (e.g., `LoginPage`, `CheckoutPage`).
- Functions/methods: `snake_case` with verb-first names that express intent.
- Variables: `snake_case` with descriptive names; avoid 1–2 letter identifiers.
- Constants / test data classes: `PascalCase` class names (e.g., `TestData`, `OrangeHRMData`).

### Imports and style
- Group imports as: stdlib, third-party, local; isort will enforce with Black profile.
- Avoid wildcard imports.
- Keep lines ≤ 88 chars; let Black handle wrapping.
- Add type hints for public method parameters where helpful; keep private internals lightweight.

### Control flow and errors
- Prefer guard clauses and early returns over deep nesting.
- Raise precise exceptions (e.g., `IndexError` for out-of-range selection) when a method cannot complete its action.
- Avoid silent `try/except`; handle meaningfully or let errors propagate to fail the test.

### Selectors and waits
- Prefer CSS selectors; keep them specific but resilient.
- Use SeleniumBase conveniences: `wait_for_element_visible`, `is_element_visible`, etc., for stability.
- Centralize frequently used selectors as attributes in page objects when reused within that class.

### Test data and randomness
- Use `faker` for dynamic values and mask sensitive outputs in logs.
- When randomness is involved (e.g., selecting items or flights), consider logging the chosen values for diagnosability.

### Pytest configuration
- Put new tests under `tests/` to be auto-discovered.
- Use markers defined in `pyproject.toml` (`smoke`, `e2e`) for suite selection. Example: `pytest -m smoke`.

### Documentation and readability
- Keep methods short and single-purpose.
- Name methods/variables to explain “why”; avoid redundant comments.
- Update this file when conventions evolve so newcomers can align quickly.

