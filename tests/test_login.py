import pytest

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.mark.skip("template")
def test_login_flow(page, base_url, page_factory):
    """Template test demonstrating how to use LoginPage/DashboardPage.

    This test is skipped by default — adapt selectors and remove skip to use it.
    """
    login = page_factory(LoginPage)
    dashboard = page_factory(DashboardPage)

    login.goto(base_url + "/login")
    assert login.is_login_form_visible()

    # Replace with real credentials for an environment-safe test
    login.login("user@example.com", "password")

    # Example: wait for dashboard to load
    assert dashboard.is_loaded()
