import Layout from '../../components/Layout';

export default function Blog() {
  return (
    <Layout
      title="Blog - Cleanroom Labs"
      description="News, updates, and articles from Cleanroom Labs."
    >
      <main className="container mx-auto px-4 py-12 max-w-4xl">
        <h1 className="text-4xl font-bold mb-8">Blog</h1>

        <div className="bg-gray-50 rounded-lg p-12 text-center">
          <p className="text-xl text-gray-600">Coming soon</p>
          <p className="text-gray-500 mt-4">
            Check back later for news and updates about our tools.
          </p>
        </div>
      </main>
    </Layout>
  );
}
