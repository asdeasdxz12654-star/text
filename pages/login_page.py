from .base_page import BasePage


class LoginPage(BasePage):
    """Template Login Page Object. Adapt selectors for your application."""

    _username = "#username"
    _password = "#password"
    _submit = "button[type=submit]"

    def login(self, username: str, password: str):
        """Fill login form and submit."""
        self.page.fill(self._username, username)
        self.page.fill(self._password, password)
        self.page.click(self._submit)

    def is_login_form_visible(self) -> bool:
        return self.page.locator(self._submit).is_visible()
