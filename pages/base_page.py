"""Base page object that all page objects can inherit from."""

import re
from typing import Optional, TypeVar
from playwright.sync_api import Page, Locator, expect

T = TypeVar('T', bound='BasePage')

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self: T, path: str = "") -> T:
        """Navigate to a specific path and return self for chaining."""
        self.page.goto(f"{self.base_url}/{path.lstrip('/')}")
        return self

    @property
    def base_url(self) -> str:
        """Get base URL from page's first context option."""
        return self.page.context.browser.browser_type.launch_options.get('base_url', '')

    def get_by_test_id(self, test_id: str) -> Locator:
        """Get element by data-testid attribute."""
        return self.page.locator(f'[data-testid="{test_id}"]')

    def should_be_visible(self, selector: str, *, timeout: Optional[float] = None) -> None:
        """Assert that element is visible."""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def should_have_text(self, selector: str, text: str, *, timeout: Optional[float] = None) -> None:
        """Assert that element has specific text."""
        expect(self.page.locator(selector)).to_have_text(text, timeout=timeout)

    def should_be_on_page(self, path: str) -> None:
        """Assert that current URL ends with the given path."""
        expect(self.page).to_have_url(re.compile(f".*{path}$"))