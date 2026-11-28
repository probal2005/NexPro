import { shareUrl, sharedTool } from './tool-share.js';
import { toolPreview } from './tool-preview.js';

const examples = new Map([
  ['bill', ['Bill Splitter', 'tool_bill']],
  ['quote', ['Freelance Quote', 'tool_quote']],
  ['inventory', ['Inventory Reorder', 'tool_inventory']],
]);
const title = document.querySelector('#public-title');
const status = document.querySelector('#public-status');
const start = document.querySelector('#public-start');
const stop = document.querySelector('#public-stop');
const output = document.querySelector('#public-output');
const sourcePanel = document.querySelector('#public-source');
let program;
let worker;
let timer;

function setBusy(busy) {
  start.disabled = busy;
  stop.hidden = !busy;
  toolPreview.setEnabled(!busy);
}

function fail(message) {
  clearTimeout(timer);
  worker?.terminate();
  worker = undefined;
  setBusy(false);
  start.hidden = false;
  status.textContent = message;
}

function execute(fields = {}) {
  if (start.disabled) return;
  setBusy(true);
  output.hidden = true;
  status.textContent = 'Running tool…';
  const run = () => worker.postMessage({
    action: 'preview', source: program.source, input: '', modules: JSON.stringify(program.modules),
    trace: false, fields: JSON.stringify(fields),
  });
  const runWithTimeout = () => {
    clearTimeout(timer);
    timer = setTimeout(() => fail('The tool took too long to finish.'), 8000);
    run();
  };
  if (worker) {
    runWithTimeout();
    return;
  }
  const current = new Worker('worker.js');
  worker = current;
  current.onmessage = ({ data }) => {
    if (worker !== current) return;
    clearTimeout(timer);
    if (data.action === 'init') {
      if (data.ok) runWithTimeout();
      else fail(data.error);
      return;
    }
    setBusy(false);
    toolPreview.render(data.tool, data.ok);
    start.hidden = Boolean(data.tool?.fields.length && data.ok);
    output.textContent = [data.output, data.error].filter(Boolean).join('\n');
    output.hidden = !output.textContent;
    status.textContent = !data.ok ? 'Tool failed' :
      Object.keys(data.tool?.errors ?? {}).length ? 'Check the highlighted fields.' : 'Tool ready';
  };
  current.onerror = () => { if (worker === current) fail('The runtime could not start.'); };
  timer = setTimeout(() => fail('Loading the runtime timed out.'), 45000);
  worker.postMessage({ action: 'init' });
}

async function load() {
  const shared = sharedTool();
  const example = examples.get(new URLSearchParams(location.search).get('example'));
  if (shared) program = shared;
  else if (example) {
    const [name, filename] = example;
    const response = await fetch(`examples/${filename}.pa`);
    if (!response.ok) throw new Error('The example could not be loaded.');
    program = { source: await response.text(), modules: {} };
    title.textContent = document.title = name;
  } else {
    throw new Error('Open this page using a NexPro tool link.');
  }
  const edit = document.querySelector('#public-edit');
  try {
    edit.href = shareUrl(program.source, program.modules);
  } catch {
    edit.hidden = true;
  }
  const files = document.querySelector('#public-files');
  for (const [name, content] of [['playground.pa', program.source], ...Object.entries(program.modules)]) {
    const heading = document.createElement('h2');
    const pre = document.createElement('pre');
    heading.textContent = name;
    pre.textContent = content;
    files.append(heading, pre);
  }
  sourcePanel.hidden = false;
  start.hidden = false;
  status.textContent = 'Start the tool to load its form.';
  if (!shared) execute();
}

start.addEventListener('click', () => execute());
stop.addEventListener('click', () => fail('Execution stopped.'));
toolPreview.onSubmit(execute);
load().catch(error => { status.textContent = error.message; });
