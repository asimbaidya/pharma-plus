/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pharma_plus/templates/*.html"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["corporate"],
  },
};
