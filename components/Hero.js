import Link from 'next/link';

export default function Hero() {
  return (
    <section className="relative bg-slate-900 text-white min-h-[70vh] flex items-center overflow-hidden">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Gradient orbs */}
        <div className="absolute top-1/4 -right-20 w-96 h-96 bg-emerald/20 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 -left-20 w-80 h-80 bg-emerald/10 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-emerald-glow rounded-full blur-3xl opacity-30" />

        {/* Grid pattern overlay */}
        <div
          className="absolute inset-0 opacity-5"
          style={{ backgroundImage: "url('/grid.svg')", backgroundRepeat: 'repeat' }}
        />

        {/* Floating shapes */}
        <div className="absolute top-20 right-1/4 w-4 h-4 bg-emerald/40 rounded-full animate-float" />
        <div className="absolute bottom-32 right-1/3 w-2 h-2 bg-emerald/30 rounded-full animate-float-delayed" />
        <div className="absolute top-1/3 left-1/4 w-3 h-3 bg-emerald/25 rounded-full animate-float" />
        <div className="absolute bottom-1/4 left-1/3 w-2 h-2 bg-emerald/35 rounded-full animate-float-delayed" />

        {/* Dotted line decorations (air gap visualization) */}
        <svg className="absolute top-1/4 right-10 w-32 h-32 opacity-20" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#10b981" strokeWidth="1" strokeDasharray="4 4" />
        </svg>
        <svg className="absolute bottom-1/3 left-10 w-24 h-24 opacity-15" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#10b981" strokeWidth="1" strokeDasharray="6 6" />
        </svg>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-20 relative z-10">
        <div className="max-w-3xl">
          {/* Tagline */}
          <p className="text-emerald text-sm font-medium tracking-wide uppercase mb-4">
            Privacy-First Development Tools
          </p>

          {/* Headline */}
          <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            Build software that{' '}
            <span className="text-emerald">respects privacy</span>
          </h1>

          {/* Description */}
          <p className="text-xl text-text-secondary max-w-2xl leading-relaxed mb-8">
            Cleanroom Labs builds free and open source tools that work without
            network dependency. Privacy shouldn't require expertise—just the right tools.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-wrap gap-4">
            <Link
              href="#products"
              className="inline-flex items-center px-6 py-3 bg-emerald text-white font-semibold rounded-lg hover:bg-emerald-light transition-all duration-200 hover:scale-105"
            >
              Explore Our Tools
              <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </Link>
            <Link
              href="/docs/index.html"
              className="inline-flex items-center px-6 py-3 border border-slate-700 text-text-primary font-semibold rounded-lg hover:border-emerald hover:text-emerald transition-all duration-200"
            >
              Documentation
              <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
