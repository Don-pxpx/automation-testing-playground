# Test design: principles and patterns (web UI)

Guidance for improving E2E tests in this repo, aligned with **ISO/IEC 25010 functional suitability** (completeness, correctness, appropriateness).

## Design principles

| Principle | Application in this repo |
|-----------|-------------------------|
| **Single Responsibility** | Tests assert one functional outcome; page objects handle UI mechanics. |
| **DRY (Don't Repeat Yourself)** | Shared login/navigation via fixtures or flow helpers—not copy-pasted in every test. |
| **Separation of concerns** | Tests = intent + oracles; pages = locators/actions; models = data. |
| **Stable abstractions** | Tests call `login_with_valid_credentials()`, not raw selectors. |
| **Determinism** | Prefer fixed test data for correctness cases; isolate randomness to exploratory flows. |
| **Fail fast, diagnose clearly** | One primary assertion per requirement; descriptive failure messages tied to REQ IDs. |
| **Traceability** | Every test documents `REQ-ID` in its docstring (see `REQUIREMENTS_TRACE.md`). |

## Patterns in use

| Pattern | Where | Improvement direction |
|---------|--------|------------------------|
| **Page Object Model (POM)** | `src/.../pages/*` | Keep intent methods on pages; move multi-page journeys to **Flow** objects. |
| **Facade** | SauceDemo/BlazeDemo page facades | Extend to OrangeHRM; tests depend on facades only. |
| **Data objects / models** | Pydantic models (BlazeDemo, OrangeHRM) | Use for all apps; builders for valid/invalid variants. |
| **Object Mother / Test Data Builder** | Partial (Faker, `TestData`) | Add `LoginData.valid()`, `PaymentDetails.visa()` for typed, reusable data. |
| **Fixture (pytest)** | Playwright `page` | Add `logged_in_inventory`, `blazedemo_at_purchase` session fixtures. |

## Patterns to introduce next

### 1. Flow / Journey objects (recommended)

Combine pages into task-level APIs:

```python
# flows/saucedemo_checkout_flow.py
class CheckoutFlow:
    def checkout_single_item(self, customer: CustomerInfo) -> None:
        ...
```

Tests read like user stories and satisfy **functional appropriateness**.

### 2. pytest fixtures for common preconditions

```python
@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    LoginPage(page).login_with_valid_credentials()
    return InventoryPage(page)
```

Reduces duplication and **wait_for_timeout** anti-patterns.

### 3. Strategy for locators

- Prefer `get_by_role`, `get_by_label`, `get_by_test_id` over CSS/XPath.
- Centralise locator changes in one page class (**Open/Closed**).

### 4. Parametrize by requirement, not copy-paste

```python
@pytest.mark.parametrize("username,password,req_id", [
    (None, "x", "SDC-LOGIN-003"),
    ("x", None, "SDC-LOGIN-004"),
])
```

One test function, multiple REQ IDs—clearer completeness coverage.

## Anti-patterns to reduce

| Anti-pattern | Example in codebase | Fix |
|--------------|---------------------|-----|
| **Logic in tests** | Random city/flight selection inline | Move to flow helper or parametrized data |
| **Sleep instead of wait** | `page.wait_for_timeout(3000)` (OrangeHRM) | `expect(locator).to_be_visible()` |
| **Duplicate scenarios** | Login empty user in `test_login` and `test_login_edge_cases` | Merge or parametrize; one REQ ID |
| **Mixed layers** | Direct `page.fill` in OrangeHRM login test | Use `LoginPage` only |
| **Logger as assertion** | `logger.summary(passed=1)` | Rely on pytest outcome; logger for diagnostics only |
| **Intentionally failing tests** | BlazeDemo price match / extreme values | Mark `@pytest.mark.xfail` with REQ + defect note |

## Layering model (target)

```
Tests (REQ ID, oracles, markers smoke/regression)
    ↓
Flows / fixtures (user journeys)
    ↓
Page objects (UI actions + element queries)
    ↓
Playwright Page
```

## Improvement pilot (batched)

| Batch | Change | Pilot scope | Status |
|-------|--------|-------------|--------|
| 1 | `logged_in_inventory` fixture | `test_cart.py` → all SauceDemo cart/checkout | Done |
| 2 | `CheckoutFlow` journey object | `test_complete_checkout_single_item` | Done |
| 3 | Parametrize login negatives | `test_login_edge_cases.py` (4 cases) | Done |
| 4 | `@pytest.mark.xfail` | BlazeDemo extreme values, OrangeHRM job titles | Done |
| 5 | OrangeHRM login façade | `test_orangehrm_login.py` | Done |

## Markers (suggested)

- `@pytest.mark.smoke` — one path per app (CI sanity)
- `@pytest.mark.regression` — full functional suite
- `@pytest.mark.requirement("SDC-LOGIN-001")` — optional plugin/custom report filter

## ISO 25010 mapping (functional only)

| Sub-characteristic | Test design action |
|--------------------|-------------------|
| **Completeness** | Trace matrix; mark gaps; parametrize variants (card types, roles) |
| **Correctness** | Strong oracles on visible state; negative tests with exact messages |
| **Appropriateness** | Journey/flow tests; avoid atomic click tests without business meaning |
