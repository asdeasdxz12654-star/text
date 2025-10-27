"""Accessibility tests using axe-core via axe-playwright-python."""

import json
import pytest
from typing import Any, Dict, List
from playwright.sync_api import Page, expect
from axe_playwright_python import Axe

def save_violations(violations: List[Dict[str, Any]], path: str) -> None:
    """Save accessibility violations to a JSON file."""
    with open(path, 'w') as f:
        json.dump(violations, f, indent=2)

@pytest.mark.accessibility
def test_homepage_accessibility(page: Page, base_url: str):
    """Test homepage for accessibility violations."""
    page.goto(base_url)
    
    # Initialize axe
    axe = Axe(page)
    
    # Run accessibility scan
    results = axe.run()
    
    # Save results (always, for reporting)
    save_violations(results['violations'], 'reports/a11y-home.json')
    
    # Assert no violations
    assert len(results['violations']) == 0, (
        f"Found {len(results['violations'])} accessibility violations. "
        "See reports/a11y-home.json for details."
    )

@pytest.mark.accessibility
def test_login_page_accessibility(login_page: Page, auth_base_url: str):
    """Test login page for accessibility violations."""
    page = login_page
    page.goto(f"{auth_base_url}/login")
    
    # Initialize axe
    axe = Axe(page)
    
    # Run accessibility scan with login-specific rules
    results = axe.run(
        # Include specific rules relevant for login forms
        rules={
            'label': {'enabled': True},
            'aria-required-attr': {'enabled': True},
            'aria-valid-attr-value': {'enabled': True},
            'color-contrast': {'enabled': True}
        }
    )
    
    # Save results
    save_violations(results['violations'], 'reports/a11y-login.json')
    
    # Assert no violations
    assert len(results['violations']) == 0, (
        f"Found {len(results['violations'])} accessibility violations. "
        "See reports/a11y-login.json for details."
    )

@pytest.mark.accessibility
def test_dynamic_content_accessibility(page: Page, authenticated_api):
    """Test accessibility of dynamically loaded content."""
    # Load a page with dynamic content
    page.goto(f"{authenticated_api.base_url}/dashboard")
    
    # Wait for dynamic content to load
    page.wait_for_selector('[data-testid="dashboard-content"]')
    
    # Initialize axe
    axe = Axe(page)
    
    # Run accessibility scan
    results = axe.run()
    
    # Save results
    save_violations(results['violations'], 'reports/a11y-dynamic.json')
    
    # Assert no violations
    assert len(results['violations']) == 0, (
        f"Found {len(results['violations'])} accessibility violations. "
        "See reports/a11y-dynamic.json for details."
    )