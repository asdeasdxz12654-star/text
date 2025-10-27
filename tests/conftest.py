import os
import pytest


@pytest.fixture(scope="session")
def base_url():
    """Base URL for tests, can be overridden with BASE_URL env var."""
    return os.environ.get("BASE_URL", "https://example.com")


def pytest_configure(config):
    # register custom marker to avoid warnings
    config.addinivalue_line("markers", "e2e: end-to-end tests")
