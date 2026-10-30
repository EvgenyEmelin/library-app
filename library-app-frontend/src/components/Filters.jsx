import { STATUSES } from '../constants.js';

export default function Filters({ search, onSearchChange, status, onStatusChange }) {
  return (
    <div className="filters">
      <input
        type="search"
        placeholder="Поиск по названию или автору..."
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
      />
      <select value={status} onChange={(e) => onStatusChange(e.target.value)}>
        <option value="">Все статусы</option>
        {STATUSES.map((s) => (
          <option key={s.value} value={s.value}>{s.label}</option>
        ))}
      </select>
    </div>
  );
}