export default function BlogEmptyState({ onClear }) {
  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-12 text-center">
      <svg
        className="w-16 h-16 mx-auto text-text-muted mb-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <h3 className="text-xl font-semibold text-text-primary mb-2">
        No posts found
      </h3>
      <p className="text-text-secondary mb-6">
        Try adjusting your search or filter criteria.
      </p>
      <button
        onClick={onClear}
        className="inline-flex items-center gap-2 px-4 py-2 bg-emerald text-white rounded-lg hover:bg-emerald-light transition-colors"
      >
        <svg
          className="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
        Clear filters
      </button>
    </div>
  );
}
