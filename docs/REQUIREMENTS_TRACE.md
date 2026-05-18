# Requirements traceability (web UI E2E)

Requirement IDs appear in test docstrings as `APP-AREA-NNN`.

| ID | Application | Capability | ISO 25010 focus | Test module |
|----|-------------|------------|-----------------|-------------|
| SDC-LOGIN-001 | SauceDemo | Valid login → inventory | Correctness | `test_login.py` |
| SDC-LOGIN-002 | SauceDemo | Invalid credentials error | Correctness | `test_login.py` |
| SDC-LOGIN-003 | SauceDemo | Empty username error | Correctness | `test_login.py`, `test_login_edge_cases.py` |
| SDC-LOGIN-004 | SauceDemo | Empty password error | Correctness | `test_login.py`, `test_login_edge_cases.py` |
| SDC-LOGIN-005 | SauceDemo | Locked-out user error | Correctness | `test_login_edge_cases.py` |
| SDC-LOGIN-006 | SauceDemo | Wrong password error message | Correctness | `test_login_edge_cases.py` |
| SDC-CART-001 | SauceDemo | Add single product; badge count | Correctness | `test_cart.py` |
| SDC-CART-002 | SauceDemo | Add backpack + fleece only | Completeness | `test_cart.py` |
| SDC-CART-003 | SauceDemo | Remove items; retain preferred product | Appropriateness | `test_cart_removal.py` |
| SDC-CART-004 | SauceDemo | Remove all items; empty cart | Correctness | `test_cart_removal.py` |
| SDC-CART-005 | SauceDemo | Cancel checkout then complete purchase | Appropriateness | `test_cart_removal.py` |
| SDC-CHKO-001 | SauceDemo | Checkout single item to confirmation | Correctness | `test_checkout.py` |
| SDC-CHKO-002 | SauceDemo | Checkout blocks missing customer info | Correctness | `test_checkout.py` |
| SDC-CHKO-003 | SauceDemo | Checkout multiple items | Completeness | `test_checkout.py` |
| SDC-CHKO-004 | SauceDemo | Cancel checkout returns to inventory | Appropriateness | `test_checkout.py` |
| BZD-BOOK-001 | BlazeDemo | End-to-end flight booking | Appropriateness | `test_booking_flow.py` |
| BZD-BOOK-002 | BlazeDemo | Purchase vs confirmation details | Correctness | `test_booking_details_match.py` |
| BZD-BOOK-003 | BlazeDemo | Booking with multiple card types | Completeness | `test_booking_with_various_card_types.py` |
| BZD-FORM-001 | BlazeDemo | Empty purchase form behaviour | Correctness | `test_blazedemo_form_validation.py` |
| BZD-FORM-002 | BlazeDemo | Invalid email format behaviour | Correctness | `test_blazedemo_form_validation.py` |
| BZD-FORM-003 | BlazeDemo | Special characters in name | Correctness | `test_blazedemo_form_validation.py` |
| BZD-FORM-004 | BlazeDemo | Missing required fields | Correctness | `test_blazedemo_form_validation.py` |
| BZD-FORM-005 | BlazeDemo | Extreme input values (known demo gap) | Correctness | `test_blazedemo_form_validation.py` |
| BZD-FORM-006 | BlazeDemo | Purchase form fields visible | Completeness | `test_blazedemo_form_validation.py` |
| BZD-FORM-007 | BlazeDemo | Valid purchase confirmation message | Correctness | `test_blazedemo_form_validation.py` |
| OHR-AUTH-001 | OrangeHRM | Valid and invalid login | Correctness | `test_orangehrm_login.py` |
| OHR-PIM-001 | OrangeHRM | Add employee (random + custom ID) | Appropriateness | `test_orangehrm_add_employee.py` |
| OHR-PIM-002 | OrangeHRM | Search employee | Correctness | `test_orangehrm_employee_search.py` |
| OHR-ADMIN-001 | OrangeHRM | Job titles list | Completeness | `test_orangehrm_job_titles.py` |
| OHR-SELF-001 | OrangeHRM | My Info personal details | Appropriateness | `test_orangehrm_my_info.py` |
