import { useEffect, useRef } from 'react';

export default function BlogFilters({
  searchQuery,
  setSearchQuery,
  selectedTags,
  setSelectedTags,
  allTags,
  filteredCount,
  totalCount,
  onClose,
  showCloseButton,
}) {
  const inputRef = useRef(null);
  const hasFilters = searchQuery || selectedTags.length > 0;

  const toggleTag = (tag) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedTags([]);
    if (inputRef.current) {
      inputRef.current.value = '';
    }
  };

  // Sync input value with searchQuery (for URL-initialized state)
  useEffect(() => {
    if (inputRef.current && inputRef.current.value !== searchQuery) {
      inputRef.current.value = searchQuery;
    }
  }, [searchQuery]);

  return (
    <div className="space-y-4">
      {/* Mobile close button */}
      {showCloseButton && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-text-primary font-medium">Filters</span>
          <button
            onClick={onClose}
            className="p-1 text-text-muted hover:text-text-primary transition-colors"
            aria-label="Close filters"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}

      {/* Search input */}
      <div className="relative">
        <svg
          className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <input
          ref={inputRef}
          type="text"
          placeholder="Search..."
          defaultValue={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full h-9 bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-lg py-1.5 pl-8 pr-3 text-sm text-text-primary placeholder-text-muted focus:border-emerald focus:ring-1 focus:ring-emerald focus:outline-none transition-colors"
        />
      </div>

      {/* Tags - wrapped in column */}
      {allTags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {allTags.map((tag) => {
            const isActive = selectedTags.includes(tag);
            return (
              <button
                key={tag}
                onClick={() => toggleTag(tag)}
                className={`px-2 py-1 rounded text-sm transition-all duration-200 ${
                  isActive
                    ? 'bg-emerald text-white shadow-lg shadow-emerald-glow'
                    : 'bg-slate-800 text-text-muted border border-slate-700 hover:border-emerald/50 hover:text-text-secondary'
                }`}
              >
                {tag}
              </button>
            );
          })}
        </div>
      )}

      {/* Results count and clear - always visible when filtering */}
      {hasFilters && (
        <div className="pt-3 border-t border-slate-700 space-y-2">
          <p className="text-text-muted text-sm">
            Showing {filteredCount} of {totalCount} post{totalCount !== 1 ? 's' : ''}
          </p>
          <button
            onClick={clearFilters}
            className="text-sm text-emerald hover:text-emerald-light transition-colors"
          >
            Clear filters
          </button>
        </div>
      )}
    </div>
  );
}
