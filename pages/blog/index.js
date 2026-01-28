import { useState, useMemo, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../components/Layout';
import BlogCard from '../../components/BlogCard';
import BlogFilters from '../../components/BlogFilters';
import BlogEmptyState from '../../components/BlogEmptyState';
import { getAllPosts, getAllTags } from '../../lib/blog';
import { DashedCircle } from '../../components/icons';

export default function Blog({ posts, allTags }) {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [isInitialized, setIsInitialized] = useState(false);
  const [showMobileFilters, setShowMobileFilters] = useState(false);

  const hasActiveFilters = searchQuery || selectedTags.length > 0;
  const activeFilterCount = (searchQuery ? 1 : 0) + selectedTags.length;

  // Initialize state from URL query params on mount
  useEffect(() => {
    if (router.isReady && !isInitialized) {
      const { q, tags } = router.query;
      if (q) setSearchQuery(q);
      if (tags) {
        const tagArray = Array.isArray(tags) ? tags : tags.split(',');
        setSelectedTags(tagArray.filter((t) => allTags.includes(t)));
      }
      setIsInitialized(true);
    }
  }, [router.isReady, router.query, allTags, isInitialized]);

  // Update URL when filters change (after initialization)
  useEffect(() => {
    if (!isInitialized) return;

    const query = {};
    if (searchQuery) query.q = searchQuery;
    if (selectedTags.length > 0) query.tags = selectedTags.join(',');

    const hasQuery = Object.keys(query).length > 0;
    const currentPath = router.asPath.split('?')[0];

    router.replace(
      {
        pathname: currentPath,
        query: hasQuery ? query : undefined,
      },
      undefined,
      { shallow: true }
    );
  }, [searchQuery, selectedTags, isInitialized]);

  // Filter posts based on search query and selected tags
  const filteredPosts = useMemo(() => {
    return posts.filter((post) => {
      // Text search: match against title, excerpt, or content
      const query = searchQuery.toLowerCase();
      const matchesSearch =
        !searchQuery ||
        post.title.toLowerCase().includes(query) ||
        (post.excerpt && post.excerpt.toLowerCase().includes(query)) ||
        (post.searchContent && post.searchContent.includes(query));

      // Tag filter: post must have ALL selected tags (AND logic)
      const matchesTags =
        selectedTags.length === 0 ||
        selectedTags.every((tag) => post.tags && post.tags.includes(tag));

      return matchesSearch && matchesTags;
    });
  }, [posts, searchQuery, selectedTags]);

  const handleTagClick = (tag) => {
    if (!selectedTags.includes(tag)) {
      setSelectedTags((prev) => [...prev, tag]);
    }
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedTags([]);
  };

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
        <div className="container mx-auto px-4 max-w-6xl">
          <h1 className="text-4xl font-bold text-text-primary mb-4">Blog</h1>
          <p className="text-text-secondary mb-8">
            News, updates, and articles about air-gapped computing and privacy-first software.
          </p>

          {/* Mobile filter toggle - visible only on small screens */}
          <button
            onClick={() => setShowMobileFilters(!showMobileFilters)}
            className="md:hidden mb-6 flex items-center gap-2 px-4 py-2 bg-slate-800 rounded-lg text-text-secondary hover:text-text-primary transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Filters {hasActiveFilters && `(${activeFilterCount})`}
          </button>

          {/* Mobile filter overlay */}
          {showMobileFilters && (
            <div className="md:hidden fixed inset-0 z-50 bg-slate-950/95 px-6 pt-20 pb-6 overflow-y-auto">
              <BlogFilters
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                selectedTags={selectedTags}
                setSelectedTags={setSelectedTags}
                allTags={allTags}
                filteredCount={filteredPosts.length}
                totalCount={posts.length}
                onClose={() => setShowMobileFilters(false)}
                showCloseButton={true}
              />
            </div>
          )}

          {/* Tablet: inline filters - visible on md-xl screens */}
          <div className="hidden md:block xl:hidden mb-8">
            <BlogFilters
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              selectedTags={selectedTags}
              setSelectedTags={setSelectedTags}
              allTags={allTags}
              filteredCount={filteredPosts.length}
              totalCount={posts.length}
            />
          </div>

          {/* Blog posts - with right padding on xl screens to avoid fixed sidebar */}
          <div className="flex xl:pr-48">
            <div className="flex-1 min-w-0">
              {filteredPosts.length > 0 ? (
                <div className="space-y-6">
                  {filteredPosts.map((post) => (
                    <BlogCard key={post.slug} post={post} onTagClick={handleTagClick} />
                  ))}
                </div>
              ) : (
                <BlogEmptyState onClear={clearFilters} />
              )}
            </div>
          </div>

          {/* Right: Fixed filter sidebar - positioned on right edge, only on xl+ screens */}
          <div className="w-56 hidden xl:block fixed top-32 right-8">
            <BlogFilters
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              selectedTags={selectedTags}
              setSelectedTags={setSelectedTags}
              allTags={allTags}
              filteredCount={filteredPosts.length}
              totalCount={posts.length}
            />
          </div>
        </div>
      </main>
    </Layout>
  );
}

export async function getStaticProps() {
  const posts = getAllPosts();
  const allTags = getAllTags(posts);
  return {
    props: {
      posts,
      allTags,
    },
  };
}
