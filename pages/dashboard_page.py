"""Dashboard page object."""

from playwright.sync_api import expect
from .base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.welcome_message = self.page.get_by_test_id("welcome-message")
        self.upload_button = self.page.get_by_test_id("upload-button")
        self.file_input = self.page.locator('input[type="file"]')

    def upload_file(self, file_path: str) -> None:
        """Upload a file using the file input."""
        # Set file input files
        self.file_input.set_input_files(file_path)
        # Click upload button
        self.upload_button.click()
        # Wait for upload success message
        self.page.get_by_text("File uploaded successfully").wait_for()

    def should_be_logged_in(self) -> None:
        """Assert that user is logged in by checking welcome message."""
        expect(self.welcome_message).to_be_visible()
        expect(self.welcome_message).to_contain_text("Welcome")