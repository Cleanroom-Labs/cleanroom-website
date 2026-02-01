// Donate page temporarily hidden — redirect to home
// To re-enable: restore the original page content below and uncomment
// nav.donate in cleanroom-theme/tokens/navigation.js

export async function getServerSideProps() {
  return {
    redirect: {
      destination: '/',
      permanent: false,
    },
  };
}

export default function Donate() {
  return null;
}

/*
// Original donate page — uncomment to restore
import Layout from '../components/Layout';

export default function Donate() {
  return (
    <Layout
      title="Donate - Cleanroom Labs"
      description="Support Cleanroom Labs and help us continue building free, open-source tools for air-gapped development."
    >
      <main className="bg-slate-950 min-h-screen py-12">
        <div className="container mx-auto px-4 max-w-2xl">
          <h1 className="text-4xl font-bold text-text-primary mb-8 text-center">Donate</h1>

          <div className="bg-slate-900 rounded-xl p-8 text-center border border-slate-700">
            <div className="w-16 h-16 bg-emerald/20 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-emerald" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>

            <p className="text-xl text-text-secondary mb-6">
              If you found any of our software useful, consider supporting our work.
              Your contribution helps us maintain existing tools and develop new ones.
            </p>

            <p className="text-text-muted mb-8">
              All donations go directly toward development, hosting, and keeping
              our tools free and open source.
            </p>

            <a
              href="https://www.cleanroomlabs.dev/c/products/donate"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-emerald text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-emerald-light transition-all duration-200 hover:scale-105"
            >
              Support Us
            </a>

            <p className="mt-6 text-sm text-text-muted">
              Donations start at $10
            </p>
          </div>
        </div>
      </main>
    </Layout>
  );
}
*/
