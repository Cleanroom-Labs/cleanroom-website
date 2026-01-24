import Head from 'next/head';
import Link from 'next/link';

const defaultTitle = 'Cleanroom Labs';
const defaultDescription = 'Technical documentation and resources';
const siteUrl = 'https://cleanroomlabs.dev';

export default function Layout({ children, title, description }) {
  const pageTitle = title || defaultTitle;
  const pageDescription = description || defaultDescription;

  return (
    <>
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
        <link rel="icon" href="/favicon.ico" sizes="48x48" />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/site.webmanifest" />
      </Head>
      <nav className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex gap-6">
          <Link href="/" className="font-bold">Cleanroom Labs</Link>
          <Link href="/docs" className="hover:underline">Docs</Link>
        </div>
      </nav>
      {children}
    </>
  );
}
