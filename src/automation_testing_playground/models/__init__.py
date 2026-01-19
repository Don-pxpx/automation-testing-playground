"""Pydantic models for test data validation."""

from .orangehrm_models import (
    LoginCredentials,
    EmployeeData,
    EmployeeSearchCriteria,
    JobTitleData,
)
from .blazedemo_models import (
    FlightSearch,
    BookingDetails,
    PaymentDetails,
    PassengerInfo,
)

__all__ = [
    "LoginCredentials",
    "EmployeeData",
    "EmployeeSearchCriteria",
    "JobTitleData",
    "FlightSearch",
    "BookingDetails",
    "PaymentDetails",
    "PassengerInfo",
]
