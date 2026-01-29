"""
Configuration settings for test targets and security config
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class TestTargetsConfig:
    """Configuration for test targets"""
    DEMO_APPS: Dict[str, str] = None
    API_ENDPOINTS: Dict[str, str] = None
    INTERNAL_APPS: Dict[str, str] = None  # Optional; used by scripts/run_tests.py targets

    def __post_init__(self):
        if self.DEMO_APPS is None:
            self.DEMO_APPS = {
                "saucedemo": "https://www.saucedemo.com",
                "blazedemo": "https://blazedemo.com",
                "orangehrm": "https://opensource-demo.orangehrmlive.com"
            }
        if self.API_ENDPOINTS is None:
            self.API_ENDPOINTS = {
                "jsonplaceholder": "https://jsonplaceholder.typicode.com",
                "httpbin": "https://httpbin.org"
            }
        if self.INTERNAL_APPS is None:
            self.INTERNAL_APPS = {}  # No internal apps by default; override via env if needed


@dataclass
class SecurityConfig:
    """Configuration for security scanning"""
    SCAN_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    VULNERABILITY_SEVERITIES: list = None
    
    def __post_init__(self):
        if self.VULNERABILITY_SEVERITIES is None:
            self.VULNERABILITY_SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


# Global configuration instances
TEST_TARGETS_CONFIG = TestTargetsConfig()
SECURITY_CONFIG = SecurityConfig()
