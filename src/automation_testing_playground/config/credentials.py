# config/credentials.py
# Values are read from environment when set. Fallbacks are public demo values only
# (SauceDemo publishes these). Never commit real credentials; use env vars in CI/local.
import os
import random

_DEMO_BASE_URL = "https://www.saucedemo.com/"
_DEMO_VALID_USER = "standard_user"
_DEMO_VALID_PASSWORD = "secret_sauce"
_DEMO_INVALID_USER = "locked_out_user"
_DEMO_INVALID_PASSWORD = "wrong_password"


class TestData:
    BASE_URL = os.environ.get("SAUCEDEMO_BASE_URL", _DEMO_BASE_URL)
    VALID_USER = os.environ.get("SAUCEDEMO_VALID_USER", _DEMO_VALID_USER)
    VALID_PASSWORD = os.environ.get("SAUCEDEMO_VALID_PASSWORD", _DEMO_VALID_PASSWORD)
    INVALID_USER = os.environ.get("SAUCEDEMO_INVALID_USER", _DEMO_INVALID_USER)
    INVALID_PASSWORD = os.environ.get("SAUCEDEMO_INVALID_PASSWORD", _DEMO_INVALID_PASSWORD)
    DEFAULT_CARD_TYPE = random.choice(["Visa", "American Express", "Diner's Club"])
