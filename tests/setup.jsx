import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock Next.js router
vi.mock('next/router', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    query: {},
    asPath: '/blog',
    isReady: true,
  }),
}));

// Mock Next.js Link - pass through all props including className
vi.mock('next/link', () => ({
  default: ({ children, href, className, ...props }) => (
    <a href={href} className={className} {...props}>{children}</a>
  ),
}));
