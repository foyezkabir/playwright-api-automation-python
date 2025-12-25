import pytest
from playwright.sync_api import Playwright, APIRequestContext
from client import SignupClient, BASE_URL

# --- Fixtures ---
@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> APIRequestContext:
    """Creates a shared API Request Context for the session."""
    headers = {"Content-Type": "application/json"}
    context = playwright.request.new_context(base_url=BASE_URL, extra_http_headers=headers)
    yield context
    context.dispose()

@pytest.fixture(scope="session")
def signup_api(api_context: APIRequestContext) -> SignupClient:
    """Returns an instance of the SignupClient."""
    return SignupClient(api_context)
