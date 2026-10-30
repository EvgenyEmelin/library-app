import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Всё, что начинается с /api, Vite проксирует на бекенд.
      // Браузер думает, что это тот же origin → никакого CORS не нужно.
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
});