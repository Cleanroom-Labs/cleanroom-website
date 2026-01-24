import Layout from '../components/Layout';

export default function Donate() {
  return (
    <Layout
      title="Donate - Cleanroom Labs"
      description="Support Cleanroom Labs and help us continue building free, open-source tools for air-gapped development."
    >
      <main className="container mx-auto px-4 py-12 max-w-2xl">
        <h1 className="text-4xl font-bold mb-8 text-center">Donate</h1>

        <div className="bg-gray-50 rounded-lg p-8 text-center">
          <p className="text-xl text-gray-700 mb-6">
            If you found any of our software useful, consider supporting our work.
            Your contribution helps us maintain existing tools and develop new ones.
          </p>

          <p className="text-gray-600 mb-8">
            All donations go directly toward development, hosting, and keeping
            our tools free and open source.
          </p>

          <a
            href="https://www.cleanroomlabs.dev/c/products/donate"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-gray-900 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-700 transition-colors"
          >
            Support Us
          </a>

          <p className="mt-6 text-sm text-gray-500">
            Donations start at $10
          </p>
        </div>
      </main>
    </Layout>
  );
}
