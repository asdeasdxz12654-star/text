def test_example_title(page):
    """A tiny smoke test using the pytest-playwright `page` fixture.

    It navigates to example.com and asserts the page title.
    """
    page.goto("https://example.com")
    assert "Example Domain" in page.title()
