from typing import Generator
import os
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from dotenv import load_dotenv
load_dotenv()  # load environment variables from .env file

@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for tests, can be overridden with BASE_URL env var."""
    return os.environ.get("BASE_URL", "https://example.com")

@pytest.fixture(scope="session")
def auth_base_url() -> str:
    """Auth service URL, override with AUTH_URL env var."""
    return os.environ.get("AUTH_URL", "https://example.com/auth")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Browser context arguments with defaults for CI."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "record_video_dir": "reports/videos" if os.getenv("CI") else None,
    }

@pytest.fixture(scope="function")
def auth_context(browser: Browser, auth_base_url: str) -> Generator[BrowserContext, None, None]:
    """Browser context that's authenticated. Use this to skip login steps."""
    context = browser.new_context(storage_state="tests/.auth/state.json")
    try:
        yield context
    finally:
        context.close()

@pytest.fixture
def auth_page(auth_context: BrowserContext) -> Generator[Page, None, None]:
    """Page fixture that's already authenticated."""
    page = auth_context.new_page()
    try:
        yield page
    finally:
        page.close()

def pytest_configure(config):
    # register custom markers
    config.addinivalue_line("markers", "e2e: end-to-end tests")
    config.addinivalue_line("markers", "login: login-related tests")
    config.addinivalue_line("markers", "smoke: quick smoke tests")
