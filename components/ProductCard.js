import Link from 'next/link';
import { ProductIcon } from './icons';

export default function ProductCard({ name, description, docsUrl, status = 'active' }) {
  const isPlanned = status === 'planned';
  const CardWrapper = docsUrl ? Link : 'div';
  const wrapperProps = docsUrl ? { href: docsUrl } : {};

  // Style variations based on status
  const borderClass = isPlanned
    ? 'border-dashed border-slate-600 hover:border-slate-500'
    : 'border-slate-700 hover:border-emerald/50';
  const iconColorClass = isPlanned ? 'text-slate-500' : 'text-emerald';
  const hoverGlowClass = isPlanned ? '' : 'hover:shadow-emerald-glow';
  const titleHoverClass = isPlanned ? '' : 'group-hover:text-emerald';

  return (
    <CardWrapper
      {...wrapperProps}
      className={`group block bg-slate-900 rounded-xl overflow-hidden border ${borderClass} transition-all duration-150 ease-out hover:scale-[1.02] hover:shadow-lg ${hoverGlowClass} cursor-pointer`}
    >
      {/* Icon area */}
      <div className="h-32 flex items-center justify-center bg-slate-800/50 relative overflow-hidden">
        {/* Subtle glow effect on hover (active only) */}
        {!isPlanned && (
          <div className="absolute inset-0 bg-emerald/0 group-hover:bg-emerald/5 transition-colors duration-150 ease-out" />
        )}

        <div className={`${iconColorClass} transition-transform duration-150 ease-out group-hover:scale-110`}>
          <ProductIcon productName={name} className="w-16 h-16" />
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        <h3 className={`text-xl font-bold text-text-primary mb-1 ${titleHoverClass} transition-colors duration-150`}>{name}</h3>
        {isPlanned && (
          <span className="inline-block text-xs font-semibold uppercase tracking-wide text-amber-500 mb-2">Planned</span>
        )}
        <p className="text-text-secondary leading-relaxed">{description}</p>
      </div>
    </CardWrapper>
  );
}
