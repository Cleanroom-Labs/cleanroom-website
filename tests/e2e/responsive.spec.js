import { test, expect } from '@playwright/test';

// Next.js dev server requires explicit index.html paths for static Sphinx docs.
const DOCS_ROOT = '/docs/dev/index.html';
const TRANSFER_INDEX = '/docs/dev/transfer/index.html';

// Pages to test for horizontal overflow.
const PAGES = ['/', '/about', '/blog', DOCS_ROOT, TRANSFER_INDEX];

// Viewports to test.
const VIEWPORTS = [
  { label: 'iPhone SE', width: 375, height: 667 },
  { label: 'iPhone 14', width: 393, height: 852 },
  { label: 'iPad Mini', width: 768, height: 1024 },
  { label: 'Desktop 1080p', width: 1920, height: 1080 },
  { label: 'Landscape', width: 667, height: 375 },
];

// ---------------------------------------------------------------------------
// No Horizontal Overflow
// ---------------------------------------------------------------------------
test.describe('No Horizontal Overflow', () => {
  for (const vp of VIEWPORTS) {
    for (const pagePath of PAGES) {
      test(`${pagePath} at ${vp.label} (${vp.width}x${vp.height})`, async ({ page }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto(pagePath);
        await page.waitForLoadState('domcontentloaded');

        const overflow = await page.evaluate(() => {
          return document.documentElement.scrollWidth > document.documentElement.clientWidth;
        });
        expect(overflow, `Horizontal overflow detected at ${vp.width}px`).toBe(false);
      });
    }
  }
});

// ---------------------------------------------------------------------------
// Touch Targets — Mobile
// ---------------------------------------------------------------------------
test.describe('Touch Targets', () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test('nav links have minimum 44px tap height', async ({ page }) => {
    await page.goto('/');
    const navLinks = page.locator('nav a[href]');
    const count = await navLinks.count();
    expect(count).toBeGreaterThan(0);

    for (let i = 0; i < count; i++) {
      const box = await navLinks.nth(i).boundingBox();
      if (box) {
        expect(box.height, `Nav link ${i} height ${box.height}px < 44px`).toBeGreaterThanOrEqual(44);
      }
    }
  });

  test('footer links have minimum 44px tap height', async ({ page }) => {
    await page.goto('/');
    const footerLinks = page.locator('footer a');
    const count = await footerLinks.count();
    expect(count).toBeGreaterThan(0);

    for (let i = 0; i < count; i++) {
      const box = await footerLinks.nth(i).boundingBox();
      if (box) {
        expect(box.height, `Footer link ${i} height ${box.height}px < 44px`).toBeGreaterThanOrEqual(44);
      }
    }
  });

  test('logo tap area is at least 44px', async ({ page }) => {
    await page.goto('/');
    const logo = page.locator('nav a img[alt*="home"]').first();
    const parentLink = logo.locator('..');
    const box = await parentLink.boundingBox();
    expect(box).not.toBeNull();
    expect(box.height).toBeGreaterThanOrEqual(44);
    expect(box.width).toBeGreaterThanOrEqual(44);
  });
});

// ---------------------------------------------------------------------------
// Layout Transitions at Breakpoints
// ---------------------------------------------------------------------------
test.describe('Layout Transitions', () => {
  test('product cards are single-column at 375px', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    // Product card container uses Tailwind grid classes
    const cardContainer = page.locator('.grid').first();
    if (await cardContainer.isVisible()) {
      const columns = await cardContainer.evaluate((el) => {
        return window.getComputedStyle(el).gridTemplateColumns.split(' ').length;
      });
      expect(columns).toBe(1);
    }
  });

  test('product cards are multi-column at 768px+', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    const cardContainer = page.locator('.grid').first();
    if (await cardContainer.isVisible()) {
      const columns = await cardContainer.evaluate((el) => {
        return window.getComputedStyle(el).gridTemplateColumns.split(' ').length;
      });
      expect(columns).toBeGreaterThan(1);
    }
  });

  test('brand text hidden at 375px, visible at 768px', async ({ page }) => {
    // Mobile — hidden
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    const brandLink = page.locator('nav a', { hasText: 'Cleanroom Labs' }).first();
    await expect(brandLink).not.toBeVisible();

    // Tablet — visible
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    await expect(brandLink).toBeVisible();
  });

  test('docs sidebar hidden at 375px, visible at 1024px', async ({ page }) => {
    // Mobile — hidden
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(TRANSFER_INDEX);
    const sidebar = page.locator('.wy-nav-side');
    await expect(sidebar).not.toBeInViewport();

    // Desktop — visible
    await page.setViewportSize({ width: 1024, height: 768 });
    await page.goto(TRANSFER_INDEX);
    await expect(sidebar).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// Content Constraints
// ---------------------------------------------------------------------------
test.describe('Content Constraints', () => {
  test('docs content width <= 1200px at 1920px viewport', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto(TRANSFER_INDEX);
    const contentWidth = await page.locator('.wy-nav-content').evaluate((el) => {
      return el.getBoundingClientRect().width;
    });
    expect(contentWidth).toBeLessThanOrEqual(1200);
  });

  test('about page content does not stretch to full viewport at 1920px', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/about');
    const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
    const contentContainer = page.locator('.container').first();
    const containerWidth = await contentContainer.evaluate((el) => {
      return el.getBoundingClientRect().width;
    });
    expect(containerWidth).toBeLessThan(bodyWidth);
  });
});

// ---------------------------------------------------------------------------
// Landscape Mode
// ---------------------------------------------------------------------------
test.describe('Landscape Mode', () => {
  test('homepage renders without overflow at 667x375', async ({ page }) => {
    await page.setViewportSize({ width: 667, height: 375 });
    await page.goto('/');
    const overflow = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(overflow).toBe(false);
  });

  test('docs page renders without overflow at 667x375', async ({ page }) => {
    await page.setViewportSize({ width: 667, height: 375 });
    await page.goto(TRANSFER_INDEX);
    const overflow = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(overflow).toBe(false);
  });
});
