/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#fbf7f4',
          100: '#f5ebe4',
          200: '#ebd8cc',
          300: '#dcbcaa',
          400: '#c89a80',
          500: '#b87f62',
          600: '#aa6c51',
          700: '#8e5641',
          800: '#734737',
          900: '#5e3c30',
          950: '#321e18',
        }
      }
    },
  },
  plugins: [],
}
