"""Pydantic models for OrangeHRM test data."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class LoginCredentials(BaseModel):
    """Model for OrangeHRM login credentials."""
    
    username: str = Field(..., description="Username for login")
    password: str = Field(..., description="Password for login")
    
    @field_validator("username", "password")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Username and password cannot be empty")
        return v.strip()


class EmployeeData(BaseModel):
    """Model for employee data."""
    
    first_name: str = Field(..., min_length=1, description="Employee first name")
    middle_name: Optional[str] = Field(None, description="Employee middle name")
    last_name: str = Field(..., min_length=1, description="Employee last name")
    employee_id: Optional[str] = Field(None, description="Custom employee ID")
    
    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("First and last names cannot be empty")
        return v.strip()


class EmployeeSearchCriteria(BaseModel):
    """Model for employee search criteria."""
    
    employee_name: Optional[str] = Field(None, description="Employee name to search")
    employee_id: Optional[str] = Field(None, description="Employee ID to search")
    supervisor_name: Optional[str] = Field(None, description="Supervisor name to search")
    
    def has_criteria(self) -> bool:
        """Check if any search criteria is provided."""
        return any([self.employee_name, self.employee_id, self.supervisor_name])


class JobTitleData(BaseModel):
    """Model for job title data."""
    
    job_title: str = Field(..., min_length=1, description="Job title name")
    job_description: Optional[str] = Field(None, description="Job description")
    note: Optional[str] = Field(None, description="Additional notes")
    
    @field_validator("job_title")
    @classmethod
    def validate_job_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Job title cannot be empty")
        return v.strip()
