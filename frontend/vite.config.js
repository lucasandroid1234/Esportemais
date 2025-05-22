import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      external: [
        '@rollup/rollup-linux-x64-gnu',
        '@rollup/rollup-linux-x64-musl'
      ],
      output: {
        manualChunks: {
          react: ['react', 'react-dom'],
          vendor: ['react-toastify', 'axios']
        }
      }
    }
  }
})