/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html", "./templates/**/*.html"],
  theme: {
    extend: {
      container: {
        center: true,
        DEFAULT: "1em",
        sm: ".5em",
      },
      colors: {
        aliceblue: "#eff7ff",
      },
      screens: {
        sm: "320px",
        md: "728px",
        lg: "984px",
        xl: "1240px",
        "2xl": "1496px",
      },
    },
  },
  plugins: [require("daisyui")],
};
