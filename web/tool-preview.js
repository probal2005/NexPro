const panel = document.querySelector('#tool-panel');
const form = document.querySelector('#tool-form');
const fieldList = document.querySelector('#tool-fields');
const resultsList = document.querySelector('#tool-results');
const calculate = document.querySelector('#tool-calculate');

function render(tool, ok) {
  resultsList.replaceChildren();
  if (!ok) return;
  fieldList.replaceChildren();
  panel.hidden = false;
  calculate.hidden = tool.fields.length === 0;
  for (const [index, field] of tool.fields.entries()) {
    const wrapper = document.createElement('div');
    const label = document.createElement('label');
    const input = document.createElement('input');
    input.id = `tool-field-${index}`;
    input.name = field.label;
    input.type = field.kind;
    input.value = field.value;
    if (field.kind === 'number') {
      input.step = 'any';
      input.required = true;
      if (field.minimum !== null) input.min = field.minimum;
    } else {
      input.maxLength = 4096;
    }
    label.htmlFor = input.id;
    label.textContent = field.label;
    wrapper.append(label, input);
    fieldList.append(wrapper);
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
      if (!form.reportValidity()) return;
      const fields = Object.fromEntries([...fieldList.querySelectorAll('input')].map(input => [
        input.name, input.type === 'number' ? input.valueAsNumber : input.value,
      ]));
      run(fields);
    });
  },
};
