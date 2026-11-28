// Input forms for the NexPro project demos.
const text = (label, required = true) => ({ type: 'text', label, required });
const multiline = label => ({ type: 'textarea', label, required: true });
const number = (label, step = 'any', initial = 0) => ({ type: 'number', label, step, initial });
const object = fields => ({ type: 'object', fields });
const list = (label, itemName, item) => ({ type: 'list', label, itemName, item });
const rows = (label, itemName, fields) => list(label, itemName, object(fields));

export const schemas = {
  'invoice-audit': rows('Invoices', 'Invoice', {
    number: text('Invoice number'), cents: number('Amount (cents)', '1'),
    customer: object({ name: text('Customer name'), email: text('Customer email', false) }),
  }),
  'subscription-changes': object({
    plan: object({
      seats: number('Starting seats', '1'), unit_cents: number('Starting price per seat (cents)', '1'),
      credit_cents: number('Starting credit (cents)', '1'),
    }),
    changes: rows('Plan changes', 'Change', {
      seats: number('New seats', '1'), unit_cents: number('New price per seat (cents)', '1'),
      credit_cents: number('New credit (cents)', '1'),
    }),
  }),
  'event-booking': object({
    capacity: number('Event capacity', '1'),
    requests: rows('Seat requests', 'Request', { name: text('Attendee name'), seats: number('Seats requested', '1') }),
  }),
  'warranty-triage': object({
    coverage_days: number('Coverage limit (days)', '1'),
    claims: rows('Warranty claims', 'Claim', { id: text('Claim ID'), age_days: number('Claim age (days)', '1') }),
  }),
  'supplier-performance': rows('Deliveries', 'Delivery', {
    supplier: text('Supplier'), planned_days: number('Planned days', '1'), actual_days: number('Actual days', '1'),
  }),
  'expense-policy': object({
    meal_cap: number('Meal limit (cents)', '1'),
    expenses: rows('Expenses', 'Expense', {
      id: text('Expense ID'), category: text('Category'), cents: number('Expense (cents)', '1'),
    }),
  }),
  'warehouse-transfer': object({
    stock: object({
      source: number('Source stock', '1'), destination: number('Destination stock', '1'),
      destination_capacity: number('Destination capacity', '1'),
    }),
    quantities: list('Transfers', 'Transfer', number('Units to transfer', '1')),
  }),
  'service-timeline': object({
    notes: list('Starting notes', 'Note', text('Note')),
    edits: rows('Timeline edits', 'Edit', {
      action: text('Action (insert or remove)'), position: number('Position (zero-based)', '1'), note: text('New note', false),
    }),
  }),
  'batch-quality': object({
    max_percent: number('Maximum rejection rate (%)'), csv: multiline('Batch CSV'),
  }),
  'loan-repayment': object({
    principal_cents: number('Principal (cents)', '1'),
    payments: rows('Payments', 'Payment', { reference: text('Payment reference'), cents: number('Amount (cents)', '1') }),
  }),
  'expense-settlement': object({
    participants: rows('Participants', 'Participant', {
      name: text('Name'), paid_cents: number('Amount paid (cents)', '1'),
    }),
  }),
  'freelance-quote': object({
    discount_percent: number('Discount (%)'),
    items: rows('Quote items', 'Item', {
      name: text('Work item'), hours: number('Hours'), rate_cents: number('Hourly rate (cents)', '1'),
    }),
  }),
  'student-report-card': rows('Students', 'Student', {
    name: text('Student name'), scores: list('Scores', 'Score', number('Score')),
  }),
  'inventory-reorder': rows('Inventory', 'Product', {
    sku: text('SKU'), stock: number('Current stock', '1'), minimum: number('Minimum stock', '1'),
    target: number('Target stock', '1', 1),
  }),
  'monthly-budget': rows('Budget categories', 'Category', {
    category: text('Category name'), budget_cents: number('Budget (cents)', '1'),
    spent_cents: number('Spent (cents)', '1'),
  }),
  'contact-cleaner': rows('Contacts', 'Contact', {
    name: text('Name', false), email: text('Email', false), phone: text('Phone', false),
  }),
  'quiz-score': object({
    questions: rows('Questions', 'Question', { question: text('Question'), answer: text('Correct answer') }),
    answers: list('Submitted answers', 'Answer', text('Submitted answer', false)),
  }),
  'overtime-report': object({
    weekly_threshold: number('Weekly threshold (hours)', 'any', 40),
    overtime_multiplier: number('Overtime multiplier', 'any', 1.5),
    employees: rows('Employees', 'Employee', {
      name: text('Employee name'), rate_cents: number('Hourly rate (cents)', '1'),
      hours: list('Daily hours', 'Day', number('Hours')),
    }),
  }),
  'tournament-standings': object({
    teams: list('Teams', 'Team', text('Team name')),
    matches: rows('Matches', 'Match', {
      home: text('Home team'), away: text('Away team'),
      home_goals: number('Home goals', '1'), away_goals: number('Away goals', '1'),
    }),
  }),
};
