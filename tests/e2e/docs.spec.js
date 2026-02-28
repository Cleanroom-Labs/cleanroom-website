import { test, expect } from '@playwright/test';

// Next.js dev server requires explicit index.html paths for static Sphinx docs.
// Trailing-slash paths get 308-redirected and may not resolve to directory indexes.
const DOCS_ROOT = '/docs/dev/index.html';
const TRANSFER_INDEX = '/docs/dev/transfer/index.html';
const DEPLOY_INDEX = '/docs/dev/deploy/index.html';
const WHISPER_INDEX = '/docs/dev/whisper/index.html';

// Helper: extract nav link {text, href} pairs from the main site header.
async function getMainSiteNavLinks(page) {
  const links = page.locator('nav a[href]');
  const count = await links.count();
  const result = [];
  for (let i = 0; i < count; i++) {
    const text = (await links.nth(i).innerText()).trim();
    const href = await links.nth(i).getAttribute('href');
    if (text && href) result.push({ text, href });
  }
  return result;
}

// Helper: extract nav link {text, href} pairs from the Sphinx docs header.
async function getDocsNavLinks(page) {
  const links = page.locator('.site-nav-menu a[href]');
  const count = await links.count();
  const result = [];
  for (let i = 0; i < count; i++) {
    const text = (await links.nth(i).innerText()).trim();
    const href = await links.nth(i).getAttribute('href');
    if (text && href) result.push({ text, href });
  }
  return result;
}

// ---------------------------------------------------------------------------
// Docs Landing
// ---------------------------------------------------------------------------
test.describe('Documentation Landing', () => {
  test('master index page loads', async ({ page }) => {
    await page.goto(DOCS_ROOT);
    await expect(page.locator('.wy-nav-content')).toBeVisible();
  });

  test('master index lists all three projects', async ({ page }) => {
    await page.goto(DOCS_ROOT);
    const sidebar = page.locator('.wy-menu-vertical');
    await expect(sidebar.locator('text=Transfer').first()).toBeVisible();
    await expect(sidebar.locator('text=Deploy').first()).toBeVisible();
    await expect(sidebar.locator('text=Whisper').first()).toBeVisible();
  });

  test('project links navigate to project index pages', async ({ page }) => {
    await page.goto(DOCS_ROOT);
    const transferLink = page.locator('.wy-menu-vertical a', { hasText: 'Transfer' }).first();
    const href = await transferLink.getAttribute('href');
    expect(href).toContain('transfer');
  });
});

// ---------------------------------------------------------------------------
// Project Index Pages
// ---------------------------------------------------------------------------
test.describe('Project Index Pages', () => {
  test('transfer project index loads', async ({ page }) => {
    const resp = await page.goto(TRANSFER_INDEX);
    expect(resp?.ok()).toBeTruthy();
    await expect(page.locator('.wy-nav-content')).toBeVisible();
  });

  test('deploy project index loads', async ({ page }) => {
    const resp = await page.goto(DEPLOY_INDEX);
    expect(resp?.ok()).toBeTruthy();
    await expect(page.locator('.wy-nav-content')).toBeVisible();
  });

  test('whisper project index loads', async ({ page }) => {
    const resp = await page.goto(WHISPER_INDEX);
    expect(resp?.ok()).toBeTruthy();
    await expect(page.locator('.wy-nav-content')).toBeVisible();
  });

  test('project pages have sidebar navigation', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const sidebar = page.locator('.wy-menu-vertical');
    await expect(sidebar).toBeVisible();
    const count = await sidebar.locator('a').count();
    expect(count).toBeGreaterThan(0);
  });
});

// ---------------------------------------------------------------------------
// Website Integration (NOT standalone mode)
// ---------------------------------------------------------------------------
test.describe('Website Integration', () => {
  test('docs pages show website header with nav links', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const navMenu = page.locator('.site-nav-menu');
    await expect(navMenu).toBeVisible();
    await expect(navMenu.locator('a', { hasText: 'About' })).toBeVisible();
    await expect(navMenu.locator('a', { hasText: 'Blog' })).toBeVisible();
    await expect(navMenu.locator('a', { hasText: 'Docs' })).toBeVisible();
  });

  test('docs pages do NOT show standalone project branding', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const brand = page.locator('.nav-brand');
    await expect(brand).toContainText('Cleanroom Labs');
  });

  test('header Blog link navigates to /blog', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const blogLink = page.locator('.site-nav-menu a', { hasText: 'Blog' });
    await blogLink.click();
    await expect(page).toHaveURL('/blog');
  });

  test('header About link navigates to /about', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const aboutLink = page.locator('.site-nav-menu a', { hasText: 'About' });
    await aboutLink.click();
    await expect(page).toHaveURL('/about');
  });
});

// ---------------------------------------------------------------------------
// Header Consistency (main site vs docs)
// ---------------------------------------------------------------------------
test.describe('Header Consistency', () => {
  test('homepage and docs have matching nav links', async ({ page }) => {
    await page.goto('/');
    const homeLinks = await getMainSiteNavLinks(page);

    await page.goto(TRANSFER_INDEX);
    const docsLinks = await getDocsNavLinks(page);

    // Both should have the same navigation links (About, Blog, Docs)
    const homeNav = homeLinks.filter(l => ['About', 'Blog', 'Docs'].includes(l.text));
    expect(homeNav.length).toBe(docsLinks.length);
    for (const docLink of docsLinks) {
      const matching = homeNav.find(h => h.text === docLink.text);
      expect(matching, `Nav link "${docLink.text}" missing from homepage`).toBeDefined();
      expect(matching?.href).toBe(docLink.href);
    }
  });

  test('about page and docs have matching nav links', async ({ page }) => {
    await page.goto('/about');
    const aboutLinks = await getMainSiteNavLinks(page);

    await page.goto(DEPLOY_INDEX);
    const docsLinks = await getDocsNavLinks(page);

    const aboutNav = aboutLinks.filter(l => ['About', 'Blog', 'Docs'].includes(l.text));
    expect(aboutNav.length).toBe(docsLinks.length);
    for (const docLink of docsLinks) {
      const matching = aboutNav.find(h => h.text === docLink.text);
      expect(matching, `Nav link "${docLink.text}" missing from about page`).toBeDefined();
      expect(matching?.href).toBe(docLink.href);
    }
  });

  test('brand name is consistent across main site and docs', async ({ page }) => {
    await page.goto('/');
    const homeBrand = await page.locator('nav a', { hasText: 'Cleanroom Labs' }).first().innerText();

    await page.goto(TRANSFER_INDEX);
    const docsBrand = await page.locator('.nav-brand').innerText();

    expect(homeBrand.trim()).toBe(docsBrand.trim());
  });
});

// ---------------------------------------------------------------------------
// Sidebar & Navigation
// ---------------------------------------------------------------------------
test.describe('Docs Sidebar & Navigation', () => {
  test('sidebar is present on docs pages', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    await expect(page.locator('.wy-nav-side')).toBeVisible();
  });

  test('sidebar collapse toggle works', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const toggle = page.locator('#sidebar-toggle');
    await expect(toggle).toBeVisible();

    await toggle.click();
    await expect(page.locator('html')).toHaveClass(/sidebar-collapsed/);

    await toggle.click();
    await expect(page.locator('html')).not.toHaveClass(/sidebar-collapsed/);
  });

  test('sidebar state persists across navigation', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const toggle = page.locator('#sidebar-toggle');

    await toggle.click();
    await expect(page.locator('html')).toHaveClass(/sidebar-collapsed/);

    // Navigate to another page via direct URL (sidebar links are off-viewport when collapsed)
    await page.goto('/docs/dev/transfer/readme.html');
    await page.waitForLoadState('domcontentloaded');

    await expect(page.locator('html')).toHaveClass(/sidebar-collapsed/);
  });

  test('breadcrumbs are visible on sub-pages', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const subLink = page.locator('.wy-menu-vertical a.reference.internal').first();
    await subLink.click();
    await page.waitForLoadState('domcontentloaded');

    const breadcrumbs = page.locator('.wy-breadcrumbs');
    await expect(breadcrumbs).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// Search
// ---------------------------------------------------------------------------
test.describe('Docs Search', () => {
  test('search box is present on docs pages', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const searchInput = page.locator('#rtd-search-form input[name="q"]');
    await expect(searchInput).toBeVisible();
  });

  test('search returns results', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const searchInput = page.locator('#rtd-search-form input[name="q"]');
    await searchInput.fill('requirements');
    await searchInput.press('Enter');
    // Wait for results to appear (don't use networkidle — Sphinx search keeps polling)
    const results = page.locator('#search-results li');
    await expect(results.first()).toBeVisible({ timeout: 15000 });
  });
});

// ---------------------------------------------------------------------------
// Responsive / Mobile
// ---------------------------------------------------------------------------
test.describe('Docs - Mobile', () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test('sidebar is hidden on mobile by default', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const sidebar = page.locator('.wy-nav-side');
    await expect(sidebar).not.toBeInViewport();
  });

  test('mobile nav toggle is visible', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    // On mobile, the custom sidebar-toggle is hidden; RTD uses its own hamburger
    const hamburger = page.locator('[data-toggle="wy-nav-top"]');
    await expect(hamburger).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// Version Sub-bar
// ---------------------------------------------------------------------------
test.describe('Version Sub-bar', () => {
  test('version sub-bar is visible on docs pages', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const versionBar = page.locator('.version-sub-bar');
    await expect(versionBar).toBeVisible();
  });

  test('version select dropdown is present', async ({ page }) => {
    await page.goto(TRANSFER_INDEX);
    const versionSelect = page.locator('#version-select');
    await expect(versionSelect).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// No Console Errors
// ---------------------------------------------------------------------------
test.describe('No Console Errors on Docs Pages', () => {
  test('transfer index page produces no unexpected console errors', async ({ page }) => {
    const errors = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        const text = msg.text();
        // Filter known non-issues: CDN warnings, resource 404s, React DevTools
        if (
          text.includes('Failed to load resource') ||
          text.includes('cdn.tailwindcss.com') ||
          text.includes('React DevTools') ||
          text.includes('versions.json')
        ) return;
        errors.push(text);
      }
    });

    await page.goto(TRANSFER_INDEX);
    // Use domcontentloaded — networkidle is unreliable with Sphinx search polling
    await page.waitForLoadState('domcontentloaded');
    // Give scripts a moment to execute
    await page.waitForTimeout(2000);

    expect(errors, `Unexpected console errors: ${errors.join('; ')}`).toHaveLength(0);
  });
});
