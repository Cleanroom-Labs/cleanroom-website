// Product Icons for Cleanroom Labs
// Icons sourced from cleanroom-theme - single source of truth
import { iconPaths, projectToIcon, chevronPaths, dashedCirclePresets } from '../../theme/icons';

function renderIcon(iconName, className) {
  const icon = iconPaths[iconName];
  if (!icon) return null;

  return (
    <svg className={className} viewBox={icon.viewBox} fill="none" xmlns="http://www.w3.org/2000/svg">
      {icon.elements.map((el, i) => {
        const Element = el.type;
        return <Element key={i} stroke="currentColor" fill="none" {...el.props} />;
      })}
    </svg>
  );
}

export function TransferIcon({ className = "w-12 h-12" }) {
  return renderIcon('transfer', className);
}

export function DeployIcon({ className = "w-12 h-12" }) {
  return renderIcon('deploy', className);
}

export function WhisperIcon({ className = "w-12 h-12" }) {
  return renderIcon('whisper', className);
}

export function ProductIcon({ productName, className = "w-12 h-12" }) {
  const iconName = projectToIcon[productName];
  return iconName ? renderIcon(iconName, className) : null;
}

export function ChevronIcon({ direction = "right", className = "w-4 h-4" }) {
  const path = chevronPaths[direction];
  if (!path) return null;

  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={path.d} />
    </svg>
  );
}

export function DashedCircle({ preset = "large", className, color = "#10b981" }) {
  const config = dashedCirclePresets[preset];
  if (!config) return null;

  return (
    <svg className={className} viewBox="0 0 100 100">
      <circle
        cx="50"
        cy="50"
        r={config.r}
        fill="none"
        stroke={color}
        strokeWidth={config.strokeWidth}
        strokeDasharray={config.strokeDasharray}
      />
    </svg>
  );
}
