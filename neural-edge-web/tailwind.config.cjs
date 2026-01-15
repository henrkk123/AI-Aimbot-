/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        accent: "#00ffff",
        primary: "#6366f1"
      }
    },
  },
  plugins: [],
}
