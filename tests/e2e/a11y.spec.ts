import { readdirSync } from 'node:fs';
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const pages = (readdirSync('dist', { recursive: true }) as string[]).filter((f) => f.endsWith('.html'));

for (const file of pages) {
  test(`axe: ${file}`, async ({ page }) => {
    await page.goto(`/${file}`);
    const { violations } = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();
    const blocking = violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
    for (const v of violations.filter((v) => !blocking.includes(v))) console.log(`${file} [${v.impact}] ${v.id}`);
    expect(blocking.map((v) => `${file}: ${v.id} (${v.impact})`)).toEqual([]);
  });
}
