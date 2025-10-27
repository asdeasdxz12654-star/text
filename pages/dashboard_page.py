from .base_page import BasePage


class DashboardPage(BasePage):
    """Template Dashboard Page Object. Adapt selectors for your application."""

    _user_greeting = ".user-greeting"

    def get_user_greeting(self) -> str:
        return self.page.locator(self._user_greeting).inner_text()

    def is_loaded(self) -> bool:
        return self.page.locator(self._user_greeting).count() > 0
