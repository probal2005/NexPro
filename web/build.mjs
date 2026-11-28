import { cp, mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
import { schemas } from './project-demo/schemas.mjs';

await mkdir('dist/nexpro', { recursive: true });
await mkdir('dist/examples', { recursive: true });
for (const name of ['styles.css', 'app.js', 'tool-preview.js', 'tool-share.js', 'tool.html', 'public-tool.js', 'worker.js', 'playground.py', 'nexpro-icon.png', 'favicon.png']) {
  await cp(`web/${name}`, `dist/${name}`);
}
const versionFile = await readFile('nexpro/__version__.py', 'utf8');
const version = versionFile.match(/^VERSION = "([^"]+)"/m)?.[1];
if (!version) throw new Error('NexPro version not found');
const template = await readFile('web/index.html', 'utf8');
const demoTemplate = await readFile('web/project-demo/index.html', 'utf8');
await mkdir('dist/project-demo', { recursive: true });
for (const name of ['app.js', 'schemas.mjs', 'styles.css']) {
  await cp(`web/project-demo/${name}`, `dist/project-demo/${name}`);
}
const escape = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const projectOptions = [];
const liveProjects = [{
  slug: 'bill-splitter',
  title: 'Bill Splitter',
  description: 'Divide a bill into shares that add up to the exact total.',
}];
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
  const description = readme.split(/\r?\n/).find(line => line.includes('[Read the NexPro code]'))
    ?.split('[Read the NexPro code]')[0].trim() ?? '';
  if (Object.hasOwn(schemas, project.name) || project.name === 'order-dispatch') {
    liveProjects.push({ slug: project.name, title, description });
  }
  if (Object.hasOwn(schemas, project.name)) {
    const page = demoTemplate
      .replaceAll('__PROJECT_SLUG__', () => escape(project.name))
      .replaceAll('__PROJECT_TITLE__', () => escape(title))
      .replaceAll('__PROJECT_DESCRIPTION__', () => escape(description));
    await writeFile(`dist/${folder}/index.html`, page);
    await cp(`${folder}/main.pa`, `dist/${folder}/main.pa`);
  }
  projectOptions.push(`<option value="project:${escape(project.name)}">${escape(title)}</option>`);
}
const projectLinks = liveProjects.map(({ slug, title, description }) => (
  `<li><a href="/projects/${encodeURIComponent(slug)}/">` +
  `<strong>${escape(title)}</strong><span>${escape(description)}</span></a></li>`
));
await writeFile('dist/index.html', template.replaceAll('__NEXPRO_VERSION__', version)
  .replace('<!-- NEXPRO_PROJECT_OPTIONS -->', () => projectOptions.join('\n            '))
  .replace('<!-- NEXPRO_PROJECT_LINKS -->', () => projectLinks.join('\n        ')));

for (const name of await readdir('nexpro')) {
  if (name.endsWith('.py')) await cp(`nexpro/${name}`, `dist/nexpro/${name}`);
}
for (const name of [
  'hello', 'variables', 'precedence', 'functions', 'scope', 'temperature', 'greeting',
  'grades', 'multiplication_table', 'sum_1_to_10', 'lists', 'scores', 'input', 'imports', 'math_utils', 'score_series', 'score_filter', 'scorecard', 'student_report', 'clean_names', 'namespaces', 'namespace_math', 'namespace_report', 'ranked_scores', 'json_report', 'tool_bill', 'tool_quote', 'tool_inventory', 'invoice_total', 'recover_csv', 'dispatch_summary', 'structured_inventory', 'named_invoice', 'invoice_record', 'inventory_csv',
]) {
  await cp(`examples/${name}.pa`, `dist/examples/${name}.pa`);
}

for (const project of ['bill-splitter', 'order-dispatch']) {
  const demo = `projects/${project}`;
  await mkdir(`dist/${demo}`, { recursive: true });
  for (const name of ['index.html', 'app.js', 'styles.css', 'main.pa']) {
    await cp(`${demo}/${name}`, `dist/${demo}/${name}`);
  }
}
await cp('projects/bill-splitter/main.pa', 'dist/examples/bill_splitter.pa');
