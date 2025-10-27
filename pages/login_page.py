"""Login page object."""

from typing import Optional
from .base_page import BasePage

class LoginPage(BasePage):
    def login(self, username: str, password: str) -> 'DashboardPage':
        """Login with the given credentials and return DashboardPage."""
        self.page.get_by_label("Username").fill(username)
        self.page.get_by_label("Password").fill(password)

        with self.page.expect_navigation():
            self.page.get_by_role("button", name="Login").click()

        from .dashboard_page import DashboardPage
        return DashboardPage(self.page)

    def attempt_login(self, username: str, password: str) -> 'LoginPage':
        """Try to login but expect to stay on login page (e.g., for invalid credentials)."""
        self.page.get_by_label("Username").fill(username)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
        return self

    def get_error_message(self) -> Optional[str]:
        """Get error message if present, None otherwise."""
        error = self.page.get_by_test_id("login-error")
        return error.text_content() if error.is_visible() else None