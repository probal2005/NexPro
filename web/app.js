const source = document.querySelector('#source');
const programInput = document.querySelector('#program-input');
const moduleFiles = document.querySelector('#module-files');
const check = document.querySelector('#check');
const traceEnabled = document.querySelector('#trace');
const traceDetails = document.querySelector('#execution-trace');
const traceOutput = document.querySelector('#trace-output');
const sampleInputs = new Map([['bill_splitter', '{"bill":"10.00","people":"3"}'], ['json_report', '{"name":"আদা","scores":[70,85,100]}'], ['clean_names', '  Ada, GRACE, Linus  '], ['scores', '70\n85\n100'], ['input', 'Ada\n2000'], ['score_series', '70\n85\n100\n\n']]);
const gutter = document.querySelector('#gutter');
const examples = document.querySelector('#examples');
const run = document.querySelector('#run');
const stop = document.querySelector('#stop');
const compile = document.querySelector('#compile');
const heading = document.querySelector('#result-heading');
const result = document.querySelector('#result');
const status = document.querySelector('#status');
const download = document.querySelector('#download');
const retry = document.querySelector('#retry');
let worker;
let timer;
let pythonOutput;
let exampleRequest;
let sampleInput = '';
let exampleModules = {};

function syncGutter() {
  gutter.textContent = Array.from({ length: source.value.split('\n').length }, (_, i) => i + 1).join('\n');
  gutter.scrollTop = source.scrollTop;
}

function setReady(ready) {
  stop.hidden = true;
  run.disabled = !ready;
  check.disabled = !ready;
  compile.disabled = !ready;
}

function show(action, { ok, output = '', error = '', trace = '' }) {
  traceOutput.textContent = trace;
  traceDetails.hidden = !trace;
  traceDetails.open = Boolean(trace);
  heading.textContent = action === 'compile' && ok ? 'Generated Python' : 'Output';
  result.textContent = ok ? output || '(No output)' : [output.trimEnd(), error].filter(Boolean).join('\n\n');
  result.toggleAttribute('data-error', !ok);
  pythonOutput = action === 'compile' && ok ? output : undefined;
  download.hidden = pythonOutput === undefined;
  const completed = { check: 'Check complete', compile: 'Compiled successfully', run: 'Run complete' };
  status.textContent = ok ? completed[action] : 'Program failed';
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
      status.textContent = 'Ready';
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

async function execute(action) {
  if (run.disabled) return;
  const current = worker;
  const code = source.value;
  const input = programInput.value;
  const trace = action === 'run' && traceEnabled.checked;
  const files = [...moduleFiles.files];
  const modules = { ...exampleModules };
  setReady(false);
  stop.hidden = action !== 'run';
  traceDetails.hidden = true;
  download.hidden = true;
  const pending = { check: 'Checking…', compile: 'Compiling…', run: 'Running…' };
  status.textContent = pending[action];
  timer = setTimeout(() => failWorker('The program took too long to finish.'), 8000);
  try {
    const names = new Set();
    for (const file of files) {
      if (!file.name.endsWith('.pa') || file.name === 'playground.pa' || names.has(file.name)) {
        throw new Error("Choose .pa modules with unique names other than playground.pa.");
      }
      names.add(file.name);
      modules[file.name] = await file.text();
    }
    if (current === worker) current.postMessage({ action, source: code, input, modules: JSON.stringify(modules), trace });
  } catch (error) {
    if (current !== worker) return;
    clearTimeout(timer);
    show(action, { ok: false, error: error.message });
    setReady(true);
  }
}

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
  try {
    async function loadExample(name) {
      const response = await fetch(`examples/${name}.pa`, { signal: request.signal });
      if (!response.ok) throw new Error('The example could not be loaded.');
      return response.text();
    }

    const name = examples.value;
    const modules = { imports: ['math_utils'], namespaces: ['namespace_math', 'namespace_report'] };
    const required = modules[name] ?? [];
    const [code, ...sources] = await Promise.all([loadExample(name), ...required.map(loadExample)]);
    if (request.signal.aborted) return;
    exampleModules = Object.fromEntries(required.map((module, i) => [module + '.pa', sources[i]]));
    source.value = code;
    if (!programInput.value || programInput.value === sampleInput) {
      sampleInput = sampleInputs.get(examples.value) ?? '';
      programInput.value = sampleInput;
    }
    syncGutter();
    source.focus();
  } catch (error) {
    if (!request.signal.aborted) status.textContent = error.message;
  }
});
download.addEventListener('click', () => {
  const url = URL.createObjectURL(new Blob([pythonOutput], { type: 'text/x-python' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'playground.py';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

syncGutter();
startWorker();
