import { schemas } from './schemas.mjs';

const slug = document.body.dataset.project;
const schema = schemas[slug];
const form = document.querySelector('#project-form');
const inputs = document.querySelector('#input-fields');
const editor = document.querySelector('#editor');
const run = document.querySelector('#run-project');
const reset = document.querySelector('#reset-sample');
const status = document.querySelector('#status');
const summary = document.querySelector('#summary');
const details = document.querySelector('#json-details');
const raw = document.querySelector('#raw-result');
const shareStatus = document.querySelector('#share-status');
const worker = new Worker('/worker.js');
const numeric = new Intl.NumberFormat(undefined, { maximumFractionDigits: 8 });
let sample;
let program;
let rootEditor;
let timer;

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function button(label) {
  const node = element('button', '', label);
  node.type = 'button';
  return node;
}

function createEditor(spec, value) {
  if (spec.type === 'object') {
    const node = element('div', 'object-fields');
    const fields = Object.entries(spec.fields).map(([key, field]) => {
      const editor = createEditor(field, value?.[key]);
      node.append(editor.node);
      return [key, editor];
    });
    return { node, read: () => Object.fromEntries(fields.map(([key, field]) => [key, field.read()])) };
  }

  if (spec.type === 'list') {
    const node = element('fieldset', 'editor-list');
    node.append(element('legend', '', spec.label));
    const items = element('div', 'list-items');
    const add = button(`Add ${spec.itemName.toLowerCase()}`);
    const rows = [];
    node.append(items, add);

    function labelRows() {
      rows.forEach((row, index) => {
        row.title.textContent = `${spec.itemName} ${index + 1}`;
        row.remove.setAttribute('aria-label', `Remove ${spec.itemName.toLowerCase()} ${index + 1}`);
      });
    }

    function addRow(initial, focus = false) {
      const child = createEditor(spec.item, initial);
      const title = element('strong');
      const remove = button('Remove');
      const row = element('div', 'list-item');
      const header = element('div', 'row-heading');
      header.append(title, remove);
      row.append(header, child.node);
      const entry = { child, title, remove };
      rows.push(entry);
      items.append(row);
      labelRows();
      remove.addEventListener('click', () => {
        rows.splice(rows.indexOf(entry), 1);
        row.remove();
        labelRows();
        add.focus();
        status.textContent = 'Inputs changed. Run again to update the result.';
      });
      if (focus) (row.querySelector('input') ?? row.querySelector('button')).focus();
    }

    for (const item of value ?? []) addRow(item);
    add.addEventListener('click', () => {
      addRow(undefined, true);
      status.textContent = 'Inputs changed. Run again to update the result.';
    });
    return { node, read: () => rows.map(row => row.child.read()) };
  }

  const node = element('label', 'field', spec.label);
  const input = element('input');
  input.type = spec.type;
  input.required = spec.required ?? true;
  input.value = value ?? spec.initial ?? '';
  if (spec.type === 'number') input.step = spec.step;
  node.append(input);
  return { node, read: () => spec.type === 'number' ? input.valueAsNumber : input.value };
}

function formatLabel(key) {
  const label = key.replaceAll('_', ' ');
  return label ? label[0].toUpperCase() + label.slice(1) : '';
}

function renderResult(value) {
  if (Array.isArray(value)) {
    if (value.length === 0) return element('span', 'muted', 'None');
    const node = element('ol', 'result-list');
    for (const item of value) {
      const row = element('li');
      row.append(renderResult(item));
      node.append(row);
    }
    return node;
  }
  if (value !== null && typeof value === 'object') {
    const node = element('dl', 'result-fields');
    for (const [key, item] of Object.entries(value)) {
      const term = element('dt', '', formatLabel(key));
      const description = element('dd');
      description.append(renderResult(item));
      node.append(term, description);
    }
    return node;
  }
  const text = typeof value === 'number' ? numeric.format(value) : String(value ?? 'None');
  return element('span', '', text);
}

function setEnabled(enabled) {
  inputs.disabled = !enabled;
  run.disabled = !enabled;
  reset.disabled = !enabled;
}

function loadSample() {
  rootEditor = createEditor(schema, sample);
  editor.replaceChildren(rootEditor.node);
}

function fail(message) {
  clearTimeout(timer);
  worker.terminate();
  setEnabled(false);
  status.textContent = message;
}

function execute() {
  const input = JSON.stringify(rootEditor.read());
  setEnabled(false);
  status.textContent = 'Running NexPro…';
  summary.replaceChildren();
  details.hidden = true;
  timer = setTimeout(() => fail('The run timed out. Reload to try again.'), 8000);
  worker.postMessage({
    action: 'run', source: program.source, input, modules: JSON.stringify(program.modules), trace: false,
  });
}

worker.onmessage = ({ data }) => {
  clearTimeout(timer);
  if (data.action === 'init') {
    if (!data.ok) {
      fail('NexPro could not load. Reload to try again.');
      return;
    }
    loadSample();
    execute();
    return;
  }
  setEnabled(true);
  if (!data.ok) {
    summary.replaceChildren(element('p', 'error', data.error ?? 'Review your inputs and try again.'));
    status.textContent = 'The project could not run with these inputs.';
    return;
  }
  try {
    const result = JSON.parse(data.output);
    summary.replaceChildren(renderResult(result));
    raw.textContent = JSON.stringify(result, null, 2);
    details.hidden = false;
    status.textContent = 'Result updated.';
  } catch {
    status.textContent = 'NexPro returned an unexpected result.';
  }
};

worker.onerror = () => fail('NexPro could not load. Reload to try again.');
form.addEventListener('submit', event => {
  event.preventDefault();
  if (!run.disabled) execute();
});
form.addEventListener('input', () => {
  status.textContent = 'Inputs changed. Run again to update the result.';
});
reset.addEventListener('click', () => {
  loadSample();
  execute();
});
document.querySelector('#share-link').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(new URL(location.pathname, location.origin).href);
    shareStatus.textContent = 'Link copied.';
  } catch {
    shareStatus.textContent = 'Copy the link from your address bar.';
  }
});

timer = setTimeout(() => fail('NexPro took too long to load. Reload to try again.'), 45000);
fetch(`/projects/${encodeURIComponent(slug)}/example.json`)
  .then(response => {
    if (!response.ok || !schema) throw new Error('Sample unavailable');
    return response.json();
  })
  .then(example => {
    program = example;
    sample = JSON.parse(program.input);
    worker.postMessage({ action: 'init' });
  })
  .catch(() => fail('The project sample could not load. Reload to try again.'));
