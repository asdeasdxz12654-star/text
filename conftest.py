import os
import pytest
from typing import Callable

from pages.example_page import ExamplePage


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for tests. Can be overridden with the BASE_URL environment variable."""
    return os.getenv("BASE_URL", "https://example.com")


@pytest.fixture
def page_factory(page) -> Callable:
    """Factory fixture to build Page Object instances.

    Usage in tests:
        example = page_factory(ExamplePage)
    """
    def _create(page_class):
        return page_class(page)

    return _create


@pytest.fixture
def example_page(page) -> ExamplePage:
    """Convenience fixture that returns an `ExamplePage` instance."""
    return ExamplePage(page)
