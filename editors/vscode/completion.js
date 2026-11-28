const vscode = require('vscode');

const builtins = {
  append: 'append(list, value) — Add an item to a list.',
  float: 'float(value) — Convert a value to a decimal number.',
  get: 'get(dictionary, key, default) — Look up a key with a fallback.',
  input: 'input() — Read a line.',
  int: 'int(value) — Convert a value to an integer.',
  join: 'join(items, separator) — Join text items.',
  keys: 'keys(dictionary) — Return the keys in insertion order.',
  len: 'len(value) — Return the number of items or characters.',
  lower: 'lower(text) — Convert text to lowercase.',
  max: 'max(items) — Return the largest number.',
  min: 'min(items) — Return the smallest number.',
  number_field: 'number_field(label, default, minimum) — Declare a numeric form field.',
  range: 'range(start, stop, step) — Generate integers with an exclusive stop.',
  result: 'result(label, value) — Display a labeled result.',
  reverse: 'reverse(items) — Return a reversed copy.',
  sorted: 'sorted(items) — Return a sorted copy.',
  split: 'split(text, separator) — Split text at a separator.',
  sum: 'sum(items) — Add the numbers in a list.',
  text_field: 'text_field(label, default) — Declare a text form field.',
  trim: 'trim(text) — Remove whitespace from both ends.',
  upper: 'upper(text) — Convert text to uppercase.',
};

const modules = {
  math: {
    abs: 'abs(value) — Return the absolute value.',
    round: 'round(value, digits) — Round a number. Digits are optional.',
    sqrt: 'sqrt(value) — Return the square root of a nonnegative number.',
  },
  json: {
    parse: 'parse(text) — Read a JSON value.',
    stringify: 'stringify(value) — Serialize a value to JSON.',
  },
};

function moduleFunctions(document, alias) {
  const imports = document.getText().matchAll(
    /^\s*import\s+["']std\/(math|json)["']\s+as\s+([\p{L}_][\p{L}\p{N}_]*)/gmu,
  );
  for (const [, name, importedAlias] of imports) {
    if (alias === importedAlias) return modules[name];
  }
  return {};
}

function registerCompletion(context) {
  context.subscriptions.push(
    vscode.languages.registerCompletionItemProvider('nexpro', {
      provideCompletionItems(document, position) {
        const prefix = document.lineAt(position.line).text.slice(0, position.character);
        const match = prefix.match(/([\p{L}_][\p{L}\p{N}_]*)\.[\p{L}\p{N}_]*$/u);
        const descriptions = match ? moduleFunctions(document, match[1]) : builtins;
        return Object.entries(descriptions).map(([name, description]) => {
          const item = new vscode.CompletionItem(name, vscode.CompletionItemKind.Function);
          item.detail = description;
          return item;
        });
      },
    }, '.'),
    vscode.languages.registerHoverProvider('nexpro', {
      provideHover(document, position) {
        const range = document.getWordRangeAtPosition(position, /[\p{L}_][\p{L}\p{N}_]*/u);
        if (!range) return undefined;
        const name = document.getText(range);
        const prefix = document.lineAt(position.line).text.slice(0, range.start.character);
        const match = prefix.match(/([\p{L}_][\p{L}\p{N}_]*)\.$/u);
        const description = (match ? moduleFunctions(document, match[1]) : builtins)[name];
        return description ? new vscode.Hover(description, range) : undefined;
      },
    }),
  );
}

module.exports = { registerCompletion };
