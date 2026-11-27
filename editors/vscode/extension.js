const vscode = require('vscode');

function activate(context) {
  context.subscriptions.push(vscode.commands.registerCommand('nexpro.check', async () => {
    const document = vscode.window.activeTextEditor?.document;
    if (!document || document.languageId !== 'nexpro' || document.uri.scheme !== 'file') {
      await vscode.window.showInformationMessage('Save a NexPro .pa file before checking syntax.');
      return;
    }
    if (document.isDirty && !(await document.save())) return;

    const folder = vscode.workspace.getWorkspaceFolder(document.uri);
    const executable = vscode.workspace.getConfiguration('nexpro', document.uri).get('executablePath');
    const task = new vscode.Task(
      { type: 'nexpro', sourceFile: document.uri.fsPath },
      folder ?? vscode.TaskScope.Global,
      'Check Syntax',
      'NexPro',
      new vscode.ProcessExecution(executable, ['check', document.uri.fsPath]),
      '$nexpro',
    );
    await vscode.tasks.executeTask(task);
  }));
}

module.exports = { activate };
