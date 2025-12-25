import pytest
from api_objects import SignupClient

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
