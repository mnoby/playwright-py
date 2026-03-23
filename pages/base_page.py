"""
Base page — all page objects inherit from this.
Provides navigation helpers wired to the active environment config.
"""
from __future__ import annotations

import pathlib
from playwright.sync_api import Page, expect

from config.environments import EnvironmentConfig


class BasePage:
    def __init__(self, page: Page, config: EnvironmentConfig) -> None:
        self.page = page
        self.config = config

    def navigate(self, path: str = "") -> None:
        """Navigate to base_url + optional path."""
        self.page.goto(f"{self.config.base_url}{path}")

    def take_screenshot(self, name: str) -> None:
        pathlib.Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
        self.page.screenshot(
            path=f"reports/screenshots/{name}.png", full_page=True
        )