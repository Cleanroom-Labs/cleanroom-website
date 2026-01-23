# Website Migration Plan: Articulation to Next.js with Vercel

## Repository Structure

This plan uses a **git submodule architecture** where the technical documentation is embedded within the website repository:

```
cleanroom-website/
├── cleanroom-technical-docs/   # Git submodule → Sphinx documentation
│   ├── airgap-whisper-docs/    # Git submodule → Project docs
│   ├── airgap-deploy-docs/     # Git submodule → Project docs
│   ├── airgap-transfer-docs/   # Git submodule → Project docs
│   ├── source/                 # Master documentation source
│   └── build/                  # Generated documentation
├── scripts/
│   └── build-docs.mjs          # Sphinx build integration
├── public/
│   └── docs/                   # Copied Sphinx output (gitignored)
└── ... (Next.js files)
```

The build script copies documentation from the submodule's build output to `public/docs/`.

**Benefits of submodule approach:**
- Single repository to clone for development
- Documentation versions tied to website versions via git SHAs
- Simplified CI/CD (no coordination between repos needed)
- Independent documentation development workflow

## Quick Reference

**Essential Commands:**
```bash
# Initial setup
npm run build-docs        # Build Sphinx documentation
npm run dev              # Start dev server (fast, uses cached docs)
npm run dev:clean        # Rebuild docs + start dev server
npm run build            # Production build (rebuilds docs)

# Deployment
git push                 # Triggers automatic Vercel deployment
```

**Key Files:**
- `scripts/build-docs.mjs` - Sphinx build integration
- `next.config.js` - Next.js configuration with security headers
- `public/docs/` - Generated Sphinx output (gitignored)
- `.gitignore` - Excludes node_modules, .next, public/docs, etc.

**Troubleshooting:**
- Docs not loading? Run `npm run build-docs` first
- Sphinx build fails? Check Python venv and Graphviz installation
- See full troubleshooting guide below

## Migration Progress

### Phase 1: Documentation Infrastructure ✅ Complete
- [x] Sphinx documentation setup with nested submodules
- [x] Build script (`scripts/build-docs.mjs`) with cross-platform support
- [x] Python venv integration
- [x] GitHub Actions CI/CD (`build-all-docs.yml`, `verify-submodules.yml`)
- [x] Output to `public/docs/` (gitignored)

### Phase 2: Next.js Integration ❌ Not Started
- [ ] Initialize Next.js project (Section 1)
- [ ] Install dependencies - Tailwind, fs-extra (Section 1)
- [ ] Configure `next.config.js` with security headers (Section 2)
- [ ] Add npm scripts to `package.json` (Section 2)

### Phase 3: Web UI ❌ Not Started
- [ ] Create Layout component with SEO meta tags (Section 3)
- [ ] Create docs landing page (Section 2)
- [ ] Implement navigation

### Phase 4: Deployment ❌ Not Started
- [ ] Set up Vercel account and connect repo (Section 4)
- [ ] Configure build settings (Section 4)
- [ ] Set up custom domain - cleanroomlabs.dev (Section 5)

### Phase 5: Monitoring ❌ Not Started
- [ ] Add Vercel Analytics (Section 7)
- [ ] Set up Sentry error monitoring (Section 8)

## 1. Project Setup & Development

1. **Initialize Next.js project:**
   ```bash
   npx create-next-app@latest cleanroom-website
   cd cleanroom-website
   ```

2. **Add dependencies for styling:**
   ```bash
   npm install tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

3. **Add additional dependencies:**
   ```bash
   npm install --save-dev fs-extra
   ```

4. **Set up Python environment for Sphinx (required):**

   **Minimum version: Python 3.9+** (Python 3.11+ recommended)

   ```bash
   # Navigate to cleanroom-technical-docs directory
   cd ../cleanroom-technical-docs
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt

   # Install system dependencies (required for needflow diagrams)
   # macOS: brew install graphviz
   # Ubuntu/Debian: sudo apt-get install graphviz
   # Windows: Download from graphviz.org and add to PATH
   cd ../cleanroom-website
   ```

5. **Set up basic project structure:**
   ```
   cleanroom-website/
   ├── components/        # Reusable UI components
   │   ├── Layout.js      # Main layout with nav/footer
   │   ├── DocsSidebar.js # Navigation for docs section
   │   └── ...
   ├── pages/             # Route pages
   │   ├── index.js       # Home page
   │   ├── about.js       # About page
   │   ├── blog/          # Blog posts
   │   └── docs/          # Special docs integration area
   ├── public/            # Static assets
   │   ├── docs/          # Where Sphinx output will go (generated, gitignored)
   │   └── ...
   ├── styles/            # Custom CSS
   ├── scripts/           # Build/automation scripts
   ├── .gitignore         # Git ignore file
   └── package.json       # Node dependencies
   ```

6. **Configure Node.js version in package.json:**
   Add this to your `package.json`:
   ```json
   "engines": {
     "node": ">=18.0.0",
     "npm": ">=9.0.0"
   }
   ```

7. **Set up .gitignore:**
   Create/update `.gitignore` in your Next.js project:
   ```gitignore
   # Dependencies
   node_modules/

   # Next.js
   .next/
   out/

   # Generated Sphinx docs (rebuilds on deploy)
   public/docs/

   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   .venv/
   venv/

   # Build artifacts
   build/
   dist/

   # Environment variables
   .env*.local

   # Debug
   npm-debug.log*
   yarn-debug.log*
   yarn-error.log*

   # OS
   .DS_Store
   Thumbs.db
   ```

## 2. Sphinx Documentation Integration

1. **Build script (`scripts/build-docs.mjs`):**

   > **✅ Implemented:** This script already exists. See `scripts/build-docs.mjs` for the full implementation.

   The existing script handles:
   - Submodule verification
   - Python 3 version check
   - Virtual environment setup (creates `.venv` if missing)
   - Dependency installation from `requirements.txt`
   - Sphinx build execution
   - Cross-platform support (Windows/macOS/Linux)
   - Colorful console output with status indicators
   - Output copying to `public/docs/`

2. **Configure Next.js to serve Sphinx docs (`next.config.js`):**
   ```javascript
   /** @type {import('next').NextConfig} */
   const nextConfig = {
     reactStrictMode: true,

     // Next.js automatically serves static files from public/docs/

     // Security headers
     async headers() {
       return [
         {
           source: '/:path*',
           headers: [
             { key: 'X-Frame-Options', value: 'DENY' },
             { key: 'X-Content-Type-Options', value: 'nosniff' },
             { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
             {
               key: 'Content-Security-Policy',
               value: [
                 "default-src 'self'",
                 "script-src 'self' 'unsafe-inline' 'unsafe-eval'", // Sphinx search needs eval
                 "style-src 'self' 'unsafe-inline'", // Sphinx styles need inline
                 "img-src 'self' data: https:",
                 "font-src 'self' data:",
                 "connect-src 'self'",
               ].join('; '),
             },
           ],
         },
       ];
     },
   };

   module.exports = nextConfig;
   ```

### CSS Integration Strategy

**Approach:** Keep Sphinx and Next.js styling separate (no conflicts)
- Sphinx generates its own CSS in `public/docs/_static/`
- Next.js/Tailwind CSS only affects your React components
- Both systems coexist without interference

**For unified branding:**
1. Define CSS variables for shared colors/fonts
2. Customize Sphinx theme via `cleanroom-technical-docs/source/_static/custom.css`
3. Reference same color values in both stylesheets

**Example custom.css:**
```css
:root {
  --brand-primary: #3b82f6;
  --brand-dark: #1e293b;
}

.wy-nav-top {
  background-color: var(--brand-primary);
}
```

3. **Create a docs landing page component (`pages/docs.js`):**
   ```javascript
   import Layout from '../components/Layout';
   import Link from 'next/link';

   export default function DocsIndex() {
     return (
       <Layout>
         <div className="docs-container">
           <h1>Documentation</h1>
           <p>View the complete technical documentation:</p>
           <Link href="/docs/index.html" className="btn-primary">
             Browse Documentation →
           </Link>
         </div>
       </Layout>
     );
   }
   ```

   **Note:** Next.js 13+ no longer requires wrapping `<Link>` around `<a>` tags. Apply className directly to Link.

4. **Add npm scripts to package.json:**
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

   **Development workflow:**
   - `npm run dev` - Fast startup, uses existing built docs (run `build-docs` manually when docs change)
   - `npm run dev:clean` - Rebuilds docs first, slower but ensures latest docs
   - `npm run build` - Production build (always rebuilds docs)

   **Note:** This significantly improves dev startup time. Only rebuild docs when they actually change.

5. **Sphinx Search Integration:**

   Sphinx generates its own search functionality (`searchindex.js`) which will work automatically:
   - Search box appears in Sphinx-generated pages
   - Requires JavaScript enabled (allowed by CSP above)
   - Search is client-side, no backend needed
   - Works with Sphinx themes that include search (most do)

   If you want to integrate Sphinx search into your main Next.js site:
   ```javascript
   // Optional: Fetch Sphinx search index in your Next.js pages
   // public/docs/searchindex.js contains the search data
   // Can be parsed and integrated into a unified search experience
   ```

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

---

## Appendix: Technical Decisions

### Why Next.js?
- Server-side rendering for better SEO
- Built-in routing and API routes
- Excellent developer experience
- Strong ecosystem and community

### Why Vercel?
- Seamless Next.js integration (by the same company)
- Automatic deployments and preview URLs
- Built-in CDN and edge functions
- Generous free tier
- Simple custom domain setup with automatic SSL

### Why Keep Sphinx Separate?
- Sphinx is purpose-built for technical documentation
- Rich ecosystem of extensions (autodoc, napoleon, needflow, etc.)
- Proven for large documentation projects
- Better than converting everything to MDX
- Separation of concerns: docs vs marketing site

### Alternative Approaches Considered
1. **Convert Sphinx to MDX:** Would lose Sphinx's powerful features (autodoc, needflow, etc.)
2. **Separate docs subdomain:** More complex DNS setup, less integrated user experience
3. **Full client-side rendering:** Worse SEO, slower initial page load
4. **Other hosting (Netlify, AWS):** Vercel has better Next.js integration and simpler setup
5. **TypeScript from start:** Adds initial complexity; can migrate incrementally later

### Technology Choices
- **Next.js 13+:** Modern features, excellent DX, strong ecosystem
- **Vercel:** Seamless Next.js integration, free tier, automatic deployments
- **Sphinx:** Industry-standard for technical docs, rich extension ecosystem
- **ES Modules:** Modern JavaScript, better tree-shaking, standardized
- **Tailwind CSS:** Utility-first, fast development, small bundle size

### Repository Structure Decision

**Chosen Approach: Git Submodules** ✅

```
cleanroom-website/
└── cleanroom-technical-docs/  # Git submodule
    ├── airgap-whisper-docs/   # Nested submodule
    ├── airgap-deploy-docs/    # Nested submodule
    └── airgap-transfer-docs/  # Nested submodule
```

**Why submodules:**
- Documentation version tied to website version via git SHAs
- Single repository to clone for development
- Simplified CI/CD (no coordination between repos)
- Independent documentation development workflow
- Version coupling for reproducible deployments

**Setup:**
```bash
# Clone with all submodules
git clone --recurse-submodules <repo-url>

# Or initialize submodules after clone
git submodule update --init --recursive

# Update submodules to latest
git submodule update --remote --recursive
```

**Alternative Approaches Considered:**

**Sibling Directories:**
```
Projects/
├── cleanroom-website/
└── cleanroom-technical-docs/
```
- ❌ Rejected: Requires coordinating separate repositories
- ❌ Documentation version not tied to website version
- Build script would use `../../cleanroom-technical-docs`

**Monorepo:**
- ❌ Rejected: Overkill for current scope
- Would require tools like Turborepo or Nx
- More complex setup, better for larger teams

---

## Quick Start Checklist

### Phase 1: Project Setup (5-10 min)
- [ ] Clone repository with submodules: `git clone --recurse-submodules <repo-url>`
- [ ] Initialize Next.js project and install dependencies
- [ ] Configure Node.js version (18+) in package.json
- [ ] Set up .gitignore with comprehensive exclusions
- [ ] Set up Python venv in cleanroom-technical-docs submodule
- [ ] Install Graphviz system dependency

### Phase 2: Build Integration (10-15 min)
- [ ] Create build-docs.mjs script with cross-platform support
- [ ] Configure next.config.js with security headers
- [ ] Update package.json scripts (dev, dev:clean, build)
- [ ] Test builds: `npm run build-docs && npm run dev`

### Phase 3: Core Pages (1-2 hours)
- [ ] Implement Layout component with SEO meta tags
- [ ] Create home page, docs landing page, navigation
- [ ] Verify mobile responsive design
- [ ] Test on Chrome, Firefox, Safari

### Phase 4: SEO & Performance (30 min)
- [ ] Configure robots.txt and sitemap (next-sitemap)
- [ ] Add Open Graph meta tags
- [ ] Run Lighthouse audit (aim for >90)

### Phase 5: CI/CD (20 min)
- [ ] Set up GitHub Actions workflow
- [ ] Verify CI builds successfully with artifact checks

### Phase 6: Vercel Deployment (15 min)
- [ ] Create Vercel account and connect GitHub repo
- [ ] Configure build settings and environment variables
- [ ] Verify preview deployment works

### Phase 7: Domain Setup (10 min + DNS propagation)
- [ ] Configure custom domain in Vercel
- [ ] Update DNS records in Porkbun (A and CNAME)
- [ ] Wait for SSL certificate (automatic)

### Phase 8: Monitoring & Launch
- [ ] Set up Sentry error monitoring and Vercel Analytics
- [ ] Complete pre-launch checklist (Section 9)
- [ ] Deploy to production and verify all systems
- [ ] Monitor for errors and performance issues

---

## Troubleshooting

### Common Issues and Solutions

**Issue: "Cannot use import statement outside a module" error**
- Solution: Ensure build script is named `build-docs.mjs` (not `.js`)
- Or add `"type": "module"` to package.json if using .js extension

**Issue: Sphinx build fails with "No module named 'sphinx'"**
- Solution: Verify Python venv exists and has dependencies installed:
  ```bash
  cd ../cleanroom-technical-docs
  python3 -m venv .venv
  source .venv/bin/activate  # Windows: .venv\Scripts\activate
  pip install -r requirements.txt
  ```

**Issue: needflow diagrams not rendering**
- Solution: Install Graphviz system package (see step 4 in Project Setup)
- Verify installation: `dot -V` should show version number

**Issue: Documentation not loading on localhost**
- Solution: Build docs first, then start dev server:
  ```bash
  npm run build-docs
  npm run dev
  ```

**Issue: "Sphinx directory not found" error**
- Solution: Verify submodules are initialized: `git submodule update --init --recursive`
- Check that cleanroom-technical-docs exists as a submodule
- Verify paths in build script: `../cleanroom-technical-docs` (not `../../`)

**Issue: GitHub Actions failing on Sphinx build**
- Solution: Verify workflow includes:
  1. Checkout with `submodules: recursive`
  2. Python setup with correct version
  3. Graphviz installation
  4. Python venv creation and activation
  5. Submodule verification step

**Issue: 404 errors on /docs paths in production**
- Solution: Verify next.config.js includes rewrites configuration
- Check public/docs/ contains index.html after build
- Inspect Vercel build logs for Sphinx errors

**Issue: Vercel build timing out**
- Solution: Sphinx builds are usually fast, but check:
  1. Complex Sphinx extensions may slow builds
  2. Large number of pages increases build time
  3. Vercel caches between builds (first build slowest)
  4. Consider simplifying Sphinx configuration if chronic

**Issue: Custom domain SSL not working**
- Solution: Wait up to 48 hours for DNS propagation
- Verify A record: @ → 76.76.21.21
- Verify CNAME: www → cname.vercel-dns.com
- Check domain status in Vercel dashboard

**Issue: CSP blocking Sphinx functionality**
- Solution: Sphinx search requires 'unsafe-eval' in script-src
- Sphinx styles require 'unsafe-inline' in style-src
- These are included in the recommended CSP configuration

**Issue: Dev server doesn't show updated docs**
- Solution: Run `npm run build-docs` to rebuild
- Or use `npm run dev:clean` which rebuilds automatically
- Remember: `npm run dev` uses cached docs for speed

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