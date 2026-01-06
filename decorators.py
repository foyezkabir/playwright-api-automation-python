"""
Custom decorators for API test automation.
Provides reusable decorators for test categorization, retry logic, and reporting.
"""

import functools
from collections.abc import Callable

import allure
import pytest


def regression_test(title: str | None = None, description: str | None = None, severity: str = "NORMAL"):
    """
    Decorator for regression tests with automatic Allure annotations.

    Args:
        title: Test title (optional)
        description: Test description (optional)
        severity: Test severity (BLOCKER, CRITICAL, NORMAL, MINOR, TRIVIAL)

    Usage:
        @regression_test(title="User Profile", description="Test profile update")
        def test_profile_update(self):
            ...
    """

    def decorator(func: Callable):
        if title:
            func = allure.title(title)(func)
        if description:
            func = allure.description(description)(func)

        # Map severity string to Allure severity
        severity_map = {
            "BLOCKER": allure.severity_level.BLOCKER,
            "CRITICAL": allure.severity_level.CRITICAL,
            "NORMAL": allure.severity_level.NORMAL,
            "MINOR": allure.severity_level.MINOR,
            "TRIVIAL": allure.severity_level.TRIVIAL,
        }
        func = allure.severity(severity_map.get(severity, allure.severity_level.NORMAL))(func)
        func = pytest.mark.regression(func)
        return func

    return decorator


def known_bug(bug_id: str, reason: str | None = None):
    """
    Decorator for tests with known bugs (xfail).

    Args:
        bug_id: Bug tracking ID (e.g., JIRA-123)
        reason: Reason for expected failure (optional)

    Usage:
        @known_bug(bug_id="JIRA-123", reason="API returns 500 error")
        def test_with_bug(self):
            ...
    """

    def decorator(func: Callable):
        xfail_reason = f"Known Bug [{bug_id}]"
        if reason:
            xfail_reason += f": {reason}"

        func = pytest.mark.xfail(reason=xfail_reason)(func)
        func = allure.link(bug_id, name=f"Bug: {bug_id}", link_type="issue")(func)
        return func

    return decorator


def feature_story(feature: str, story: str):
    """
    Decorator to categorize tests by feature and story.

    Args:
        feature: Feature name
        story: Story/scenario name

    Usage:
        @feature_story(feature="Authentication", story="User Signup")
        def test_signup(self):
            ...
    """

    def decorator(func: Callable):
        func = allure.feature(feature)(func)
        func = allure.story(story)(func)
        return func

    return decorator


def api_smoke(method: str, endpoint: str):
    """API smoke test decorator."""

    def decorator(func: Callable):
        test_title = f"{method} {endpoint}"
        func = allure.title(test_title)(func)
        func = allure.description(f"API Test: {method} {endpoint}")(func)
        func = pytest.mark.smoke(func)
        func = allure.severity(allure.severity_level.CRITICAL)(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with allure.step(f"{method} {endpoint}"):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def validation_test(field: str, validation_type: str):
    """
    Decorator for field validation tests.

    Args:
        field: Field name being validated
        validation_type: Type of validation (format, length, required, etc.)

    Usage:
        @validation_test(field="email", validation_type="format")
        def test_email_format(self):
            ...
    """

    def decorator(func: Callable):
        func = allure.title(f"Validate {field} - {validation_type}")(func)
        func = allure.description(f"Test {validation_type} validation for {field} field")(func)
        func = allure.label("validation_field", field)(func)
        func = allure.label("validation_type", validation_type)(func)
        return func

    return decorator
