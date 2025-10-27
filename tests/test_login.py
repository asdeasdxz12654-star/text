from typing import Generator
import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def login_page(page: Page, auth_base_url: str) -> Generator[Page, None, None]:
    """Navigate to login page and return it."""
    page.goto(f"{auth_base_url}/login")
    try:
        yield page
    finally:
        page.close()

@pytest.mark.login
def test_successful_login(login_page: Page):
    """Test successful login flow with valid credentials."""
    # Fill in login form
    login_page.get_by_label("Username").fill("test@example.com")
    login_page.get_by_label("Password").fill("password123")

    # Click login and wait for navigation
    with login_page.expect_navigation():
        login_page.get_by_role("button", name="Login").click()

    # Assert we're logged in (URL changed and welcome text visible)
    expect(login_page).to_have_url(re.compile(r".*/dashboard"))
    expect(login_page.get_by_text("Welcome back")).to_be_visible()

@pytest.mark.login
def test_failed_login(login_page: Page):
    """Test login failure with invalid credentials."""
    # Fill in login form with bad password
    login_page.get_by_label("Username").fill("test@example.com")
    login_page.get_by_label("Password").fill("wrong-password")

    # Click login (no navigation expected)
    login_page.get_by_role("button", name="Login").click()

    # Assert error message appears
    error = login_page.get_by_text("Invalid username or password")
    expect(error).to_be_visible()