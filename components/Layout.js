import Head from 'next/head';
import Link from 'next/link';
import Footer from './Footer';

const nav = require('../common/tokens/navigation');

const defaultTitle = 'Cleanroom Labs';
const defaultDescription = 'Free and open source tools for air-gapped development';
const siteUrl = 'https://cleanroomlabs.dev';

export default function Layout({ children, title, description }) {
  const pageTitle = title || defaultTitle;
  const pageDescription = description || defaultDescription;

  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <Head>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />

        {/* Open Graph */}
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        <meta property="og:type" content="website" />
        <meta property="og:url" content={siteUrl} />

        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={pageTitle} />
        <meta name="twitter:description" content={pageDescription} />

        {/* Favicons */}
        <link rel="icon" href="/favicon.ico" sizes="32x32" />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/site.webmanifest" />
      </Head>

      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-slate-800 border-b border-slate-700 text-white flex-shrink-0">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-6 md:gap-8">
            <Link href={nav.brand.href} className="p-2 -m-2 hover:opacity-80 transition-opacity">
              <img src="/favicon.svg" alt="Cleanroom Labs home" className="w-8 h-8" />
            </Link>
            <Link href={nav.brand.href} className="hidden md:block font-bold text-lg hover:text-emerald transition-colors">
              {nav.brand.text}
            </Link>
            <div className="flex gap-4 md:gap-6">
              {nav.links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="py-2.5 text-text-secondary hover:text-emerald transition-colors"
                >
                  {link.text}
                </Link>
              ))}
            </div>
          </div>
          {/* Donate button hidden — uncomment nav.donate in common/tokens/navigation.js to re-enable */}
        </div>
      </nav>

      <div className="flex-grow">
        {children}
      </div>

      <Footer />
    </div>
  );
}
