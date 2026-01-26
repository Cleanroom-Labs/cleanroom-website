import Link from 'next/link';
import { ProductIcon } from './icons';

export default function ProductCard({ name, description, docsUrl }) {
  return (
    <div className="group bg-slate-900 rounded-xl overflow-hidden border border-slate-700 hover:border-emerald/50 transition-all duration-150 ease-out hover:scale-[1.02] hover:shadow-lg hover:shadow-emerald-glow">
      {/* Icon area */}
      <div className="h-32 flex items-center justify-center bg-slate-800/50 relative overflow-hidden">
        {/* Subtle glow effect on hover */}
        <div className="absolute inset-0 bg-emerald/0 group-hover:bg-emerald/5 transition-colors duration-150 ease-out" />

        <div className="text-emerald transition-transform duration-150 ease-out group-hover:scale-110">
          <ProductIcon productName={name} className="w-16 h-16" />
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        <h3 className="text-xl font-bold text-text-primary mb-3">{name}</h3>
        <p className="text-text-secondary mb-4 leading-relaxed">{description}</p>

        {docsUrl && (
          <Link
            href={docsUrl}
            className="inline-flex items-center text-emerald hover:text-emerald-light transition-colors duration-150 ease-out font-medium"
          >
            Learn more
            <svg className="ml-1 w-4 h-4 transition-transform duration-150 ease-out group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        )}
      </div>
    </div>
  );
}
