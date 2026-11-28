const panel = document.querySelector('#tool-panel');
const form = document.querySelector('#tool-form');
const fieldList = document.querySelector('#tool-fields');
const resultsList = document.querySelector('#tool-results');
const calculate = document.querySelector('#tool-calculate');

function render(tool, ok) {
  resultsList.replaceChildren();
  if (!ok || !tool) return;
  fieldList.replaceChildren();
  panel.hidden = false;
  calculate.hidden = tool.fields.length === 0;
  for (const [index, field] of tool.fields.entries()) {
    const wrapper = document.createElement('div');
    const label = document.createElement('label');
    const input = document.createElement(field.kind === 'select' ? 'select' : 'input');
    input.id = `tool-field-${index}`;
    input.name = field.label;
    if (field.kind === 'select') {
      for (const option of field.options) input.add(new Option(option));
    } else {
      input.type = field.kind;
    }
    input.value = field.value;
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
    input.addEventListener('input', () => {
      if (input.hasAttribute('aria-invalid')) validate(input);
    });
    wrapper.append(label, input, message);
    fieldList.append(wrapper);
    const error = tool.errors?.[field.label];
    if (typeof error === 'string') {
      message.textContent = error;
      input.setAttribute('aria-invalid', 'true');
    }
  }
  for (const { label, value } of tool.results) {
    const term = document.createElement('dt');
    const detail = document.createElement('dd');
    term.textContent = label;
    detail.textContent = value;
    resultsList.append(term, detail);
  }
  if (!tool.fields.length && !tool.results.length) {
    resultsList.textContent = 'Add a field or result call in your NexPro code to create a tool.';
  }
}

function validate(input) {
  const invalid = !input.validity.valid;
  if (invalid) input.setAttribute('aria-invalid', 'true');
  else input.removeAttribute('aria-invalid');
  document.getElementById(`${input.id}-error`).textContent = (invalid ? input.dataset.message || input.validationMessage : '');
  return !invalid;
}

export const toolPreview = {
  render,
  clear() {
    panel.hidden = true;
    fieldList.replaceChildren();
    resultsList.replaceChildren();
  },
  setEnabled(available) {
    calculate.disabled = !available;
  },
  onSubmit(run) {
    form.addEventListener('submit', event => {
      event.preventDefault();
      const inputs = [...fieldList.querySelectorAll('input, select')];
      const invalid = inputs.filter(input => !validate(input));
      if (invalid.length) {
        invalid[0].focus();
        return;
      }
      const fields = Object.fromEntries(inputs.map(input => [
        input.name, input.type === 'number' ? input.valueAsNumber : input.type === 'checkbox' ? input.checked : input.value,
      ]));
      run(fields);
    });
  },
};
