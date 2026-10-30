import { useCallback, useEffect, useState } from 'react';
import { api } from './api.js';
import { useDebounced } from './hooks/useDebounced.js';
import Filters from './components/Filters.jsx';
import BookList from './components/BookList.jsx';
import BookFormModal from './components/BookFormModal.jsx';

export default function App() {
  const [searchInput, setSearchInput] = useState('');
  const debouncedSearch = useDebounced(searchInput, 300);
  const [status, setStatus] = useState('');

  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  // modal state: null = closed, {} = create, book = edit
  const [editing, setEditing] = useState(null);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    const ctrl = new AbortController();
    setLoading(true);
    setError(null);

    api
      .list({ status, search: debouncedSearch }, ctrl.signal)
      .then((data) => {
        setBooks(data);
        setLoading(false);
      })
      .catch((err) => {
        if (err.name === 'AbortError') return;
        setError(err.message);
        setLoading(false);
      });

    return () => ctrl.abort();
  }, [status, debouncedSearch, refreshKey]);

  const refresh = useCallback(() => setRefreshKey((k) => k + 1), []);

  const closeModal = () => {
    setCreating(false);
    setEditing(null);
  };
  const openCreate = () => {
    setEditing(null);
    setCreating(true);
  };
  const openEdit = (book) => {
    setCreating(false);
    setEditing(book);
  };

  const handleSave = async (payload) => {
    if (editing) {
      await api.update(editing.id, payload);
    } else {
      await api.create(payload);
    }
    closeModal();
    refresh();
  };

  const handleDelete = async (id) => {
    if (!confirm('Удалить эту книгу?')) return;
    try {
      await api.remove(id);
      refresh();
    } catch (err) {
      alert('Не получилось удалить: ' + err.message);
    }
  };

  const modalOpen = creating || editing !== null;

  return (
    <div className="app">
      <header className="app-header">
        <h1>📚 Моя библиотека</h1>
        <button className="btn btn-primary" onClick={openCreate}>
          + Добавить книгу
        </button>
      </header>

      <Filters
        search={searchInput}
        onSearchChange={setSearchInput}
        status={status}
        onStatusChange={setStatus}
      />

      <BookList
        books={books}
        loading={loading}
        error={error}
        onEdit={openEdit}
        onDelete={handleDelete}
        onRetry={refresh}
      />

      {modalOpen && (
        <BookFormModal
          initial={editing}
          onClose={closeModal}
          onSave={handleSave}
        />
      )}
    </div>
  );
}