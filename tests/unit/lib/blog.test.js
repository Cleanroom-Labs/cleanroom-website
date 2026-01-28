import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

describe('lib/blog', () => {
  describe('extractPlainText', () => {
    // Since extractPlainText is not exported, we test its behavior through getAllPosts
    // But we can test the logic directly by implementing the same regex transformations
    const extractPlainText = (mdxContent) => {
      return mdxContent
        .replace(/```[\s\S]*?```/g, '') // code blocks
        .replace(/`[^`]*`/g, '') // inline code
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // links -> text only
        .replace(/^#{1,6}\s+/gm, '') // headers
        .replace(/\*\*?([^*]+)\*\*?/g, '$1') // bold/italic
        .replace(/<[^>]+>/g, '') // HTML tags
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase();
    };

    it('strips code blocks', () => {
      const input = 'Before ```javascript\nconst x = 1;\n``` After';
      expect(extractPlainText(input)).toBe('before after');
    });

    it('strips inline code', () => {
      const input = 'Use `npm install` to install';
      expect(extractPlainText(input)).toBe('use to install');
    });

    it('extracts text from markdown links', () => {
      const input = 'Check the [documentation](https://example.com) for details';
      expect(extractPlainText(input)).toBe('check the documentation for details');
    });

    it('strips headers', () => {
      const input = '# Title\n## Subtitle\nContent';
      expect(extractPlainText(input)).toBe('title subtitle content');
    });

    it('strips bold and italic', () => {
      const input = 'This is **bold** and *italic* text';
      expect(extractPlainText(input)).toBe('this is bold and italic text');
    });

    it('strips HTML tags', () => {
      const input = 'Text with <strong>HTML</strong> and <a href="#">links</a>';
      expect(extractPlainText(input)).toBe('text with html and links');
    });

    it('normalizes whitespace', () => {
      const input = 'Multiple   spaces\n\nand\nnewlines';
      expect(extractPlainText(input)).toBe('multiple spaces and newlines');
    });

    it('converts to lowercase', () => {
      const input = 'UPPERCASE and MixedCase';
      expect(extractPlainText(input)).toBe('uppercase and mixedcase');
    });

    it('handles complex markdown', () => {
      const input = `# Header

Some **bold** text with \`code\` and a [link](http://example.com).

\`\`\`javascript
const x = 1;
\`\`\`

More content here.`;
      const result = extractPlainText(input);
      expect(result).toContain('header');
      expect(result).toContain('bold text');
      expect(result).toContain('link');
      expect(result).toContain('more content');
      expect(result).not.toContain('const x');
      expect(result).not.toContain('javascript');
    });
  });

  describe('getAllTags', () => {
    let getAllTags;

    beforeEach(async () => {
      vi.resetModules();
      const blogModule = await import('../../../lib/blog.js');
      getAllTags = blogModule.getAllTags;
    });

    it('returns empty array for posts with no tags', () => {
      const posts = [
        { title: 'Post 1' },
        { title: 'Post 2' },
      ];
      expect(getAllTags(posts)).toEqual([]);
    });

    it('extracts unique tags from posts', () => {
      const posts = [
        { title: 'Post 1', tags: ['privacy', 'security'] },
        { title: 'Post 2', tags: ['privacy', 'tools'] },
      ];
      const tags = getAllTags(posts);
      expect(tags).toContain('privacy');
      expect(tags).toContain('security');
      expect(tags).toContain('tools');
      expect(tags).toHaveLength(3);
    });

    it('sorts tags alphabetically', () => {
      const posts = [
        { title: 'Post 1', tags: ['zebra', 'apple'] },
        { title: 'Post 2', tags: ['banana'] },
      ];
      const tags = getAllTags(posts);
      expect(tags).toEqual(['apple', 'banana', 'zebra']);
    });

    it('handles posts with empty tags array', () => {
      const posts = [
        { title: 'Post 1', tags: [] },
        { title: 'Post 2', tags: ['security'] },
      ];
      const tags = getAllTags(posts);
      expect(tags).toEqual(['security']);
    });

    it('handles mixed posts with and without tags', () => {
      const posts = [
        { title: 'Post 1', tags: ['privacy'] },
        { title: 'Post 2' },
        { title: 'Post 3', tags: null },
      ];
      const tags = getAllTags(posts);
      expect(tags).toEqual(['privacy']);
    });
  });

  describe('getAllPosts (integration with real files)', () => {
    // These tests use the real blog files in the repo
    let getAllPosts;

    beforeEach(async () => {
      vi.resetModules();
      const blogModule = await import('../../../lib/blog.js');
      getAllPosts = blogModule.getAllPosts;
    });

    it('reads mdx files from content/blog directory', () => {
      const posts = getAllPosts();
      expect(posts.length).toBeGreaterThan(0);
      posts.forEach(post => {
        expect(post).toHaveProperty('slug');
        expect(post).toHaveProperty('title');
        expect(post).toHaveProperty('date');
      });
    });

    it('includes searchContent for each post', () => {
      const posts = getAllPosts();
      posts.forEach(post => {
        expect(post).toHaveProperty('searchContent');
        expect(typeof post.searchContent).toBe('string');
        expect(post.searchContent.length).toBeGreaterThan(0);
      });
    });

    it('sorts posts by date descending (newest first)', () => {
      const posts = getAllPosts();
      for (let i = 1; i < posts.length; i++) {
        const prevDate = new Date(posts[i - 1].date);
        const currDate = new Date(posts[i].date);
        expect(prevDate.getTime()).toBeGreaterThanOrEqual(currDate.getTime());
      }
    });

    it('extracts frontmatter correctly', () => {
      const posts = getAllPosts();
      const introPost = posts.find(p => p.slug === 'introducing-airgap-tools');
      if (introPost) {
        expect(introPost.title).toBe('Privacy-First Tools for Air-Gapped Environments');
        expect(introPost.tags).toContain('privacy');
        expect(introPost.tags).toContain('security');
      }
    });
  });

  describe('getPostBySlug (integration with real files)', () => {
    let getPostBySlug;

    beforeEach(async () => {
      vi.resetModules();
      const blogModule = await import('../../../lib/blog.js');
      getPostBySlug = blogModule.getPostBySlug;
    });

    it('returns post with frontmatter and content', () => {
      const post = getPostBySlug('introducing-airgap-tools');
      expect(post.slug).toBe('introducing-airgap-tools');
      expect(post.frontmatter).toHaveProperty('title');
      expect(post.frontmatter).toHaveProperty('date');
      expect(post.frontmatter).toHaveProperty('tags');
      expect(post.content).toBeDefined();
      expect(post.content.length).toBeGreaterThan(0);
    });

    it('separates frontmatter from content', () => {
      const post = getPostBySlug('introducing-airgap-tools');
      // Content should not contain frontmatter delimiters
      expect(post.content).not.toMatch(/^---\s*\n/);
      // Content should have the actual post content
      expect(post.content).toContain('air-gapped');
    });

    it('parses frontmatter fields correctly', () => {
      const post = getPostBySlug('introducing-airgap-tools');
      expect(post.frontmatter.title).toBe('Privacy-First Tools for Air-Gapped Environments');
      expect(post.frontmatter.author).toBe('Lead Dev');
      expect(Array.isArray(post.frontmatter.tags)).toBe(true);
    });
  });

  describe('getAllSlugs (integration with real files)', () => {
    let getAllSlugs;

    beforeEach(async () => {
      vi.resetModules();
      const blogModule = await import('../../../lib/blog.js');
      getAllSlugs = blogModule.getAllSlugs;
    });

    it('returns array of slugs', () => {
      const slugs = getAllSlugs();
      expect(Array.isArray(slugs)).toBe(true);
      expect(slugs.length).toBeGreaterThan(0);
    });

    it('slugs do not include file extension', () => {
      const slugs = getAllSlugs();
      slugs.forEach(slug => {
        expect(slug).not.toContain('.mdx');
      });
    });

    it('includes known blog post slugs', () => {
      const slugs = getAllSlugs();
      expect(slugs).toContain('introducing-airgap-tools');
    });
  });
});
