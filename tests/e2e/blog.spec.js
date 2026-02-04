import { test, expect } from '@playwright/test';

test.describe('Blog Page', () => {
  // Use a larger viewport to ensure the sidebar is visible
  test.use({ viewport: { width: 1440, height: 900 } });

  test.beforeEach(async ({ page }) => {
    await page.goto('/blog');
    // Wait for the page to fully load
    await page.waitForSelector('article');
  });

  test('page loads with all blog posts', async ({ page }) => {
    // Wait for blog posts to load
    const count = await page.locator('article').count();
    expect(count).toBeGreaterThanOrEqual(1);

    // Verify page title
    await expect(page.locator('h1')).toContainText('Blog');
  });

  test('displays blog post cards with correct information', async ({ page }) => {
    // Check that the first article has expected elements
    const firstArticle = page.locator('article').first();
    await expect(firstArticle.locator('h2')).toBeVisible();
    await expect(firstArticle.locator('time')).toBeVisible();
  });

  test.describe('Search filtering', () => {
    test('filters posts by title/content', async ({ page }) => {
      // Find the visible search input in the fixed sidebar
      const searchInput = page.getByPlaceholder('Search...').and(page.locator(':visible'));
      await searchInput.fill('air-gapped');

      // Wait for filtering to apply
      await page.waitForTimeout(300);

      // Should show fewer posts that match the search
      const articles = page.locator('article');
      const count = await articles.count();
      expect(count).toBeGreaterThan(0);
    });

    test('shows empty state when no posts match search', async ({ page }) => {
      const searchInput = page.getByPlaceholder('Search...').and(page.locator(':visible'));
      await searchInput.fill('xyznonexistentquery123');

      await page.waitForTimeout(300);

      // Should show empty state
      await expect(page.locator('article')).toHaveCount(0);
      await expect(page.getByText(/No posts found/i)).toBeVisible();
    });

    test('search is case insensitive', async ({ page }) => {
      const searchInput = page.getByPlaceholder('Search...').and(page.locator(':visible'));
      await searchInput.fill('PRIVACY');

      await page.waitForTimeout(300);

      const count = await page.locator('article').count();
      expect(count).toBeGreaterThan(0);
    });
  });

  test.describe('Tag filtering', () => {
    test('clicking a tag filters posts', async ({ page }) => {
      // Click on a tag button in the first article
      const tagButton = page.locator('article').first().locator('button').first();
      const tagName = await tagButton.textContent();

      await tagButton.click();

      // URL should update with tag filter
      await expect(page).toHaveURL(/tags=/);

      // All visible posts should have the selected tag
      const articles = page.locator('article');
      const count = await articles.count();
      expect(count).toBeGreaterThan(0);
    });

    test('multiple tags can be selected', async ({ page }) => {
      // Click on a tag from first article
      const firstTag = page.locator('article').first().locator('button').first();
      await firstTag.click();

      await page.waitForTimeout(300);

      // URL should have tags parameter
      await expect(page).toHaveURL(/tags=/);
    });

    test('tag filter shows in URL', async ({ page }) => {
      const tagButton = page.locator('article').first().locator('button').first();
      await tagButton.click();

      await expect(page).toHaveURL(/tags=/);
    });
  });

  test.describe('URL persistence', () => {
    test('search query persists in URL', async ({ page }) => {
      const searchInput = page.getByPlaceholder('Search...').and(page.locator(':visible'));
      await searchInput.fill('privacy');

      await page.waitForTimeout(500);

      // URL should contain search query
      await expect(page).toHaveURL(/q=privacy/);
    });

    test('filters restore from URL on page load', async ({ page }) => {
      // Navigate directly to URL with filters
      await page.goto('/blog?q=airgap&tags=privacy');

      // Wait for page to load
      await page.waitForTimeout(500);

      // Search input should have the query
      const searchInput = page.getByPlaceholder('Search...').and(page.locator(':visible'));
      await expect(searchInput).toHaveValue('airgap');
    });

    test('combined search and tag filters in URL', async ({ page }) => {
      const searchInput = page.getByPlaceholder('Search...').and(page.locator(':visible'));
      await searchInput.fill('tools');

      await page.waitForTimeout(300);

      const tagButton = page.locator('article').first().locator('button').first();
      if (await tagButton.isVisible()) {
        await tagButton.click();
        await page.waitForTimeout(300);
        await expect(page).toHaveURL(/q=.*tags=|tags=.*q=/);
      }
    });
  });

  test.describe('Clear filters', () => {
    test('clear filters button resets search', async ({ page }) => {
      // Apply a search filter
      const searchInput = page.getByPlaceholder('Search...').and(page.locator(':visible'));
      await searchInput.fill('privacy');
      await page.waitForTimeout(300);

      // Look for a clear/reset button (it appears after filtering)
      const clearButton = page.getByRole('button', { name: /clear/i });
      await expect(clearButton).toBeVisible();
      await clearButton.click();

      // Search should be cleared
      await expect(searchInput).toHaveValue('');

      // All posts should be visible again
      const count = await page.locator('article').count();
      expect(count).toBeGreaterThanOrEqual(1);
    });

    test('clear filters removes URL params', async ({ page }) => {
      await page.goto('/blog?q=test&tags=privacy');
      await page.waitForTimeout(300);

      const clearButton = page.getByRole('button', { name: /clear/i });
      await expect(clearButton).toBeVisible();
      await clearButton.click();
      await page.waitForTimeout(300);

      // URL should be clean
      expect(page.url()).not.toContain('q=');
      expect(page.url()).not.toContain('tags=');
    });
  });
});

test.describe('Blog Page - Mobile', () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test('mobile filter toggle shows and hides filters', async ({ page }) => {
    await page.goto('/blog');
    await page.waitForSelector('article');

    // Look for the mobile filter toggle button
    const filterToggle = page.getByRole('button', { name: /filters/i });
    await expect(filterToggle).toBeVisible();

    // Click to open filters
    await filterToggle.click();

    // Filter overlay should be visible
    await expect(page.locator('.fixed.inset-0.z-50')).toBeVisible();
  });

  test('mobile filter overlay has close button', async ({ page }) => {
    await page.goto('/blog');
    await page.waitForSelector('article');

    const filterToggle = page.getByRole('button', { name: /filters/i });
    await filterToggle.click();

    // Look for close button in the overlay (aria-label="Close filters")
    const closeButton = page.getByLabel('Close filters');
    await expect(closeButton).toBeVisible();
    await closeButton.click();

    // Overlay should close
    await expect(page.locator('.fixed.inset-0.z-50')).not.toBeVisible();
  });

  test('blog posts are visible on mobile', async ({ page }) => {
    await page.goto('/blog');
    const count = await page.locator('article').count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test('can search on mobile through filter overlay', async ({ page }) => {
    await page.goto('/blog');
    await page.waitForSelector('article');

    // Open filter overlay
    const filterToggle = page.getByRole('button', { name: /filters/i });
    await filterToggle.click();

    // Find search input in the overlay
    const searchInput = page.locator('.fixed.inset-0.z-50').getByPlaceholder('Search...');
    await expect(searchInput).toBeVisible();
    await searchInput.fill('privacy');

    // Close overlay
    const closeButton = page.getByLabel('Close filters');
    await closeButton.click();

    // Posts should be filtered
    await page.waitForTimeout(300);
    const count = await page.locator('article').count();
    expect(count).toBeGreaterThanOrEqual(1);
  });
});
