/** @type {import('tailwindcss').Config} */
const designPreset = require('./cleanroom-design-system/tailwind/preset');
const tokens = require('./cleanroom-design-system/tokens/colors');

module.exports = {
  presets: [designPreset],
  content: [
    './pages/**/*.{js,jsx}',
    './components/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      // Website-specific extensions (animations, typography styling)
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'float-delayed': 'float 6s ease-in-out infinite 3s',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        },
      },
      typography: {
        DEFAULT: {
          css: {
            color: tokens.colors['text-secondary'],
            h1: { color: tokens.colors['text-primary'] },
            h2: { color: tokens.colors['text-primary'] },
            h3: { color: tokens.colors['text-primary'] },
            h4: { color: tokens.colors['text-primary'] },
            strong: { color: tokens.colors['text-primary'] },
            a: {
              color: tokens.colors['emerald'],
              textDecoration: 'underline',
              '&:hover': {
                color: tokens.colors['emerald-light'],
              },
            },
            code: {
              color: tokens.colors['code-text'],
              '&::before': { content: 'none' },
              '&::after': { content: 'none' },
            },
            blockquote: {
              color: tokens.colors['text-muted'],
              borderLeftColor: tokens.colors['emerald'],
            },
            hr: { borderColor: tokens.colors['slate-700'] },
            'ul > li::marker': { color: tokens.colors['emerald'] },
            'ol > li::marker': { color: tokens.colors['emerald'] },
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
