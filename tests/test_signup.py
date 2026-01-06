import pytest

from apiObjects.api_objects import SignupClient
from data_factory import UserDataFactory
from decorators import api_smoke, feature_story, known_bug, regression_test, validation_test
from schemas import SignupSuccessResponseSchema, assert_response_schema


# --- Test Suite ---
@feature_story(feature="Authentication", story="User Signup")
class TestSignup:
    """Test suite for User Signup API."""

    @api_smoke(method="POST", endpoint="/api/authentication/signup")
    def test_signup_success(self, signup_api: SignupClient):
        """Verify successful user registration with valid data."""
        payload = UserDataFactory.create_signup_payload()
        response = signup_api.create_user(payload)

        assert response.status in [200, 201], f"Expected 200/201, got {response.status}. Body: {response.text()}"
        assert_response_schema(response.json(), SignupSuccessResponseSchema)

    @regression_test(title="Test duplicate email registration", severity="CRITICAL")
    def test_signup_duplicate_email(self, signup_api: SignupClient):
        """Verify error when attempting to register with an existing email."""
        payload = UserDataFactory.create_signup_payload()

        first_response = signup_api.create_user(payload)
        assert first_response.status in [200, 201], "First signup should succeed"

        duplicate_response = signup_api.create_user(payload)
        assert duplicate_response.status == 409, f"Expected 409 for duplicate email, got {duplicate_response.status}"

        response_data = duplicate_response.json()
        assert response_data.get("code") == "USERNAME_EXISTS", (
            f"Expected code USERNAME_EXISTS, got {response_data.get('code')}"
        )
        assert response_data.get("message") == "User already exists", (
            f"Expected message 'User already exists', got {response_data.get('message')}"
        )

    @regression_test(title="Test missing required fields", severity="CRITICAL")
    def test_signup_missing_fields(self, signup_api: SignupClient):
        """Verify validation error when required fields are missing."""
        payload = {"email": signup_api.generate_unique_email("missing"), "password": "Password123!"}
        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400, got {response.status}"

    @validation_test(field="email", validation_type="format")
    def test_signup_invalid_email(self, signup_api: SignupClient):
        """Verify validation error for invalid email format."""
        payload = signup_api.default_payload()
        payload["email"] = "invalid-email-format"

        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400, got {response.status}"

    # Note: API only uses password field (no confirm_password validation)

    # --- Name Validations (Security: Frontend validation can be bypassed) ---

    @pytest.mark.parametrize(
        "invalid_name, reason",
        [
            ("Ab", "Name too short"),
            ("@User", "Starts with special char"),
            ("User!", "Ends with special char"),
            (" User", "Leading space"),
            ("User ", "Trailing space"),
            ("User123", "Contains numbers"),
            ("A" * 81, "Name too long"),
        ],
    )
    @known_bug(
        bug_id="API-001",
        reason="Security Issue: API lacks name validation - accepts invalid names when frontend is bypassed",
    )
    def test_signup_name_validation_failures(self, signup_api: SignupClient, invalid_name, reason):
        """Verify API rejects invalid names when frontend validation is bypassed (Postman, curl, etc.)."""
        payload = signup_api.default_payload("name_val")
        payload["name"] = invalid_name

        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400 for {reason}, got {response.status}"

    # --- Email Validations ---

    @pytest.mark.parametrize("domain", ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"])
    @validation_test(field="email", validation_type="public domain blocking")
    def test_signup_email_public_domain(self, signup_api: SignupClient, domain):
        """Verify that API rejects public email domains (aligned with frontend validation)."""
        payload = signup_api.default_payload("public_domain")
        # Replace domain
        user_part = payload["email"].split("@")[0]
        payload["email"] = f"{user_part}@{domain}"

        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400 for domain {domain}, got {response.status}"

    # --- Password Validations (Security: Frontend validation can be bypassed) ---

    @pytest.mark.parametrize(
        "password, reason",
        [
            ("password123!", "Missing uppercase"),
            ("PASSWORD123!", "Missing lowercase"),
            ("Password!", "Missing number"),
            ("Password123", "Missing special char"),
        ],
    )
    @known_bug(
        bug_id="API-003",
        reason="Critical Security Bug: API crashes (500) with weak passwords when frontend is bypassed",
    )
    def test_signup_password_complexity(self, signup_api: SignupClient, password, reason):
        """Verify API rejects weak passwords when frontend validation is bypassed (Postman, curl, etc.)."""
        payload = signup_api.default_payload("pass_complex")
        payload["password"] = password

        response = signup_api.create_user(payload)
        assert response.status == 400, f"Expected 400 for {reason}, got {response.status}"
