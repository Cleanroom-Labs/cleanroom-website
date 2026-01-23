# Website Migration Plan: Articulation to Next.js with Vercel

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
   npm install fs-extra
   ```

4. **Set up Python environment for Sphinx (required):**
   ```bash
   # Navigate to technical-docs directory
   cd ../technical-docs
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt

   # Install system dependencies (required for needflow diagrams)
   # macOS: brew install graphviz
   # Ubuntu/Debian: sudo apt-get install graphviz
   # Windows: Download from graphviz.org
   cd ../cleanroom-website
   ```

3. **Set up basic project structure:**
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
   │   ├── docs/          # Where Sphinx output will go
   │   └── ...
   ├── styles/            # Custom CSS
   └── scripts/           # Build/automation scripts
   ```

## 2. Sphinx Documentation Integration

1. **Create a build script (`scripts/build-docs.js`):**
   ```javascript
   const { execSync } = require('child_process');
   const fs = require('fs-extra');
   const path = require('path');

   // Path to your technical-docs directory (CORRECTED PATH)
   const SPHINX_DIR = '../technical-docs';
   const VENV_PYTHON = path.join(SPHINX_DIR, '.venv/bin/python');
   const TARGET_DIR = './public/docs';

   try {
     // Verify Sphinx directory exists
     if (!fs.existsSync(SPHINX_DIR)) {
       throw new Error(`Sphinx directory not found: ${SPHINX_DIR}`);
     }

     // Build Sphinx docs (using venv python if available)
     console.log('Building Sphinx docs...');
     const sphinxCmd = fs.existsSync(VENV_PYTHON)
       ? `${VENV_PYTHON} -m sphinx -M html source build`
       : 'make html';

     execSync(sphinxCmd, {
       cwd: SPHINX_DIR,
       stdio: 'inherit'
     });

     // Copy built files to public/docs
     console.log('Copying docs to public folder...');
     fs.ensureDirSync(TARGET_DIR);
     fs.copySync(
       path.join(SPHINX_DIR, 'build/html'),
       TARGET_DIR,
       { overwrite: true }
     );

     console.log('✓ Documentation integrated successfully!');
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

     // Serve Sphinx HTML directly without redirects
     async rewrites() {
       return [
         {
           source: '/docs',
           destination: '/docs/index.html',
         },
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
           ],
         },
       ];
     },
   };

   module.exports = nextConfig;
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
           <Link href="/docs/index.html">
             <a className="btn-primary">Browse Documentation →</a>
           </Link>
         </div>
       </Layout>
     );
   }
   ```

3. **Add npm script to package.json:**
   ```json
   "scripts": {
     "build-docs": "node scripts/build-docs.js",
     "build": "npm run build-docs && next build",
     "dev": "npm run build-docs && next dev"
   }
   ```

## 3. Styling & Customization

1. **Create theme similar to dreamsofcode.io:**
   - Dark mode with clean typography
   - Code highlighting with Prism.js
   - Custom styling for docs section to match your branding

2. **Modify Sphinx theme as needed:**
   - Create custom CSS to override Sphinx styles for better integration
   - Customize `_static/custom.css` in Sphinx to match website theme

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
   - Install Command: `npm install`
   - Environment Variables: Add any needed

5. **Deploy your site:**
   - Click "Deploy"
   - Vercel provides a preview URL (yourproject.vercel.app)

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
      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          submodules: true  # Pull technical-docs submodule

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install system dependencies
        run: sudo apt-get update && sudo apt-get install -y graphviz

      - name: Install Python dependencies
        working-directory: ./technical-docs
        run: pip install -r requirements.txt

      - name: Install npm dependencies
        run: npm install

      - name: Lint code
        run: npm run lint

      - name: Build Sphinx documentation
        working-directory: ./technical-docs
        run: make html

      - name: Build Next.js site
        run: npm run build

      - name: Check for build artifacts
        run: |
          ls -la .next
          ls -la public/docs
```

This workflow:
- ✓ Verifies Sphinx docs build successfully
- ✓ Verifies Next.js site builds without errors
- ✓ Runs on every PR and push to main
- ✓ Blocks merging if builds fail

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

## Summary: Key Improvements in This Plan

This migration plan has been enhanced with several critical improvements:

### Critical Fixes
1. ✓ Correct Sphinx directory path (`technical-docs` not `sphinx-docs`)
2. ✓ Python environment setup with venv
3. ✓ Install fs-extra dependency
4. ✓ Better docs integration (rewrites, not redirects)
5. ✓ Error handling in build script
6. ✓ Venv activation in build process

### Testing & CI/CD
7. ✓ Enhanced GitHub Actions workflow
8. ✓ Test both Sphinx and Next.js builds
9. ✓ Submodule support in CI
10. ✓ Blocks deployment on build failures

### Deployment Strategy
11. ✓ Pre-launch checklist
12. ✓ Post-launch verification steps
13. ✓ Rollback procedure
14. ✓ Staging environment documentation

### Monitoring & Security
15. ✓ Sentry error tracking setup
16. ✓ Security headers configuration
17. ✓ Analytics and monitoring dashboard

### Architecture Improvements
- Uses Next.js rewrites instead of client-side redirects (better SEO, no flash)
- Proper error handling with exit codes for CI/CD
- Virtual environment isolation for Python dependencies
- Security headers for production deployment

### Future Enhancements (Optional)
- Sphinx search integration (can be added later if needed)
- Advanced performance optimizations (can optimize post-launch)
- Automated content migration tools (manual migration acceptable for hybrid approach)

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
1. **Convert Sphinx to MDX:** Would lose Sphinx's powerful features
2. **Separate docs subdomain:** More complex DNS setup, less integrated feel
3. **Full client-side rendering:** Worse SEO, slower initial page load
4. **Other hosting (Netlify, AWS):** Vercel has better Next.js integration

---

## Quick Start Checklist

Use this checklist to track your migration progress:

- [ ] 1. Initialize Next.js project
- [ ] 2. Install all dependencies (Node + Python)
- [ ] 3. Set up Python virtual environment for Sphinx
- [ ] 4. Create build script with error handling
- [ ] 5. Configure Next.js rewrites and security headers
- [ ] 6. Implement core pages and navigation
- [ ] 7. Test Sphinx documentation integration locally
- [ ] 8. Set up GitHub Actions workflow
- [ ] 9. Create Vercel account and connect repo
- [ ] 10. Configure custom domain in Vercel
- [ ] 11. Update DNS records in Porkbun
- [ ] 12. Set up Sentry error monitoring
- [ ] 13. Add Vercel Analytics
- [ ] 14. Run pre-launch checklist
- [ ] 15. Deploy to production
- [ ] 16. Verify post-launch checklist
- [ ] 17. Monitor for errors and performance

---

## Troubleshooting

### Common Issues and Solutions

**Issue: Sphinx build fails with "No module named 'sphinx'"**
- Solution: Activate the virtual environment first: `source ../technical-docs/.venv/bin/activate`

**Issue: needflow diagrams not rendering**
- Solution: Install Graphviz system package (see step 4 in Project Setup)

**Issue: Documentation not loading on localhost**
- Solution: Run `npm run build-docs` first, then `npm run dev`

**Issue: GitHub Actions failing on Sphinx build**
- Solution: Check the workflow includes Python setup and Graphviz installation

**Issue: 404 errors on /docs paths in production**
- Solution: Verify `next.config.js` includes the rewrites configuration

**Issue: Vercel build timing out**
- Solution: Sphinx builds are cached; first build may be slow but subsequent builds faster

**Issue: Custom domain SSL not working**
- Solution: Wait up to 48 hours for DNS propagation; verify A and CNAME records are correct

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
1. Make changes in technical-docs repository
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