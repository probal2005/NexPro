const panel = document.querySelector('#tool-panel');
const form = document.querySelector('#tool-form');
const fieldList = document.querySelector('#tool-fields');
const resultsList = document.querySelector('#tool-results');
const downloads = document.querySelector('#tool-downloads');
const calculate = document.querySelector('#tool-calculate');

function render(tool, ok) {
  revision++;
  resultsList.replaceChildren();
  downloads.replaceChildren();
  if (!ok || !tool) return;
  const files = new Map([...fieldList.querySelectorAll('input[type=file]')].map(input => [input.name, input]));
  fieldList.replaceChildren();
  panel.hidden = false;
  calculate.hidden = tool.fields.length === 0;
  for (const [index, field] of tool.fields.entries()) {
    const wrapper = document.createElement('div');
    const label = document.createElement('label');
    const input = (field.kind === 'file' && files.get(field.label))
      || document.createElement(field.kind === 'select' ? 'select' : 'input');
    input.id = `tool-field-${index}`;
    input.name = field.label;
    if (field.kind === 'select') {
      for (const option of field.options) input.add(new Option(option));
    } else {
      input.type = field.kind;
    }
    if (field.kind === 'file') {
      input.accept = '.csv,text/csv';
      input.required = field.required;
    } else {
      input.value = field.value;
    }
    if (field.kind === 'checkbox') input.checked = field.value;
    if (field.kind === 'number') {
      input.step = field.step ?? 'any';
      input.required = true;
      if (field.minimum !== null) input.min = field.minimum;
      if (field.maximum !== null) input.max = field.maximum;
      input.dataset.message = field.message ?? '';
    } else {
      input.maxLength = 4096;
    }
    label.htmlFor = input.id;
    label.textContent = field.label;
    const message = document.createElement('small');
    message.id = `${input.id}-error`;
    message.className = 'field-error';
    input.setAttribute('aria-describedby', message.id);
    input.oninput = () => {
      if (input.hasAttribute('aria-invalid')) validate(input);
    };
    wrapper.append(label, input, message);
    fieldList.append(wrapper);
    const error = tool.errors?.[field.label];
    if (typeof error === 'string') {
      message.textContent = error;
      input.setAttribute('aria-invalid', 'true');
    }
  }
  for (const { label, value } of tool.results) {
    const pair = document.createElement('div');
    const term = document.createElement('dt');
    const detail = document.createElement('dd');
    term.textContent = label;
    detail.textContent = value;
    pair.append(term, detail);
    resultsList.append(pair);
  }
  for (const [name, content] of Object.entries(tool.downloads ?? {})) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = `Download ${name}`;
    button.onclick = () => {
      const url = URL.createObjectURL(new Blob([content], { type: 'text/csv;charset=utf-8' }));
      const link = document.createElement('a');
      link.href = url;
      link.download = name;
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    };
    downloads.append(button);
  }
  if (!tool.fields.length && !tool.results.length && !downloads.children.length) {
    resultsList.textContent = 'Add a field or result call in your NexPro code to create a tool.';
  }
}

function fieldError(input, message) {
  if (message) input.setAttribute('aria-invalid', 'true');
  else input.removeAttribute('aria-invalid');
  document.getElementById(`${input.id}-error`).textContent = message;
  return !message;
}

function validate(input) {
  if (!input.validity.valid) return fieldError(input, input.dataset.message || input.validationMessage);
  if (input.type === 'file' && input.files[0]?.size > 512 * 1024) {
    return fieldError(input, 'Choose a CSV file of up to 512 KB.');
  }
  return fieldError(input, '');
}

async function fieldValue(input) {
  if (input.type === 'number') return input.valueAsNumber;
  if (input.type === 'checkbox') return input.checked;
  if (input.type === 'file') {
    return new TextDecoder('utf-8', { fatal: true }).decode(await input.files[0].arrayBuffer());
  }
  return input.value;
}

let revision = 0;

export const toolPreview = {
  render,
  clear() {
    revision++;
    downloads.replaceChildren();
    panel.hidden = true;
    fieldList.replaceChildren();
    resultsList.replaceChildren();
  },
  setEnabled(available) {
    calculate.disabled = !available;
  },
  onSubmit(run) {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (calculate.disabled) return;
      downloads.replaceChildren();
      const inputs = [...fieldList.querySelectorAll('input, select')];
      const invalid = inputs.filter(input => !validate(input));
      if (invalid.length) {
        invalid[0].focus();
        return;
      }
      const current = ++revision;
      const entries = await Promise.all(inputs.map(async input => {
        try {
          return [input.name, await fieldValue(input)];
        } catch {
          if (revision === current) fieldError(input, 'Choose a readable UTF-8 CSV file.');
          return null;
        }
      }));
      if (revision === current && entries.every(Boolean)) run(Object.fromEntries(entries));
    });
  },
};
