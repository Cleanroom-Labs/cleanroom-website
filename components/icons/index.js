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
        strokeWidth="2.5"
        strokeDasharray="4 3"
        opacity="0.4"
      />
      {/* Up arrow */}
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
      {/* Down arrow */}
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
      />
    </svg>
  );
}

export function DeployIcon({ className = "w-12 h-12" }) {
  return (
    <svg className={className} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Dotted circle boundary */}
      <circle
        cx="24"
        cy="24"
        r="20"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeDasharray="4 3"
        opacity="0.4"
      />
      {/* Package box - back edges with opacity */}
      <path
        d="M10 18L24 10L38 18"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
        opacity="0.7"
      />
      <path
        d="M10 18V32L24 40V26"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
        opacity="0.7"
      />
      {/* Package box - front edges */}
      <path
        d="M24 26L38 18V32L24 40"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
      />
      {/* Box top surface */}
      <path
        d="M10 18L24 26L38 18"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function WhisperIcon({ className = "w-12 h-12" }) {
  return (
    <svg className={className} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Dotted circle boundary */}
      <circle
        cx="24"
        cy="24"
        r="20"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeDasharray="4 3"
        opacity="0.4"
      />
      {/* Central circle - sound source */}
      <circle
        cx="16"
        cy="24"
        r="5"
        stroke="currentColor"
        strokeWidth="2.5"
        fill="none"
      />
      {/* Concentric sound wave arcs */}
      <path
        d="M24 17a10 10 0 0 1 0 14"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M30 13a16 16 0 0 1 0 22"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        fill="none"
        opacity="0.7"
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
