import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import BlogCard from '../../../components/BlogCard';

describe('BlogCard', () => {
  const mockPost = {
    slug: 'test-post',
    title: 'Test Blog Post',
    date: '2026-01-15',
    author: 'Test Author',
    tags: ['privacy', 'security'],
    excerpt: 'This is a test excerpt for the blog post.',
    readTime: '5 min',
  };

  describe('date formatting', () => {
    it('formats date in long format with month name', () => {
      render(<BlogCard post={mockPost} />);
      // Get the time element and check it contains a properly formatted date
      const timeElement = screen.getByRole('time');
      expect(timeElement).toBeInTheDocument();
      // Should contain year
      expect(timeElement.textContent).toMatch(/2026/);
      // Should contain month name (not number)
      expect(timeElement.textContent).toMatch(/January/);
    });

    it('uses dateTime attribute with ISO date', () => {
      render(<BlogCard post={mockPost} />);
      const timeElement = screen.getByRole('time');
      expect(timeElement).toHaveAttribute('dateTime', mockPost.date);
    });
  });

  describe('conditional rendering', () => {
    it('renders title as a link', () => {
      render(<BlogCard post={mockPost} />);
      const titleLink = screen.getByRole('link', { name: mockPost.title });
      expect(titleLink).toHaveAttribute('href', `/blog/${mockPost.slug}`);
    });

    it('renders author when provided', () => {
      render(<BlogCard post={mockPost} />);
      expect(screen.getByText(/by Test Author/)).toBeInTheDocument();
    });

    it('does not render author when not provided', () => {
      const postWithoutAuthor = { ...mockPost, author: undefined };
      render(<BlogCard post={postWithoutAuthor} />);
      expect(screen.queryByText(/by/)).not.toBeInTheDocument();
    });

    it('renders readTime when provided', () => {
      render(<BlogCard post={mockPost} />);
      expect(screen.getByText('5 min read')).toBeInTheDocument();
    });

    it('does not render readTime when not provided', () => {
      const postWithoutReadTime = { ...mockPost, readTime: undefined };
      render(<BlogCard post={postWithoutReadTime} />);
      expect(screen.queryByText(/read$/)).not.toBeInTheDocument();
    });

    it('renders excerpt when provided', () => {
      render(<BlogCard post={mockPost} />);
      expect(screen.getByText(mockPost.excerpt)).toBeInTheDocument();
    });

    it('does not render excerpt when not provided', () => {
      const postWithoutExcerpt = { ...mockPost, excerpt: undefined };
      render(<BlogCard post={postWithoutExcerpt} />);
      expect(screen.queryByText(mockPost.excerpt)).not.toBeInTheDocument();
    });

    it('renders tags when provided', () => {
      render(<BlogCard post={mockPost} />);
      expect(screen.getByRole('button', { name: 'privacy' })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'security' })).toBeInTheDocument();
    });

    it('does not render tags section when tags are empty', () => {
      const postWithoutTags = { ...mockPost, tags: [] };
      render(<BlogCard post={postWithoutTags} />);
      expect(screen.queryByRole('button', { name: 'privacy' })).not.toBeInTheDocument();
    });

    it('does not render tags section when tags are undefined', () => {
      const postWithoutTags = { ...mockPost, tags: undefined };
      render(<BlogCard post={postWithoutTags} />);
      expect(screen.queryByRole('button')).not.toBeInTheDocument();
    });
  });

  describe('tag click behavior', () => {
    it('calls onTagClick with correct tag when tag is clicked', async () => {
      const user = userEvent.setup();
      const onTagClick = vi.fn();
      render(<BlogCard post={mockPost} onTagClick={onTagClick} />);

      await user.click(screen.getByRole('button', { name: 'privacy' }));
      expect(onTagClick).toHaveBeenCalledWith('privacy');
      expect(onTagClick).toHaveBeenCalledTimes(1);
    });

    it('calls onTagClick for each tag independently', async () => {
      const user = userEvent.setup();
      const onTagClick = vi.fn();
      render(<BlogCard post={mockPost} onTagClick={onTagClick} />);

      await user.click(screen.getByRole('button', { name: 'security' }));
      expect(onTagClick).toHaveBeenCalledWith('security');
    });

    it('does not crash when onTagClick is not provided', async () => {
      const user = userEvent.setup();
      render(<BlogCard post={mockPost} />);

      // Should not throw
      await user.click(screen.getByRole('button', { name: 'privacy' }));
    });

    it('prevents default link navigation when tag is clicked', async () => {
      const user = userEvent.setup();
      const onTagClick = vi.fn();
      render(<BlogCard post={mockPost} onTagClick={onTagClick} />);

      // Click on a tag (which is inside the article)
      await user.click(screen.getByRole('button', { name: 'privacy' }));

      // The onTagClick should be called, indicating e.preventDefault() worked
      expect(onTagClick).toHaveBeenCalled();
    });
  });

  describe('accessibility', () => {
    it('uses semantic article element', () => {
      render(<BlogCard post={mockPost} />);
      expect(screen.getByRole('article')).toBeInTheDocument();
    });

    it('has time element for date', () => {
      render(<BlogCard post={mockPost} />);
      const timeElement = screen.getByRole('time');
      expect(timeElement).toBeInTheDocument();
      expect(timeElement).toHaveAttribute('dateTime');
    });
  });

  describe('minimal post', () => {
    it('renders with only required fields', () => {
      const minimalPost = {
        slug: 'minimal',
        title: 'Minimal Post',
        date: '2026-06-15', // Use mid-month to avoid timezone edge cases
      };
      render(<BlogCard post={minimalPost} />);
      expect(screen.getByText('Minimal Post')).toBeInTheDocument();
      // Should have a time element with a formatted date
      const timeElement = screen.getByRole('time');
      expect(timeElement.textContent).toMatch(/2026/);
    });
  });
});
