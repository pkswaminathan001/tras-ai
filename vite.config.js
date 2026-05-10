import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/tras-ai/',
  build: {
    outDir: 'dist'
  }
})
