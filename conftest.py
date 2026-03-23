# conftest.py
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def test_config(request):
    configs = {
        "user_login": {"user": "admin", "pass": "123"},
        "data_load": {"user": "tester", "pass": "456"},
    }
    # Get the test ID from the marker or function name
    marker = request.node.get_closest_marker("id")
    if marker:
        test_id = marker.args[0]
        return configs.get(test_id)
    return {}


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


# test_suite.py
import pytest


@pytest.mark.test_id("user_login")
def test_login(test_config):
    assert test_config["user"] == "admin"
