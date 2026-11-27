const { execFile } = require('node:child_process');
const { promisify } = require('node:util');
const vscode = require('vscode');
const { registerCompletion } = require('./completion');

const run = promisify(execFile);

function activate(context) {
  registerCompletion(context);
  const diagnostics = vscode.languages.createDiagnosticCollection('nexpro');
  const checks = new Map();
  const requests = new Map();

  function refresh(uri) {
    if (!uri) return;
    const problems = new Map();
    for (const item of checks.values()) {
      if (item.uri.toString() === uri.toString()) problems.set(item.key, item.diagnostic);
    }
    if (problems.size) diagnostics.set(uri, [...problems.values()]);
    else diagnostics.delete(uri);
  }

  function report(entry, item) {
    const previous = checks.get(entry)?.uri;
    if (item) checks.set(entry, item);
    else checks.delete(entry);
    refresh(previous);
    refresh(item?.uri);
  }

  async function check(document, manual) {
    if (document.languageId !== 'nexpro' || document.uri.scheme !== 'file') return;
    if (!manual && !vscode.workspace.isTrusted) return;

    const uri = document.uri;
    const entry = uri.toString();
    const request = Symbol();
    requests.set(entry, request);
    const config = vscode.workspace.getConfiguration('nexpro', uri);
    try {
      const executable = config.get('executablePath');
      let stdout;
      try {
        ({ stdout } = await run(executable, ['check', '--json', uri.fsPath], { timeout: 7000 }));
      } catch (error) {
        if (error.code !== 1 || !error.stdout) throw error;
        stdout = error.stdout;
      }
      if (requests.get(entry) !== request) return;
      const result = JSON.parse(stdout);
      const problem = result.diagnostics[0];
      if (!problem) {
        report(entry);
        if (manual) void vscode.window.showInformationMessage('NexPro syntax check passed.');
        return;
      }

      const target = problem.filename ? vscode.Uri.file(problem.filename) : uri;
      const line = Math.max(0, (problem.line ?? 1) - 1);
      const column = Math.max(0, (problem.column ?? 1) - 1);
      const diagnostic = new vscode.Diagnostic(
        new vscode.Range(line, column, line, column + 1),
        problem.message, vscode.DiagnosticSeverity.Error,
      );
      diagnostic.source = 'NexPro';
      report(entry, { uri: target, key: JSON.stringify([line, column, problem.message]), diagnostic });
      if (manual) await vscode.commands.executeCommand('workbench.actions.view.problems');
    } catch {
      if (requests.get(entry) !== request) return;
      report(entry);
      if (manual) {
        void vscode.window.showErrorMessage('NexPro check failed. Verify that nexpro.executablePath points to NexPro CLI 1.8 or later.');
      }
    } finally {
      if (requests.get(entry) === request) requests.delete(entry);
    }
  }

  async function getSavedDocument() {
    const document = vscode.window.activeTextEditor?.document;
    if (!document || document.languageId !== 'nexpro' || document.uri.scheme !== 'file') {
      await vscode.window.showInformationMessage('Save a NexPro .pa file first.');
      return undefined;
    }
    if (document.isDirty && !(await document.save())) return undefined;
    return document;
  }

  context.subscriptions.push(
    diagnostics,
    vscode.debug.registerDebugAdapterDescriptorFactory('nexpro', {
      createDebugAdapterDescriptor(session) {
        const config = vscode.workspace.getConfiguration('nexpro', session.workspaceFolder?.uri);
        return new vscode.DebugAdapterExecutable(config.get('executablePath'), ['debug-adapter']);
      },
    }),
    vscode.debug.registerDebugConfigurationProvider('nexpro', {
      resolveDebugConfiguration(_folder, config) {
        if (config.type) return config;
        const document = vscode.window.activeTextEditor?.document;
        if (document?.languageId === 'nexpro' && document.uri.scheme === 'file') {
          return { type: 'nexpro', request: 'launch', name: 'Debug NexPro file', program: document.uri.fsPath };
        }
        return undefined;
      },
    }),
    vscode.commands.registerCommand('nexpro.check', async () => {
      const document = await getSavedDocument();
      if (document) await check(document, true);
    }),
    vscode.commands.registerCommand('nexpro.trace', async () => {
      const document = await getSavedDocument();
      if (!document) return;
      const uri = document.uri;
      const executable = vscode.workspace.getConfiguration('nexpro', uri).get('executablePath');
      const task = new vscode.Task(
        { type: 'nexpro', sourceFile: uri.fsPath },
        vscode.workspace.getWorkspaceFolder(uri) ?? vscode.TaskScope.Global,
        'Run with Trace',
        'NexPro',
        new vscode.ProcessExecution(executable, ['run', '--trace', uri.fsPath]),
      );
      await vscode.tasks.executeTask(task);
    }),
    vscode.workspace.onDidSaveTextDocument(document => {
      if (document.languageId !== 'nexpro') return;
      const config = vscode.workspace.getConfiguration('nexpro', document.uri);
      if (!config.get('checkOnSave')) return;
      const uri = document.uri.toString();
      void check(document, false);
      for (const other of vscode.workspace.textDocuments) {
        const entry = other.uri.toString();
        if (entry !== uri && checks.get(entry)?.uri.toString() === uri) void check(other, false);
      }
    }),
    vscode.workspace.onDidCloseTextDocument(document => {
      const entry = document.uri.toString();
      requests.delete(entry);
      report(entry);
    }),
  );
}

module.exports = { activate };
