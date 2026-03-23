from __future__ import annotations

import json
import re

from playwright.sync_api import Page, expect

from config.environments import EnvironmentConfig
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page, config: EnvironmentConfig) -> None:
        super().__init__(page, config)

        # ── Locators ──────────────────────────────────────────────────────
        self.title_text = page.get_by_text(re.compile("A real backend you"))
        self.reqres_terminal_text = page.get_by_text(re.compile("reqres-terminal"))
        self.boot_sequence = page.get_by_test_id("bootSequence")
        self.post_button = page.get_by_role("button", name="POST")
        self.payload_input = page.locator(".code-editor-textarea")
        self.send_button = page.get_by_role("button", name="Send")
        self.response_status = page.locator("#responseStatus")
        self.parent_response_body = page.locator("#responseBody")
        self.id_property_response = (
            self.parent_response_body
            .locator('.json-string:right-of(:text("id"))')
            .first
        )
        self.title_property_response = (
            self.parent_response_body
            .locator('.json-string:right-of(:text("title"))')
            .first
        )
        self.completed_property_response = (
            self.parent_response_body
            .locator('.json-boolean:near(:text("completed"))')
            .first
        )

    # ── Actions / Assertions ──────────────────────────────────────────────
    # NOTE: these were incorrectly @property in the original — fixed to
    # regular methods so they can accept arguments and be called with ()

    def open(self) -> "HomePage":
        """Navigate to the home page using the active environment base_url."""
        self.navigate()
        return self

    def is_page_and_API_ready(self) -> None:
        expect(self.title_text).to_be_visible()
        expect(self.reqres_terminal_text).to_be_visible()
        expect(self.boot_sequence).not_to_be_visible()

    def click_post_button(self, attr_text: str) -> None:
        self.post_button.click()
        expect(self.post_button).to_have_class(re.compile(f"{attr_text}"))

    def send_post_request(self, payload: str) -> None:
        self.payload_input.fill(payload)
        self.send_button.click()

    def is_response_ok(self, response_status: str, payload: str) -> None:
        data = json.loads(payload)
        expect(self.response_status).to_contain_text(response_status)
        expect(self.id_property_response).to_be_visible()
        expect(self.title_property_response).to_contain_text(str(data["title"]))
        expect(self.completed_property_response).to_contain_text(
            str(data["completed"]), ignore_case=True
        )