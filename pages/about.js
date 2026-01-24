import Layout from '../components/Layout';

export default function About() {
  return (
    <Layout
      title="About Us - Cleanroom Labs"
      description="Learn about Cleanroom Labs' mission to build free, open-source tools for air-gapped development."
    >
      <main className="container mx-auto px-4 py-12 max-w-4xl">
        <h1 className="text-4xl font-bold mb-8">About Us</h1>

        <section className="mb-12">
          <p className="text-xl text-gray-700 leading-relaxed">
            Cleanroom Labs builds free, open-source tools for air-gapped development.
            Our mission is to make privacy-preserving software accessible to everyone,
            not just security experts.
          </p>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Core Principles</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="font-bold text-lg mb-2">Privacy by Default</h3>
              <p className="text-gray-600">
                Every tool we build works offline first. Your data never leaves your machine
                unless you explicitly choose to share it.
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="font-bold text-lg mb-2">Accessibility over Expertise</h3>
              <p className="text-gray-600">
                Security tools shouldn't require a PhD to use. We design for developers
                of all skill levels.
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="font-bold text-lg mb-2">Minimalism</h3>
              <p className="text-gray-600">
                Each tool does one thing well. No bloat, no unnecessary features,
                just focused functionality.
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="font-bold text-lg mb-2">Transparency</h3>
              <p className="text-gray-600">
                All our code is open source. You can audit, modify, and distribute
                it freely.
              </p>
            </div>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Technical Philosophy</h2>
          <p className="text-gray-700 leading-relaxed mb-4">
            We build primarily in Rust for its memory safety, performance, and
            ability to compile to standalone binaries. Our tools are self-contained
            with no external dependencies at runtime.
          </p>
          <p className="text-gray-700 leading-relaxed">
            Offline-first means every feature works without network connectivity.
            When AI capabilities are needed, we integrate local models that run
            entirely on your hardware.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-bold mb-4">Contact</h2>
          <p className="text-gray-700">
            For inquiries, reach out to{' '}
            <a
              href="mailto:lead@cleanroomlabs.dev"
              className="text-blue-600 hover:underline"
            >
              lead@cleanroomlabs.dev
            </a>
          </p>
        </section>
      </main>
    </Layout>
  );
}
