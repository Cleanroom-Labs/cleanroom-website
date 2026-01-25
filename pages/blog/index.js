import Layout from '../../components/Layout';
import BlogCard from '../../components/BlogCard';
import { getAllPosts } from '../../lib/blog';

export default function Blog({ posts }) {
  return (
    <Layout
      title="Blog - Cleanroom Labs"
      description="News, updates, and articles from Cleanroom Labs about air-gapped computing, privacy-first software, and offline development tools."
    >
      <main className="bg-slate-950 min-h-screen py-12">
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
