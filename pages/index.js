import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout title="Cleanroom Labs" description="Cleanroom Labs - Technical documentation and resources for software engineering">
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold">Cleanroom Labs</h1>
        <p className="mt-4">Technical documentation and resources.</p>
      </main>
    </Layout>
  );
}
