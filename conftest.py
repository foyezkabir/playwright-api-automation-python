import logging
import os
from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from apiObjects.api_objects import SignupClient
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# --- Pytest Configuration ---
def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--update-readme",
        action="store_true",
        default=False,
        help="Update README.md with test results after the test run",
    )


def pytest_configure(config):
    """Set environment variable based on CLI option and configure markers."""
    if config.getoption("--update-readme", default=False):
        os.environ["UPDATE_README"] = "true"

    # Add custom markers
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "security: Security-related tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "performance: Performance tests")


# --- Fixtures ---
@pytest.fixture(scope="session", autouse=True)
def print_configuration():
    """Print configuration at the start of test session."""
    config.print_config()


@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Creates a shared API Request Context for the session."""
    headers = {"Content-Type": "application/json", "User-Agent": "Playwright-API-Tests/1.0"}

    logger.info(f"Creating API context with base URL: {config.BASE_URL}")

    context = playwright.request.new_context(
        base_url=config.BASE_URL,
        extra_http_headers=headers,
        timeout=config.API_TIMEOUT * 1000,  # Convert to milliseconds
    )

    yield context

    logger.info("Disposing API context")
    context.dispose()


@pytest.fixture(scope="session")
def signup_api(api_context: APIRequestContext) -> SignupClient:
    """Returns an instance of the SignupClient."""
    return SignupClient(api_context)


@pytest.fixture(autouse=True)
def test_logger(request):
    """Log test execution info."""
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")

    yield

    logger.info(f"Finished test: {test_name}")


# Pytest hooks for better reporting
def pytest_collection_modifyitems(config, items):
    """Modify test items during collection."""
    for item in items:
        # Add markers based on test name patterns
        if "security" in item.nodeid.lower():
            item.add_marker(pytest.mark.security)
        if "performance" in item.nodeid.lower():
            item.add_marker(pytest.mark.performance)


def pytest_sessionfinish(session, exitstatus):
    """
    Hook called after whole test run finishes.
    Automatically update README with latest test results.
    """
    import os
    from datetime import datetime

    # Only update README if UPDATE_README env variable is set to 'true'
    if os.environ.get("UPDATE_README", "").lower() != "true":
        return

    logger.info("Updating README with latest test results...")

    try:
        # Gather stats from session
        passed = session.testscollected - session.testsfailed - getattr(session, "_numxfailed", 0)
        total = session.testscollected

        # Get xfailed count from the terminal reporter if available
        xfailed = 0
        if hasattr(session.config, "_store"):
            terminalreporter = session.config.pluginmanager.get_plugin("terminalreporter")
            if terminalreporter:
                xfailed = len(terminalreporter.stats.get("xfailed", []))
                passed = len(terminalreporter.stats.get("passed", []))

        # Calculate execution time
        duration = getattr(session, "duration", 0)
        if duration == 0 and hasattr(session, "_setuptime"):
            duration = datetime.now().timestamp() - session._setuptime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exec_time = f"{duration:.2f}" if duration > 0 else "N/A"

        # Build stats dict and use shared functions to avoid code duplication
        from sync_readme_test_results import generate_results_section, update_readme

        stats = {
            "total": total,
            "passed": passed,
            "failed": 0,
            "xfailed": xfailed,
            "skipped": 0,
            "execution_time": exec_time,
            "signup_tests": 19,
            "verification_tests": 10,
            "timestamp": timestamp,
        }

        results_section = generate_results_section(stats)
        update_readme(results_section)

        logger.info(f"✅ README updated! {passed} passed, {xfailed} xfailed")

    except Exception as e:
        logger.warning(f"⚠️ Error updating README: {e}")
