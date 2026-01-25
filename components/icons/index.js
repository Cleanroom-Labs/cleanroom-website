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
      {/* Head silhouette */}
      <path
        d="M16 36V28C16 20 20 14 28 14C28 14 32 14 32 20V24C32 28 30 32 26 34L24 36"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        opacity="0.8"
      />
      {/* Ear area */}
      <circle
        cx="14"
        cy="24"
        r="3"
        stroke="currentColor"
        strokeWidth="2"
        fill="none"
      />
      {/* Sound waves - shifted left to fit in viewBox */}
      <path
        d="M34 18C36 20 37 22 37 24C37 26 36 28 34 30"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.7"
      />
      <path
        d="M38 15C40 18 41 21 41 24C41 27 40 30 38 33"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.5"
      />
      <path
        d="M42 12C44 15 45 19 45 24C45 29 44 33 42 36"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.3"
      />
      {/* Microphone dot */}
      <circle
        cx="20"
        cy="26"
        r="2"
        fill="currentColor"
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
