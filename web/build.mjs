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
const projectOptions = [];
for (const project of await readdir('projects', { withFileTypes: true })) {
  if (!project.isDirectory() || project.name === 'bill-splitter') continue;
  const folder = `projects/${project.name}`;
  const readme = await readFile(`${folder}/README.md`, 'utf8');
  const title = readme.match(/^# (.+)$/m)?.[1].trim();
  const sample = readme.match(/^```json\s*\n([\s\S]*?)\n```/m)?.[1];
  if (!title || !sample) throw new Error(`Project name or sample missing in ${folder}/README.md`);
  const modules = {};
  for (const name of await readdir(folder)) {
    if (name.endsWith('.pa') && name !== 'main.pa' && !name.startsWith('test_')) {
      modules[name] = await readFile(`${folder}/${name}`, 'utf8');
    }
  }
  const program = {
    source: await readFile(`${folder}/main.pa`, 'utf8'),
    input: JSON.stringify(JSON.parse(sample)),
    modules,
  };
  await mkdir(`dist/${folder}`, { recursive: true });
  await writeFile(`dist/${folder}/example.json`, JSON.stringify(program));
  const escape = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;').replaceAll('"', '&quot;');
  projectOptions.push(`<option value="project:${escape(project.name)}">${escape(title)}</option>`);
}
await writeFile('dist/index.html', template.replaceAll('__NEXPRO_VERSION__', version)
  .replace('<!-- NEXPRO_PROJECT_OPTIONS -->', projectOptions.join('\n            ')));

for (const name of await readdir('nexpro')) {
  if (name.endsWith('.py')) await cp(`nexpro/${name}`, `dist/nexpro/${name}`);
}
for (const name of [
  'hello', 'variables', 'precedence', 'functions', 'scope', 'temperature', 'greeting',
  'grades', 'multiplication_table', 'sum_1_to_10', 'lists', 'scores', 'input', 'imports', 'math_utils', 'score_series', 'score_filter', 'scorecard', 'student_report', 'clean_names', 'namespaces', 'namespace_math', 'namespace_report', 'ranked_scores', 'json_report',
]) {
  await cp(`examples/${name}.pa`, `dist/examples/${name}.pa`);
}

const demo = 'projects/bill-splitter';
await mkdir(`dist/${demo}`, { recursive: true });
for (const name of ['index.html', 'app.js', 'styles.css', 'main.pa']) {
  await cp(`${demo}/${name}`, `dist/${demo}/${name}`);
}
await cp(`${demo}/main.pa`, 'dist/examples/bill_splitter.pa');
