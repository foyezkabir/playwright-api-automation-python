import pytest
import logging
from playwright.sync_api import Playwright, APIRequestContext
from api_objects import SignupClient
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


# --- Fixtures ---
@pytest.fixture(scope="session", autouse=True)
def print_configuration():
    """Print configuration at the start of test session."""
    config.print_config()


@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> APIRequestContext:
    """Creates a shared API Request Context for the session."""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Playwright-API-Tests/1.0"
    }
    
    logger.info(f"Creating API context with base URL: {config.BASE_URL}")
    
    context = playwright.request.new_context(
        base_url=config.BASE_URL,
        extra_http_headers=headers,
        timeout=config.API_TIMEOUT * 1000  # Convert to milliseconds
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
def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "security: Security-related tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "performance: Performance tests")


def pytest_collection_modifyitems(config, items):
    """Modify test items during collection."""
    for item in items:
        # Add markers based on test name patterns
        if "security" in item.nodeid.lower():
            item.add_marker(pytest.mark.security)
        if "performance" in item.nodeid.lower():
            item.add_marker(pytest.mark.performance)
