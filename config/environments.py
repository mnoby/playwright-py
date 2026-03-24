"""
Environment configuration for playwright-py.
Supports: dev | stg

Resolution order:
  1. --env CLI argument  (pytest --env stg)
  2. ENV environment variable  (ENV=stg pytest)
  3. Default → dev
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from pyee import base


@dataclass
class BrowserConfig:
    headless: bool = True
    slow_mo: int = 0
    timeout: int = 30_000
    navigation_timeout: int = 60_000
    viewport_width: int = 1920
    viewport_height: int = 1080


@dataclass
class EnvironmentConfig:
    name: str
    base_url: str = os.getenv("BASE_URL", "https://reqres.in")
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    retries: int = 1
    screenshot_on_failure: bool = True
    video: str = "retain-on-failure"   # "on" | "off" | "retain-on-failure"
    tracing: str = "retain-on-failure" # "on" | "off" | "retain-on-failure"


_CONFIGS: dict[str, EnvironmentConfig] = {
    "dev": EnvironmentConfig(
        name="dev",
        browser=BrowserConfig(
            headless=os.getenv("HEADLESS", "true").lower() == "true",
            slow_mo=int(os.getenv("SLOW_MO", "0")),
            timeout=int(os.getenv("TIMEOUT", "30000")),
        ),
        retries=int(os.getenv("RETRIES", "1")),
        video="off",
        tracing="retain-on-failure",
    ),
    "stg": EnvironmentConfig(
        name="stg",
        browser=BrowserConfig(
            headless=os.getenv("HEADLESS", "true").lower() == "true",
            slow_mo=int(os.getenv("SLOW_MO", "0")),
            timeout=int(os.getenv("TIMEOUT", "30000")),
        ),
        retries=int(os.getenv("RETRIES", "2")),
        video="retain-on-failure",
        tracing="retain-on-failure",
    ),
}


def get_config(env: Optional[str] = None) -> EnvironmentConfig:
    resolved = (env or os.getenv("ENV", "dev")).lower()
    if resolved not in _CONFIGS:
        valid = ", ".join(_CONFIGS.keys())
        raise ValueError(f"Unknown environment '{resolved}'. Valid options: {valid}")
    return _CONFIGS[resolved]