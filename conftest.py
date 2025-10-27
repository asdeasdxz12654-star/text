import os
import pytest
from pathlib import Path
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to take a screenshot when a test fails (during the call phase).

    Saves screenshots to `results/screenshots/{testname}-{browser}.png`.
    """
    outcome = yield
    rep = outcome.get_result()
    try:
        if rep.when == "call" and rep.failed:
            page = item.funcargs.get("page") if hasattr(item, "funcargs") else None
            if page:
                screenshots_dir = Path("results/screenshots")
                screenshots_dir.mkdir(parents=True, exist_ok=True)
                browser = None
                # try to find the browser name from fixtures or env
                if "browser_name" in item.funcargs:
                    browser = item.funcargs.get("browser_name")
                if not browser:
                    browser = os.getenv("BROWSER") or os.getenv("PLAYWRIGHT_BROWSER") or "unknown"
                safe_test_name = rep.nodeid.replace("::", "__").replace("/", "_")
                screenshot_path = screenshots_dir / f"{safe_test_name}-{browser}.png"
                try:
                    page.screenshot(path=str(screenshot_path))
                except Exception:
                    # best-effort: ignore screenshot failures
                    pass
    except Exception:
        # Do not let hook errors break tests reporting
        pass
