def test_example_domain(example_page, base_url):
    """Smoke test using the `example_page` fixture.

    Navigates to the base URL and checks title and heading.
    """
    example_page.goto(base_url)
    assert "Example Domain" in example_page.title()
    assert example_page.heading_text() == "Example Domain"
