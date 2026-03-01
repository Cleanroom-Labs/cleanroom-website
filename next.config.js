/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
  reactStrictMode: true,
  // Avoid Next.js guessing the workspace root when multiple lockfiles exist.
  outputFileTracingRoot: __dirname,
};

// Mirror public/_redirects for local dev (Cloudflare handles these in production)
if (process.env.NODE_ENV !== 'production') {
  nextConfig.redirects = async () => [
    { source: '/docs', destination: '/docs/dev/index.html', permanent: false },
    { source: '/donate', destination: '/', permanent: false },
  ];
}

module.exports = nextConfig;
