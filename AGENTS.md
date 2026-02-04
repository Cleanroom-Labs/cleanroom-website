# Repository Guidelines

## Project Structure & Module Organization
- `pages/` contains Next.js routes and page-level logic.
- `components/` holds reusable UI components (React + Tailwind).
- `styles/` and `tailwind.config.js` define global styling and tokens.
- `lib/` contains shared helpers (e.g., content parsing).
- `tests/unit/` for Vitest unit tests, `tests/e2e/` for Playwright specs.
- `public/` hosts static assets and generated docs output (`public/docs/index.html`).
- `technical-docs/` and `common/` are submodules for docs content and shared design system/build tools.

## Build, Test, and Development Commands
```bash
npm run dev          # Start Next.js dev server (webpack)
npm run dev:clean    # Rebuild docs, then start dev server (webpack)
npm run build        # Build docs + production build (webpack)
npm run build:web    # Build Next.js site only (webpack)
npm run build-docs   # Run scripts/build-docs.mjs only
npm run start        # Start production server
npm run lint         # Print lint guidance (not configured)
npm run test         # Vitest unit tests
npm run test:e2e     # Playwright E2E tests
```
For doc-only workflows, `node scripts/build-docs.mjs` generates `public/docs/index.html`.

## Coding Style & Naming Conventions
- JavaScript/React, 2-space indentation, single quotes, semicolons.
- Components are PascalCase in `components/` (e.g., `BlogCard.js`).
- Tests use `.test.js/.test.jsx` (unit) and `.spec.js` (E2E).
- Tailwind utility classes are preferred for styling; keep long class lists readable.

## Testing Guidelines
- Unit tests: Vitest + Testing Library in `tests/unit/`.
- E2E tests: Playwright in `tests/e2e/`.
- Run all tests with `npm run test:all` when changing UI or routing.

## Commit & Pull Request Guidelines
- Commit messages generally follow Conventional Commits (e.g., `chore: update cleanroom-technical-docs submodule`).
- Keep subjects short, imperative, and scoped to the change.
- PRs should include: a concise summary, testing notes, and screenshots for UI changes.
- If you touch submodules, mention the updated project/version in the PR description.

## Docs & Submodules
- `technical-docs/` contains its own submodules, and those submodules also nest more submodules (multi-level recursion).
- Example nested path: `technical-docs/deploy/common/`.
- Always sync recursively: `git submodule update --init --recursive`.
- Inspect nested state with `git submodule status --recursive`.
- Use `./scripts/check-submodules.py` to verify submodule health.
Current submodules (top-level and nested):
- Top-level: `technical-docs/`, `common/`.
- Under `technical-docs/`: `whisper/`, `deploy/`, `transfer/`, and `common/`.
- Under each project: `common/`.

## Reference Docs
- `README.md` is the primary contributor guide (setup, commands, workflows).
- `CLAUDE.md` lists repo-specific automation tips and key scripts.
- `docs/ARCHITECTURE.md` explains the submodule structure and design rationale.
- `docs/SUBMODULES_GUIDE.md` covers submodule operations and troubleshooting.
