"""Visual regression test utilities."""

import os
from typing import Optional
from PIL import Image, ImageChops
from playwright.sync_api import Page

class VisualTest:
    def __init__(self, page: Page, snapshot_dir: str = "tests/snapshots"):
        self.page = page
        self.snapshot_dir = snapshot_dir
        os.makedirs(snapshot_dir, exist_ok=True)
    
    def _get_snapshot_path(self, name: str) -> str:
        """Get full path for a snapshot file."""
        return os.path.join(self.snapshot_dir, f"{name}.png")
    
    async def take_snapshot(
        self,
        name: str,
        selector: str = "body",
        *,
        full_page: bool = False,
        threshold: float = 0.1
    ) -> Optional[float]:
        """Take a snapshot and compare with baseline if it exists."""
        # Ensure element is visible
        element = self.page.locator(selector)
        element.wait_for(state="visible")
        
        # Take screenshot
        screenshot_path = self._get_snapshot_path(f"{name}_current")
        if full_page:
            self.page.screenshot(path=screenshot_path, full_page=True)
        else:
            element.screenshot(path=screenshot_path)
        
        # Compare with baseline if it exists
        baseline_path = self._get_snapshot_path(name)
        if not os.path.exists(baseline_path):
            # No baseline exists, use current as baseline
            os.rename(screenshot_path, baseline_path)
            return None
        
        # Compare images
        current = Image.open(screenshot_path)
        baseline = Image.open(baseline_path)
        
        # Calculate difference
        diff = ImageChops.difference(current, baseline)
        diff_ratio = sum(x * y for x, y in diff.getcolors()) / (diff.size[0] * diff.size[1])
        
        if diff_ratio > threshold:
            # Save diff image for inspection
            diff_path = self._get_snapshot_path(f"{name}_diff")
            diff.save(diff_path)
        
        return diff_ratio
    
    def approve_snapshot(self, name: str) -> None:
        """Approve current snapshot as new baseline."""
        current_path = self._get_snapshot_path(f"{name}_current")
        baseline_path = self._get_snapshot_path(name)
        if os.path.exists(current_path):
            os.replace(current_path, baseline_path)
    
    def cleanup_snapshots(self, name: str) -> None:
        """Clean up temporary snapshot files."""
        for suffix in ['_current', '_diff']:
            path = self._get_snapshot_path(f"{name}{suffix}")
            if os.path.exists(path):
                os.unlink(path)