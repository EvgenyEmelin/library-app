import BookCard from './BookCard.jsx';

export default function BookList({ books, loading, error, onEdit, onDelete, onRetry }) {
  if (error) {
    return (
      <div className="state state-error">
        <p>Не удалось загрузить книги: {error}</p>
        <button className="btn btn-ghost" onClick={onRetry}>Попробовать снова</button>
      </div>
    );
  }

  if (loading && books.length === 0) {
    return <div className="state">Загрузка...</div>;
  }

  if (!loading && books.length === 0) {
    return <div className="state">Книг нет. Добавьте первую 👆</div>;
  }

  return (
    <div className="book-list" aria-busy={loading}>
      {books.map((book) => (
        <BookCard
          key={book.id}
          book={book}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}