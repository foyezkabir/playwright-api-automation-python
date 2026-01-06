"""
API Response Schema Validation using Pydantic models.
Validates API responses against expected schemas.
"""

from typing import Any, Type

from pydantic import BaseModel, EmailStr, Field, validator

# ========== Signup API Schemas ==========


class SignupRequestSchema(BaseModel):
    """Schema for signup request payload."""

    name: str = Field(..., min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @validator("name")
    def validate_name(cls, v):
        """Validate name doesn't contain numbers or special chars."""
        if any(char.isdigit() for char in v):
            raise ValueError("Name should not contain numbers")
        return v

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        """Validate password and confirm_password match."""
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class SignupSuccessResponseSchema(BaseModel):
    """Schema for successful signup response."""

    message: str
    error: bool
    code: str
    data: dict | None = None

    class Config:
        extra = "allow"  # Allow additional fields


class ErrorDetailSchema(BaseModel):
    """Schema for error detail object."""

    field: str | None = None
    message: str
    code: str | None = None


class SignupErrorResponseSchema(BaseModel):
    """Schema for error response."""

    error: str | None = None
    errors: list[ErrorDetailSchema] | None = None
    message: str | None = None
    detail: str | None = None
    status_code: int | None = None

    class Config:
        extra = "allow"


# ========== Login API Schemas ==========


class LoginRequestSchema(BaseModel):
    """Schema for login request payload."""

    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginSuccessResponseSchema(BaseModel):
    """Schema for successful login response."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None
    user: dict[str, Any] | None = None

    class Config:
        extra = "allow"


# ========== User Profile Schemas ==========


class UserProfileSchema(BaseModel):
    """Schema for user profile data."""

    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    is_active: bool = True

    class Config:
        extra = "allow"


# ========== Validation Helper Functions ==========


def validate_response_schema(response_data: dict, schema: Type[BaseModel]) -> tuple[bool, str | None]:
    """
    Validates response data against a Pydantic schema.

    Args:
        response_data: Dictionary containing API response
        schema: Pydantic model class to validate against

    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    try:
        schema(**response_data)
        return True, None
    except Exception as e:
        return False, str(e)


def assert_response_schema(
    response_data: dict, schema: Type[BaseModel], error_message: str = "Schema validation failed"
):
    """
    Asserts that response data matches the expected schema.

    Args:
        response_data: Dictionary containing API response
        schema: Pydantic model class to validate against
        error_message: Custom error message prefix

    Raises:
        AssertionError: If validation fails
    """
    is_valid, error = validate_response_schema(response_data, schema)
    assert is_valid, f"{error_message}: {error}"


# ========== Response Time Validator ==========


class PerformanceAssertion:
    """Helper class for performance assertions."""

    @staticmethod
    def assert_response_time(actual_time_ms: float, max_time_ms: float, endpoint: str = ""):
        """
        Asserts that response time is within acceptable limits.

        Args:
            actual_time_ms: Actual response time in milliseconds
            max_time_ms: Maximum acceptable time in milliseconds
            endpoint: Endpoint name for error message

        Raises:
            AssertionError: If response time exceeds limit
        """
        assert actual_time_ms <= max_time_ms, (
            f"{endpoint} Response time {actual_time_ms}ms exceeds limit of {max_time_ms}ms"
        )

    @staticmethod
    def get_response_time_ms(response) -> float:
        """
        Extracts response time from Playwright APIResponse object.
        This is a placeholder - actual implementation depends on how you track timing.

        Args:
            response: Playwright APIResponse object

        Returns:
            Response time in milliseconds
        """
        # You may need to implement custom timing logic
        # For example, using time.time() before and after request
        return 0.0  # Placeholder
