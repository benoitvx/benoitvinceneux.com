import { defineConfig } from 'astro/config';

export default defineConfig({
  build: { format: 'file' },
  trailingSlash: 'never',
  compressHTML: false,
  markdown: { smartypants: false },
});
