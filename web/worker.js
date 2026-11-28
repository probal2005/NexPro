const RUNTIME_URL = new URL('pyodide/', self.location.href).href;
const MODULES = [
  '__init__', '__version__', 'ast', 'compiler', 'data_builtins', 'errors',
  'interpreter', 'lexer', 'loader', 'parser', 'runtime', 'standard', 'tokens',
];

async function loadFile(path) {
  const response = await fetch(new URL(path, self.location.href));
  if (!response.ok) throw new Error(`Could not load ${path} (HTTP ${response.status})`);
  return [path, await response.text()];
}

let execute;
self.onmessage = async ({ data }) => {
  try {
    if (data.action === 'init') {
      importScripts(`${RUNTIME_URL}pyodide.js`);
      const [python, files] = await Promise.all([
        loadPyodide({ indexURL: RUNTIME_URL }),
        Promise.all(['playground.py', ...MODULES.map(name => `nexpro/${name}.py`)].map(loadFile)),
      ]);
      python.FS.mkdir('nexpro');
      for (const [path, content] of files) python.FS.writeFile(path, content, { encoding: 'utf8' });
      execute = python.pyimport('playground').run_playground;
      self.postMessage({ action: 'init', ok: true });
      return;
    }
    const result = JSON.parse(execute(data.source, data.action, data.input, data.modules, data.trace, data.fields ?? '{}'));
    self.postMessage({ action: data.action, ...result });
  } catch (error) {
    self.postMessage({ action: data.action, ok: false, error: error.message });
  }
};
