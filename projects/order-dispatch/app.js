const form = document.querySelector('#order-form');
const fields = document.querySelector('#order-fields');
const orders = document.querySelector('#orders');
const template = document.querySelector('#order-template');
const check = document.querySelector('#check-orders');
const add = document.querySelector('#add-order');
const reset = document.querySelector('#reset-sample');
const status = document.querySelector('#status');
const shareStatus = document.querySelector('#share-status');
const readyList = document.querySelector('#ready-orders');
const blockedList = document.querySelector('#blocked-orders');
const readyCount = document.querySelector('#ready-count');
const blockedCount = document.querySelector('#blocked-count');
const worker = new Worker('/worker.js');
let source;
let sample;
let timer;

function setEnabled(enabled) {
  fields.disabled = !enabled;
  add.disabled = !enabled;
  reset.disabled = !enabled;
  check.disabled = !enabled;
}

function labelOrders() {
  const rows = [...orders.querySelectorAll('.order')];
  rows.forEach((row, index) => {
    const name = `Order ${index + 1}`;
    row.querySelector('legend').textContent = name;
    const remove = row.querySelector('.remove');
    remove.setAttribute('aria-label', `Remove ${name.toLowerCase()}`);
    remove.disabled = rows.length === 1;
  });
}

function addOrder(order = {}) {
  const row = template.content.firstElementChild.cloneNode(true);
  row.querySelector('[name=id]').value = order.id ?? '';
  row.querySelector('[name=quantity]').value = order.quantity ?? '';
  row.querySelector('[name=address]').value = order.address ?? '';
  row.querySelector('[name=paid]').checked = order.paid ?? false;
  orders.append(row);
  return row;
}

function loadSample() {
  orders.replaceChildren();
  for (const order of sample) addOrder(order);
  labelOrders();
}

function clearReport() {
  readyCount.textContent = '0';
  blockedCount.textContent = '0';
  readyList.replaceChildren();
  blockedList.replaceChildren();
}

function buildItem(text) {
  const item = document.createElement('li');
  item.textContent = text;
  return item;
}

function showReport({ ready, blocked }) {
  readyCount.textContent = ready.length;
  blockedCount.textContent = blocked.length;
  for (const id of ready) readyList.append(buildItem(id));
  for (const { id, reasons } of blocked) {
    const item = buildItem(id);
    const list = document.createElement('ul');
    for (const reason of reasons) list.append(buildItem(reason));
    item.append(list);
    blockedList.append(item);
  }
  status.textContent = 'Dispatch report updated.';
}

function fail(message) {
  clearTimeout(timer);
  worker.terminate();
  setEnabled(false);
  status.textContent = message;
}

function checkOrders() {
  const entries = [...orders.querySelectorAll('.order')].map(row => ({
    id: row.querySelector('[name=id]').value.trim(),
    quantity: Number(row.querySelector('[name=quantity]').value),
    address: row.querySelector('[name=address]').value,
    paid: row.querySelector('[name=paid]').checked,
  }));
  if (entries.some(entry => !entry.id)) {
    status.textContent = 'Enter an ID for every order.';
    return;
  }
  clearReport();
  setEnabled(false);
  status.textContent = 'Checking orders…';
  timer = setTimeout(() => fail('The check timed out. Reload to try again.'), 8000);
  worker.postMessage({ action: 'run', source, input: JSON.stringify(entries), modules: '{}', trace: false });
}

worker.onmessage = ({ data }) => {
  clearTimeout(timer);
  if (data.action === 'init') {
    if (!data.ok) {
      fail('NexPro could not load. Reload to try again.');
      return;
    }
    loadSample();
    checkOrders();
    return;
  }
  setEnabled(true);
  if (!data.ok) {
    status.textContent = 'NexPro could not check these orders. Review the inputs and try again.';
    return;
  }
  try {
    showReport(JSON.parse(data.output));
  } catch {
    status.textContent = 'NexPro returned an unexpected report.';
  }
};

worker.onerror = () => fail('NexPro could not load. Reload to try again.');

form.addEventListener('submit', event => {
  event.preventDefault();
  checkOrders();
});
orders.addEventListener('input', () => {
  status.textContent = 'Orders changed. Check again to update the report.';
});
orders.addEventListener('click', event => {
  const remove = event.target.closest('.remove');
  if (!remove || remove.disabled) return;
  remove.closest('.order').remove();
  labelOrders();
  add.focus();
  status.textContent = 'Order removed. Check again to update the report.';
});
add.addEventListener('click', () => {
  addOrder().querySelector('[name=id]').focus();
  labelOrders();
  status.textContent = 'Order added. Fill it in and check again.';
});
reset.addEventListener('click', () => {
  loadSample();
  checkOrders();
});
document.querySelector('#share-link').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(new URL(location.pathname, location.origin).href);
    shareStatus.textContent = 'Link copied.';
  } catch {
    shareStatus.textContent = 'Copy the link from your address bar.';
  }
});

setEnabled(false);
timer = setTimeout(() => fail('NexPro took too long to load. Reload to try again.'), 45000);
fetch('/projects/order-dispatch/example.json')
  .then(response => {
    if (!response.ok) throw new Error('Example unavailable');
    return response.json();
  })
  .then(program => {
    source = program.source;
    sample = JSON.parse(program.input);
    worker.postMessage({ action: 'init' });
  })
  .catch(() => fail('The order example could not load. Reload to try again.'));
