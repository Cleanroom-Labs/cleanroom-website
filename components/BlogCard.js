import Link from 'next/link';

export default function BlogCard({ post, onTagClick }) {
  const { slug, title, date, author, tags, excerpt, readTime } = post;

  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <article className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 hover:border-emerald/50 hover:bg-slate-800/70 transition-all duration-300 hover:shadow-lg hover:shadow-emerald-glow">
      <Link href={`/blog/${slug}`} className="block group">
        <h2 className="text-2xl font-semibold text-text-primary mb-2 group-hover:text-emerald transition-colors">
          {title}
        </h2>
      </Link>

      <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-text-muted mb-3">
        <time dateTime={date} className="whitespace-nowrap">{formattedDate}</time>
        {author && (
          <>
            <span>•</span>
            <span className="whitespace-nowrap">by {author}</span>
          </>
        )}
        {readTime && (
          <>
            <span>•</span>
            <span className="whitespace-nowrap">{readTime} read</span>
          </>
        )}
      </div>

      {excerpt && (
        <p className="text-text-secondary mb-4">{excerpt}</p>
      )}

      {tags && tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {tags.map((tag) => (
            <button
              key={tag}
              onClick={(e) => {
                e.preventDefault();
                if (onTagClick) onTagClick(tag);
              }}
              className="bg-slate-800 text-text-muted px-2 py-1 rounded text-sm border border-slate-700 hover:border-emerald/50 hover:text-emerald transition-colors"
            >
              {tag}
            </button>
          ))}
        </div>
      )}
    </article>
  );
}
