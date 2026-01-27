import Layout from '../../components/Layout';
import BlogCard from '../../components/BlogCard';
import { getAllPosts } from '../../lib/blog';
import { DashedCircle } from '../../components/icons';

export default function Blog({ posts }) {
  return (
    <Layout
      title="Blog - Cleanroom Labs"
      description="News, updates, and articles from Cleanroom Labs about air-gapped computing, privacy-first software, and offline development tools."
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

      <main className="relative bg-slate-950/80 min-h-screen py-12 z-10">
        <div className="container mx-auto px-4 max-w-4xl">
          <h1 className="text-4xl font-bold text-text-primary mb-4">Blog</h1>
          <p className="text-text-secondary mb-8">
            News, updates, and articles about air-gapped computing and privacy-first software.
          </p>

          <div className="space-y-6">
            {posts.map((post) => (
              <BlogCard key={post.slug} post={post} />
            ))}
          </div>
        </div>
      </main>
    </Layout>
  );
}

export async function getStaticProps() {
  const posts = getAllPosts();
  return {
    props: {
      posts,
    },
  };
}
