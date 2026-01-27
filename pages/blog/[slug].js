import { MDXRemote } from 'next-mdx-remote';
import { serialize } from 'next-mdx-remote/serialize';
import remarkGfm from 'remark-gfm';
import Layout from '../../components/Layout';
import MDXComponents from '../../components/MDXComponents';
import { getPostBySlug, getAllSlugs } from '../../lib/blog';
import Link from 'next/link';
import { DashedCircle } from '../../components/icons';

export default function BlogPost({ frontmatter, mdxSource }) {
  const formattedDate = new Date(frontmatter.date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <Layout
      title={`${frontmatter.title} - Cleanroom Labs Blog`}
      description={frontmatter.excerpt || `Read ${frontmatter.title} on the Cleanroom Labs blog.`}
    >
      {/* Background decoration - fixed to viewport */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        {/* Large gradient orbs - more visible */}
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
        <div className="absolute top-[85%] right-[18%] w-32 h-32 bg-emerald/28 rounded-full blur-2xl" />

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
        <div className="absolute top-[55%] right-[5%] w-2 h-2 bg-emerald/40 rounded-full animate-float" />

        {/* Tiny particles */}
        <div className="absolute top-[45%] right-[8%] w-1.5 h-1.5 bg-emerald/50 rounded-full animate-pulse-slow" />
        <div className="absolute bottom-[15%] left-[20%] w-1.5 h-1.5 bg-emerald/55 rounded-full animate-float" />
        <div className="absolute top-[25%] right-[22%] w-1.5 h-1.5 bg-emerald/48 rounded-full animate-drift" />
        <div className="absolute bottom-[50%] left-[10%] w-1 h-1 bg-emerald/60 rounded-full animate-float-delayed" />
        <div className="absolute top-[65%] right-[12%] w-1 h-1 bg-emerald/55 rounded-full animate-wander" />

        {/* Dashed circle decorations */}
        <DashedCircle preset="medium" className="absolute top-[20%] right-12 w-32 h-32 opacity-20 animate-pulse-slow" />
        <DashedCircle preset="small" className="absolute bottom-1/3 left-16 w-28 h-28 opacity-15 animate-drift-reverse" />
        <DashedCircle preset="large" className="absolute top-[60%] right-20 w-40 h-40 opacity-12 animate-drift" />
        <DashedCircle preset="medium" className="absolute bottom-[20%] left-8 w-24 h-24 opacity-18 animate-float" />
      </div>

      <main className="relative bg-slate-950/80 min-h-screen py-12 z-10">
        <div className="container mx-auto px-6 max-w-5xl relative bg-slate-900 py-12 rounded-lg shadow-2xl shadow-black/50 border border-slate-700">
          <div className="max-w-3xl mx-auto">
          <Link href="/blog" className="text-emerald hover:text-emerald-light transition-colors mb-6 inline-block">
            &larr; Back to Blog
          </Link>

          <article>
            <header className="mb-8">
              <h1 className="text-4xl font-bold text-text-primary mb-4">{frontmatter.title}</h1>
              <div className="flex items-center gap-4 text-text-muted mb-4">
                <time dateTime={frontmatter.date}>{formattedDate}</time>
                {frontmatter.author && <span>by {frontmatter.author}</span>}
              </div>
              {frontmatter.tags && frontmatter.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {frontmatter.tags.map((tag) => (
                    <span
                      key={tag}
                      className="bg-slate-800 text-text-muted px-2 py-1 rounded text-sm border border-slate-700"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </header>

            <div className="prose prose-lg max-w-none">
              <MDXRemote {...mdxSource} components={MDXComponents} />
            </div>
          </article>

          <div className="mt-12 pt-8 border-t border-slate-800">
            <Link href="/blog" className="text-emerald hover:text-emerald-light transition-colors">
              &larr; Back to Blog
            </Link>
          </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export async function getStaticPaths() {
  const slugs = getAllSlugs();
  return {
    paths: slugs.map((slug) => ({ params: { slug } })),
    fallback: false,
  };
}

export async function getStaticProps({ params }) {
  const { frontmatter, content } = getPostBySlug(params.slug);
  const mdxSource = await serialize(content, {
    mdxOptions: {
      remarkPlugins: [remarkGfm],
    },
    parseFrontmatter: false,
  });

  return {
    props: {
      frontmatter,
      mdxSource,
    },
  };
}
