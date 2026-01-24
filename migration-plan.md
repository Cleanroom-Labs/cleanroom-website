# Website Migration Plan: Articulation to Next.js with Vercel

## Repository Structure

See [README.md](README.md) for the current repository structure and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design decisions.

## Migration Progress

### Phase 1: Project Setup ✅ Complete
- [x] Clone repository with submodules
- [x] Initialize Next.js project and install dependencies
- [x] Configure Node.js version (18+) in package.json
- [x] Set up .gitignore
- [x] Set up Python venv in cleanroom-technical-docs
- [x] Install Graphviz system dependency

### Phase 2: Build Integration ✅ Complete
- [x] Create build-docs.mjs script with cross-platform support
- [x] Configure next.config.js with security headers
- [x] Add npm scripts to package.json
- [x] Test builds: npm run build-docs && npm run dev

### Phase 3: Core Pages 🟡 In Progress
- [x] Create Layout component with basic SEO meta tags
- [x] Create docs landing page
- [x] Implement basic navigation
- [ ] Enhance SEO meta tags (Open Graph, Twitter cards)
- [ ] Verify mobile responsive design
- [ ] Test on Chrome, Firefox, Safari

### Phase 4: SEO & Performance ❌ Not Started
- [ ] Configure robots.txt and sitemap (Section 3)
- [ ] Run Lighthouse audit (aim for >90)

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
- [ ] Complete pre-launch checklist (Section 9)
- [ ] Deploy to production

## 1. Project Setup & Development ✅ Complete

> **Implemented.** See actual files for current configuration.

| File | Purpose |
|------|---------|
| `package.json` | Dependencies (Next.js, Tailwind, fs-extra) and npm scripts |
| `.gitignore` | Ignores `node_modules/`, `.next/`, `public/docs/`, `.venv/`, etc. |
| `next.config.js` | Security headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy) |

**Python environment:** The build script auto-creates `.venv` in `cleanroom-technical-docs/` if missing. Requires Python 3.9+ and Graphviz for diagrams.

## 2. Sphinx Documentation Integration ✅ Complete

> **Implemented.** See actual files for current configuration.

| File | Purpose |
|------|---------|
| `scripts/build-docs.mjs` | Build orchestrator - submodule verification, venv setup, Sphinx build, output copy |
| `next.config.js` | Serves static files from `public/docs/` automatically |
| `pages/docs.js` | Landing page linking to Sphinx docs |
| `components/Layout.js` | Shared layout with navigation |

### npm Scripts Reference

```json
"scripts": {
  "dev": "next dev",
  "dev:clean": "npm run build-docs && next dev",
  "build": "npm run build-docs && next build",
  "build-docs": "node scripts/build-docs.mjs",
  "start": "next start",
  "lint": "next lint"
}
```

- `npm run dev` - Fast startup, uses existing built docs
- `npm run dev:clean` - Rebuilds docs first
- `npm run build` - Production build (always rebuilds docs)

### CSS Integration Strategy

**Approach:** Keep Sphinx and Next.js styling separate (no conflicts)
- Sphinx generates its own CSS in `public/docs/_static/`
- Next.js/Tailwind CSS only affects React components
- Both systems coexist without interference

**For unified branding:**
1. Define CSS variables for shared colors/fonts
2. Customize Sphinx theme via `cleanroom-technical-docs/source/_static/custom.css`
3. Reference same color values in both stylesheets

### Sphinx Search

Sphinx generates client-side search (`searchindex.js`) that works automatically in the docs pages.

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

3. **Add SEO meta tags to Layout component:**
   ```javascript
   import Head from 'next/head';

   export default function Layout({ children, title, description }) {
     const defaultTitle = 'Cleanroom Labs - Software Engineering';
     const defaultDescription = 'Technical documentation and resources';

     return (
       <>
         <Head>
           <title>{title || defaultTitle}</title>
           <meta name="description" content={description || defaultDescription} />
           <meta property="og:title" content={title || defaultTitle} />
           <meta property="og:description" content={description || defaultDescription} />
           <meta property="og:type" content="website" />
           <meta name="twitter:card" content="summary_large_image" />
           <link rel="icon" href="/favicon.ico" />
         </Head>
         {children}
       </>
     );
   }
   ```

4. **Performance optimizations:**
   - Use Next.js `<Image>` component for optimized images
   - Enable font optimization in `next.config.js`
   - Consider static generation (SSG) for marketing pages
   - Use Incremental Static Regeneration (ISR) for blog posts

   ```javascript
   // Example: Static generation for home page
   export async function getStaticProps() {
     return {
       props: {},
       revalidate: 3600, // Rebuild every hour
     };
   }
   ```

## 4. Vercel Deployment

1. **Initialize Git repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub:**
   ```bash
   # Create a new GitHub repository through the web interface
   git remote add origin https://github.com/your-username/cleanroom-website.git
   git branch -M main
   git push -u origin main
   ```

3. **Connect to Vercel:**
   - Create a Vercel account at vercel.com (free tier)
   - Click "Add New..." and select "Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js settings

4. **Configure build settings:**
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

5. **Configure environment variables in Vercel:**
   Add any needed environment variables:
   - `NEXT_PUBLIC_SENTRY_DSN` (if using Sentry)
   - Apply to Production, Preview, and Development environments

6. **Deploy your site:**
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

## 9. Pre-Launch Checklist

**Before deploying to production:**

### Development Complete
- [ ] All core pages implemented
- [ ] Sphinx documentation building successfully
- [ ] Content migration completed (if applicable)
- [ ] Navigation working across all sections
- [ ] Mobile responsive design verified

### Testing Complete
- [ ] Test on Chrome, Firefox, Safari
- [ ] Test on mobile devices
- [ ] Verify all internal links work
- [ ] Verify Sphinx docs navigation works
- [ ] Check for console errors
- [ ] Run Lighthouse audit (aim for >90 on all metrics)

### Deployment Configuration
- [ ] Domain DNS configured in Porkbun
- [ ] Domain added in Vercel
- [ ] SSL certificate issued (automatic)
- [ ] Environment variables set (Sentry DSN, etc.)
- [ ] GitHub Actions passing

### Monitoring Setup
- [ ] Vercel Analytics enabled
- [ ] Sentry error tracking configured
- [ ] Sentry alerts configured for team
- [ ] Analytics dashboard bookmarked

### Post-Launch Verification
- [ ] Test custom domain (cleanroomlabs.dev)
- [ ] Test www redirect
- [ ] Verify HTTPS working
- [ ] Check Sentry for any errors
- [ ] Verify analytics tracking
- [ ] Test documentation search (if implemented)

### Rollback Plan
If critical issues are found:
1. Identify the last working deployment in Vercel dashboard
2. Click "..." menu → "Promote to Production"
3. Investigate issues in preview deployment
4. Redeploy when fixed

## 10. Staging Environment (Optional but Recommended)

**Use Vercel preview deployments:**

Every pull request automatically gets a preview URL like:
```
https://cleanroom-website-git-feature-branch-username.vercel.app
```

**For a dedicated staging environment:**

1. **Create staging branch:**
   ```bash
   git checkout -b staging
   git push -u origin staging
   ```

2. **Configure in Vercel:**
   - Vercel will auto-deploy the staging branch
   - Assign a custom domain: `staging.cleanroomlabs.dev`
   - Use staging for final testing before merging to main

3. **Workflow:**
   - Feature branches → Preview deployments (for development testing)
   - Merge to staging → Staging URL (for final QA)
   - Merge staging to main → Production deployment

---

## 11. Optional: Testing Strategy

While not strictly required for launch, testing improves reliability:

### Unit Testing (Optional)
```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
```

Create `jest.config.js`:
```javascript
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleDirectories: ['node_modules', '<rootDir>/'],
  testEnvironment: 'jest-environment-jsdom',
};

module.exports = createJestConfig(customJestConfig);
```

Example component test:
```javascript
import { render, screen } from '@testing-library/react';
import Layout from '../components/Layout';

test('renders layout with title', () => {
  render(<Layout title="Test">Content</Layout>);
  expect(screen.getByText('Content')).toBeInTheDocument();
});
```

### E2E Testing (Optional)
Consider Playwright for critical user flows:
```bash
npm install --save-dev @playwright/test
```

Example test:
```javascript
import { test, expect } from '@playwright/test';

test('docs navigation works', async ({ page }) => {
  await page.goto('/');
  await page.click('text=Documentation');
  await expect(page).toHaveURL('/docs');
});
```

### Lighthouse CI (Recommended)
Add to GitHub Actions for automated performance checks:
```yaml
- name: Run Lighthouse CI
  uses: treosh/lighthouse-ci-action@v9
  with:
    urls: |
      https://preview-url.vercel.app
      https://preview-url.vercel.app/docs
    uploadArtifacts: true
```

## 12. Optional: TypeScript Migration

While this plan uses JavaScript, TypeScript is recommended for larger projects:

1. **Initialize TypeScript:**
   ```bash
   npm install --save-dev typescript @types/react @types/node
   npx tsc --init
   ```

2. **Rename files:**
   - `.js` → `.tsx` (components)
   - `.js` → `.ts` (utilities)
   - Update imports

3. **Configure tsconfig.json:**
   ```json
   {
     "compilerOptions": {
       "target": "es5",
       "lib": ["dom", "dom.iterable", "esnext"],
       "allowJs": true,
       "skipLibCheck": true,
       "strict": true,
       "forceConsistentCasingInFileNames": true,
       "noEmit": true,
       "esModuleInterop": true,
       "module": "esnext",
       "moduleResolution": "node",
       "resolveJsonModule": true,
       "isolatedModules": true,
       "jsx": "preserve",
       "incremental": true
     },
     "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
     "exclude": ["node_modules"]
   }
   ```

4. **Benefits:**
   - Catch errors at build time
   - Better IDE autocomplete
   - Easier refactoring
   - Self-documenting code

---

## 13. Advanced Optimizations

**Note:** Implement these optimizations after basic deployment is working.

### Build Caching

To speed up builds, consider caching Sphinx output if docs haven't changed.

Update `scripts/build-docs.mjs` to check for changes:
```javascript
// Add at the top of try block
const lastCommitPath = path.join(__dirname, '../.sphinx-last-commit');
const currentCommit = execSync('git rev-parse HEAD', { encoding: 'utf8' }).trim();

if (fs.existsSync(lastCommitPath)) {
  const lastCommit = fs.readFileSync(lastCommitPath, 'utf8').trim();
  const docsChanged = execSync(
    `git diff --quiet ${lastCommit} HEAD -- ../cleanroom-technical-docs || echo changed`,
    { encoding: 'utf8' }
  ).trim();

  if (docsChanged !== 'changed' && fs.existsSync(TARGET_DIR)) {
    console.log('✓ Docs unchanged, using cached build');
    return;
  }
}

// ... existing build logic ...

// After successful build, save commit hash
fs.writeFileSync(lastCommitPath, currentCommit);
```

This skips Sphinx rebuild if technical docs haven't changed, significantly speeding up deployments.

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

## Maintenance and Updates

### Regular Maintenance Tasks
- Monitor Sentry for errors weekly
- Review Vercel Analytics monthly
- Update dependencies quarterly (`npm audit`, `pip list --outdated`)
- Test documentation builds after Sphinx updates
- Verify SSL certificate renewal (automatic with Vercel)

### Updating Documentation
1. Make changes in cleanroom-technical-docs repository
2. Commit and push changes
3. Website will automatically rebuild and redeploy
4. Verify changes on preview deployment before merging to main

### Adding New Features
1. Create feature branch
2. Develop and test locally
3. Push and create pull request
4. Review preview deployment
5. Merge to staging (if using staging branch)
6. Final testing on staging
7. Merge to main for production deployment

---

## Related Documentation

- [README.md](README.md) - Getting started and current build commands
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Design decisions and rationale
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) - GitHub Actions workflows
- [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) - Production deployment steps
- [docs/SUBMODULES_GUIDE.md](docs/SUBMODULES_GUIDE.md) - Submodule operations