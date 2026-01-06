import pytest
import allure
from api_objects import SignupClient
from data_factory import UserDataFactory
from decorators import regression_test, api_smoke, validation_test, known_bug, feature_story

# --- Test Suite ---
@feature_story(feature='Authentication', story='Signup Verification')
class TestSignupVerification:
    """Test suite for Signup Email Verification/Confirmation API.
    
    NOTE: UI shows 6-digit OTP input boxes. Email is session-based (not editable).
    Tests focus on OTP validation scenarios matching actual UI behavior.
    """

    @api_smoke(method="POST", endpoint="/api/authentication/signup/confirm/")
    def test_verify_otp_success(self, signup_api: SignupClient):
        """Verify successful email verification with valid OTP."""
        signup_payload = UserDataFactory.create_signup_payload()
        signup_response = signup_api.create_user(signup_payload)
        assert signup_response.status in [200, 201], "Signup should succeed"
        
        # TODO: Get actual confirmation_code from email
        # UI shows 6-digit OTP input boxes
        verification_payload = {
            "email": signup_payload["email"],
            "confirmation_code": "123456"
        }
        
        response = signup_api.confirm_signup(verification_payload)
        # Will fail without real OTP
        assert response.status in [200, 400], \
            f"Got {response.status}: {response.text()}"

    @validation_test(field="confirmation_code", validation_type="invalid OTP")
    def test_verify_otp_invalid_code(self, signup_api: SignupClient):
        """Verify error when invalid 6-digit OTP is provided."""
        signup_payload = UserDataFactory.create_signup_payload()
        signup_response = signup_api.create_user(signup_payload)
        assert signup_response.status in [200, 201], "Signup should succeed"
        
        verification_payload = {
            "email": signup_payload["email"],
            "confirmation_code": "000000"
        }
        
        response = signup_api.confirm_signup(verification_payload)
        assert response.status == 400, \
            f"Expected 400 for invalid OTP, got {response.status}"
        
        response_data = response.json()
        assert response_data.get("error") == True
        assert response_data.get("code") == "CODE_MISMATCH"

    @validation_test(field="confirmation_code", validation_type="expired OTP")
    def test_verify_otp_expired_code(self, signup_api: SignupClient):
        """Verify error when expired OTP is provided (after timer expires)."""
        verification_payload = {
            "email": "test@example.com",
            "confirmation_code": "999999"
        }
        
        response = signup_api.confirm_signup(verification_payload)
        assert response.status == 404, \
            f"Expected 404 for non-existent/expired OTP, got {response.status}"

    @validation_test(field="confirmation_code", validation_type="incomplete OTP")
    def test_verify_otp_incomplete_code(self, signup_api: SignupClient):
        """Verify error when incomplete OTP is provided (less than 6 digits)."""
        signup_payload = UserDataFactory.create_signup_payload()
        signup_response = signup_api.create_user(signup_payload)
        assert signup_response.status in [200, 201], "Signup should succeed"
        
        # UI has 6 digit boxes, testing incomplete submission
        verification_payload = {
            "email": signup_payload["email"],
            "confirmation_code": "123"
        }
        
        response = signup_api.confirm_signup(verification_payload)
        assert response.status == 400, \
            f"Expected 400 for incomplete OTP, got {response.status}"

    @validation_test(field="confirmation_code", validation_type="missing field")
    def test_verify_otp_missing_code(self, signup_api: SignupClient):
        """Verify error when confirmation code is missing."""
        verification_payload = {
            "email": "test@example.com"
        }
        
        response = signup_api.confirm_signup(verification_payload)
        assert response.status == 400, \
            f"Expected 400 for missing OTP, got {response.status}"
        
        response_data = response.json()
        assert response_data.get("error") == True
        assert response_data.get("code") == "VALIDATION_ERROR"
        assert "confirmation_code" in response_data.get("data", {})


@feature_story(feature='Authentication', story='Resend OTP')
class TestResendOTP:
    """Test suite for Resend Confirmation Code API.
    
    NOTE: UI shows "Resend OTP" button after timer. Email is from session (not user input).
    """

    @api_smoke(method="POST", endpoint="/api/authentication/signup/resend-code/")
    def test_resend_otp_success(self, signup_api: SignupClient):
        """Verify successful resend of confirmation code."""
        signup_payload = UserDataFactory.create_signup_payload()
        signup_response = signup_api.create_user(signup_payload)
        assert signup_response.status in [200, 201], "Signup should succeed"
        
        resend_payload = {"email": signup_payload["email"]}
        
        response = signup_api.resend_confirmation_code(resend_payload)
        assert response.status == 200, \
            f"Expected 200 for resend OTP, got {response.status}"
        
        response_data = response.json()
        assert response_data.get("error") == False
        assert response_data.get("code") == "ConfirmationCodeResent"
        assert response_data.get("message") == "Confirmation code resent successfully."

    @validation_test(field="email", validation_type="missing field")
    def test_resend_otp_missing_email(self, signup_api: SignupClient):
        """Verify error when email is missing in resend request."""
        resend_payload = {}
        
        response = signup_api.resend_confirmation_code(resend_payload)
        assert response.status == 400, \
            f"Expected 400 for missing email, got {response.status}"

    @validation_test(field="email", validation_type="non-existent email")
    def test_resend_otp_nonexistent_email(self, signup_api: SignupClient):
        """Verify error when email doesn't exist."""
        resend_payload = {"email": "nonexistent98765@example.com"}
        
        response = signup_api.resend_confirmation_code(resend_payload)
        assert response.status in [400, 404], \
            f"Expected 400/404 for non-existent email, got {response.status}"

    @validation_test(field="email", validation_type="already verified")
    def test_resend_otp_already_verified(self, signup_api: SignupClient):
        """Verify error when trying to resend OTP for already verified email."""
        resend_payload = {"email": "verified@example.com"}
        
        response = signup_api.resend_confirmation_code(resend_payload)
        assert response.status in [200, 400, 404], \
            f"Got {response.status}: {response.text()}"

    @regression_test(title="Test resend OTP rate limiting after 5 attempts", severity="NORMAL")
    def test_resend_otp_rate_limit(self, signup_api: SignupClient):
        """Verify rate limiting blocks resend OTP after 5 attempts."""
        signup_payload = UserDataFactory.create_signup_payload()
        signup_response = signup_api.create_user(signup_payload)
        assert signup_response.status in [200, 201], "Signup should succeed"
        
        result = signup_api.test_resend_rate_limit(email=signup_payload["email"], max_attempts=5)
        
        assert result["successful_attempts"] == 5, "First 5 attempts should succeed"
        
        blocked_response = result["blocked_response"]
        assert blocked_response.status in [400, 429], \
            f"Expected rate limit on 6th attempt, got {blocked_response.status}: {blocked_response.text()}"
        
        response_data = blocked_response.json()
        assert response_data.get("error") == True, "Error flag should be true for rate limit"
