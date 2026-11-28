const numbers = new Intl.NumberFormat(undefined, { maximumFractionDigits: 8 });

const metrics = {
  'batch-quality': [['Released', 'released', 'good'], ['Held', 'held', 'warn'], ['Row issues', 'row_issues', 'warn']],
  'booking-optimizer': [['Booking value', 'value_cents'], ['Accepted bookings', 'accepted', 'good'], ['Requests', 'requests']],
  'contact-cleaner': [['Clean contacts', 'contacts', 'good'], ['Duplicates', 'duplicates', 'warn'], ['Incomplete', 'incomplete', 'warn']],
  'critical-path': [['Total duration', 'duration'], ['Scheduled tasks', 'schedule']],
  'event-booking': [['Seats reserved', 'reserved'], ['Seats remaining', 'remaining'], ['Rejected requests', 'rejected', 'warn']],
  'expense-policy': [['Approved amount', 'approved_cents'], ['Decisions', 'decisions']],
  'expense-settlement': [['Total expenses', 'total_cents'], ['Participants', 'shares'], ['Transfers', 'payments']],
  'freelance-quote': [['Quote total', 'total_cents'], ['Subtotal', 'subtotal_cents'], ['Discount', 'discount_cents']],
  'fulfillment-planner': [['Fulfilled orders', 'summary.fulfilled', 'good'], ['Backordered', 'summary.backordered', 'warn'], ['Units allocated', 'summary.allocated_units'], ['Invalid orders', 'summary.invalid', 'warn']],
  'inventory-reorder': [['Items to reorder', 'reorder', 'warn']],
  'invoice-audit': [['Valid invoice total', 'total_cents'], ['Valid invoices', 'valid', 'good'], ['Issues', 'issues', 'warn']],
  'loan-repayment': [['Outstanding', 'balance.outstanding_cents'], ['Received', 'balance.received_cents', 'good'], ['Issues', 'issues', 'warn']],
  'monthly-budget': [['Remaining budget', 'total_remaining_cents'], ['Categories', 'categories']],
  'overtime-report': [['Employees', 'employees']],
  'quiz-score': [['Correct answers', 'correct', 'good'], ['Questions', 'total'], ['Mistakes', 'mistakes', 'warn']],
  reconciliation: [['Balance difference', 'balance_difference_cents'], ['Matched', 'matched', 'good'], ['Mismatches', 'mismatches', 'warn']],
  'service-timeline': [['Current notes', 'notes'], ['Removed notes', 'removed'], ['Issues', 'issues', 'warn']],
  'student-report-card': [['Ranked students', 'ranked', 'good'], ['Invalid entries', 'invalid', 'warn']],
  'subscription-changes': [['Amount due', 'due_cents'], ['Changes checked', 'history']],
  'supplier-performance': [['Suppliers', 'suppliers'], ['Issues', 'issues', 'warn']],
  'tournament-standings': [['Leading team', 'standings.0.team', 'good'], ['Teams', 'standings']],
  'warehouse-transfer': [['Source stock', 'stock.source'], ['Destination stock', 'stock.destination'], ['Destination capacity', 'stock.destination_capacity']],
  'warranty-triage': [['Covered', 'covered', 'good'], ['Expired', 'expired', 'warn'], ['Invalid', 'invalid', 'warn']],
};

const labels = {
  accepted: 'Accepted', actual_days: 'Actual days', backordered: 'Backordered',
  balance_difference_cents: 'Balance difference', code: 'Error code', cents: 'Amount',
  cost_cents: 'Cost', critical_path: 'Critical path', goal_difference: 'Goal difference',
  id: 'ID', incomplete: 'Incomplete rows', invalid_orders: 'Invalid orders', ranked: 'Ranked students',
  remaining_inventory: 'Remaining inventory', reorder: 'Reorder list', row_issues: 'Row issues',
  sku: 'SKU', standing: 'Standing', valid: 'Valid invoices', value_cents: 'Value',
};
const good = new Set(['accepted', 'approved', 'covered', 'fulfilled', 'matched', 'ready', 'released', 'valid']);
const warn = new Set(['backordered', 'blocked', 'duplicates', 'expired', 'held', 'incomplete', 'invalid',
  'invalid_orders', 'issues', 'mismatches', 'mistakes', 'rejected', 'review', 'row_issues']);

function element(tag, classes, text) {
  const node = document.createElement(tag);
  if (classes) node.className = classes;
  if (text !== undefined) node.textContent = text;
  return node;
}

function label(key) {
  return Object.hasOwn(labels, key) ? labels[key] :
    key.replace(/_cents$/, '').replaceAll('_', ' ').replace(/^./, char => char.toUpperCase());
}

function tone(key) {
  if (good.has(key)) return 'good';
  if (warn.has(key)) return 'warn';
  return 'neutral';
}

function isAmount(key) {
  return key === 'cents' || key.endsWith('_cents');
}

function textValue(key, value) {
  if (typeof value === 'number') {
    if (isAmount(key)) return `${numbers.format(value)}¢`;
    if (key.endsWith('_percent')) return `${numbers.format(value)}%`;
    return numbers.format(value);
  }
  if (value === null) return '—';
  if (value === '') return 'Blank';
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  return String(value);
}

function primitive(value) {
  return value === null || typeof value !== 'object';
}

function badge(text, color) {
  return element('span', `result-badge tone-${color}`, text);
}

function scalar(key, value) {
  if (key === 'status') return badge(label(String(value)), tone(value));
  if (key === 'accepted' && typeof value === 'boolean') return badge(value ? 'Accepted' : 'Rejected', value ? 'good' : 'warn');
  if (key === 'over_budget' && typeof value === 'boolean') return badge(value ? 'Over budget' : 'Within budget', value ? 'warn' : 'good');
  if (key === 'code') return element('code', 'result-code', textValue(key, value));
  return element('span', typeof value === 'number' ? 'result-number' : '', textValue(key, value));
}

function valuesGrid(value, omit = []) {
  const fields = element('dl', 'result-values');
  for (const [key, item] of Object.entries(value)) {
    if (omit.includes(key)) continue;
    const pair = element('div', 'result-pair');
    const content = element('dd');
    content.append(renderValue(key, item));
    pair.append(element('dt', '', label(key)), content);
    if (!primitive(item)) pair.classList.add('result-pair-wide');
    fields.append(pair);
  }
  return fields;
}

function resultTable(rows, name) {
  const keys = [...new Set(rows.flatMap(row => Object.keys(row)))];
  const container = element('div', 'result-table-wrap');
  container.tabIndex = 0;
  container.setAttribute('role', 'region');
  container.setAttribute('aria-label', `${name} table`);
  const table = element('table', 'result-table');
  const head = table.createTHead().insertRow();
  for (const key of keys) {
    const column = element('th', isAmount(key) ? 'result-number' : '', label(key));
    column.scope = 'col';
    head.append(column);
  }
  const body = table.createTBody();
  for (const row of rows) {
    const line = body.insertRow();
    for (const key of keys) {
      const value = Object.hasOwn(row, key) ? row[key] : null;
      const cell = line.insertCell();
      if (typeof value === 'number') cell.classList.add('result-number');
      cell.append(scalar(key, value));
    }
  }
  container.append(table);
  return container;
}

function reportRows(key, rows) {
  if (!rows.length) return element('p', 'result-empty', 'No entries');
  if (rows.every(primitive)) {
    const list = element(key === 'critical_path' || key === 'notes' ? 'ol' : 'ul', 'result-items');
    for (const row of rows) {
      const item = element('li');
      item.append(scalar(key, row));
      list.append(item);
    }
    return list;
  }
  if (rows.every(row => !primitive(row) && !Array.isArray(row) && Object.keys(row).length && Object.values(row).every(primitive))) {
    return resultTable(rows, label(key));
  }
  const cards = element('ul', 'result-cards');
  for (const row of rows) {
    const card = element('li', 'result-card');
    if (primitive(row) || Array.isArray(row)) {
      card.append(renderValue(key, row));
    } else {
      const title = ['id', 'name', 'number', 'reference', 'invoice', 'row'].find(field => Object.hasOwn(row, field));
      const status = Object.hasOwn(row, 'status') ? 'status' : Object.hasOwn(row, 'accepted') ? 'accepted' : undefined;
      if (title || status) {
        const header = element('div', 'result-card-title');
        if (title) header.append(element('strong', '', title === 'row' ? `Row ${row[title]}` : textValue(title, row[title])));
        if (status) header.append(scalar(status, row[status]));
        card.append(header);
      }
      card.append(valuesGrid(row, [title, status]));
    }
    cards.append(card);
  }
  return cards;
}

function renderValue(key, value) {
  if (Array.isArray(value)) return reportRows(key, value);
  if (!primitive(value)) return valuesGrid(value);
  return scalar(key, value);
}

export function outputMessage(text, error = false, code) {
  const box = element('div', error ? 'result-notice tone-warn' : 'result-notice');
  if (code) box.append(badge(code, 'warn'));
  box.append(element('p', '', text));
  return box;
}

function progress(labelText, value, max) {
  const row = element('div', 'result-progress');
  const labels = element('div', 'result-progress-labels');
  const percent = Math.round(value * 100 / max);
  labels.append(element('span', '', labelText), element('strong', '', `${percent}%`));
  const meter = element('progress');
  meter.max = max;
  meter.value = value;
  meter.setAttribute('aria-label', labelText);
  row.append(labels, meter);
  return row;
}

function scheduleView(rows, duration, criticalPath) {
  if (!rows.length || !duration) return reportRows('schedule', rows);
  const list = element('ul', 'result-schedule');
  const critical = new Set(criticalPath);
  for (const { id, start, finish } of rows) {
    const line = element('li');
    const heading = element('div', 'result-progress-labels');
    const task = element('span', '', id);
    if (critical.has(id)) task.append(badge('Critical', 'warn'));
    heading.append(task, element('strong', '', `${numbers.format(start)}–${numbers.format(finish)}`));
    const track = element('div', 'result-track');
    track.setAttribute('aria-hidden', 'true');
    const bar = element('span', critical.has(id) ? 'critical' : '');
    bar.style.marginInlineStart = `${start / duration * 100}%`;
    bar.style.width = `${(finish - start) / duration * 100}%`;
    track.append(bar);
    line.append(heading, track);
    list.append(line);
  }
  return list;
}

export function renderProjectResult(slug, result) {
  if (result?.error) {
    return outputMessage(result.error.message || String(result.error), true, result.error.code);
  }
  if (primitive(result) || Array.isArray(result)) return renderValue('result', result);
  const report = element('div', 'project-report');
  const consumed = new Set();
  const tiles = element('dl', 'result-metrics');
  for (const [title, path, color = 'neutral'] of metrics[slug] ?? []) {
    const parts = path.split('.');
    const value = parts.reduce((current, key) => current?.[key], result);
    if (value === undefined || value === null) continue;
    const count = Array.isArray(value) ? value.length : value;
    const tile = element('div', `result-metric tone-${count === 0 ? 'neutral' : color}`);
    tile.append(element('dt', '', title), element('dd', '', textValue(parts.at(-1), count)));
    tiles.append(tile);
    if (primitive(value)) consumed.add(path);
  }
  if (tiles.children.length) report.append(tiles);
  if (result.file_error) report.append(outputMessage('Check the CSV headers and row format.', true, result.file_error));
  if (slug === 'quiz-score' && result.total > 0) report.append(progress('Score', result.correct, result.total));
  if (slug === 'warehouse-transfer' && result.stock.destination_capacity > 0) {
    report.append(progress('Destination capacity used', result.stock.destination, result.stock.destination_capacity));
  }
  for (const [key, value] of Object.entries(result)) {
    if (consumed.has(key) || key === 'file_error') continue;
    const section = element('section', `result-section tone-${tone(key)}`);
    const heading = element('h3', '', label(key));
    const isObject = !primitive(value) && !Array.isArray(value);
    const counted = isObject ? Object.keys(value).filter(field => consumed.has(`${key}.${field}`)) : [];
    if (isObject && counted.length && counted.length === Object.keys(value).length) continue;
    if (slug === 'critical-path' && key === 'schedule') {
      section.append(heading, scheduleView(value, result.duration, result.critical_path));
    } else {
      section.append(heading, isObject ? valuesGrid(value, counted) : renderValue(key, value));
    }
    report.append(section);
  }
  return report;
}
