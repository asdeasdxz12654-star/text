"""Performance tests measuring page load times and interactions."""

import pytest
from playwright.sync_api import Page, expect

from tests.perf_utils import measure_timing, assert_load_time
from pages.login_page import LoginPage

@pytest.mark.performance
def test_page_load_performance(page: Page, base_url: str):
    """Test that pages load within acceptable time limits."""
    # Homepage should load fast (3s limit)
    assert_load_time(page, base_url, max_time=3.0)
    
    # Login page might be slightly slower (4s limit)
    assert_load_time(page, f"{base_url}/login", max_time=4.0)

@pytest.mark.performance
@measure_timing
def test_login_performance(login_page: LoginPage, benchmark):
    """Benchmark login operation performance."""
    def run_login():
        return login_page.login("test@example.com", "password123")
    
    # Run login multiple times and collect metrics
    result = benchmark(run_login)
    
    # Basic validation that the login worked
    assert result  # Should be the dashboard page
    
    # Specific timing assertions can be added based on requirements
    assert benchmark.stats['min'] < 2.0  # Login should take < 2s
    assert benchmark.stats['max'] < 5.0  # Even worst case should be < 5s

@pytest.mark.performance
def test_resource_usage(page: Page, base_url: str):
    """Test page resource usage (memory, CPU, network)."""
    page.goto(base_url)
    
    # Get memory usage
    memory = page.evaluate("""() => {
        const memory = performance.memory;
        return {
            used: memory.usedJSHeapSize,
            total: memory.totalJSHeapSize,
            limit: memory.jsHeapSizeLimit
        };
    }""")
    
    # Check memory usage limits (adjust thresholds as needed)
    max_heap = 50 * 1024 * 1024  # 50MB
    assert memory['used'] < max_heap, f"Memory usage too high: {memory['used']/1024/1024:.1f}MB"
    
    # Get network metrics
    network = page.evaluate("""() => {
        const resources = performance.getEntriesByType('resource');
        return {
            count: resources.length,
            total_size: resources.reduce((sum, r) => sum + r.transferSize, 0),
            total_time: resources.reduce((max, r) => Math.max(max, r.responseEnd), 0)
        };
    }""")
    
    # Check network limits
    max_resources = 50
    max_size = 2 * 1024 * 1024  # 2MB total transfer
    assert network['count'] < max_resources, f"Too many resources: {network['count']}"
    assert network['total_size'] < max_size, f"Total transfer too large: {network['total_size']/1024:.1f}KB"