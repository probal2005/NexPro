const vscode = require('vscode');

const builtins = {
  append: 'append(list, value) — Add an item to a list.',
  checkbox_field: 'checkbox_field(label, default) — Declare a boolean checkbox.',
  csv_field: 'csv_field(label, columns, default) — Declare a CSV file upload.',
  download_csv: 'download_csv(filename, text) — Export a CSV file.',
  field_check: 'field_check(label, condition, message) — Validate a declared field.',
  select_field: 'select_field(label, options, default) — Declare a dropdown.',
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
  number_field: 'number_field(label, default, min, max, step, message) — Declare a numeric form field.',
  range: 'range(start, stop, step) — Generate integers with an exclusive stop.',
  result: 'result(label, value) — Display a labeled result.',
  reverse: 'reverse(items) — Return a reversed copy.',
  sorted: 'sorted(items) — Return a sorted copy.',
  split: 'split(text, separator) — Split text at a separator.',
  sum: 'sum(items) — Add the numbers in a list.',
  text_field: 'text_field(label, default) — Declare a text form field.',
  trim: 'trim(text) — Remove whitespace from both ends.',
  type_of: 'type_of(value) — Return the type name as text.',
  upper: 'upper(text) — Convert text to uppercase.',
};

const modules = {
  queue: {
    new: 'new(items) — Create a FIFO queue, optionally from a list.',
    enqueue: 'enqueue(queue, value) — Add a value to the back.',
    dequeue: 'dequeue(queue) — Remove and return the first value.',
    peek: 'peek(queue) — Read the first value.',
    to_list: 'to_list(queue) — Read the queue as a list.',
  },
  linked_list: {
    new: 'new(items) — Create a linked list, optionally from a list.',
    append: 'append(linked, value) — Add a value at the tail.',
    insert: 'insert(linked, index, value) — Insert at a position.',
    remove: 'remove(linked, index) — Remove and return an item.',
    to_list: 'to_list(linked) — Traverse the chain into a list.',
  },
  stats: {
    mean: 'mean(items) — Compute the arithmetic mean.',
    median: 'median(items) — Find the median.',
    count_by: 'count_by(items, key) — Count values or record fields.',
  },
  text: {
    replace: 'replace(text, old, new) — Replace every occurrence.',
    find: 'find(text, fragment) — Return the first matching index or -1.',
    contains: 'contains(text, fragment) — Test for a substring.',
    starts_with: 'starts_with(text, prefix) — Test the prefix.',
    ends_with: 'ends_with(text, suffix) — Test the suffix.',
  },
  list: {
    insert: 'insert(items, index, value) — Insert into the list.',
    pop: 'pop(items, index) — Remove and return an item. Defaults to the last.',
    remove: 'remove(items, value) — Remove the first matching item.',
    unique: 'unique(items) — Return a new list without duplicates.',
  },
  dict: {
    has: 'has(record, key) — Test whether the key exists.',
    remove: 'remove(record, key, default) — Remove and return an entry.',
    merge: 'merge(left, right) — Return a new dictionary with right-side values taking precedence.',
  },
  csv: {
    parse: 'parse(text, columns) — Read CSV as a list of rows with named columns.',
    stringify: 'stringify(rows) — Write a list of dictionaries as CSV.',
  },
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
    /^\s*import\s+["']std\/(math|json|csv|text|list|dict|queue|linked_list|stats)["']\s+as\s+([\p{L}_][\p{L}\p{N}_]*)/gmu,
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
