import Link from 'next/link';

export default function Hero() {
  return (
    <section className="relative bg-slate-900 text-white min-h-screen flex items-center overflow-hidden">
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

        {/* Floating particles - varied sizes, positions, and animations */}
        {/* Large wandering particles */}
        <div className="absolute top-[15%] right-[20%] w-5 h-5 bg-emerald/35 rounded-full animate-wander" />
        <div className="absolute top-[60%] left-[15%] w-4 h-4 bg-emerald/30 rounded-full animate-wander-alt" />
        <div className="absolute top-[80%] right-[60%] w-5 h-5 bg-emerald/25 rounded-full animate-wander" />
        <div className="absolute top-[10%] left-[50%] w-4 h-4 bg-emerald/20 rounded-full animate-wander-alt" />

        {/* Medium drifting particles */}
        <div className="absolute top-[25%] left-[30%] w-3 h-3 bg-emerald/40 rounded-full animate-drift" />
        <div className="absolute bottom-[30%] right-[25%] w-3 h-3 bg-emerald/25 rounded-full animate-drift-reverse" />
        <div className="absolute top-[45%] right-[10%] w-3 h-3 bg-emerald/35 rounded-full animate-drift-slow" />
        <div className="absolute top-[75%] left-[45%] w-3 h-3 bg-emerald/30 rounded-full animate-drift" />
        <div className="absolute top-[5%] right-[35%] w-3 h-3 bg-emerald/25 rounded-full animate-drift-reverse" />
        <div className="absolute bottom-[15%] left-[60%] w-3 h-3 bg-emerald/35 rounded-full animate-drift-slow" />

        {/* Small floating particles */}
        <div className="absolute top-[20%] right-[40%] w-2 h-2 bg-emerald/45 rounded-full animate-float" />
        <div className="absolute bottom-[25%] left-[25%] w-2 h-2 bg-emerald/30 rounded-full animate-float-delayed" />
        <div className="absolute top-[70%] right-[35%] w-2 h-2 bg-emerald/35 rounded-full animate-drift" />
        <div className="absolute top-[35%] left-[10%] w-2 h-2 bg-emerald/25 rounded-full animate-drift-reverse" />
        <div className="absolute top-[85%] right-[15%] w-2 h-2 bg-emerald/40 rounded-full animate-float" />
        <div className="absolute top-[50%] left-[55%] w-2 h-2 bg-emerald/30 rounded-full animate-float-delayed" />
        <div className="absolute bottom-[10%] right-[55%] w-2 h-2 bg-emerald/35 rounded-full animate-wander" />
        <div className="absolute top-[30%] right-[5%] w-2 h-2 bg-emerald/25 rounded-full animate-wander-alt" />

        {/* Tiny accent particles */}
        <div className="absolute top-[40%] right-[15%] w-1.5 h-1.5 bg-emerald/50 rounded-full animate-pulse-slow" />
        <div className="absolute bottom-[40%] left-[40%] w-1.5 h-1.5 bg-emerald/40 rounded-full animate-pulse-slow" />
        <div className="absolute top-[55%] left-[35%] w-1 h-1 bg-emerald/55 rounded-full animate-float" />
        <div className="absolute bottom-[20%] right-[45%] w-1 h-1 bg-emerald/45 rounded-full animate-float-delayed" />
        <div className="absolute top-[12%] left-[20%] w-1.5 h-1.5 bg-emerald/50 rounded-full animate-pulse-slow" />
        <div className="absolute top-[65%] right-[50%] w-1 h-1 bg-emerald/55 rounded-full animate-float" />
        <div className="absolute bottom-[5%] left-[30%] w-1.5 h-1.5 bg-emerald/45 rounded-full animate-pulse-slow" />
        <div className="absolute top-[90%] right-[25%] w-1 h-1 bg-emerald/40 rounded-full animate-float-delayed" />

        {/* Dashed circle decorations (air gap visualization) */}
        <svg className="absolute top-1/4 right-10 w-32 h-32 opacity-20 animate-pulse-slow" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#10b981" strokeWidth="1" strokeDasharray="4 4" />
        </svg>
        <svg className="absolute bottom-1/3 left-10 w-24 h-24 opacity-15 animate-pulse-slow" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#10b981" strokeWidth="1" strokeDasharray="6 6" />
        </svg>
        <svg className="absolute top-[10%] left-[35%] w-20 h-20 opacity-10 animate-drift-reverse" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="35" fill="none" stroke="#10b981" strokeWidth="1" strokeDasharray="3 5" />
        </svg>
        <svg className="absolute bottom-[15%] right-[30%] w-28 h-28 opacity-12 animate-drift-slow" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="none" stroke="#10b981" strokeWidth="0.8" strokeDasharray="2 4" />
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
              className="inline-flex items-center px-6 py-3 bg-emerald text-white font-semibold rounded-lg hover:bg-emerald-light transition-all duration-150 ease-out hover:scale-105"
            >
              Explore Our Tools
              <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </Link>
            <Link
              href="/docs/index.html"
              className="inline-flex items-center px-6 py-3 border border-slate-700 bg-slate-800/50 backdrop-blur-sm text-text-primary font-semibold rounded-lg hover:border-emerald hover:text-emerald hover:bg-slate-800/70 transition-all duration-150 ease-out"
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
