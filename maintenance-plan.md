# Website Maintenance Plan

Post-migration improvements and ongoing maintenance tasks. This plan covers optional enhancements to implement after the core website migration is complete.

## Maintenance Progress

### Phase 1: Testing Infrastructure ❌ Not Started
- [ ] Set up Jest unit testing
- [ ] Set up Playwright E2E testing
- [ ] Add Lighthouse CI to GitHub Actions

### Phase 2: Developer Experience ❌ Not Started
- [ ] Migrate to TypeScript
- [ ] Configure tsconfig.json
- [ ] Convert components to .tsx

### Phase 3: Staging Environment ❌ Not Started
- [ ] Create staging branch
- [ ] Configure staging.cleanroomlabs.dev subdomain
- [ ] Set up staging deployment in Vercel

### Phase 4: Build Optimizations ❌ Not Started
- [ ] Implement Sphinx build caching
- [ ] Add commit hash tracking for cache invalidation

---

## 1. Staging Environment

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

## 2. Testing Strategy

While not strictly required for launch, testing improves reliability.

### Manual Testing Checklist
- [ ] Verify mobile responsive design (320px, 768px, 1024px viewports)
- [ ] Test on Chrome, Firefox, Safari

### Unit Testing
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

### E2E Testing
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

### Lighthouse CI
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

## 3. TypeScript Migration

While the migration uses JavaScript, TypeScript is recommended for larger projects:

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

## 4. Advanced Optimizations

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

## Pre-Launch Testing Checklist

Before going live, complete these verification steps:

### Browser & Device Testing
- [ ] Test on Chrome, Firefox, Safari
- [ ] Test on mobile devices (iOS and Android)
- [ ] Verify mobile responsive design (320px, 768px, 1024px viewports)

### Functionality Testing
- [ ] Verify all internal links work
- [ ] Verify Sphinx docs navigation works
- [ ] Check for console errors
- [ ] Test documentation search (if implemented)

### Performance Testing
- [ ] Run Lighthouse audit (aim for >90 on all metrics)

### Monitoring Verification
- [ ] Sentry alerts configured for team notifications
- [ ] Analytics dashboard bookmarked for easy access

---

## Regular Maintenance Tasks

- Monitor Sentry for errors weekly
- Review Vercel Analytics monthly
- Update dependencies quarterly (`npm audit`, `pip list --outdated`)
- Test documentation builds after Sphinx updates
- Verify SSL certificate renewal (automatic with Vercel)

## Updating Documentation

1. Make changes in cleanroom-technical-docs repository
2. Commit and push changes
3. Website will automatically rebuild and redeploy
4. Verify changes on preview deployment before merging to main

## Adding New Features

1. Create feature branch
2. Develop and test locally
3. Push and create pull request
4. Review preview deployment
5. Merge to staging (if using staging branch)
6. Final testing on staging
7. Merge to main for production deployment

---

## Related Documentation

- [deployment-plan.md](deployment-plan.md) - Deployment checklist
- [README.md](README.md) - Getting started and current build commands
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Design decisions and rationale
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and solutions
