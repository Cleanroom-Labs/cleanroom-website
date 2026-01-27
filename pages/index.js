import Layout from '../components/Layout';
import Hero from '../components/Hero';
import ProductCard from '../components/ProductCard';
import { products } from '../data/products';
import { DashedCircle } from '../components/icons';

export default function Home() {
  return (
    <Layout
      title="Cleanroom Labs"
      description="Free and open source tools for air-gapped development. Privacy shouldn't require expertise."
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

        {/* Small particles */}
        <div className="absolute top-[35%] left-[18%] w-2 h-2 bg-emerald/45 rounded-full animate-float" />
        <div className="absolute bottom-[40%] right-[10%] w-2 h-2 bg-emerald/40 rounded-full animate-float-delayed" />
        <div className="absolute top-[75%] left-[25%] w-2 h-2 bg-emerald/42 rounded-full animate-drift" />

        {/* Tiny particles */}
        <div className="absolute top-[45%] right-[8%] w-1.5 h-1.5 bg-emerald/50 rounded-full animate-pulse-slow" />
        <div className="absolute bottom-[15%] left-[20%] w-1.5 h-1.5 bg-emerald/55 rounded-full animate-float" />

        {/* Dashed circle decorations */}
        <DashedCircle preset="medium" className="absolute top-[20%] right-12 w-32 h-32 opacity-20 animate-pulse-slow" />
        <DashedCircle preset="small" className="absolute bottom-1/3 left-16 w-28 h-28 opacity-15 animate-drift-reverse" />
        <DashedCircle preset="large" className="absolute top-[60%] right-20 w-40 h-40 opacity-12 animate-drift" />
        <DashedCircle preset="medium" className="absolute bottom-[20%] left-8 w-24 h-24 opacity-18 animate-float" />
      </div>

      <Hero />

      <main id="products" className="relative bg-slate-950/80 py-16 z-10">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-text-primary mb-4">Our Tools</h2>
          <p className="text-text-secondary text-center max-w-2xl mx-auto mb-12">
            Privacy-first tools designed to work completely offline.
            <br />
            No cloud, no telemetry, no compromises.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {products.map((product) => (
              <ProductCard
                key={product.name}
                name={product.name}
                description={product.description}
                docsUrl={product.docsUrl}
              />
            ))}

            {/* Coming Soon card */}
            <div className="bg-slate-900/50 rounded-xl border-2 border-dashed border-slate-700 flex flex-col items-center justify-center p-6 min-h-[280px]">
              <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center mb-4">
                <svg className="w-8 h-8 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-text-muted mb-2">More Coming Soon</h3>
              <p className="text-text-muted text-center text-sm">
                Additional privacy-first tools are in development
              </p>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}
