# Website Migration Plan: Articulation to Next.js with Vercel

## Repository Structure

See [README.md](README.md) for the current repository structure and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design decisions.

## Migration Progress

### Phases 1-3: ✅ Complete
Project setup, build integration, and core pages are done. See git history for details.

### Phase 4: SEO & Performance ✅ Complete
- [x] Configure robots.txt and sitemap (Section 3)
- [ ] Run Lighthouse audit (aim for >90) — manual verification after deployment

### Phase 5: CI/CD ❌ Not Started
- [ ] Set up GitHub Actions quality-checks workflow (Section 6)
- [ ] Verify CI builds successfully with artifact checks

### Phase 6: Vercel Deployment ❌ Not Started
- [ ] Create Vercel account and connect repo (Section 4)
- [ ] Configure build settings and environment variables
- [ ] Verify preview deployment works

### Phase 7: Domain Setup ❌ Not Started
- [ ] Configure custom domain in Vercel (Section 5)
- [ ] Update DNS records in Porkbun
- [ ] Wait for SSL certificate

### Phase 8: Monitoring & Launch ❌ Not Started
- [ ] Set up Vercel Analytics (Section 7)
- [ ] Set up Sentry error monitoring (Section 8)
- [ ] Deploy to production
- [ ] Verify custom domain and HTTPS working
- [ ] Confirm analytics and error tracking active

## 3. SEO & Performance Optimization

1. **Create robots.txt (`public/robots.txt`):**
   ```txt
   # Allow all crawlers
   User-agent: *
   Allow: /

   # Sitemap location
   Sitemap: https://cleanroomlabs.dev/sitemap.xml
   ```

2. **Generate sitemap (`public/sitemap.xml`):**
   Consider using `next-sitemap` package:
   ```bash
   npm install --save-dev next-sitemap
   ```

   Create `next-sitemap.config.js`:
   ```javascript
   module.exports = {
     siteUrl: 'https://cleanroomlabs.dev',
     generateRobotsTxt: true,
     exclude: ['/docs/*'],  // Sphinx generates its own sitemap
     robotsTxtOptions: {
       additionalSitemaps: [
         'https://cleanroomlabs.dev/docs/sitemap.xml',  // Sphinx sitemap
       ],
     },
   };
   ```

   Add to package.json scripts:
   ```json
   "postbuild": "next-sitemap"
   ```

## 4. Vercel Deployment

1. **Connect to Vercel:**
   - Create a Vercel account at vercel.com (free tier)
   - Click "Add New..." and select "Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js settings

2. **Configure build settings:**
   - Build Command: `npm run build` (includes Sphinx build)
   - Output Directory: `.next` (Next.js default)
   - Install Command: `npm ci`
   - Node.js Version: 18.x (or 20.x)

   **Important: Build timeout considerations**
   - Free tier: 45 minute build timeout
   - Hobby tier: 45 minute timeout
   - Sphinx builds are typically fast (< 5 minutes) but complex docs may take longer
   - Vercel caches dependencies and build artifacts between deploys
   - First build may be slower; subsequent builds are faster

3. **Configure environment variables in Vercel:**
   Add any needed environment variables:
   - `NEXT_PUBLIC_SENTRY_DSN` (if using Sentry)
   - Apply to Production, Preview, and Development environments

4. **Deploy your site:**
   - Click "Deploy"
   - Vercel provides a preview URL (yourproject.vercel.app)
   - Watch build logs for any Sphinx or Python issues

## 5. Custom Domain Setup

1. **Add domain in Vercel:**
   - Go to project settings in Vercel dashboard
   - Navigate to "Domains" section
   - Click "Add" and enter your domain (cleanroomlabs.dev)

2. **Update DNS in Porkbun:**
   - Option 1: Use Vercel nameservers
     - Copy nameservers from Vercel
     - Update nameservers in Porkbun domain settings
   
   - Option 2: Keep Porkbun DNS and add records
     - Add A record: @ → 76.76.21.21
     - Add CNAME record: www → cname.vercel-dns.com

3. **Verify domain:**
   - Vercel will verify your domain settings
   - SSL certificate is automatically issued
   - Custom domain becomes active (may take up to 48 hours for DNS propagation)

## 6. Continuous Integration

Vercel automatically builds and deploys on every push to your repository and creates preview deployments for pull requests.

**Add quality checks with GitHub Actions:**

Create `.github/workflows/quality-checks.yml`:

```yaml
name: Quality Checks
on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

jobs:
  test-build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository with submodules
        uses: actions/checkout@v4
        with:
          submodules: recursive  # Initialize all nested submodules
          fetch-depth: 0         # Full history for proper submodule resolution

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
          cache-dependency-path: 'cleanroom-technical-docs/requirements.txt'

      - name: Install system dependencies
        run: sudo apt-get update && sudo apt-get install -y graphviz

      - name: Install Python dependencies
        run: |
          cd ../cleanroom-technical-docs
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt

      - name: Install npm dependencies
        run: npm ci  # Faster than npm install in CI

      - name: Lint code
        run: npm run lint

      - name: Build Next.js site (includes Sphinx build)
        run: npm run build

      - name: Verify build artifacts
        run: |
          test -d .next || (echo "Next.js build failed" && exit 1)
          test -f public/docs/index.html || (echo "Sphinx docs missing" && exit 1)
          echo "✓ Build artifacts verified"

      - name: Check bundle size
        run: |
          npx next build --profile
          # Add bundle size checks here if desired
```

**Key improvements:**
- ✓ Recursive submodule checkout with full history
- ✓ Removed duplicate Sphinx build (npm run build includes it)
- ✓ Uses `npm ci` for faster, reproducible installs
- ✓ Verifies artifacts exist instead of just listing
- ✓ Updated to latest action versions
- ✓ Python venv activation in CI

## 7. Analytics Integration

1. **Add Vercel Analytics:**
   ```bash
   npm install @vercel/analytics
   ```

2. **Add to `_app.js`:**
   ```javascript
   import { Analytics } from '@vercel/analytics/react';

   function MyApp({ Component, pageProps }) {
     return (
       <>
         <Component {...pageProps} />
         <Analytics />
       </>
     );
   }
   ```

## 8. Error Monitoring with Sentry

1. **Create free Sentry account:**
   - Sign up at sentry.io
   - Create a new Next.js project
   - Copy your DSN (Data Source Name)

2. **Install Sentry:**
   ```bash
   npm install @sentry/nextjs
   npx @sentry/wizard@latest -i nextjs
   ```

3. **Add DSN to Vercel:**
   - Go to Vercel project settings
   - Navigate to Environment Variables
   - Add: `NEXT_PUBLIC_SENTRY_DSN=your-dsn-here`
   - Apply to Production, Preview, and Development

4. **Configure error tracking:**
   The wizard creates `sentry.client.config.js` and `sentry.server.config.js`.

   Update to include additional context:
   ```javascript
   import * as Sentry from '@sentry/nextjs';

   Sentry.init({
     dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
     tracesSampleRate: 0.1,  // 10% of transactions
     debug: false,
     environment: process.env.VERCEL_ENV || 'development',
   });
   ```

This provides real-time error alerts and helps diagnose production issues.

**Rollback Plan:** If critical issues are found after launch, go to Vercel dashboard → find last working deployment → click "..." → "Promote to Production".

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues and solutions.

---

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Sentry Next.js Integration](https://docs.sentry.io/platforms/javascript/guides/nextjs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

---

## Related Documentation

- [maintenance-plan.md](maintenance-plan.md) - Post-launch improvements (testing, TypeScript, staging)
- [README.md](README.md) - Getting started and current build commands
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Design decisions and rationale
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) - GitHub Actions workflows
- [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) - Production deployment steps
- [docs/SUBMODULES_GUIDE.md](docs/SUBMODULES_GUIDE.md) - Submodule operations