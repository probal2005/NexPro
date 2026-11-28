// Input forms for the NexPro project demos.
const text = (label, required = true) => ({ type: 'text', label, required });
const number = (label, step = 'any', initial = 0) => ({ type: 'number', label, step, initial });
const object = fields => ({ type: 'object', fields });
const list = (label, itemName, item) => ({ type: 'list', label, itemName, item });
const rows = (label, itemName, fields) => list(label, itemName, object(fields));

export const schemas = {
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
