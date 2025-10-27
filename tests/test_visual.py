"""Visual regression tests."""

import pytest
from playwright.sync_api import Page, expect

from tests.visual_utils import VisualTest

@pytest.fixture
def visual(page: Page) -> VisualTest:
    """Create VisualTest helper."""
    return VisualTest(page)

@pytest.mark.visual
async def test_homepage_visual(page: Page, base_url: str, visual: VisualTest):
    """Test homepage appearance hasn't changed."""
    page.goto(base_url)
    
    # Wait for any animations to complete
    page.wait_for_load_state("networkidle")
    
    try:
        # Take snapshots of key components
        diff_ratio = await visual.take_snapshot("home_hero", "[data-testid='hero']")
        if diff_ratio is not None:
            assert diff_ratio < 0.1, "Homepage hero section changed significantly"
        
        # Test responsive layouts
        for width in [375, 768, 1280]:  # mobile, tablet, desktop
            page.set_viewport_size({"width": width, "height": 800})
            diff_ratio = await visual.take_snapshot(f"home_responsive_{width}", "body")
            if diff_ratio is not None:
                assert diff_ratio < 0.1, f"Homepage at {width}px changed significantly"
    
    finally:
        visual.cleanup_snapshots("home_hero")
        for width in [375, 768, 1280]:
            visual.cleanup_snapshots(f"home_responsive_{width}")

@pytest.mark.visual
async def test_login_form_visual(page: Page, auth_base_url: str, visual: VisualTest):
    """Test login form appearance and states."""
    page.goto(f"{auth_base_url}/login")
    
    try:
        # Test normal state
        diff_ratio = await visual.take_snapshot("login_form", "[data-testid='login-form']")
        if diff_ratio is not None:
            assert diff_ratio < 0.1, "Login form changed significantly"
        
        # Test error state
        page.get_by_label("Username").fill("test@example.com")
        page.get_by_label("Password").fill("wrong")
        page.get_by_role("button", name="Login").click()
        
        # Wait for error to appear
        page.wait_for_selector("[data-testid='login-error']")
        
        diff_ratio = await visual.take_snapshot("login_form_error", "[data-testid='login-form']")
        if diff_ratio is not None:
            assert diff_ratio < 0.1, "Login form error state changed significantly"
    
    finally:
        visual.cleanup_snapshots("login_form")
        visual.cleanup_snapshots("login_form_error")