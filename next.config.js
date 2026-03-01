/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
  reactStrictMode: true,
  // Avoid Next.js guessing the workspace root when multiple lockfiles exist.
  outputFileTracingRoot: __dirname,
  // Headers and redirects are handled by the hosting platform (Cloudflare Pages)
  // via public/_headers and public/_redirects files.
};

module.exports = nextConfig;
