"""
Performance and Security Logger
Provides structured logging for performance and security testing
"""

import time
from datetime import datetime
from typing import Optional, Dict, Any
from contextlib import contextmanager


class PerformanceSecurityLogger:
    """Logger for performance and security testing"""
    
    def __init__(self, name: str = "Logger"):
        self.name = name
        self.start_time: Optional[float] = None
        self.test_name: Optional[str] = None
    
    def start_test(self, test_name: str, test_type: str = "test"):
        """Start a test session"""
        self.test_name = test_name
        self.start_time = time.time()
        print(f"\n[{self.name}] Starting {test_type}: {test_name}")
    
    def end_test(self, test_name: Optional[str] = None):
        """End a test session"""
        if self.start_time:
            duration = time.time() - self.start_time
            name = test_name or self.test_name or "Test"
            print(f"[{self.name}] Completed {name} in {duration:.2f}s")
    
    def step(self, message: str):
        """Log a step"""
        print(f"[{self.name}] STEP: {message}")
    
    def info(self, message: str):
        """Log info"""
        print(f"[{self.name}] INFO: {message}")
    
    def success(self, message: str):
        """Log success"""
        print(f"[{self.name}] SUCCESS: {message}")
    
    def error(self, message: str):
        """Log error"""
        print(f"[{self.name}] ERROR: {message}")
    
    def warning(self, message: str):
        """Log warning"""
        print(f"[{self.name}] WARNING: {message}")
    
    @contextmanager
    def performance_context(self, operation: str):
        """Context manager for performance measurement"""
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            print(f"[{self.name}] {operation} took {duration:.2f}s")
    
    def performance_metric(self, name: str, value: float, unit: str = "ms"):
        """Log a performance metric"""
        print(f"[{self.name}] METRIC: {name} = {value} {unit}")
