"""
Custom decorators for API test automation.
Provides reusable decorators for test categorization, retry logic, and reporting.
"""

import functools
from collections.abc import Callable
from typing import Optional

import allure
import pytest


def smoke_test(title: Optional[str] = None, description: Optional[str] = None):
    """
    Decorator for smoke tests with automatic Allure annotations.

    Args:
        title: Test title (optional)
        description: Test description (optional)

    Usage:
        @smoke_test(title="Login API", description="Test successful login")
        def test_login_success(self):
            ...
    """

    def decorator(func: Callable):
        # Apply Allure decorators
        if title:
            func = allure.title(title)(func)
        if description:
            func = allure.description(description)(func)
        func = allure.severity(allure.severity_level.CRITICAL)(func)
        func = pytest.mark.smoke(func)
        return func

    return decorator


def regression_test(
    title: Optional[str] = None, description: Optional[str] = None, severity: str = "NORMAL"
):
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


def api_test(method: str, endpoint: str, title: Optional[str] = None):
    """
    Decorator for API tests with method and endpoint information.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        endpoint: API endpoint path
        title: Test title (optional)

    Usage:
        @api_test(method="POST", endpoint="/api/signup", title="Test signup")
        def test_signup(self):
            ...
    """

    def decorator(func: Callable):
        test_title = title or f"{method} {endpoint}"
        func = allure.title(test_title)(func)
        func = allure.description(f"API Test: {method} {endpoint}")(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with allure.step(f"{method} {endpoint}"):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def known_bug(bug_id: str, reason: Optional[str] = None):
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


def flaky_test(reruns: int = 2, reruns_delay: int = 1):
    """
    Decorator for flaky tests that may need retries.

    Args:
        reruns: Number of retry attempts (default: 2)
        reruns_delay: Delay between retries in seconds (default: 1)

    Usage:
        @flaky_test(reruns=3, reruns_delay=2)
        def test_unstable_api(self):
            ...
    """

    def decorator(func: Callable):
        func = pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)(func)
        return func

    return decorator


def performance_test(max_duration: int = 5):
    """
    Decorator for performance tests with timeout.

    Args:
        max_duration: Maximum allowed duration in seconds

    Usage:
        @performance_test(max_duration=3)
        def test_fast_response(self):
            ...
    """

    def decorator(func: Callable):
        func = pytest.mark.timeout(max_duration)(func)
        func = allure.label("test_type", "performance")(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time

            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time

            with allure.step(f"Response time: {duration:.2f}s"):
                assert duration <= max_duration, f"Test took {duration:.2f}s, expected <= {max_duration}s"
            return result

        return wrapper

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


def with_test_data(**test_data):
    """
    Decorator to attach test data to Allure report.

    Args:
        **test_data: Key-value pairs of test data

    Usage:
        @with_test_data(username="test_user", role="admin")
        def test_with_data(self):
            ...
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key, value in test_data.items():
                allure.attach(str(value), name=key, attachment_type=allure.attachment_type.TEXT)
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Convenience decorators combining common patterns
def critical_smoke(title: str, description: Optional[str] = None):
    """Critical smoke test (combines smoke_test with CRITICAL severity)."""
    return smoke_test(title=title, description=description)


def api_smoke(method: str, endpoint: str):
    """API smoke test (combines api_test with smoke marker)."""

    def decorator(func: Callable):
        func = api_test(method=method, endpoint=endpoint)(func)
        func = pytest.mark.smoke(func)
        func = allure.severity(allure.severity_level.CRITICAL)(func)
        return func

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
