import { MDXRemote } from 'next-mdx-remote';
import { serialize } from 'next-mdx-remote/serialize';
import remarkGfm from 'remark-gfm';
import Layout from '../../components/Layout';
import MDXComponents from '../../components/MDXComponents';
import { getPostBySlug, getAllSlugs } from '../../lib/blog';
import Link from 'next/link';

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
      <main className="bg-slate-950 min-h-screen py-12">
        <div className="container mx-auto px-4 max-w-3xl">
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
