# Repository Guidelines

## Project Structure & Module Organization
- `pages/` holds Next.js routes, including dynamic routes like `pages/blog/[slug].js`.
- `components/`, `lib/`, and `data/` contain reusable UI, helpers, and site data.
- `content/blog/` stores MDX posts; static assets live in `public/`; shared CSS is in `styles/`.
- `tests/unit/` contains Vitest component/lib tests; `tests/e2e/` contains Playwright specs.
- `technical-docs/` is a nested submodule tree for Sphinx docs; `common/` holds shared theme tokens and build scripts.
- `scripts/` includes automation for docs builds and PDF generation.

## Build, Test, and Development Commands
- `npm run dev`: start the local Next.js dev server.
- `npm run dev:clean`: rebuild docs, then start dev server.
- `npm run build`: build docs and then run a production web build.
- `npm run build:web`: build only the website.
- `npm run build-docs`: build Sphinx docs into `public/docs/...`.
- `npm run test -- --run`: run unit tests once.
- `npm run test:coverage`: run unit tests with coverage output.
- `npm run test:e2e -- --project=chromium`: run Playwright E2E tests.
- `pytest scripts/generate-pdf/tests/ -v -m "not integration"`: run Python PDF module tests.
- `./scripts/test-ci-locally.sh`: simulate CI checks locally.

## Coding Style & Naming Conventions
- JavaScript/React style follows existing files: 2-space indentation, single quotes, semicolons.
- Use `PascalCase` for React components and `camelCase` for helpers/data modules.
- Keep route filenames descriptive and consistent with Next.js patterns (`[slug].js` for dynamic routes).
- Prefer existing Tailwind patterns; shared design tokens should be updated in `common/tokens/`.
- Follow terminology in `docs/STYLE_GUIDE.md` ("air gap" noun, "air-gapped" adjective).
- `npm run lint` is currently a placeholder that exits with setup guidance.

## Testing Guidelines
- Unit tests use Vitest + Testing Library in `tests/unit/**/*.test.{js,jsx}`.
- E2E tests use Playwright in `tests/e2e/**/*.spec.js` (desktop and mobile profiles).
- Add or update tests when behavior changes in `components/` or `lib/`.
- Coverage is published in CI; no hard threshold is enforced, but avoid regressions in touched areas.

## Commit & Pull Request Guidelines
- Follow Conventional Commit prefixes used in history: `feat:`, `fix:`, `chore:`, `docs:`, `test:` (optional scope like `fix(ux): ...`).
- For submodule bumps, include the module and commit SHA in the message.
- PRs should include a summary, linked issue (if available), tests run, and screenshots for UI changes.
- Before opening a PR, run `git submodule status` and `grove check`.
- Optional: enable hooks with `git config core.hooksPath .githooks` to catch secrets and local paths.
