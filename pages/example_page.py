from .base_page import BasePage


class ExamplePage(BasePage):
    """Page Object for https://example.com (simple demo page).

    Selectors are intentionally minimal — adapt for your real app.
    """

    _heading = "h1"

    def heading_text(self) -> str:
        return self.page.locator(self._heading).inner_text()
