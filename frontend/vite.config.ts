import path from 'path';
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  server: {
    host: "0.0.0.0", // Listen on all network interfaces
    port: 3000, // The port number should match the Docker container's internal port
  },

  resolve: {
    alias: {
      "@src": path.resolve(__dirname, "src"),
      // "@utils": path.resolve(__dirname, "src/utils"),
    },
  },

  build: {
    sourcemap: true,
  },

})
