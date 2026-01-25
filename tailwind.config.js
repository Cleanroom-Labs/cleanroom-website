/** @type {import('tailwindcss').Config} */
const designPreset = require('./cleanroom-design-system/tailwind/preset');

module.exports = {
  presets: [designPreset],
  content: [
    './pages/**/*.{js,jsx}',
    './components/**/*.{js,jsx}',
  ],
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
