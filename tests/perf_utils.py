"""Performance test utilities."""

import time
from functools import wraps
from typing import Any, Callable, TypeVar

import pytest
from playwright.sync_api import Page, expect

T = TypeVar('T')

def measure_timing(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        
        # Add timing to pytest report
        if hasattr(pytest, 'timing_data'):
            pytest.timing_data.append({
                'name': func.__name__,
                'duration': duration
            })
        return result
    return wrapper

def assert_load_time(page: Page, url: str, max_time: float = 3.0) -> None:
    """Assert that a page loads within specified time (in seconds)."""
    with page.expect_navigation(timeout=max_time * 1000) as navigation_info:
        page.goto(url)
    
    # Get actual navigation timing
    timing = page.evaluate("""() => {
        const nav = performance.getEntriesByType('navigation')[0];
        return {
            dns: nav.domainLookupEnd - nav.domainLookupStart,
            connect: nav.connectEnd - nav.connectStart,
            ttfb: nav.responseStart - nav.requestStart,
            download: nav.responseEnd - nav.responseStart,
            dom_load: nav.domContentLoadedEventEnd - nav.navigationStart,
            total: nav.loadEventEnd - nav.navigationStart
        }
    }""")
    
    actual_time = navigation_info.value.timing['responseEnd'] / 1000
    assert actual_time <= max_time, f"Page took {actual_time:.2f}s to load (max: {max_time}s)"
    
    # Add timing data to report
    if hasattr(pytest, 'timing_data'):
        pytest.timing_data.append({
            'name': f'page_load_{url.replace("://", "_").replace("/", "_")}',
            'timing': timing
        })