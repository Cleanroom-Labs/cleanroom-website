import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test.describe('Blog card navigation', () => {
    test('clicking blog card title navigates to post', async ({ page }) => {
      await page.goto('/blog');

      // Get the first blog post title link
      const firstPostLink = page.locator('article').first().locator('a').first();
      const href = await firstPostLink.getAttribute('href');

      await firstPostLink.click();

      // Should navigate to the post page
      await expect(page).toHaveURL(href);
    });

    test('blog post page loads correctly', async ({ page }) => {
      await page.goto('/blog');

      // Click on first post
      const firstPostLink = page.locator('article').first().locator('a').first();
      await firstPostLink.click();

      // Post page should have content
      await expect(page.locator('h1')).toBeVisible();
      // The blog post page has an article element wrapping the content
      await expect(page.locator('article').first()).toBeVisible();
    });

    test('blog post page shows post content', async ({ page }) => {
      // Navigate directly to a known post
      await page.goto('/blog/introducing-airgap-tools');

      // Should show the post title
      await expect(page.locator('h1')).toContainText(/air-gapped|tools/i);

      // Should have post content
      await expect(page.locator('article')).toBeVisible();
    });
  });

  test.describe('Back to Blog navigation', () => {
    test('back to blog link exists on post page', async ({ page }) => {
      await page.goto('/blog/introducing-airgap-tools');

      // Look for back link
      const backLink = page.getByRole('link', { name: /back.*blog|blog/i }).first();
      await expect(backLink).toBeVisible();
    });

    test('back to blog link navigates to blog index', async ({ page }) => {
      await page.goto('/blog/introducing-airgap-tools');

      // Find and click back link
      const backLink = page.getByRole('link', { name: /back.*blog/i }).or(
        page.locator('a[href="/blog"]')
      ).first();

      if (await backLink.isVisible()) {
        await backLink.click();
        await expect(page).toHaveURL('/blog');
      }
    });
  });

  test.describe('Cross-page navigation', () => {
    test('can navigate from homepage to blog', async ({ page }) => {
      await page.goto('/');

      // Find blog link in navigation
      const blogLink = page.getByRole('link', { name: /blog/i }).first();
      await blogLink.click();

      await expect(page).toHaveURL('/blog');
      await expect(page.locator('h1')).toContainText('Blog');
    });

    test('can navigate from blog to homepage', async ({ page }) => {
      await page.goto('/blog');

      // Find home link or logo
      const homeLink = page.getByRole('link', { name: /home|cleanroom/i }).first();
      await homeLink.click();

      await expect(page).toHaveURL('/');
    });

    test('navigation is consistent across pages', async ({ page }) => {
      // Check homepage nav
      await page.goto('/');
      const homeNavLinks = await page.locator('nav a').count();

      // Check blog page nav
      await page.goto('/blog');
      const blogNavLinks = await page.locator('nav a').count();

      // Navigation should have same number of links
      expect(homeNavLinks).toBe(blogNavLinks);
    });

    test('product card links navigate to docs', async ({ page }) => {
      await page.goto('/');

      // Click on AirGap Transfer product
      const productLink = page.getByRole('link').filter({
        has: page.getByRole('heading', { name: 'AirGap Transfer' }),
      });

      const href = await productLink.getAttribute('href');
      expect(href).toContain('/docs/transfer');
    });
  });

  test.describe('About page navigation', () => {
    test('can navigate to about page', async ({ page }) => {
      await page.goto('/');

      const aboutLink = page.getByRole('link', { name: /about/i }).first();
      if (await aboutLink.isVisible()) {
        await aboutLink.click();
        await expect(page).toHaveURL('/about');
      }
    });
  });

  // Donate page navigation — hidden for now, re-enable with donate button
  // test.describe('Donate page navigation', () => {
  //   test('can navigate to donate page', async ({ page }) => {
  //     await page.goto('/');
  //     const donateLink = page.getByRole('link', { name: /donate|support/i }).first();
  //     if (await donateLink.isVisible()) {
  //       await donateLink.click();
  //       await expect(page).toHaveURL('/donate');
  //     }
  //   });
  // });
});

test.describe('Navigation - Mobile', () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test('mobile navigation works', async ({ page }) => {
    await page.goto('/');

    // Look for mobile menu button (hamburger)
    const menuButton = page.getByRole('button', { name: /menu|navigation/i }).or(
      page.locator('[aria-label="Menu"]')
    ).or(
      page.locator('button').filter({ has: page.locator('svg') }).first()
    );

    // If there's a mobile menu, test it
    if (await menuButton.isVisible()) {
      await menuButton.click();
      // Menu should show navigation links
      await expect(page.getByRole('link', { name: /blog/i })).toBeVisible();
    }
  });

  test('blog posts are navigable on mobile', async ({ page }) => {
    await page.goto('/blog');

    const firstPostLink = page.locator('article').first().locator('a').first();
    await firstPostLink.click();

    // Should navigate to post
    await expect(page.locator('h1')).toBeVisible();
    // The blog post page has an article element wrapping the content
    await expect(page.locator('article').first()).toBeVisible();
  });
});
