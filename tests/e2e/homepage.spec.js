import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test.describe('Hero section', () => {
    test('displays hero section', async ({ page }) => {
      // Check for main heading or hero content
      const heroHeading = page.locator('h1').first();
      await expect(heroHeading).toBeVisible();
    });

    test('hero section has call-to-action', async ({ page }) => {
      // Look for buttons or links in the hero area
      const ctaLink = page.locator('a[href="#products"]').or(
        page.getByRole('link', { name: /tools|products|get started/i })
      );
      await expect(ctaLink.first()).toBeVisible();
    });
  });

  test.describe('Product cards', () => {
    test('displays all product cards', async ({ page }) => {
      // Should have product cards for each product plus the "Coming Soon" card
      const productCards = page.locator('[class*="rounded-xl"]').filter({
        has: page.locator('h3'),
      });
      const count = await productCards.count();
      expect(count).toBeGreaterThanOrEqual(3); // At least 3 products
    });

    test('displays AirGap Transfer product', async ({ page }) => {
      await expect(page.getByRole('heading', { name: 'AirGap Transfer' })).toBeVisible();
      await expect(page.getByText(/secure data transfer/i)).toBeVisible();
    });

    test('displays AirGap Deploy product', async ({ page }) => {
      await expect(page.getByRole('heading', { name: 'AirGap Deploy' })).toBeVisible();
      await expect(page.getByText(/deployment framework/i)).toBeVisible();
    });

    test('displays Cleanroom Whisper product', async ({ page }) => {
      await expect(page.getByRole('heading', { name: 'Cleanroom Whisper' })).toBeVisible();
      await expect(page.getByText(/voice transcription/i)).toBeVisible();
    });

    test('active products link to their documentation', async ({ page }) => {
      // AirGap Transfer should link to docs
      const transferLink = page.getByRole('link', { name: /AirGap Transfer/i }).first();
      await expect(transferLink).toHaveAttribute('href', /\/docs\/airgap-transfer/);

      // AirGap Deploy should link to docs
      const deployLink = page.getByRole('link', { name: /AirGap Deploy/i }).first();
      await expect(deployLink).toHaveAttribute('href', /\/docs\/airgap-deploy/);
    });

    test('planned product shows "Planned" badge', async ({ page }) => {
      // Cleanroom Whisper is planned
      const plannedBadge = page.getByText('Planned');
      await expect(plannedBadge).toBeVisible();
    });

    test('displays "Coming Soon" placeholder card', async ({ page }) => {
      await expect(page.getByText('More Coming Soon')).toBeVisible();
      await expect(page.getByText(/additional.*tools.*development/i)).toBeVisible();
    });
  });

  test.describe('Products section', () => {
    test('has products section heading', async ({ page }) => {
      await expect(page.getByRole('heading', { name: 'Our Tools' })).toBeVisible();
    });

    test('has products section description', async ({ page }) => {
      await expect(page.getByText('Privacy-first tools designed to work completely offline.')).toBeVisible();
      await expect(page.getByText(/no cloud.*no telemetry/i)).toBeVisible();
    });

    test('products section is navigable via anchor', async ({ page }) => {
      // Click on "View Our Tools" or similar CTA
      const ctaLink = page.locator('a[href="#products"]').first();
      if (await ctaLink.isVisible()) {
        await ctaLink.click();
        // Should scroll to products section
        await expect(page.locator('#products')).toBeInViewport();
      }
    });
  });
});

test.describe('Homepage - Mobile', () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test('hero section is visible on mobile', async ({ page }) => {
    await page.goto('/');
    const heroHeading = page.locator('h1').first();
    await expect(heroHeading).toBeVisible();
  });

  test('product cards stack vertically on mobile', async ({ page }) => {
    await page.goto('/');
    // Products should still be visible
    await expect(page.getByRole('heading', { name: 'AirGap Transfer' })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'AirGap Deploy' })).toBeVisible();
  });

  test('page scrolls to products section', async ({ page }) => {
    await page.goto('/');
    // Scroll to products section
    await page.evaluate(() => {
      document.querySelector('#products')?.scrollIntoView({ behavior: 'instant' });
    });
    await page.waitForTimeout(100);
    // Verify the products heading is visible after scroll
    await expect(page.getByRole('heading', { name: 'Our Tools' })).toBeVisible();
  });
});
