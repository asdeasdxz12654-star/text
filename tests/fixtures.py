from typing import Any, Generator
import pytest
from playwright.sync_api import Browser, BrowserContext, Page

@pytest.fixture(scope="function")
def context(
    browser: Browser,
    browser_context_args: dict[str, Any],
    base_url: str
) -> Generator[BrowserContext, None, None]:
    """Create a new browser context with video recording enabled in CI."""
    context = browser.new_context(**browser_context_args)
    context.set_default_navigation_timeout(10000)
    context.set_default_timeout(5000)
    try:
        yield context
    finally:
        context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Create a new page in the browser context."""
    page = context.new_page()
    try:
        yield page
    finally:
        page.close()