const form = document.querySelector('#bill-form');
const bill = document.querySelector('#bill');
const people = document.querySelector('#people');
const calculate = document.querySelector('#calculate');
const status = document.querySelector('#status');
const shares = document.querySelector('#shares');
const total = document.querySelector('#total');
const shareStatus = document.querySelector('#share-status');
const amounts = new Intl.NumberFormat(undefined, {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const worker = new Worker('/worker.js');
let source;
let timeout;

function setUnavailable(message) {
  clearTimeout(timeout);
  worker.terminate();
  calculate.disabled = true;
  status.textContent = message;
}

function startCalculation() {
  if (calculate.disabled) return;
  calculate.disabled = true;
  shares.replaceChildren();
  total.hidden = true;
  status.textContent = 'Calculating…';
  timeout = setTimeout(() => setUnavailable('Calculation timed out. Reload to try again.'), 8000);
  worker.postMessage({
    action: 'run', source, modules: '{}', trace: false,
    input: JSON.stringify({ bill: bill.value, people: people.value }),
  });
}

function addShare(count, cents) {
  if (!count) return;
  const row = document.createElement('li');
  const label = document.createElement('span');
  label.textContent = count === 1 ? '1 person pays' : `${count} people each pay`;
  const amount = document.createElement('strong');
  amount.textContent = amounts.format(cents / 100);
  row.append(label, amount);
  shares.append(row);
}

worker.onmessage = ({ data }) => {
  clearTimeout(timeout);
  if (!data.ok && data.action === 'init') {
    setUnavailable('NexPro could not load. Reload to try again.');
    return;
  }
  calculate.disabled = false;
  if (data.action === 'init') {
    startCalculation();
    return;
  }
  if (!data.ok) {
    status.textContent = 'The calculator could not run. Try again.';
    return;
  }
  try {
    const result = JSON.parse(data.output);
    if (result.error) {
      status.textContent = result.error;
      return;
    }
    addShare(result.base_people, result.base_cents);
    addShare(result.extra_people, result.extra_cents);
    total.textContent = `Total: ${amounts.format(result.total_cents / 100)}`;
    total.hidden = false;
    status.textContent = 'Split calculated';
  } catch {
    status.textContent = 'The calculator returned an unexpected result.';
  }
};

worker.onerror = () => setUnavailable('NexPro could not load. Reload to try again.');
form.addEventListener('submit', event => {
  event.preventDefault();
  startCalculation();
});

document.querySelector('#share').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(new URL(location.pathname, location.origin).href);
    shareStatus.textContent = 'Link copied.';
  } catch {
    shareStatus.textContent = 'Copy the link from your address bar.';
  }
});

timeout = setTimeout(() => setUnavailable('NexPro took too long to load. Reload to try again.'), 45000);
fetch('/projects/bill-splitter/main.pa')
  .then(response => {
    if (!response.ok) throw new Error('Source unavailable');
    return response.text();
  })
  .then(program => {
    source = program;
    worker.postMessage({ action: 'init' });
  })
  .catch(() => setUnavailable('The calculator source could not load. Reload to try again.'));
