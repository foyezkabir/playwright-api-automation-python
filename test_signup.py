import pytest
import time
from typing import Dict, Any
from playwright.sync_api import Playwright, APIRequestContext, APIResponse

# --- Configuration ---
BASE_URL = "https://eks-dev-lb.shadhinlab.xyz"
SIGNUP_ENDPOINT = "/api/authentication/signup/"

# --- API Object Model ---
class SignupClient:
    """Helper class to interact with the Signup API."""

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context

    def create_user(self, payload: Dict[str, Any]) -> APIResponse:
        """Sends a POST request to create a user."""
        return self.request.post(SIGNUP_ENDPOINT, data=payload)

    @staticmethod
    def generate_unique_email(prefix: str = "test") -> str:
        """Generates a unique email address based on timestamp."""
        timestamp = int(time.time() * 1000)
        return f"{prefix}_{timestamp}@example.com"

    @staticmethod
    def default_payload(email_prefix: str = "user") -> Dict[str, str]:
        """Generates a valid default payload with a unique email."""
        timestamp = int(time.time())
        email = SignupClient.generate_unique_email(email_prefix)
        return {
            "name": f"Test User {timestamp}",
            "email": email,
            "password": "Password123!",
            "confirm_password": "Password123!"
        }

# --- Fixtures ---
@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> APIRequestContext:
    """Creates a shared API Request Context for the session."""
    headers = {"Content-Type": "application/json"}
    context = playwright.request.new_context(base_url=BASE_URL, extra_http_headers=headers)
    yield context
    context.dispose()

@pytest.fixture(scope="session")
def signup_api(api_context: APIRequestContext) -> SignupClient:
    """Returns an instance of the SignupClient."""
    return SignupClient(api_context)

# --- Test Suite ---
class TestSignup:
    """Test suite for User Signup API."""

    def test_signup_success(self, signup_api: SignupClient):
        """Verify successful user registration with valid data."""
        payload = signup_api.default_payload("success")
        response = signup_api.create_user(payload)
        
        assert response.status in [200, 201], \
            f"Expected success (200/201), got {response.status}. Body: {response.text()}"

    def test_signup_missing_fields(self, signup_api: SignupClient):
        """Verify validation error when required fields are missing."""
        payload = {
            "email": signup_api.generate_unique_email("missing"),
            "password": "Password123!"
        }
        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400, got {response.status}"

    def test_signup_invalid_email(self, signup_api: SignupClient):
        """Verify validation error for invalid email format."""
        payload = signup_api.default_payload()
        payload["email"] = "invalid-email-format"
        
        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400, got {response.status}"

    @pytest.mark.xfail(reason="Bug: API accepts mismatched passwords")
    def test_signup_password_mismatch(self, signup_api: SignupClient):
        """Verify error when password and confirm_password do not match."""
        payload = signup_api.default_payload("mismatch")
        payload["confirm_password"] = "DifferentPassword!"
        
        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400, got {response.status}"

    # --- Name Validations ---
    
    @pytest.mark.parametrize("invalid_name, reason", [
        ("Ab", "Name too short"),
        ("@User", "Starts with special char"),
        ("User!", "Ends with special char"),
        (" User", "Leading space"),
        ("User ", "Trailing space"),
        ("User123", "Contains numbers"),
        ("A" * 81, "Name too long")
    ])
    @pytest.mark.xfail(reason="Bug: API lacks name validation")
    def test_signup_name_validation_failures(self, signup_api: SignupClient, invalid_name, reason):
        """Verify name validation rules (parametrized)."""
        payload = signup_api.default_payload("name_val")
        payload["name"] = invalid_name
        
        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400 for {reason}, got {response.status}"

    # --- Email Validations ---

    @pytest.mark.parametrize("domain", ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"])
    def test_signup_email_public_domain(self, signup_api: SignupClient, domain):
        """Verify that public email domains are blocked."""
        payload = signup_api.default_payload("public_domain")
        # Replace domain
        user_part = payload["email"].split("@")[0]
        payload["email"] = f"{user_part}@{domain}"
        
        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400 for domain {domain}, got {response.status}"

    # --- Password Validations ---

    @pytest.mark.parametrize("password, reason", [
        ("password123!", "Missing uppercase"),
        ("PASSWORD123!", "Missing lowercase"),
        ("Password!", "Missing number"),
        ("Password123", "Missing special char")
    ])
    @pytest.mark.xfail(reason="Critical Bug: API returns 500 instead of 400 for password complexity")
    def test_signup_password_complexity(self, signup_api: SignupClient, password, reason):
        """Verify password complexity rules (parametrized)."""
        payload = signup_api.default_payload("pass_complex")
        payload["password"] = password
        payload["confirm_password"] = password
        
        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400 for {reason}, got {response.status}"
