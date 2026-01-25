import Link from 'next/link';

export default function BlogCard({ post }) {
  const { slug, title, date, author, tags, excerpt } = post;

  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <article className="bg-slate-900 border border-slate-700 rounded-xl p-6 hover:border-emerald/50 transition-all duration-300 hover:shadow-lg hover:shadow-emerald-glow">
      <Link href={`/blog/${slug}`} className="block group">
        <h2 className="text-2xl font-semibold text-text-primary mb-2 group-hover:text-emerald transition-colors">
          {title}
        </h2>
      </Link>

      <div className="flex items-center gap-4 text-sm text-text-muted mb-3">
        <time dateTime={date}>{formattedDate}</time>
        {author && <span>by {author}</span>}
      </div>

      {excerpt && (
        <p className="text-text-secondary mb-4">{excerpt}</p>
      )}

      {tags && tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {tags.map((tag) => (
            <span
              key={tag}
              className="bg-slate-800 text-text-muted px-2 py-1 rounded text-sm border border-slate-700"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </article>
  );
}
