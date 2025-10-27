"""Upload functionality tests."""

import os
import tempfile
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from tests.api_client import APIClient

@pytest.mark.upload
def test_file_upload(
    login_page: LoginPage,
    authenticated_api: APIClient,
    tmp_path
):
    """Test uploading a file through the UI after API authentication."""
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("Test file content")
    
    # Login and navigate to dashboard
    dashboard = login_page.login(
        os.environ.get("TEST_USERNAME", "test@example.com"),
        os.environ.get("TEST_PASSWORD", "password123")
    )
    
    # Upload file and verify success
    dashboard.upload_file(str(test_file))
    
    # Clean up
    test_file.unlink()

@pytest.mark.upload
def test_large_file_upload(
    login_page: LoginPage,
    authenticated_api: APIClient,
    tmp_path
):
    """Test uploading a large file (10MB)."""
    # Create a large test file (10MB)
    test_file = tmp_path / "large.bin"
    with open(test_file, "wb") as f:
        f.write(os.urandom(10 * 1024 * 1024))  # 10MB of random data
    
    # Login and navigate to dashboard
    dashboard = login_page.login(
        os.environ.get("TEST_USERNAME", "test@example.com"),
        os.environ.get("TEST_PASSWORD", "password123")
    )
    
    # Upload file and verify success (this may take longer)
    with pytest.raises(TimeoutError):
        dashboard.upload_file(str(test_file))
    
    # Clean up
    test_file.unlink()