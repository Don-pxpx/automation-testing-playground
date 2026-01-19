"""Pydantic models for BlazeDemo test data."""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class FlightSearch(BaseModel):
    """Model for flight search criteria."""
    
    departure_city: str = Field(..., description="Departure city")
    destination_city: str = Field(..., description="Destination city")
    
    @field_validator("departure_city", "destination_city")
    @classmethod
    def validate_city(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("City names cannot be empty")
        return v.strip()
    
    def validate_different_cities(self) -> bool:
        """Ensure departure and destination are different."""
        return self.departure_city != self.destination_city


class PassengerInfo(BaseModel):
    """Model for passenger information."""
    
    name: str = Field(..., min_length=1, description="Passenger full name")
    address: str = Field(..., min_length=1, description="Street address")
    city: str = Field(..., min_length=1, description="City")
    state: str = Field(..., min_length=2, max_length=2, description="State code (2 letters)")
    zip_code: str = Field(..., pattern=r"^\d{5}(-\d{4})?$", description="ZIP code")
    
    @field_validator("name", "address", "city")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()
    
    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        if len(v) != 2:
            raise ValueError("State must be 2 characters")
        return v.upper()


class PaymentDetails(BaseModel):
    """Model for payment details."""
    
    card_type: Literal["Visa", "American Express", "Diner's Club"] = Field(
        ..., description="Credit card type"
    )
    card_number: str = Field(..., pattern=r"^\d{13,19}$", description="Credit card number")
    expiry_month: str = Field(..., pattern=r"^(0[1-9]|1[0-2])$", description="Expiry month (MM)")
    expiry_year: str = Field(..., pattern=r"^\d{4}$", description="Expiry year (YYYY)")
    name_on_card: str = Field(..., min_length=1, description="Name on credit card")
    
    @field_validator("card_number")
    @classmethod
    def validate_card_number(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Card number must contain only digits")
        if len(v) < 13 or len(v) > 19:
            raise ValueError("Card number must be between 13 and 19 digits")
        return v
    
    @field_validator("expiry_year")
    @classmethod
    def validate_expiry_year(cls, v: str) -> str:
        year = int(v)
        if year < 2024:
            raise ValueError("Expiry year must be 2024 or later")
        return v


class BookingDetails(BaseModel):
    """Complete booking details model."""
    
    flight_search: FlightSearch = Field(..., description="Flight search criteria")
    passenger_info: PassengerInfo = Field(..., description="Passenger information")
    payment_details: PaymentDetails = Field(..., description="Payment information")
    remember_me: bool = Field(False, description="Remember me checkbox")
    
    def validate(self) -> None:
        """Validate the complete booking."""
        if not self.flight_search.validate_different_cities():
            raise ValueError("Departure and destination cities must be different")
