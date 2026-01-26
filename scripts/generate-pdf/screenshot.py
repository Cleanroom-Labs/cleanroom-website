"""
Screenshot capture using Playwright.
"""

import asyncio
from pathlib import Path
from typing import Optional

try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from config import Config, config as default_config


class ScreenshotCapture:
    """Capture screenshots from the running website."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or default_config

        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is required for screenshot capture. "
                "Install with: pip install playwright && playwright install chromium"
            )

    async def capture_all(self, server_url: Optional[str] = None) -> dict[str, Path]:
        """Capture all required screenshots."""
        server_url = server_url or self.config.screenshot.server_url

        # Ensure screenshots directory exists
        self.config.paths.screenshots_dir.mkdir(parents=True, exist_ok=True)

        screenshots = {}

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(
                viewport={
                    "width": self.config.screenshot.viewport_width,
                    "height": self.config.screenshot.viewport_height,
                }
            )

            # Navigate to homepage
            if self.config.verbose:
                print(f"  Loading {server_url}...")

            try:
                await page.goto(server_url, wait_until="networkidle", timeout=30000)
            except Exception as e:
                await browser.close()
                raise RuntimeError(
                    f"Failed to connect to {server_url}. "
                    "Make sure the dev server is running (npm run dev)."
                ) from e

            # Capture hero section
            hero_path = await self._capture_hero(page)
            if hero_path:
                screenshots["hero"] = hero_path

            # Capture products section
            products_path = await self._capture_products(page)
            if products_path:
                screenshots["products"] = products_path

            await browser.close()

        return screenshots

    async def _capture_hero(self, page: Page) -> Optional[Path]:
        """Capture the hero section screenshot."""
        output_path = self.config.paths.screenshots_dir / "hero.png"

        try:
            # Find the hero section (first section element)
            hero = await page.query_selector(self.config.screenshot.hero_selector)
            if not hero:
                if self.config.verbose:
                    print("  Warning: Hero section not found")
                return None

            # Capture screenshot
            await hero.screenshot(path=str(output_path))

            if self.config.verbose:
                print(f"  Captured hero: {output_path}")

            return output_path

        except Exception as e:
            if self.config.verbose:
                print(f"  Error capturing hero: {e}")
            return None

    async def _capture_products(self, page: Page) -> Optional[Path]:
        """Capture the products/Our Tools section screenshot."""
        output_path = self.config.paths.screenshots_dir / "products.png"

        try:
            # Scroll to products section to ensure it's rendered
            products = await page.query_selector(self.config.screenshot.products_selector)
            if not products:
                if self.config.verbose:
                    print("  Warning: Products section not found")
                return None

            # Scroll into view
            await products.scroll_into_view_if_needed()
            await page.wait_for_timeout(500)  # Wait for animations

            # Capture screenshot
            await products.screenshot(path=str(output_path))

            if self.config.verbose:
                print(f"  Captured products: {output_path}")

            return output_path

        except Exception as e:
            if self.config.verbose:
                print(f"  Error capturing products: {e}")
            return None

    def capture_sync(self, server_url: Optional[str] = None) -> dict[str, Path]:
        """Synchronous wrapper for capture_all."""
        return asyncio.run(self.capture_all(server_url))


def capture_screenshots(
    config: Optional[Config] = None,
    server_url: Optional[str] = None,
) -> dict[str, Path]:
    """Convenience function to capture all screenshots."""
    capture = ScreenshotCapture(config)
    return capture.capture_sync(server_url)
