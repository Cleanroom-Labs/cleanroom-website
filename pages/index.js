import Layout from '../components/Layout';
import Hero from '../components/Hero';
import ProductCard from '../components/ProductCard';
import { products } from '../data/products';

export default function Home() {
  return (
    <Layout
      title="Cleanroom Labs"
      description="Free and open source tools for air-gapped development. Privacy shouldn't require expertise."
    >
      <Hero />

      <main id="products" className="bg-slate-950 py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-text-primary mb-4">Our Tools</h2>
          <p className="text-text-secondary text-center max-w-2xl mx-auto mb-12">
            Privacy-first tools designed to work completely offline. No cloud, no telemetry, no compromises.
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
