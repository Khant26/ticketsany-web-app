import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
// Only VITE_* variables are exposed to client code (via import.meta.env).
// Do not inject process.env here: that would bake every build-time
// environment variable (including secrets) into the public bundle.
export default defineConfig({
  plugins: [react(), tailwindcss()],
})
