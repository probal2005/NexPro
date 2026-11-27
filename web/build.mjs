import { cp, mkdir, readFile, readdir, writeFile } from 'node:fs/promises';

await mkdir('dist/nexpro', { recursive: true });
await mkdir('dist/examples', { recursive: true });
for (const name of ['styles.css', 'app.js', 'worker.js', 'playground.py', 'nexpro-icon.png', 'favicon.png']) {
  await cp(`web/${name}`, `dist/${name}`);
}
const versionFile = await readFile('nexpro/__version__.py', 'utf8');
const version = versionFile.match(/^VERSION = "([^"]+)"/m)?.[1];
if (!version) throw new Error('NexPro version not found');
const template = await readFile('web/index.html', 'utf8');
await writeFile('dist/index.html', template.replaceAll('__NEXPRO_VERSION__', version));

for (const name of await readdir('nexpro')) {
  if (name.endsWith('.py')) await cp(`nexpro/${name}`, `dist/nexpro/${name}`);
}
for (const name of [
  'hello', 'variables', 'precedence', 'functions', 'scope', 'temperature', 'greeting',
  'grades', 'multiplication_table', 'sum_1_to_10', 'lists', 'scores', 'input', 'imports', 'math_utils', 'score_series', 'score_filter', 'scorecard',
]) {
  await cp(`examples/${name}.pa`, `dist/examples/${name}.pa`);
}
