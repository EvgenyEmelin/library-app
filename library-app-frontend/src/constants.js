export const STATUSES = [
  { value: 'want', label: 'Хочу прочитать' },
  { value: 'reading', label: 'Читаю' },
  { value: 'read', label: 'Прочитано' },
];

export const STATUS_LABELS = Object.fromEntries(
  STATUSES.map((s) => [s.value, s.label])
);