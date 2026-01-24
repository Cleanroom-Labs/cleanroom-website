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
      <main className="container mx-auto px-4 py-12">
        <h2 className="text-3xl font-bold text-center mb-8">Our Tools</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.map((product) => (
            <ProductCard
              key={product.name}
              name={product.name}
              description={product.description}
              color={product.color}
            />
          ))}
        </div>
      </main>
    </Layout>
  );
}
