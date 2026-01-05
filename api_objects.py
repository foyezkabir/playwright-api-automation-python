import time
from typing import Dict, Any
from playwright.sync_api import APIRequestContext, APIResponse
from config import config

# --- Configuration ---
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
