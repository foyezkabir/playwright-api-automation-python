"""
Environment Configuration Module
Supports multiple environments (dev, staging, prod) via environment variables or .env files.
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Base configuration class."""

    # Environment
    ENV: str = os.getenv("ENV", "dev")

    # API Configuration
    BASE_URL: str = os.getenv("BASE_URL", "https://eks-dev-lb.shadhinlab.xyz")
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))

    # Authentication
    API_KEY: str | None = os.getenv("API_KEY")
    API_SECRET: str | None = os.getenv("API_SECRET")

    # Test Configuration
    RETRY_COUNT: int = int(os.getenv("RETRY_COUNT", "2"))
    PARALLEL_WORKERS: int = int(os.getenv("PARALLEL_WORKERS", "4"))

    # Reporting
    ALLURE_RESULTS_DIR: str = os.getenv("ALLURE_RESULTS_DIR", "./allure-results")

    # Database Configuration (if needed for verification)
    DB_HOST: str | None = os.getenv("DB_HOST")
    DB_PORT: int | None = int(os.getenv("DB_PORT", "5432")) if os.getenv("DB_PORT") else None
    DB_NAME: str | None = os.getenv("DB_NAME")
    DB_USER: str | None = os.getenv("DB_USER")
    DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")

    @classmethod
    def get_endpoint_url(cls, endpoint: str) -> str:
        """
        Constructs full URL for an API endpoint.

        Args:
            endpoint: API endpoint path (e.g., '/api/authentication/signup/')

        Returns:
            Complete URL
        """
        return f"{cls.BASE_URL}{endpoint}"

    @classmethod
    def is_dev(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENV.lower() == "dev"

    @classmethod
    def is_staging(cls) -> bool:
        """Check if running in staging environment."""
        return cls.ENV.lower() == "staging"

    @classmethod
    def is_prod(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENV.lower() == "prod"

    @classmethod
    def print_config(cls):
        """Print current configuration (masks sensitive data)."""
        print("\n" + "=" * 50)
        print("CURRENT CONFIGURATION")
        print("=" * 50)
        print(f"Environment: {cls.ENV}")
        print(f"Base URL: {cls.BASE_URL}")
        print(f"API Timeout: {cls.API_TIMEOUT}s")
        print(f"Retry Count: {cls.RETRY_COUNT}")
        print(f"Parallel Workers: {cls.PARALLEL_WORKERS}")
        print(f"Allure Results Dir: {cls.ALLURE_RESULTS_DIR}")
        print("=" * 50 + "\n")


class DevConfig(Config):
    """Development environment configuration."""

    ENV = "dev"
    BASE_URL = "https://eks-dev-lb.shadhinlab.xyz"


class StagingConfig(Config):
    """Staging environment configuration."""

    ENV = "staging"
    BASE_URL = os.getenv("STAGING_BASE_URL", "https://staging-api.example.com")


class ProdConfig(Config):
    """Production environment configuration."""

    ENV = "prod"
    BASE_URL = os.getenv("PROD_BASE_URL", "https://api.example.com")
    # In production, you might want to disable auto-retry or reduce parallel workers
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", "1"))
    PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "2"))


def get_config() -> Config:
    """
    Returns the appropriate configuration object based on ENV variable.

    Returns:
        Configuration object for current environment
    """
    env = os.getenv("ENV", "dev").lower()

    config_map = {"dev": DevConfig, "staging": StagingConfig, "prod": ProdConfig}

    return config_map.get(env, DevConfig)()


# Global config instance
config = get_config()
