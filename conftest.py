"""Shared Pytest fixtures."""
import pytest
import requests
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture
def api():
    """Requests session used to call the demo REST API."""
    session = requests.Session()
    session.base_url = BASE_URL
    return session

@pytest.fixture
def browser_page():
    """Launch a fresh Chromium browser page for UI tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()
