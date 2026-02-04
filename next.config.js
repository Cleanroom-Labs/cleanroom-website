/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Avoid Next.js guessing the workspace root when multiple lockfiles exist.
  outputFileTracingRoot: __dirname,
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
  async redirects() {
    return [
      {
        source: '/docs',
        destination: '/docs/dev/index.html',
        permanent: false,
      },
      {
        // Redirect non-versioned doc paths to the dev version
        source: '/docs/:path((?!dev/|latest/|versions\\.json).*)',
        destination: '/docs/dev/:path',
        permanent: false,
      },
      {
        source: '/donate',
        destination: '/',
        permanent: false,
      },
    ];
  },
};

module.exports = nextConfig;
