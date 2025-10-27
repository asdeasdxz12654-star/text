def test_example_navigation_and_content(page, base_url):
    """Navigate example.com, click the link and assert navigation occurred.

    Uses the `page` fixture provided by pytest-playwright and `base_url` from conftest.
    """
    page.goto(base_url)
    # the example.com page has one link with text 'More information...'
    link = page.locator('a')
    assert link.count() >= 1
    # Click the first link and make sure we navigate away from example.com
    with page.expect_navigation():
        link.first.click()
    assert "iana.org" in page.url or "example.com" not in page.url
