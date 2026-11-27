import { cp, mkdir, readdir } from 'node:fs/promises';

await mkdir('dist/nexpro', { recursive: true });
await mkdir('dist/examples', { recursive: true });
for (const name of ['index.html', 'styles.css', 'app.js', 'worker.js', 'playground.py']) {
  await cp(`web/${name}`, `dist/${name}`);
}
for (const name of await readdir('nexpro')) {
  if (name.endsWith('.py')) await cp(`nexpro/${name}`, `dist/nexpro/${name}`);
}
for (const name of ['hello', 'variables', 'precedence']) {
  await cp(`examples/${name}.pa`, `dist/examples/${name}.pa`);
}
