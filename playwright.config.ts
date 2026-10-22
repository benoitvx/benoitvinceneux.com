import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: 'tests/e2e',
  workers: 1, // http.server de la stdlib refuse des connexions sous charge parallèle
  use: { baseURL: 'http://127.0.0.1:4321' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } } }],
  webServer: {
    command: 'python3 -I -m http.server -b 127.0.0.1 -d dist 4321',
    url: 'http://127.0.0.1:4321',
    reuseExistingServer: false,
  },
});
