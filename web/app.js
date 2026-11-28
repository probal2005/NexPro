import { shareUrl, sharedTool } from './tool-share.js';
import { toolPreview } from './tool-preview.js';

const source = document.querySelector('#source');
const programInput = document.querySelector('#program-input');
const csvFile = document.querySelector('#csv-file');
const downloadCsv = document.querySelector('#download-csv');
const csvSample = JSON.stringify('sku,stock,minimum,target\nA-01,2,4,10\nB-02,7,3,9\n');
const moduleFiles = document.querySelector('#module-files');
const check = document.querySelector('#check');
const traceEnabled = document.querySelector('#trace');
const traceDetails = document.querySelector('#execution-trace');
const traceOutput = document.querySelector('#trace-output');
const sampleInputs = new Map([['inventory_csv', csvSample], ['bill_splitter', '{"bill":"10.00","people":"3"}'], ['json_report', '{"name":"Ada","scores":[70,85,100]}'], ['clean_names', '  Ada, GRACE, Linus  '], ['scores', '70\n85\n100'], ['input', 'Ada\n2000'], ['score_series', '70\n85\n100\n\n']]);
const gutter = document.querySelector('#gutter');
const examples = document.querySelector('#examples');
const projectSource = document.querySelector('#project-source');
const projectDemo = document.querySelector('#project-demo');
const run = document.querySelector('#run');
const share = document.querySelector('#share');
const shareTool = document.querySelector('#share-tool');
const sharePanel = document.querySelector('#share-panel');
const shareInput = document.querySelector('#share-url');
const shareNote = document.querySelector('#share-note');
const preview = document.querySelector('#preview');
const stop = document.querySelector('#stop');
const compile = document.querySelector('#compile');
const heading = document.querySelector('#result-heading');
const result = document.querySelector('#result');
const status = document.querySelector('#status');
const download = document.querySelector('#download');
const retry = document.querySelector('#retry');
let worker;
let runtimeReady = false;
let timer;
let pythonOutput;
let csvInput;
let csvOutput;
let csvRun = false;
let exampleRequest;
let sampleInput = '';
let exampleModules = {};
let previewSource;
let sharedMessage = '';

function syncGutter() {
  gutter.textContent = Array.from({ length: source.value.split('\n').length }, (_, i) => i + 1).join('\n');
  gutter.scrollTop = source.scrollTop;
}

function refreshActions() {
  const available = runtimeReady && !exampleRequest;
  run.disabled = !available;
  check.disabled = !available;
  preview.disabled = !available;
  share.disabled = shareTool.disabled = Boolean(exampleRequest);
  toolPreview.setEnabled(available);
  compile.disabled = !available;
}

function setReady(ready) {
  runtimeReady = ready;
  stop.hidden = true;
  refreshActions();
}

function show(action, { ok, output = '', error = '', trace = '', tool }) {
  if (action === 'preview' && previewSource === source.value) toolPreview.render(tool, ok);
  traceOutput.textContent = trace;
  traceDetails.hidden = !trace;
  traceDetails.open = Boolean(trace);
  heading.textContent = action === 'compile' && ok ? 'Generated Python' : 'Output';
  result.textContent = ok ? output || '(No output)' : [output.trimEnd(), error].filter(Boolean).join('\n\n');
  result.toggleAttribute('data-error', !ok);
  pythonOutput = action === 'compile' && ok ? output : undefined;
  download.hidden = pythonOutput === undefined;
  csvOutput = action === 'run' && ok && csvRun ? output.replace(/\r\n\n$/, '\r\n') : undefined;
  downloadCsv.hidden = csvOutput === undefined;
  const completed = { check: 'Check complete', compile: 'Compiled successfully', run: 'Run complete', preview: 'Preview complete' };
  status.textContent = !ok ? 'Program failed' :
    Object.keys(tool?.errors ?? {}).length ? 'Check the highlighted fields.' : completed[action];
}

function failWorker(message) {
  clearTimeout(timer);
  worker?.terminate();
  worker = undefined;
  setReady(false);
  show('init', { ok: false, error: message });
  status.textContent = 'Runtime unavailable';
  retry.hidden = false;
}

function startWorker(stopped = false) {
  retry.hidden = true;
  status.textContent = 'Loading NexPro…';
  setReady(false);
  const current = new Worker('worker.js');
  worker = current;
  current.onmessage = ({ data }) => {
    if (current !== worker) return;
    clearTimeout(timer);
    if (data.action === 'init') {
      if (!data.ok) {
        failWorker(data.error);
        return;
      }
      result.textContent = stopped ? 'Execution stopped.' : 'Run your program to see its output.';
      result.removeAttribute('data-error');
      status.textContent = sharedMessage || 'Ready';
    } else {
      show(data.action, data);
    }
    setReady(true);
  };
  current.onerror = () => {
    if (current === worker) failWorker('The NexPro runtime could not start.');
  };
  timer = setTimeout(() => failWorker('Loading the NexPro runtime timed out.'), 45000);
  worker.postMessage({ action: 'init' });
}

async function readModules() {
  const files = [...moduleFiles.files];
  const modules = { ...exampleModules };

  const names = new Set();
  for (const file of files) {
    if (!file.name.endsWith('.pa') || file.name === 'playground.pa' || names.has(file.name)) {
      throw new Error("Choose .pa modules with unique names other than playground.pa.");
    }
    names.add(file.name);
    modules[file.name] = await file.text();
  }
  return modules;
}

async function execute(action, fields = {}) {
  if (run.disabled) return;
  sharedMessage = '';
  const current = worker;
  const code = source.value;
  if (action === 'preview') previewSource = code;
  const input = programInput.value;
  csvRun = input === csvInput || examples.value === 'inventory_csv';
  const trace = action === 'run' && traceEnabled.checked;
  setReady(false);
  stop.hidden = action !== 'run' && action !== 'preview';
  traceDetails.hidden = true;
  download.hidden = true;
  downloadCsv.hidden = true;
  const pending = { check: 'Checking…', compile: 'Compiling…', run: 'Running…', preview: 'Preparing preview…' };
  status.textContent = pending[action];
  timer = setTimeout(() => failWorker('The program took too long to finish.'), 8000);
  try {
    const modules = await readModules();
    if (current === worker) current.postMessage({ action, source: code, input, modules: JSON.stringify(modules), trace, fields: JSON.stringify(fields) });
  } catch (error) {
    if (current !== worker) return;
    clearTimeout(timer);
    show(action, { ok: false, error: error.message });
    setReady(true);
  }
}

share.addEventListener('click', () => shareCurrentCode(false));
shareTool.addEventListener('click', () => shareCurrentCode(true));

async function shareCurrentCode(standalone) {
  const code = source.value;
  sharePanel.hidden = false;
  shareInput.hidden = true;
  shareNote.textContent = '';
  try {
    shareInput.value = shareUrl(code, await readModules(), standalone);
    shareInput.hidden = false;
    try {
      await navigator.clipboard.writeText(shareInput.value);
      shareNote.textContent = 'Link copied. It contains code and modules only.';
    } catch {
      shareInput.focus();
      shareInput.select();
      shareNote.textContent = 'Copy this link to share your code and modules.';
    }
  } catch (error) {
    shareNote.textContent = error.message;
  }
}

preview.addEventListener('click', () => execute('preview'));
toolPreview.onSubmit(fields => execute('preview', fields));
run.addEventListener('click', () => execute('run'));
stop.addEventListener('click', () => {
  clearTimeout(timer);
  worker.terminate();
  heading.textContent = 'Output';
  result.textContent = 'Execution stopped. Restarting the runtime…';
  result.removeAttribute('data-error');
  startWorker(true);
});
compile.addEventListener('click', () => execute('compile'));
check.addEventListener('click', () => execute('check'));
retry.addEventListener('click', () => startWorker());
source.addEventListener('input', () => {
  exampleRequest?.abort();
  toolPreview.clear();
  syncGutter();
});
source.addEventListener('scroll', () => { gutter.scrollTop = source.scrollTop; });
source.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    event.preventDefault();
    execute('run');
  }
});
examples.addEventListener('change', async () => {
  exampleRequest?.abort();
  const request = new AbortController();
  exampleRequest = request;
  refreshActions();
  try {
    const name = examples.value;
    const isProject = name.startsWith('project:');
    const slug = isProject ? name.slice('project:'.length) : undefined;
    const load = async path => {
      const response = await fetch(path, { signal: request.signal });
      if (!response.ok) throw new Error('The example could not be loaded.');
      return response;
    };
    let program;
    if (isProject) {
      program = await (await load(`projects/${encodeURIComponent(slug)}/example.json`)).json();
    } else {
      const modules = { imports: ['math_utils'], namespaces: ['namespace_math', 'namespace_report'] };
      const required = modules[name] ?? [];
      const readExample = async file => (await load(`examples/${file}.pa`)).text();
      const [code, ...sources] = await Promise.all([readExample(name), ...required.map(readExample)]);
      program = {
        source: code,
        input: sampleInputs.get(name) ?? '',
        modules: Object.fromEntries(required.map((module, i) => [module + '.pa', sources[i]])),
      };
    }
    if (request.signal.aborted) return;
    toolPreview.clear();
    source.value = program.source;
    exampleModules = program.modules;
    if (isProject || !programInput.value || programInput.value === sampleInput) {
      sampleInput = program.input;
      programInput.value = sampleInput;
    }
    const directory = slug ?? (name === 'bill_splitter' ? 'bill-splitter' : undefined);
    projectSource.hidden = !directory;
    projectDemo.hidden = !directory;
    if (directory) {
      const path = encodeURIComponent(directory);
      projectSource.href = `https://github.com/probal2005/NexPro/tree/main/projects/${path}`;
      projectDemo.href = `/projects/${path}/`;
    }
    syncGutter();
    source.focus();
  } catch (error) {
    if (!request.signal.aborted) status.textContent = error.message;
  } finally {
    if (exampleRequest === request) {
      exampleRequest = undefined;
      refreshActions();
    }
  }
});
csvFile.addEventListener('change', async () => {
  const [file] = csvFile.files;
  if (!file) return;
  csvFile.value = '';
  if (file.size > 512 * 1024) {
    status.textContent = 'Choose a CSV file of up to 512 KB.';
    return;
  }
  try {
    csvInput = JSON.stringify(await file.text());
    programInput.value = csvInput;
    status.textContent = 'CSV loaded into Program input.';
  } catch {
    status.textContent = 'The CSV file could not be read.';
  }
});
download.addEventListener('click', () => downloadOutput(pythonOutput, 'playground.py', 'text/x-python'));
downloadCsv.addEventListener('click', () => downloadOutput(csvOutput, 'output.csv', 'text/csv;charset=utf-8'));

function downloadOutput(content, filename, type) {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

try {
  const shared = sharedTool();
  if (shared) {
    source.value = shared.source;
    exampleModules = shared.modules;
    programInput.value = '';
    examples.selectedIndex = -1;
    sharedMessage = 'Shared code loaded. Select Preview tool or Run code to execute it.';
  }
} catch (error) {
  sharedMessage = error.message;
}
syncGutter();
startWorker();
