import Layout from '../components/Layout';
import Link from 'next/link';

export default function DocsIndex() {
  return (
    <Layout title="Documentation - Cleanroom Labs" description="Browse the complete technical documentation for Cleanroom Labs">
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold">Documentation</h1>
        <p className="mt-4">View the complete technical documentation:</p>
        <Link
          href="/docs/index.html"
          className="inline-block mt-4 px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Browse Documentation
        </Link>
      </main>
    </Layout>
  );
}
