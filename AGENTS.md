# Repository Guidelines

## Project Structure & Module Organization
- `pages/` contains Next.js routes and page-level logic.
- `components/` holds reusable UI components (React + Tailwind).
- `styles/` and `tailwind.config.js` define global styling and tokens.
- `content/` and `data/` store site content and metadata.
- `lib/` contains shared helpers (e.g., content parsing).
- `tests/unit/` for Vitest unit tests, `tests/e2e/` for Playwright specs.
- `public/` hosts static assets and generated docs output (`public/docs/index.html`).
- `cleanroom-technical-docs/` and `cleanroom-theme/` are submodules for docs content/theme.

## Build, Test, and Development Commands
```bash
npm run dev          # Start Next.js dev server (uses existing docs)
npm run dev:clean    # Rebuild docs, then start dev server
npm run build        # Build docs + production Next.js build
npm run build-docs   # Run scripts/build-docs.mjs only
npm run start        # Start production server
npm run lint         # Print lint setup guidance (linting not configured yet)
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
- `cleanroom-technical-docs/` contains its own submodules, and those submodules also nest more submodules (multi-level recursion).
- Example nested path: `cleanroom-technical-docs/airgap-deploy-docs/source/cleanroom-theme`.
- Always sync recursively: `git submodule update --init --recursive`.
- Inspect nested state with `git submodule status --recursive`.
- Use `./scripts/check-submodules.py` to verify submodule health.
Current submodules (top-level and nested):
- Top-level: `cleanroom-technical-docs/`, `cleanroom-theme/`.
- Under `cleanroom-technical-docs/`: `airgap-deploy-docs/`, `airgap-transfer-docs/`, `cleanroom-whisper-docs/`, and `source/cleanroom-theme/`.
- Under each `*-docs/`: `source/cleanroom-theme/`.

## Reference Docs
- `README.md` is the primary contributor guide (setup, commands, workflows).
- `CLAUDE.md` lists repo-specific automation tips and key scripts.
- `docs/ARCHITECTURE.md` explains the submodule structure and design rationale.
- `docs/SUBMODULES_GUIDE.md` covers submodule operations and troubleshooting.
