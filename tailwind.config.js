/** @type {import('tailwindcss').Config} */
const themePreset = require('./common/tailwind/preset');

module.exports = {
  presets: [themePreset],
  content: [
    './pages/**/*.{js,jsx}',
    './components/**/*.{js,jsx}',
  ],
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
