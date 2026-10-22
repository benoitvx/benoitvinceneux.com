import { readFileSync } from 'node:fs';
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

// Pages = entrées 200 sans point de legacy-urls.txt (comme tests/test_dist.py) + la 404.
const pages = readFileSync('tests/legacy-urls.txt', 'utf8').split('\n')
  .map((l) => l.split('\t'))
  .filter(([path, want]) => want === '200' && !path.includes('.'))
  .map(([path]) => (path === '/' ? 'index.html' : `${path.slice(1)}.html`))
  .concat('404.html');
// Exclusions : uniquement les entrées "axe" de l'allowlist (motif = sélecteur CSS retiré de l'analyse).
const axe: { page: string; motif: string }[] = JSON.parse(readFileSync('tests/parity-allowlist.json', 'utf8')).filter((e: { test: string }) => e.test === 'axe');

for (const file of pages) {
  test(`axe: ${file}`, async ({ page }) => {
    await page.goto(`/${file}`);
    const builder = new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']);
    for (const e of axe) {
      if (e.page !== '*' && `${e.page}.html` !== file) continue;
      expect(await page.locator(e.motif).count(), `allowlist axe : sélecteur mort ${e.motif}`).toBeGreaterThan(0);
      builder.exclude(e.motif);
    }
    const { violations } = await builder.analyze();
    const blocking = violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
    for (const v of violations.filter((v) => !blocking.includes(v))) console.log(`${file} [${v.impact}] ${v.id}`);
    expect(blocking.map((v) => `${file}: ${v.id} (${v.impact})`)).toEqual([]);
  });
}
