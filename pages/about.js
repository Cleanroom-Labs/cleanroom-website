import Layout from '../components/Layout';
import Link from 'next/link';
import { DashedCircle } from '../components/icons';

export default function About() {
  return (
    <Layout
      title="About Us - Cleanroom Labs"
      description="Learn about Cleanroom Labs' mission to build free, open-source tools for air-gapped development."
    >
      {/* Fixed background decoration - visible across all sections */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        {/* Large gradient orbs */}
        <div className="absolute -top-20 -right-32 w-[500px] h-[500px] bg-emerald/30 rounded-full blur-3xl" />
        <div className="absolute top-1/4 -left-40 w-[450px] h-[450px] bg-emerald/25 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-20 w-[400px] h-[400px] bg-emerald/25 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 -left-32 w-[350px] h-[350px] bg-emerald-glow rounded-full blur-3xl opacity-30" />

        {/* Medium gradient orbs */}
        <div className="absolute top-1/2 right-[5%] w-72 h-72 bg-emerald/20 rounded-full blur-3xl" />
        <div className="absolute top-[15%] left-[10%] w-64 h-64 bg-emerald/18 rounded-full blur-3xl" />
        <div className="absolute bottom-[35%] right-[8%] w-56 h-56 bg-emerald-glow rounded-full blur-3xl opacity-25" />
        <div className="absolute top-[70%] left-[5%] w-80 h-80 bg-emerald/22 rounded-full blur-3xl" />

        {/* Smaller accent orbs */}
        <div className="absolute top-[40%] right-[12%] w-40 h-40 bg-emerald/30 rounded-full blur-2xl" />
        <div className="absolute bottom-[20%] left-[15%] w-36 h-36 bg-emerald/25 rounded-full blur-2xl" />

        {/* Grid pattern */}
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: "url('/grid.svg')", backgroundRepeat: 'repeat' }} />

        {/* Large particles */}
        <div className="absolute top-[15%] right-[10%] w-4 h-4 bg-emerald/35 rounded-full animate-drift" />
        <div className="absolute top-[50%] left-[8%] w-4 h-4 bg-emerald/30 rounded-full animate-drift-reverse" />
        <div className="absolute bottom-[30%] right-[15%] w-4 h-4 bg-emerald/32 rounded-full animate-wander" />

        {/* Medium particles */}
        <div className="absolute top-[20%] right-[15%] w-3 h-3 bg-emerald/40 rounded-full animate-drift" />
        <div className="absolute top-[60%] left-[12%] w-3 h-3 bg-emerald/35 rounded-full animate-drift-reverse" />
        <div className="absolute bottom-[25%] right-[20%] w-3 h-3 bg-emerald/38 rounded-full animate-wander" />
        <div className="absolute top-[75%] right-[8%] w-3 h-3 bg-emerald/32 rounded-full animate-float" />
        <div className="absolute top-[35%] left-[6%] w-3 h-3 bg-emerald/30 rounded-full animate-float-delayed" />

        {/* Small particles */}
        <div className="absolute top-[35%] left-[18%] w-2 h-2 bg-emerald/45 rounded-full animate-float" />
        <div className="absolute bottom-[40%] right-[10%] w-2 h-2 bg-emerald/40 rounded-full animate-float-delayed" />
        <div className="absolute top-[75%] left-[25%] w-2 h-2 bg-emerald/42 rounded-full animate-drift" />
        <div className="absolute top-[10%] left-[20%] w-2 h-2 bg-emerald/38 rounded-full animate-wander" />
        <div className="absolute bottom-[15%] right-[25%] w-2 h-2 bg-emerald/35 rounded-full animate-drift-reverse" />

        {/* Tiny particles */}
        <div className="absolute top-[45%] right-[8%] w-1.5 h-1.5 bg-emerald/50 rounded-full animate-pulse-slow" />
        <div className="absolute bottom-[15%] left-[20%] w-1.5 h-1.5 bg-emerald/55 rounded-full animate-float" />
        <div className="absolute top-[25%] right-[22%] w-1.5 h-1.5 bg-emerald/48 rounded-full animate-drift" />

        {/* Dashed circle decorations */}
        <DashedCircle preset="medium" className="absolute top-[20%] right-12 w-32 h-32 opacity-20 animate-pulse-slow" />
        <DashedCircle preset="small" className="absolute bottom-1/3 left-16 w-28 h-28 opacity-15 animate-drift-reverse" />
        <DashedCircle preset="large" className="absolute top-[60%] right-20 w-40 h-40 opacity-12 animate-drift" />
        <DashedCircle preset="medium" className="absolute bottom-[20%] left-8 w-24 h-24 opacity-18 animate-float" />
      </div>

      <main className="relative bg-slate-950/80 min-h-screen z-10">
        {/* Hero section */}
        <section className="relative py-24 overflow-hidden bg-slate-800/50 backdrop-blur-[1px]">
          <div className="container mx-auto px-4 max-w-4xl relative z-10 text-center">
            <h1 className="text-5xl font-bold text-text-primary mb-6">About Us</h1>
            <p className="text-xl text-text-secondary leading-relaxed max-w-2xl mx-auto">
              Cleanroom Labs builds free, open-source tools for air-gapped development.
              Our mission is to make privacy-preserving software accessible to everyone,
              not just security experts.
            </p>
          </div>
        </section>

        {/* Core Principles */}
        <section className="py-12 border-t border-slate-800">
          <div className="container mx-auto px-4 max-w-4xl">
            <h2 className="text-2xl font-bold text-text-primary mb-8 text-center">Core Principles</h2>

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
        <section className="py-12 border-t border-slate-800 bg-slate-800/50 backdrop-blur-[1px]">
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

        {/* Learn More */}
        <section className="py-12 border-t border-slate-800">
          <div className="container mx-auto px-4 max-w-4xl">
            <h2 className="text-2xl font-bold text-text-primary mb-8 text-center">Learn More</h2>

            {/* Philosophy & Overview */}
            <h3 className="text-lg font-semibold text-text-primary mb-4">Philosophy & Overview</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6 mb-10">
              <Link href="/blog/why-air-gapping" className="group">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-emerald group-hover:text-emerald-light transition-colors">Why Air-Gapping?</span>
                  <svg className="w-4 h-4 text-emerald group-hover:text-emerald-light group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="text-text-secondary text-sm">The security philosophy behind offline-first development.</p>
              </Link>
              <Link href="/blog/introducing-airgap-suite" className="group">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-emerald group-hover:text-emerald-light transition-colors">Introducing the AirGap Suite</span>
                  <svg className="w-4 h-4 text-emerald group-hover:text-emerald-light group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="text-text-secondary text-sm">How our three tools work together.</p>
              </Link>
            </div>

            {/* See It In Action */}
            <h3 className="text-lg font-semibold text-text-primary mb-4">See It In Action</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-x-8 gap-y-6 mb-10">
              <Link href="/blog/demo-whisper-quick-capture" className="group">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-emerald group-hover:text-emerald-light transition-colors">Capturing Meeting Notes</span>
                  <svg className="w-4 h-4 text-emerald group-hover:text-emerald-light group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="text-text-secondary text-sm">Voice transcription without the cloud.</p>
              </Link>
              <Link href="/blog/demo-deploy-rust-app" className="group">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-emerald group-hover:text-emerald-light transition-colors">Packaging Rust Apps</span>
                  <svg className="w-4 h-4 text-emerald group-hover:text-emerald-light group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="text-text-secondary text-sm">Bundle applications for air-gapped deployment.</p>
              </Link>
              <Link href="/blog/demo-transfer-ollama" className="group">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-emerald group-hover:text-emerald-light transition-colors">Transferring Large Models</span>
                  <svg className="w-4 h-4 text-emerald group-hover:text-emerald-light group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="text-text-secondary text-sm">Multi-USB orchestration for big files.</p>
              </Link>
            </div>

            {/* Resources */}
            <h3 className="text-lg font-semibold text-text-primary mb-4">Resources</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
              <Link href="/docs/meta/principles.html" className="group">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-emerald group-hover:text-emerald-light transition-colors">Design Principles</span>
                  <svg className="w-4 h-4 text-emerald group-hover:text-emerald-light group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="text-text-secondary text-sm">The technical philosophy behind our tools.</p>
              </Link>
              <Link href="/docs/meta/release-roadmap.html" className="group">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-emerald group-hover:text-emerald-light transition-colors">Roadmap</span>
                  <svg className="w-4 h-4 text-emerald group-hover:text-emerald-light group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="text-text-secondary text-sm">What we're building next.</p>
              </Link>
              <Link href="/docs/index.html" className="group">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-emerald group-hover:text-emerald-light transition-colors">Technical Documentation</span>
                  <svg className="w-4 h-4 text-emerald group-hover:text-emerald-light group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="text-text-secondary text-sm">Requirements, design specs, and API references.</p>
              </Link>
              <a href="https://github.com/Cleanroom-Labs" target="_blank" rel="noopener noreferrer" className="group">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-emerald group-hover:text-emerald-light transition-colors">GitHub</span>
                  <svg className="w-4 h-4 text-emerald group-hover:text-emerald-light group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="text-text-secondary text-sm">Browse source code and contribute.</p>
              </a>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
