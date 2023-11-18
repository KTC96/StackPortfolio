/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./templates/**/*.html",
    "./templates/**/**/*.html",
    "./custom_account/templates/*.html",
    "./project/templates/*.html",
    "./job_post/templates/*.html",
  ],
  theme: {
    extend: {
      container: {
        center: true,
        DEFAULT: "1em",
        sm: ".5em",
      },
      colors: {
        aliceblue: "#f4f9ff",
      },
      fontFamily: {
        hind: ["Hind", "sans-serif"],
        martel: ["Martel Sans", "sans-serif"],
        maven: ["Maven Pro", "sans-serif"],
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
  daisyui: {
    themes: [
      {
        "stackportfolio-default-theme": {
          primary: "#0166ff",
          secondary: "#131e32",
          accent: "#1fb2a6",
          neutral: "#333333",
          "base-100": "#fcfcfd",
          info: "#3abff8",
          success: "#36d399",
          warning: "#fbbd23",
          error: "#f87272",
        },
      },
    ],
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
};
