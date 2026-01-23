# Website Migration Plan: Articulation to Next.js with Vercel

## Important: Repository Structure

This plan assumes `cleanroom-technical-docs` is a **sibling directory** to `cleanroom-website`:
```
Projects/
├── cleanroom-website/          # Next.js website (this project)
└── cleanroom-technical-docs/   # Sphinx documentation (sibling directory)
```

**Alternative: Submodule approach** (if you prefer tighter integration):
- Add as submodule: `git submodule add <repo-url> docs-source`
- Update script paths accordingly to `./docs-source` instead of `../cleanroom-technical-docs`

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

1. **Create a build script (`scripts/build-docs.mjs`):**

   Note: Using `.mjs` extension for ES modules compatibility with modern Next.js.

   ```javascript
   import { execSync } from 'child_process';
   import fs from 'fs-extra';
   import path from 'path';
   import { fileURLToPath } from 'url';
   import { dirname } from 'path';

   const __filename = fileURLToPath(import.meta.url);
   const __dirname = dirname(__filename);

   // Path to your cleanroom-technical-docs directory
   const SPHINX_DIR = path.resolve(__dirname, '../../cleanroom-technical-docs');
   const SPHINX_SOURCE = path.join(SPHINX_DIR, 'source');
   const SPHINX_BUILD = path.join(SPHINX_DIR, 'build/html');
   const TARGET_DIR = path.resolve(__dirname, '../public/docs');

   // Platform-specific Python paths
   const isWindows = process.platform === 'win32';
   const VENV_PYTHON = isWindows
     ? path.join(SPHINX_DIR, '.venv/Scripts/python.exe')
     : path.join(SPHINX_DIR, '.venv/bin/python');

   try {
     // Verify Sphinx directory exists
     if (!fs.existsSync(SPHINX_DIR)) {
       throw new Error(`Sphinx directory not found: ${SPHINX_DIR}\nExpected sibling directory structure.`);
     }

     if (!fs.existsSync(SPHINX_SOURCE)) {
       throw new Error(`Sphinx source directory not found: ${SPHINX_SOURCE}`);
     }

     // Build Sphinx docs
     console.log('Building Sphinx documentation...');
     console.log(`Sphinx directory: ${SPHINX_DIR}`);

     let sphinxCmd;
     if (fs.existsSync(VENV_PYTHON)) {
       // Use venv Python (cross-platform)
       sphinxCmd = `"${VENV_PYTHON}" -m sphinx -M html source build`;
       console.log('Using virtual environment Python');
     } else {
       // Fallback to system Sphinx (requires sphinx-build in PATH)
       sphinxCmd = isWindows
         ? 'sphinx-build -M html source build'
         : 'make html';
       console.log('Using system Sphinx');
     }

     try {
       execSync(sphinxCmd, {
         cwd: SPHINX_DIR,
         stdio: 'inherit',
         shell: true
       });
     } catch (buildError) {
       throw new Error(`Sphinx build failed. Check that:\n` +
         `1. Python venv is set up: ${VENV_PYTHON}\n` +
         `2. Dependencies installed: pip install -r requirements.txt\n` +
         `3. Graphviz is installed (for needflow diagrams)\n` +
         `Original error: ${buildError.message}`);
     }

     // Verify build output exists
     if (!fs.existsSync(SPHINX_BUILD)) {
       throw new Error(`Sphinx build directory not found: ${SPHINX_BUILD}`);
     }

     // Copy built files to public/docs
     console.log('Copying documentation to public folder...');
     fs.ensureDirSync(TARGET_DIR);

     try {
       fs.copySync(SPHINX_BUILD, TARGET_DIR, { overwrite: true });
     } catch (copyError) {
       throw new Error(`Failed to copy docs to public folder: ${copyError.message}`);
     }

     // Verify critical files were copied
     const indexPath = path.join(TARGET_DIR, 'index.html');
     if (!fs.existsSync(indexPath)) {
       throw new Error(`Documentation index.html not found after copy: ${indexPath}`);
     }

     console.log('✓ Documentation integrated successfully!');
     console.log(`  Source: ${SPHINX_BUILD}`);
     console.log(`  Target: ${TARGET_DIR}`);
   } catch (error) {
     console.error('✗ Documentation build failed:', error.message);
     process.exit(1);
   }
   ```

2. **Configure Next.js to serve Sphinx docs (`next.config.js`):**
   ```javascript
   /** @type {import('next').NextConfig} */
   const nextConfig = {
     reactStrictMode: true,

     // Serve Sphinx HTML directly (Next.js auto-serves /docs/index.html for /docs)
     async rewrites() {
       return [
         {
           source: '/docs/:path*',
           destination: '/docs/:path*',
         },
       ];
     },

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

   **Note on CSS Integration:**
   - Sphinx generates its own CSS in `_static/` which will be served from `/docs/_static/`
   - Tailwind CSS in your Next.js app won't affect Sphinx docs (different namespaces)
   - If you want unified styling, customize Sphinx's CSS in `source/_static/custom.css`
   - Consider using CSS variables to share colors/fonts between both systems

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

## 3. Styling & Customization

1. **Create theme similar to dreamsofcode.io:**
   - Dark mode with clean typography
   - Code highlighting with Prism.js
   - Custom styling for docs section to match your branding

2. **Modify Sphinx theme as needed:**
   - Create custom CSS to override Sphinx styles for better integration
   - Customize `_static/custom.css` in Sphinx to match website theme

## 4. SEO & Performance Optimization

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

## 5. Vercel Deployment

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

7. **Optimize build caching (optional):**

   To speed up builds, consider caching Sphinx output if docs haven't changed:

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

## 6. Custom Domain Setup

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

## 7. Continuous Integration

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
      - name: Checkout repository
        uses: actions/checkout@v4
        # If using submodules, add: with: { submodules: true }

      - name: Checkout Sphinx docs (sibling directory)
        uses: actions/checkout@v4
        with:
          repository: your-org/cleanroom-technical-docs
          path: ../cleanroom-technical-docs
          # Or use submodules approach if preferred

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
          cache-dependency-path: '../cleanroom-technical-docs/requirements.txt'

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
- ✓ Fixed pip cache path for sibling directory structure
- ✓ Removed duplicate Sphinx build (npm run build includes it)
- ✓ Uses `npm ci` for faster, reproducible installs
- ✓ Verifies artifacts exist instead of just listing
- ✓ Updated to latest action versions
- ✓ Python venv activation in CI

## 8. Analytics Integration

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

## 9. Error Monitoring with Sentry

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

## 10. Pre-Launch Checklist

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

## 11. Staging Environment (Optional but Recommended)

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

## 12. Optional: Testing Strategy

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

## 13. Optional: TypeScript Migration

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

## Summary: Key Improvements in This Plan

This migration plan includes comprehensive improvements across all areas:

### Critical Fixes
1. ✓ Clarified repository structure (sibling directories vs submodules)
2. ✓ Fixed numbering error (duplicate step 3)
3. ✓ Converted build script to ES modules (.mjs)
4. ✓ Cross-platform Python path support (Windows/Mac/Linux)
5. ✓ Fixed Next.js Link syntax (removed deprecated `<a>` wrapper)
6. ✓ Improved error messages with specific troubleshooting steps
7. ✓ fs-extra as dev dependency (not production)

### Performance & Developer Experience
8. ✓ Optimized dev script (doesn't rebuild docs on every start)
9. ✓ Added dev:clean for forced rebuild
10. ✓ Removed redundant rewrites in next.config.js
11. ✓ Eliminated duplicate Sphinx build in CI workflow
12. ✓ Uses npm ci in CI for faster, reproducible installs

### Configuration & Setup
13. ✓ Comprehensive .gitignore template
14. ✓ Node.js version specification (engines field)
15. ✓ Python version requirements (3.9+ minimum)
16. ✓ Proper pip cache configuration for CI

### Security & SEO
17. ✓ Content-Security-Policy header with Sphinx compatibility
18. ✓ robots.txt configuration
19. ✓ Sitemap generation with next-sitemap
20. ✓ SEO meta tags and Open Graph integration
21. ✓ Security headers for production

### Documentation & Guidance
22. ✓ Sphinx search integration explained
23. ✓ CSS conflict resolution strategy
24. ✓ Vercel build timeout considerations
25. ✓ Build artifact verification in CI
26. ✓ TypeScript migration path (optional)
27. ✓ Performance optimization recommendations

### Architecture Improvements
- ES modules throughout for modern JavaScript
- Platform-specific handling (Windows/Unix)
- Detailed error context for debugging
- Proper Python virtual environment in CI
- Next.js 13+ best practices

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

---

## Quick Start Checklist

Use this checklist to track your migration progress:

### Initial Setup
- [ ] 1. Initialize Next.js project
- [ ] 2. Install all Node.js dependencies
- [ ] 3. Configure Node.js version in package.json (engines field)
- [ ] 4. Set up .gitignore with all necessary exclusions
- [ ] 5. Set up Python venv for Sphinx (in cleanroom-technical-docs)
- [ ] 6. Install Python dependencies in venv
- [ ] 7. Install Graphviz system dependency

### Build Configuration
- [ ] 8. Create build-docs.mjs script with cross-platform support
- [ ] 9. Configure next.config.js with rewrites and security headers
- [ ] 10. Update package.json scripts (dev, dev:clean, build, build-docs)
- [ ] 11. Test local Sphinx build: `npm run build-docs`
- [ ] 12. Test local Next.js dev: `npm run dev`

### Content & Pages
- [ ] 13. Implement Layout component with SEO meta tags
- [ ] 14. Create home page
- [ ] 15. Create docs landing page
- [ ] 16. Implement navigation and footer
- [ ] 17. Verify mobile responsive design

### SEO & Performance
- [ ] 18. Configure robots.txt
- [ ] 19. Set up sitemap generation (next-sitemap)
- [ ] 20. Add SEO meta tags and Open Graph
- [ ] 21. Optimize images with Next.js Image component

### CI/CD & Testing
- [ ] 22. Set up GitHub Actions workflow
- [ ] 23. Verify CI builds successfully
- [ ] 24. Test on multiple browsers
- [ ] 25. Run Lighthouse audit

### Deployment
- [ ] 26. Create Vercel account and connect repo
- [ ] 27. Configure Vercel build settings
- [ ] 28. Add environment variables (Sentry DSN, etc.)
- [ ] 29. Verify preview deployment works
- [ ] 30. Configure custom domain in Vercel
- [ ] 31. Update DNS records in Porkbun
- [ ] 32. Wait for SSL certificate issuance

### Monitoring
- [ ] 33. Set up Sentry error monitoring
- [ ] 34. Add Vercel Analytics
- [ ] 35. Configure alert notifications

### Launch
- [ ] 36. Complete pre-launch checklist (Section 10)
- [ ] 37. Deploy to production
- [ ] 38. Verify post-launch checklist (Section 10)
- [ ] 39. Monitor for errors and performance issues
- [ ] 40. Document rollback procedure for team

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
- Solution: Verify directory structure - cleanroom-technical-docs should be sibling to cleanroom-website
- Check paths in build script match your actual structure

**Issue: GitHub Actions failing on Sphinx build**
- Solution: Verify workflow includes:
  1. Python setup with correct version
  2. Graphviz installation
  3. Python venv creation and activation
  4. Correct pip cache path

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