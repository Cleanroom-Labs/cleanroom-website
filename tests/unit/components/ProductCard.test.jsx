import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ProductCard from '../../../components/ProductCard';

describe('ProductCard', () => {
  const activeProduct = {
    name: 'AirGap Transfer',
    description: 'Secure data transfer for moving files between air-gapped systems.',
    docsUrl: '/docs/airgap-transfer/readme.html',
    status: 'active',
  };

  const plannedProduct = {
    name: 'Cleanroom Whisper',
    description: 'Private voice transcription powered by local AI.',
    docsUrl: '/docs/cleanroom-whisper/readme.html',
    status: 'planned',
  };

  describe('active products', () => {
    it('renders as a link when docsUrl is provided', () => {
      render(<ProductCard {...activeProduct} />);
      const link = screen.getByRole('link');
      expect(link).toHaveAttribute('href', activeProduct.docsUrl);
    });

    it('displays product name', () => {
      render(<ProductCard {...activeProduct} />);
      expect(screen.getByText(activeProduct.name)).toBeInTheDocument();
    });

    it('displays product description', () => {
      render(<ProductCard {...activeProduct} />);
      expect(screen.getByText(activeProduct.description)).toBeInTheDocument();
    });

    it('does not show "Planned" badge', () => {
      render(<ProductCard {...activeProduct} />);
      expect(screen.queryByText('Planned')).not.toBeInTheDocument();
    });

    it('applies non-dashed border styling', () => {
      render(<ProductCard {...activeProduct} />);
      const link = screen.getByRole('link');
      const className = link.className;
      // Active products should not have border-dashed
      expect(className).not.toContain('border-dashed');
    });

    it('has emerald hover glow effect class', () => {
      render(<ProductCard {...activeProduct} />);
      const link = screen.getByRole('link');
      const className = link.className;
      expect(className).toContain('hover:shadow-emerald-glow');
    });
  });

  describe('planned products', () => {
    it('shows "Planned" badge', () => {
      render(<ProductCard {...plannedProduct} />);
      expect(screen.getByText('Planned')).toBeInTheDocument();
    });

    it('applies dashed border styling', () => {
      render(<ProductCard {...plannedProduct} />);
      const link = screen.getByRole('link');
      const className = link.className;
      expect(className).toContain('border-dashed');
    });

    it('does not have emerald hover glow effect', () => {
      render(<ProductCard {...plannedProduct} />);
      const link = screen.getByRole('link');
      const className = link.className;
      expect(className).not.toContain('hover:shadow-emerald-glow');
    });

    it('renders as link when docsUrl is provided', () => {
      render(<ProductCard {...plannedProduct} />);
      const link = screen.getByRole('link');
      expect(link).toHaveAttribute('href', plannedProduct.docsUrl);
    });
  });

  describe('products without docsUrl', () => {
    it('renders as div instead of link', () => {
      const productWithoutUrl = {
        name: 'Future Tool',
        description: 'A tool for the future.',
        status: 'planned',
      };
      render(<ProductCard {...productWithoutUrl} />);
      expect(screen.queryByRole('link')).not.toBeInTheDocument();
      expect(screen.getByText('Future Tool')).toBeInTheDocument();
    });
  });

  describe('default status', () => {
    it('defaults to active status when not specified', () => {
      const productWithoutStatus = {
        name: 'Default Product',
        description: 'A product with default status.',
        docsUrl: '/docs/test',
      };
      render(<ProductCard {...productWithoutStatus} />);
      expect(screen.queryByText('Planned')).not.toBeInTheDocument();
      const link = screen.getByRole('link');
      expect(link.className).not.toContain('border-dashed');
    });
  });

  describe('styling variations', () => {
    it('active product has emerald icon color', () => {
      const { container } = render(<ProductCard {...activeProduct} />);
      // Check that the icon container has text-emerald class
      const iconContainer = container.querySelector('.text-emerald');
      expect(iconContainer).toBeInTheDocument();
    });

    it('planned product has slate icon color', () => {
      const { container } = render(<ProductCard {...plannedProduct} />);
      const iconContainer = container.querySelector('.text-slate-500');
      expect(iconContainer).toBeInTheDocument();
    });

    it('active product icon area has hover glow background', () => {
      const { container } = render(<ProductCard {...activeProduct} />);
      // Active products have a div with emerald/0 to emerald/5 transition
      const glowDiv = container.querySelector('.group-hover\\:bg-emerald\\/5');
      expect(glowDiv).toBeInTheDocument();
    });

    it('planned product icon area does not have hover glow', () => {
      const { container } = render(<ProductCard {...plannedProduct} />);
      const glowDiv = container.querySelector('.group-hover\\:bg-emerald\\/5');
      expect(glowDiv).not.toBeInTheDocument();
    });
  });

  describe('content structure', () => {
    it('renders product name as heading', () => {
      render(<ProductCard {...activeProduct} />);
      const heading = screen.getByRole('heading', { name: activeProduct.name });
      expect(heading).toBeInTheDocument();
      expect(heading.tagName).toBe('H3');
    });

    it('renders description as paragraph', () => {
      render(<ProductCard {...activeProduct} />);
      const description = screen.getByText(activeProduct.description);
      expect(description.tagName).toBe('P');
    });
  });
});
