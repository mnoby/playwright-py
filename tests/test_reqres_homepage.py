import json

import pytest
from playwright.sync_api import Page

from config.environments import EnvironmentConfig
from pages.reqres_home_page import HomePage

PAYLOAD = '{"title": "Lorem Ipsum", "completed": false}'


class TestReqresHomePage:

    def test_hit_post_request(self, page: Page, env_config: EnvironmentConfig):
        home_page = HomePage(page, env_config)

        print(f"\n🌍  Environment : [{env_config.name.upper()}]")
        print(f"🔗  Base URL    : {env_config.base_url}")
        # Navigate to the site (uses env base_url automatically)
        home_page.open()

        # Verify the application is ready
        home_page.is_page_and_API_ready()

        # Click POST request button
        home_page.click_post_button("active")

        # Input the payload
        home_page.send_post_request(PAYLOAD)

        # Assert the response
        home_page.is_response_ok("201 Created", PAYLOAD)