// Product Icons for Cleanroom Labs
// All icons designed for emerald accent color scheme

export function TransferIcon({ className = "w-12 h-12" }) {
  return (
    <svg className={className} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Dotted circle boundary representing air gap */}
      <circle
        cx="24"
        cy="24"
        r="20"
        stroke="currentColor"
        strokeWidth="2"
        strokeDasharray="4 3"
        opacity="0.5"
      />
      {/* Two arrows in circular motion */}
      <path
        d="M16 18L24 10L32 18"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M24 10V28"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
      />
      <path
        d="M32 30L24 38L16 30"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M24 38V20"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        opacity="0"
      />
    </svg>
  );
}

export function DeployIcon({ className = "w-12 h-12" }) {
  return (
    <svg className={className} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Package box - moved down to make room for arrow */}
      <path
        d="M10 20L24 12L38 20V34L24 42L10 34V20Z"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
      />
      {/* Box center line */}
      <path
        d="M24 26V42"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
      />
      <path
        d="M10 20L24 26L38 20"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
      />
      {/* Upward arrow - clearly above the box */}
      <path
        d="M24 3V10"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
      />
      <path
        d="M19 7L24 2L29 7"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function WhisperIcon({ className = "w-12 h-12" }) {
  return (
    <svg className={className} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Central circle - sound source */}
      <circle
        cx="18"
        cy="24"
        r="6"
        stroke="currentColor"
        strokeWidth="2.5"
        fill="none"
      />
      {/* Inner dot */}
      <circle
        cx="18"
        cy="24"
        r="2"
        fill="currentColor"
      />
      {/* Concentric sound wave arcs */}
      <path
        d="M26 16a12 12 0 0 1 0 16"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M32 12a18 18 0 0 1 0 24"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        fill="none"
        opacity="0.7"
      />
      <path
        d="M38 8a24 24 0 0 1 0 32"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        fill="none"
        opacity="0.4"
      />
    </svg>
  );
}

// Icon component that selects the appropriate icon based on product name
export function ProductIcon({ productName, className = "w-12 h-12" }) {
  switch (productName) {
    case 'AirGap Transfer':
      return <TransferIcon className={className} />;
    case 'AirGap Deploy':
      return <DeployIcon className={className} />;
    case 'Cleanroom Whisper':
      return <WhisperIcon className={className} />;
    default:
      return null;
  }
}
