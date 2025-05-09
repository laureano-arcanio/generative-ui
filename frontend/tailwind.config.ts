/** @type {import('tailwindcss').Config} */


export default {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
      extend: {
        colors: {
          "tempus-gray": "#2c2c2c",
          "tempus-teal-dark": "#204852",
          "tempus-teal": "#0a6f75",
          "tempus-teal-light": "#e2eced",
          "tempus-orange": "#f3d6bc",
        },
      },
    },
    corePlugins: {
      preflight: false,
    },
    important: "#root",
    plugins: [],
  };