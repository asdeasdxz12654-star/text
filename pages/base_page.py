class BasePage:
    """Simple base page wrapper around Playwright's `page` fixture."""

    def __init__(self, page):
        self.page = page

    def goto(self, url: str, **kwargs):
        """Navigate to a URL."""
        return self.page.goto(url, **kwargs)

    def title(self) -> str:
        return self.page.title()
