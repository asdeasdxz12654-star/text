"""API integration tests."""

import pytest
from datetime import datetime
from tests.api_client import APIClient

@pytest.mark.api
def test_api_authentication(api_client: APIClient):
    """Test API authentication with valid credentials."""
    assert api_client.login("test@example.com", "password123")

@pytest.mark.api
def test_api_invalid_auth(api_client: APIClient):
    """Test API authentication fails with invalid credentials."""
    assert not api_client.login("test@example.com", "wrong-password")

@pytest.mark.api
def test_create_test_data(authenticated_api: APIClient):
    """Test creating test data via API."""
    # Create a test record
    data = {
        "title": f"Test {datetime.now().isoformat()}",
        "description": "Created by automated test"
    }
    
    result = authenticated_api.create_test_data(**data)
    assert result["id"]
    assert result["title"] == data["title"]
    
    # Cleanup happens automatically via authenticated_api fixture