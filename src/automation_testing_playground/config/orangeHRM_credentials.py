# config/orangeHRM_credentials.py
# Values are read from environment when set. Fallbacks are public demo values only
# (OrangeHRM demo site uses these). Never commit real credentials; use env vars in CI/local.
import os

_DEMO_BASE_URL = "https://opensource-demo.orangehrmlive.com/"
_DEMO_USER = "Admin"
_DEMO_PASSWORD = "admin123"


class OrangeHRMData:
    BASE_URL = os.environ.get("ORANGEHRM_BASE_URL", _DEMO_BASE_URL)
    USERNAME = os.environ.get("ORANGEHRM_USER", _DEMO_USER)
    PASSWORD = os.environ.get("ORANGEHRM_PASSWORD", _DEMO_PASSWORD)
