import { STATUS_LABELS } from '../constants.js';

export default function BookCard({ book, onEdit, onDelete }) {
  const { id, title, author, year, status, rating, notes } = book;

  return (
    <article className="book-card">
      <header className="book-header">
        <h3>{title}</h3>
        <span className={`status status-${status}`}>
          {STATUS_LABELS[status] ?? status}
        </span>
      </header>

      <div className="book-author">
        {author}{year ? `, ${year}` : ''}
      </div>

      {rating != null && (
        <div className="book-rating">
          {'★'.repeat(rating)}
          {'☆'.repeat(5 - rating)}
        </div>
      )}

      {notes && <p className="book-notes">{notes}</p>}

      <div className="card-actions">
        <button className="btn btn-ghost" onClick={() => onEdit(book)}>
          ✏️ Редактировать
        </button>
        <button className="btn btn-ghost btn-danger" onClick={() => onDelete(id)}>
          🗑️ Удалить
        </button>
      </div>
    </article>
  );
}