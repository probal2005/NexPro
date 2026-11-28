import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname } from 'node:path';
import { chromium } from 'playwright';
import { compactProjectInput, parseProjectOutput } from '../browser-numbers.mjs';

const combined = '{"label":"9007199254740993","total_cents":9007199254740993,"other":[-9007199254740993,12,0.5]}';
const parsed = parseProjectOutput(combined);
assert.deepEqual(parsed.value, {
  label: '9007199254740993', total_cents: '9007199254740993', other: ['-9007199254740993', 12, 0.5],
});
assert.equal(parsed.json, combined);
assert.equal(compactProjectInput(' { "spaces here" : 9007199254740993 } '), '{"spaces here":9007199254740993}');

const types = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm',
  '.zip': 'application/zip', '.png': 'image/png',
};
const server = createServer(async (request, response) => {
  const { pathname } = new URL(request.url, 'http://localhost');
  const file = pathname.endsWith('/') ? pathname + 'index.html' : pathname;
  try {
    const content = await readFile(new URL('../../dist' + file, import.meta.url));
    response.writeHead(200, { 'Content-Type': types[extname(file)] ?? 'text/plain' });
    response.end(content);
  } catch {
    response.writeHead(404).end();
  }
});

let browser;
try {
  let base = process.env.NEXPRO_BASE_URL;
  if (!base) {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    base = `http://127.0.0.1:${server.address().port}/`;
  }
  const origin = new URL(base).origin;
  browser = await chromium.launch({ executablePath: process.env.NEXPRO_BROWSER_BIN || undefined });
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const external = [];
  await context.route('**/*', route => {
    if (new URL(route.request().url()).origin === origin) return route.continue();
    external.push(route.request().url());
    return route.abort();
  });
  const page = await context.newPage();

  await page.goto(base);
  await page.getByText('Ready', { exact: true }).waitFor();
  await page.getByText('Inputs & files', { exact: true }).click();
  await page.locator('#module-files').setInputFiles({
    name: 'form.pa', mimeType: 'text/plain',
    buffer: Buffer.from('function evaluate()\n  age = number_field("Age", 20)\n  result("Saved age", age)\nend'),
  });
  await page.locator('#source').fill('import "form.pa" as form\nform.evaluate()');
  await page.getByRole('button', { name: 'Preview tool' }).click();
  const age = page.getByLabel('Age', { exact: true });
  await age.fill('31');
  await page.getByRole('button', { name: 'Calculate', exact: true }).click();
  await page.locator('#tool-results dd').getByText('31', { exact: true }).waitFor();
  await age.fill('9007199254740993');
  await page.getByRole('button', { name: 'Calculate', exact: true }).click();
  await page.getByText('Use a whole number between -9007199254740991 and 9007199254740991.').waitFor();

  await page.goto(new URL('projects/reconciliation/', base).href);
  await page.getByText('Result updated.', { exact: true }).waitFor();
  const ledger = page.getByLabel('Ledger amount (cents)');
  const bank = page.getByLabel('Bank amount (cents)');
  await ledger.nth(0).fill('9007199254740993');
  assert.equal(await ledger.first().evaluate(input => input.validity.customError), true);
  await ledger.nth(0).fill('9007199254740991');
  await ledger.nth(1).fill('2');
  await ledger.nth(2).fill('0');
  for (const field of await bank.all()) await field.fill('0');
  await page.getByRole('button', { name: 'Run project' }).click();
  await page.getByText('Result updated.', { exact: true }).waitFor();
  assert.match(await page.locator('#raw-result').textContent(), /"balance_difference_cents":\s*-9007199254740993/);
  await page.locator('#summary').getByText('-9007199254740993¢', { exact: true }).waitFor();
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);

  await page.goto(new URL('tool.html?example=inventory', base).href);
  await page.getByLabel('Stock CSV').setInputFiles({
    name: 'stock.csv', mimeType: 'text/csv',
    buffer: Buffer.from('sku,stock,minimum,target\nPAPER,1,2,5\n'),
  });
  await page.getByRole('button', { name: 'Calculate', exact: true }).click();
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Download reorder.csv' }).click(),
  ]);
  assert.match(await readFile(await download.path(), 'utf8'), /PAPER,4/);
  assert.deepEqual(external, []);
  console.log('Browser smoke passed: imported form, exact integers, mobile report, and CSV download.');
} finally {
  await browser?.close();
  server.close();
}
