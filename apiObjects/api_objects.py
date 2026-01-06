import time
from typing import Dict, Any
from playwright.sync_api import APIRequestContext, APIResponse
from config import config

# --- Configuration ---
SIGNUP_ENDPOINT = "/api/authentication/signup/"
SIGNUP_CONFIRM_ENDPOINT = "/api/authentication/signup/confirm/"
SIGNUP_RESEND_CODE_ENDPOINT = "/api/authentication/signup/resend-code/"

# --- API Object Model ---
class SignupClient:
    """Helper class to interact with the Signup API."""

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context

    def create_user(self, payload: Dict[str, Any]) -> APIResponse:
        """Sends a POST request to create a user."""
        return self.request.post(SIGNUP_ENDPOINT, data=payload)

    def confirm_signup(self, payload: Dict[str, Any]) -> APIResponse:
        """Sends a POST request to confirm/verify user signup."""
        return self.request.post(SIGNUP_CONFIRM_ENDPOINT, data=payload)

    def resend_confirmation_code(self, payload: Dict[str, Any]) -> APIResponse:
        """Sends a POST request to resend confirmation code."""
        return self.request.post(SIGNUP_RESEND_CODE_ENDPOINT, data=payload)

    def test_resend_rate_limit(self, email: str, max_attempts: int = 5) -> Dict[str, Any]:
        """Tests resend OTP rate limiting by making multiple attempts.
        
        Args:
            email: Email address to resend OTP for
            max_attempts: Number of successful attempts before rate limit (default: 5)
            
        Returns:
            Dict with success count and final blocked response
        """
        resend_payload = {"email": email}
        successful_attempts = 0
        
        # Make max_attempts successful resends
        for attempt in range(1, max_attempts + 1):
            response = self.resend_confirmation_code(resend_payload)
            if response.status == 200:
                successful_attempts += 1
            else:
                break
        
        # Try one more time to trigger rate limit
        blocked_response = self.resend_confirmation_code(resend_payload)
        
        return {
            "successful_attempts": successful_attempts,
            "blocked_response": blocked_response
        }

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
            "password": "Password123!"
        }
