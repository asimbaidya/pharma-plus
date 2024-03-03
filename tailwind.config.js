/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pharma_plus/templates/*.html",
    "./pharma_plus/templates/components/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["corporate"],
  },
};
