import Head from 'next/head';
import Link from 'next/link';

export default function Layout({ children, title }) {
  const pageTitle = title || 'Cleanroom Labs';

  return (
    <>
      <Head>
        <title>{pageTitle}</title>
        <meta name="description" content="Technical documentation and resources" />
        <link rel="icon" href="/favicon.ico" />
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
