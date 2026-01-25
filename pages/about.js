import Layout from '../components/Layout';

export default function About() {
  return (
    <Layout
      title="About Us - Cleanroom Labs"
      description="Learn about Cleanroom Labs' mission to build free, open-source tools for air-gapped development."
    >
      <main className="bg-slate-950 min-h-screen">
        {/* Hero section with background */}
        <section className="relative py-16 overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 pointer-events-none overflow-hidden">
            <div className="absolute top-0 right-0 w-96 h-96 translate-x-1/2 -translate-y-1/2 opacity-30">
              <img src="/shield-bg.svg" alt="" className="w-full h-full" />
            </div>
            <div className="absolute inset-0 opacity-5" style={{ backgroundImage: "url('/grid.svg')", backgroundRepeat: 'repeat' }} />
          </div>

          <div className="container mx-auto px-4 max-w-4xl relative z-10">
            <h1 className="text-4xl font-bold text-text-primary mb-8">About Us</h1>

            <p className="text-xl text-text-secondary leading-relaxed">
              Cleanroom Labs builds free, open-source tools for air-gapped development.
              Our mission is to make privacy-preserving software accessible to everyone,
              not just security experts.
            </p>
          </div>
        </section>

        {/* Core Principles */}
        <section className="py-12 border-t border-slate-800">
          <div className="container mx-auto px-4 max-w-4xl">
            <h2 className="text-2xl font-bold text-text-primary mb-8">Core Principles</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900 p-6 rounded-xl border border-slate-700">
                <div className="w-10 h-10 bg-emerald/20 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-5 h-5 text-emerald" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <h3 className="font-bold text-lg text-text-primary mb-2">Privacy by Default</h3>
                <p className="text-text-secondary">
                  Every tool we build works offline first. Your data never leaves your machine
                  unless you explicitly choose to share it.
                </p>
              </div>

              <div className="bg-slate-900 p-6 rounded-xl border border-slate-700">
                <div className="w-10 h-10 bg-emerald/20 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-5 h-5 text-emerald" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <h3 className="font-bold text-lg text-text-primary mb-2">Accessibility over Expertise</h3>
                <p className="text-text-secondary">
                  Security tools shouldn't require a PhD to use. We design for developers
                  of all skill levels.
                </p>
              </div>

              <div className="bg-slate-900 p-6 rounded-xl border border-slate-700">
                <div className="w-10 h-10 bg-emerald/20 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-5 h-5 text-emerald" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6z" />
                  </svg>
                </div>
                <h3 className="font-bold text-lg text-text-primary mb-2">Minimalism</h3>
                <p className="text-text-secondary">
                  Each tool does one thing well. No bloat, no unnecessary features,
                  just focused functionality.
                </p>
              </div>

              <div className="bg-slate-900 p-6 rounded-xl border border-slate-700">
                <div className="w-10 h-10 bg-emerald/20 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-5 h-5 text-emerald" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </div>
                <h3 className="font-bold text-lg text-text-primary mb-2">Transparency</h3>
                <p className="text-text-secondary">
                  All our code is open source. You can audit, modify, and distribute
                  it freely.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Technical Philosophy */}
        <section className="py-12 border-t border-slate-800">
          <div className="container mx-auto px-4 max-w-4xl">
            <h2 className="text-2xl font-bold text-text-primary mb-6">Technical Philosophy</h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              We build primarily in Rust for its memory safety, performance, and
              ability to compile to standalone binaries. Our tools are self-contained
              with no external dependencies at runtime.
            </p>
            <p className="text-text-secondary leading-relaxed">
              Offline-first means every feature works without network connectivity.
              When AI capabilities are needed, we integrate local models that run
              entirely on your hardware.
            </p>
          </div>
        </section>

        {/* Contact */}
        <section className="py-12 border-t border-slate-800">
          <div className="container mx-auto px-4 max-w-4xl">
            <h2 className="text-2xl font-bold text-text-primary mb-4">Contact</h2>
            <p className="text-text-secondary">
              For inquiries, reach out to{' '}
              <a
                href="mailto:lead@cleanroomlabs.dev"
                className="text-emerald hover:text-emerald-light transition-colors"
              >
                lead@cleanroomlabs.dev
              </a>
            </p>
          </div>
        </section>
      </main>
    </Layout>
  );
}
