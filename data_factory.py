"""
Test Data Factory using Faker library for generating realistic test data.
This module provides utilities for creating test data for API automation.
"""

import time
from typing import Any

from faker import Faker

fake = Faker()


class UserDataFactory:
    """Factory class for generating user-related test data."""

    @staticmethod
    def generate_unique_email(prefix: str = "test", domain: str = "example.com") -> str:
        """
        Generates a unique email address based on timestamp.

        Args:
            prefix: Email prefix/username part
            domain: Email domain (default: example.com)

        Returns:
            Unique email address string
        """
        timestamp = int(time.time() * 1000)
        return f"{prefix}_{timestamp}@{domain}"

    @staticmethod
    def random_name(locale: str = "en_US") -> str:
        """
        Generates a random realistic name.

        Args:
            locale: Locale for name generation (default: en_US)

        Returns:
            Random full name
        """
        fake_locale = Faker(locale)
        return fake_locale.name()

    @staticmethod
    def random_password(length: int = 12, include_special: bool = True) -> str:
        """
        Generates a random password meeting complexity requirements.

        Args:
            length: Password length (default: 12)
            include_special: Include special characters (default: True)

        Returns:
            Random secure password
        """
        import secrets
        import string

        # Ensure password meets complexity requirements
        password = [
            secrets.choice(string.ascii_uppercase),  # At least one uppercase
            secrets.choice(string.ascii_lowercase),  # At least one lowercase
            secrets.choice(string.digits),  # At least one digit
        ]

        if include_special:
            password.append(secrets.choice("!@#$%^&*"))

        # Fill the rest with random characters
        remaining_length = length - len(password)
        all_chars = string.ascii_letters + string.digits
        if include_special:
            all_chars += "!@#$%^&*"

        password.extend(secrets.choice(all_chars) for _ in range(remaining_length))

        # Shuffle using secrets for security
        # Convert to list, shuffle indices, and reconstruct
        indices = list(range(len(password)))
        shuffled_password = []
        while indices:
            idx = secrets.choice(indices)
            shuffled_password.append(password[idx])
            indices.remove(idx)
        return "".join(shuffled_password)

    @staticmethod
    def create_signup_payload(
        name: str | None = None, email: str | None = None, password: str | None = None, **kwargs
    ) -> dict[str, Any]:
        """
        Creates a complete signup payload with optional custom values.

        Args:
            name: User name (generated if None)
            email: Email address (generated if None)
            password: Password (generated if None)
            **kwargs: Additional fields to include in payload

        Returns:
            Complete signup payload dictionary
        """
        payload = {
            "name": name or UserDataFactory.random_name(),
            "email": email or UserDataFactory.generate_unique_email(),
            "password": password or UserDataFactory.random_password(),
        }

        # Add any additional fields
        payload.update(kwargs)

        return payload
