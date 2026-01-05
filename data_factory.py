"""
Test Data Factory using Faker library for generating realistic test data.
This module provides utilities for creating test data for API automation.
"""
import time
from typing import Dict, Any
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
    def random_first_name() -> str:
        """Returns a random first name."""
        return fake.first_name()

    @staticmethod
    def random_last_name() -> str:
        """Returns a random last name."""
        return fake.last_name()

    @staticmethod
    def random_email(domain: str = None) -> str:
        """
        Generates a random email address.
        
        Args:
            domain: Custom domain or None for random
            
        Returns:
            Random email address
        """
        if domain:
            username = fake.user_name()
            return f"{username}@{domain}"
        return fake.email()

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
        import random
        import string
        
        # Ensure password meets complexity requirements
        password = [
            random.choice(string.ascii_uppercase),  # At least one uppercase
            random.choice(string.ascii_lowercase),  # At least one lowercase
            random.choice(string.digits),           # At least one digit
        ]
        
        if include_special:
            password.append(random.choice("!@#$%^&*"))
        
        # Fill the rest with random characters
        remaining_length = length - len(password)
        all_chars = string.ascii_letters + string.digits
        if include_special:
            all_chars += "!@#$%^&*"
        
        password.extend(random.choice(all_chars) for _ in range(remaining_length))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def random_phone_number(country_code: str = "+1") -> str:
        """
        Generates a random phone number.
        
        Args:
            country_code: Country calling code (default: +1 for US)
            
        Returns:
            Random phone number
        """
        return f"{country_code}{fake.msisdn()[3:]}"

    @staticmethod
    def random_address() -> Dict[str, str]:
        """
        Generates a random address dictionary.
        
        Returns:
            Dictionary with address components
        """
        return {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "country": fake.country()
        }

    @staticmethod
    def create_signup_payload(
        name: str = None,
        email: str = None,
        password: str = None,
        confirm_password: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Creates a complete signup payload with optional custom values.
        
        Args:
            name: User name (generated if None)
            email: Email address (generated if None)
            password: Password (generated if None)
            confirm_password: Confirm password (matches password if None)
            **kwargs: Additional fields to include in payload
            
        Returns:
            Complete signup payload dictionary
        """
        generated_password = password or UserDataFactory.random_password()
        
        payload = {
            "name": name or UserDataFactory.random_name(),
            "email": email or UserDataFactory.generate_unique_email(),
            "password": generated_password,
            "confirm_password": confirm_password or generated_password
        }
        
        # Add any additional fields
        payload.update(kwargs)
        
        return payload

    @staticmethod
    def create_invalid_payload(field_to_invalidate: str, invalid_value: Any = None) -> Dict[str, Any]:
        """
        Creates a payload with one intentionally invalid field.
        
        Args:
            field_to_invalidate: Which field to make invalid
            invalid_value: Custom invalid value (uses common invalid values if None)
            
        Returns:
            Payload with one invalid field
        """
        payload = UserDataFactory.create_signup_payload()
        
        if invalid_value is not None:
            payload[field_to_invalidate] = invalid_value
        else:
            # Use common invalid values based on field
            invalid_values = {
                "email": "invalid-email-format",
                "name": "User@123!",
                "password": "weak",
                "confirm_password": "mismatch_password"
            }
            payload[field_to_invalidate] = invalid_values.get(field_to_invalidate, "")
        
        return payload


class AttackVectorFactory:
    """Factory for generating security test payloads."""

    @staticmethod
    def sql_injection_payloads() -> list:
        """Returns common SQL injection attack vectors."""
        return [
            "' OR '1'='1",
            "admin'--",
            "' OR 1=1--",
            "1' AND '1'='1",
            "'; DROP TABLE users--",
            "1' UNION SELECT NULL--",
        ]

    @staticmethod
    def xss_payloads() -> list:
        """Returns common XSS attack vectors."""
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg/onload=alert('XSS')>",
            "'\"><script>alert(String.fromCharCode(88,83,83))</script>",
        ]

    @staticmethod
    def boundary_test_strings() -> list:
        """Returns strings for boundary testing."""
        return [
            "",  # Empty string
            " ",  # Single space
            "A" * 256,  # Very long string
            "A" * 1000,  # Extremely long string
            "\n\r\t",  # Special whitespace characters
            "🔥💯🎉",  # Emoji
            "测试用户",  # Chinese characters
            "مستخدم الاختبار",  # Arabic characters
            "Тест Пользователь",  # Cyrillic characters
        ]
