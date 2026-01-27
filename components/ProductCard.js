import Link from 'next/link';
import { ProductIcon } from './icons';

export default function ProductCard({ name, description, docsUrl }) {
  const CardWrapper = docsUrl ? Link : 'div';
  const wrapperProps = docsUrl ? { href: docsUrl } : {};

  return (
    <CardWrapper
      {...wrapperProps}
      className="group block bg-slate-900 rounded-xl overflow-hidden border border-slate-700 hover:border-emerald/50 transition-all duration-150 ease-out hover:scale-[1.02] hover:shadow-lg hover:shadow-emerald-glow cursor-pointer"
    >
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
        <h3 className="text-xl font-bold text-text-primary mb-3 group-hover:text-emerald transition-colors duration-150">{name}</h3>
        <p className="text-text-secondary leading-relaxed">{description}</p>
      </div>
    </CardWrapper>
  );
}
