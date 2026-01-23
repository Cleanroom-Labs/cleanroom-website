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

   // Path to your sphinx-docs directory
   const SPHINX_DIR = '../sphinx-docs';
   // Target directory in Next.js public folder
   const TARGET_DIR = './public/docs';

   // Build Sphinx docs
   console.log('Building Sphinx docs...');
   execSync('make html', { cwd: SPHINX_DIR });

   // Copy built files to public/docs
   console.log('Copying docs to public folder...');
   fs.ensureDirSync(TARGET_DIR);
   fs.copySync(
     path.join(SPHINX_DIR, 'build/html'),
     TARGET_DIR
   );

   console.log('Documentation integrated successfully!');
   ```

2. **Add custom layout wrapper for docs (`pages/docs/[[...path]].js`):**
   ```javascript
   import { useRouter } from 'next/router';
   import { useEffect } from 'react';
   import Layout from '../../components/Layout';
   import DocsSidebar from '../../components/DocsSidebar';

   // This is a special page that will serve the static Sphinx docs
   export default function DocsPage() {
     const router = useRouter();
     const { path = [] } = router.query;
     
     useEffect(() => {
       // Redirect to the actual Sphinx docs HTML
       if (path.length === 0) {
         window.location.href = '/docs/index.html';
       } else {
         window.location.href = `/docs/${path.join('/')}.html`;
       }
     }, [path]);
     
     return (
       <Layout>
         <div className="docs-container">
           <DocsSidebar />
           <div className="docs-content">
             <p>Loading documentation...</p>
           </div>
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

Vercel automatically:
- Builds and deploys on every push to your repository
- Creates preview deployments for pull requests
- Handles rollbacks and deployment history

You can enhance this with:
```yaml
# .github/workflows/quality-checks.yml
name: Quality Checks
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
      - run: npm run lint
```

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