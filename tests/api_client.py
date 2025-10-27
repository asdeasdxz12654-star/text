"""API client for test automation."""

import os
from typing import Any, Optional
import requests
from requests.exceptions import RequestException

class APIClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.environ.get('API_URL', 'https://api.example.com')
        self.session = requests.Session()
        self._auth_token: Optional[str] = None
    
    def login(self, username: str, password: str) -> bool:
        """Login via API and store auth token."""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password}
            )
            response.raise_for_status()
            self._auth_token = response.json()["token"]
            self.session.headers.update({
                "Authorization": f"Bearer {self._auth_token}"
            })
            return True
        except RequestException:
            return False
    
    def create_test_data(self, **data: Any) -> dict[str, Any]:
        """Create test data via API."""
        if not self._auth_token:
            raise ValueError("Must login first")
        
        response = self.session.post(
            f"{self.base_url}/test-data",
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def cleanup_test_data(self) -> None:
        """Clean up any test data created during the test."""
        if not self._auth_token:
            return
        
        try:
            self.session.delete(f"{self.base_url}/test-data")
        except RequestException:
            pass  # Best effort cleanup