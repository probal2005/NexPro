const source = document.querySelector('#source');
const programInput = document.querySelector('#program-input');
const sampleInputs = new Map([['scores', '70\n85\n100'], ['input', 'Ada\n2000']]);
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

function syncGutter() {
  gutter.textContent = Array.from({ length: source.value.split('\n').length }, (_, i) => i + 1).join('\n');
  gutter.scrollTop = source.scrollTop;
}

function setReady(ready) {
  stop.hidden = true;
  run.disabled = !ready;
  compile.disabled = !ready;
}

function show(action, { ok, output = '', error = '' }) {
  heading.textContent = action === 'compile' && ok ? 'Generated Python' : 'Output';
  result.textContent = ok ? output || '(No output)' : [output.trimEnd(), error].filter(Boolean).join('\n\n');
  result.toggleAttribute('data-error', !ok);
  pythonOutput = action === 'compile' && ok ? output : undefined;
  download.hidden = pythonOutput === undefined;
  status.textContent = ok ? (action === 'compile' ? 'Compiled successfully' : 'Run complete') : 'Program failed';
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

function execute(action) {
  if (run.disabled) return;
  setReady(false);
  stop.hidden = action !== 'run';
  download.hidden = true;
  status.textContent = action === 'compile' ? 'Compiling…' : 'Running…';
  timer = setTimeout(() => failWorker('The program took too long to finish.'), 8000);
  worker.postMessage({ action, source: source.value, input: programInput.value });
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
    const response = await fetch(`examples/${examples.value}.pa`, { signal: request.signal });
    if (!response.ok) throw new Error('The example could not be loaded.');
    const code = await response.text();
    if (request.signal.aborted) return;
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
