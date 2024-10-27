/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  darkMode: 'selector',
  theme: {
    fontFamily: {
      lato: ["Lato", "sans-serif"],
    },
    extend: {
      colors: {
        primary: "#366AA7",
        secondary: "#4D5770", 
        tertiary : "#374151",
        bgColor : "#F0F0F0B0",
        borderColor : "#D9D9D9",
        textColor: "#1f2937",          
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

