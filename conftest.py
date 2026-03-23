"""
conftest.py — environment-aware Playwright fixtures.

Usage:
  pytest --env dev
  pytest --env stg
  ENV=stg pytest
"""
from __future__ import annotations

import pathlib

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config.environments import get_config, EnvironmentConfig


# ── CLI option ──────────────────────────────────────────────────────────────

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Target environment: dev | stg  (overrides ENV env-var, default: dev)",
    )


# ── Session-scoped config ───────────────────────────────────────────────────

@pytest.fixture(scope="session")
def env_config(request: pytest.FixtureRequest) -> EnvironmentConfig:
    env_name = request.config.getoption("--env")
    cfg = get_config(env_name)
    print(f"\n🌍  Environment : [{cfg.name.upper()}]")
    print(f"🔗  Base URL    : {cfg.base_url}")
    return cfg


# ── Playwright / browser fixtures ───────────────────────────────────────────

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, env_config: EnvironmentConfig) -> Browser:
    bc = env_config.browser
    b = playwright_instance.chromium.launch(
        headless=bc.headless,
        slow_mo=bc.slow_mo,
    )
    yield b
    b.close()


@pytest.fixture(scope="function")
def context(browser: Browser, env_config: EnvironmentConfig, tmp_path) -> BrowserContext:
    bc = env_config.browser

    video_dir = str(tmp_path / "videos") if env_config.video != "off" else None
    ctx = browser.new_context(
        base_url=env_config.base_url,
        viewport={"width": bc.viewport_width, "height": bc.viewport_height},
        record_video_dir=video_dir,
    )
    ctx.set_default_timeout(bc.timeout)
    ctx.set_default_navigation_timeout(bc.navigation_timeout)

    if env_config.tracing != "off":
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield ctx

    # ── Teardown ─────────────────────────────────────────────────────────
    failed = getattr(ctx, "_test_failed", False)

    if env_config.tracing != "off":
        should_save = env_config.tracing == "on" or (
            env_config.tracing == "retain-on-failure" and failed
        )
        if should_save:
            trace_path = tmp_path / "trace.zip"
            ctx.tracing.stop(path=str(trace_path))
            print(f"\n📦  Trace → {trace_path}")
        else:
            ctx.tracing.stop()

    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Page:
    pg = context.new_page()
    yield pg

    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        context._test_failed = True  # type: ignore[attr-defined]

    pg.close()


# ── Screenshot on failure ────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        pg: Page | None = item.funcargs.get("page")
        cfg: EnvironmentConfig | None = item.funcargs.get("env_config")
        if pg and cfg and cfg.screenshot_on_failure:
            shot_dir = pathlib.Path("reports/screenshots")
            shot_dir.mkdir(parents=True, exist_ok=True)
            safe_name = item.nodeid.replace("/", "_").replace("::", "__")
            pg.screenshot(path=str(shot_dir / f"{safe_name}.png"), full_page=True)
            print(f"\n📸  Screenshot → reports/screenshots/{safe_name}.png")