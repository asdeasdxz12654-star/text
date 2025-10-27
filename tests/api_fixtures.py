"""Test fixtures for API client and page objects."""

import os
import pytest
from typing import Generator

from .api_client import APIClient
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.fixture(scope="session")
def api_client(base_url: str) -> APIClient:
    """Create API client configured with test base URL."""
    return APIClient(base_url)

@pytest.fixture(scope="function")
def login_page(page) -> LoginPage:
    """Create LoginPage object."""
    return LoginPage(page)

@pytest.fixture(scope="function")
def dashboard_page(page) -> DashboardPage:
    """Create DashboardPage object."""
    return DashboardPage(page)

@pytest.fixture(scope="function")
def authenticated_api(api_client: APIClient) -> Generator[APIClient, None, None]:
    """Get authenticated API client using test credentials."""
    username = os.environ.get("TEST_USERNAME", "test@example.com")
    password = os.environ.get("TEST_PASSWORD", "password123")

    if not api_client.login(username, password):
        pytest.skip("Failed to authenticate with API")

    try:
        yield api_client
    finally:
        api_client.cleanup_test_data()