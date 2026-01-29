# config/blazedemo_config.py
# Demo payment values for BlazeDemo (public demo app). Not secrets; centralised per CODING_STANDARDS.
# Override via env if needed for different test targets.

import os

_DEMO_CARD_NUMBER = "1234567890123456"
_DEMO_EXPIRY_MONTH = "12"
_DEMO_EXPIRY_YEAR = "2025"
_DEMO_NAME_ON_CARD = "Test User"


class BlazeDemoData:
    """Demo card and form data for BlazeDemo. Use in page objects and tests instead of inline values."""
    DEMO_CARD_NUMBER = os.environ.get("BLAZEDEMO_DEMO_CARD_NUMBER", _DEMO_CARD_NUMBER)
    DEMO_EXPIRY_MONTH = os.environ.get("BLAZEDEMO_DEMO_EXPIRY_MONTH", _DEMO_EXPIRY_MONTH)
    DEMO_EXPIRY_YEAR = os.environ.get("BLAZEDEMO_DEMO_EXPIRY_YEAR", _DEMO_EXPIRY_YEAR)
    DEMO_NAME_ON_CARD = os.environ.get("BLAZEDEMO_DEMO_NAME_ON_CARD", _DEMO_NAME_ON_CARD)
    DEMO_CARD_TYPE = "American Express"
