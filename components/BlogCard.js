import Link from 'next/link';

export default function BlogCard({ post }) {
  const { slug, title, date, author, tags, excerpt } = post;

  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <article className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
      <Link href={`/blog/${slug}`} className="block group">
        <h2 className="text-2xl font-semibold mb-2 group-hover:text-blue-600 transition-colors">
          {title}
        </h2>
      </Link>

      <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
        <time dateTime={date}>{formattedDate}</time>
        {author && <span>by {author}</span>}
      </div>

      {excerpt && (
        <p className="text-gray-600 mb-4">{excerpt}</p>
      )}

      {tags && tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {tags.map((tag) => (
            <span
              key={tag}
              className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-sm"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </article>
  );
}
