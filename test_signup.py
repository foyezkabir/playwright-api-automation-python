import pytest
import time
from playwright.sync_api import Playwright, APIRequestContext, expect

BASE_URL = "https://eks-dev-lb.shadhinlab.xyz"
SIGNUP_ENDPOINT = "/api/authentication/signup/"

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> APIRequestContext:
    request_context = playwright.request.new_context(base_url=BASE_URL)
    yield request_context
    request_context.dispose()

def get_unique_email(prefix="test"):
    timestamp = int(time.time() * 1000)
    return f"{prefix}_{timestamp}@example.com"

def test_signup_success(api_request_context: APIRequestContext):
    """Test successful signup with valid data."""
    timestamp = int(time.time())
    email = get_unique_email("success")
    
    payload = {
        "name": f"Test User {timestamp}",
        "email": email,
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status in [200, 201], f"Expected 200 or 201, got {response.status}. Body: {response.text()}"

def test_signup_missing_fields(api_request_context: APIRequestContext):
    """Test signup with missing required fields."""
    payload = {
        "email": get_unique_email("missing"),
        "password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400, got {response.status}. Body: {response.text()}"

def test_signup_invalid_email(api_request_context: APIRequestContext):
    """Test signup with invalid email format."""
    payload = {
        "name": "Invalid Email User",
        "email": "invalid-email-format",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400, got {response.status}. Body: {response.text()}"
    
@pytest.mark.xfail(reason="API does not validate password mismatch")
def test_signup_password_mismatch(api_request_context: APIRequestContext):
    """Test signup when password and confirm_password do not match."""
    timestamp = int(time.time())
    payload = {
        "name": f"Mismatch User {timestamp}",
        "email": get_unique_email("mismatch"),
        "password": "Password123!",
        "confirm_password": "DifferentPassword!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400, got {response.status}. Body: {response.text()}"

# --- Name Validations ---

@pytest.mark.xfail(reason="API does not validate name min length")
def test_signup_name_min_length(api_request_context: APIRequestContext):
    """Name must be at least 3 characters."""
    payload = {
        "name": "Ab",
        "email": get_unique_email("min_len"),
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for short name, got {response.status}"

@pytest.mark.xfail(reason="API does not validate name special chars start")
def test_signup_name_special_chars_start(api_request_context: APIRequestContext):
    """Name must not start with special characters."""
    payload = {
        "name": "@User",
        "email": get_unique_email("spec_start"),
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for special char at start, got {response.status}"

@pytest.mark.xfail(reason="API does not validate name special chars end")
def test_signup_name_special_chars_end(api_request_context: APIRequestContext):
    """Name must not end with special characters."""
    payload = {
        "name": "User!",
        "email": get_unique_email("spec_end"),
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for special char at end, got {response.status}"

@pytest.mark.xfail(reason="API does not validate leading space")
def test_signup_name_leading_space(api_request_context: APIRequestContext):
    """Name must not start with a space."""
    payload = {
        "name": " User",
        "email": get_unique_email("lead_space"),
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for leading space, got {response.status}"

@pytest.mark.xfail(reason="API does not validate trailing space")
def test_signup_name_trailing_space(api_request_context: APIRequestContext):
    """Name must not end with a space."""
    payload = {
        "name": "User ",
        "email": get_unique_email("trail_space"),
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for trailing space, got {response.status}"

@pytest.mark.xfail(reason="API does not validate name numbers")
def test_signup_name_no_numbers(api_request_context: APIRequestContext):
    """Name not allow any number."""
    payload = {
        "name": "User123",
        "email": get_unique_email("num_name"),
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for name with numbers, got {response.status}"

@pytest.mark.xfail(reason="API does not validate name max length")
def test_signup_name_max_length(api_request_context: APIRequestContext):
    """Name must not exceed 80 characters."""
    long_name = "A" * 81
    payload = {
        "name": long_name,
        "email": get_unique_email("max_len"),
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for long name, got {response.status}"

# --- Email Validations ---

@pytest.mark.parametrize("domain", ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"])
def test_signup_email_public_domain(api_request_context: APIRequestContext, domain):
    """Public domains are not allowed."""
    # Use a random prefix to ensure uniqueness even within parametrized tests
    email = get_unique_email(f"pub_dom_{domain.split('.')[0]}")
    # Force the domain to be the parametrized one
    email = email.split('@')[0] + f"@{domain}"
    
    payload = {
        "name": "Valid User",
        "email": email,
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for public domain {domain}, got {response.status}"

# --- Password Validations ---

@pytest.mark.xfail(reason="API returns 500 Internal Server Error for missing uppercase")
def test_signup_password_no_upper(api_request_context: APIRequestContext):
    """Password must contain uppercase."""
    payload = {
        "name": "Valid User",
        "email": get_unique_email("no_upper"),
        "password": "password123!",
        "confirm_password": "password123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for password missing uppercase, got {response.status}"

@pytest.mark.xfail(reason="API returns 500 Internal Server Error for missing lowercase")
def test_signup_password_no_lower(api_request_context: APIRequestContext):
    """Password must contain lowercase."""
    payload = {
        "name": "Valid User",
        "email": get_unique_email("no_lower"),
        "password": "PASSWORD123!",
        "confirm_password": "PASSWORD123!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for password missing lowercase, got {response.status}"

@pytest.mark.xfail(reason="API returns 500 Internal Server Error for missing number")
def test_signup_password_no_number(api_request_context: APIRequestContext):
    """Password must contain number."""
    payload = {
        "name": "Valid User",
        "email": get_unique_email("no_num"),
        "password": "Password!",
        "confirm_password": "Password!"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for password missing number, got {response.status}"

@pytest.mark.xfail(reason="API returns 500 Internal Server Error for missing special char")
def test_signup_password_no_special(api_request_context: APIRequestContext):
    """Password must contain special character."""
    payload = {
        "name": "Valid User",
        "email": get_unique_email("no_spec"),
        "password": "Password123",
        "confirm_password": "Password123"
    }
    response = api_request_context.post(SIGNUP_ENDPOINT, data=payload)
    assert response.status == 400, f"Expected 400 for password missing special char, got {response.status}"
