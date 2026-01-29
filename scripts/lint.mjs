#!/usr/bin/env node

/**
 * This repo currently does not ship an ESLint configuration.
 * Next.js v16 removed `next lint`, so `npm run lint` is a guidance command.
 */

console.error('Linting is not configured in this repo yet.');
console.error('');
console.error('Next steps (recommended):');
console.error('  1) Add ESLint + a config (e.g., eslint-config-next).');
console.error('  2) Update scripts/lint.mjs to invoke eslint.');
process.exit(1);

