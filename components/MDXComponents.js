import Link from 'next/link';

const MDXComponents = {
  h1: (props) => (
    <h1 className="text-4xl font-bold mt-8 mb-4" {...props} />
  ),
  h2: (props) => (
    <h2 className="text-2xl font-semibold mt-8 mb-4" {...props} />
  ),
  h3: (props) => (
    <h3 className="text-xl font-semibold mt-6 mb-3" {...props} />
  ),
  p: (props) => (
    <p className="mb-4 leading-relaxed" {...props} />
  ),
  ul: (props) => (
    <ul className="list-disc pl-6 mb-4 space-y-2" {...props} />
  ),
  ol: (props) => (
    <ol className="list-decimal pl-6 mb-4 space-y-2" {...props} />
  ),
  li: (props) => (
    <li className="leading-relaxed pl-2" {...props} />
  ),
  a: ({ href, children, ...props }) => {
    const isInternal = href && (href.startsWith('/') || href.startsWith('#'));
    if (isInternal) {
      return (
        <Link href={href} className="text-emerald hover:text-emerald-light transition-colors" {...props}>
          {children}
        </Link>
      );
    }
    return (
      <a
        href={href}
        className="text-emerald hover:text-emerald-light transition-colors"
        target="_blank"
        rel="noopener noreferrer"
        {...props}
      >
        {children}
      </a>
    );
  },
  blockquote: (props) => (
    <blockquote
      className="border-l-4 border-gray-300 pl-4 my-4 italic text-gray-700"
      {...props}
    />
  ),
  code: ({ className, children, ...props }) => {
    const isInline = !className;
    // Strip any stray backticks that might pass through
    const cleanChildren = typeof children === 'string'
      ? children.replace(/^`|`$/g, '')
      : children;
    if (isInline) {
      return (
        <code
          className="bg-slate-800 text-slate-200 px-1.5 py-0.5 rounded text-sm font-mono border border-slate-700"
          {...props}
        >
          {cleanChildren}
        </code>
      );
    }
    return (
      <code className={className} {...props}>
        {cleanChildren}
      </code>
    );
  },
  pre: (props) => (
    <pre
      className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto mb-4 text-sm"
      {...props}
    />
  ),
  hr: () => (
    <hr className="my-8 border-t border-slate-700" />
  ),
  strong: (props) => (
    <strong className="font-semibold" {...props} />
  ),
  em: (props) => (
    <em className="italic" {...props} />
  ),
};

export default MDXComponents;
