import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

// Shared base configuration
const baseConfig = {
  plugins: [vue()],
  css: {
    preprocessorOptions: {
      sass: {
        // To fix Deprecation [legacy-js-api]: The legacy JS API is deprecated
        // More info: https://sass-lang.com/d/legacy-js-api
        api: 'modern-compiler', // or 'modern'
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
};

export default defineConfig({
  ...baseConfig,
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: path.resolve(__dirname, 'index.html'),
    },
  },
});
