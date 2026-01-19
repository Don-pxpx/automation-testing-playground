# config/credentials.py
import random

class TestData:
    BASE_URL = "https://www.saucedemo.com/"
    VALID_USER = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    INVALID_USER = "locked_out_user"
    INVALID_PASSWORD = "wrong_password"
    DEFAULT_CARD_TYPE = random.choice(["Visa", "American Express", "Diner's Club"])  # optional randomness

    # Optional: Secure this file with .gitignore so you don't leak sensitive defaults

