import { useEffect, useState } from 'react';
import { STATUSES } from '../constants.js';

const EMPTY = {
  title: '',
  author: '',
  year: '',
  status: 'want',
  rating: '',
  notes: '',
};

function toForm(book) {
  if (!book) return { ...EMPTY };
  return {
    title: book.title ?? '',
    author: book.author ?? '',
    year: book.year ?? '',
    status: book.status ?? 'want',
    rating: book.rating ?? '',
    notes: book.notes ?? '',
  };
}

function toPayload(v) {
  return {
    title: v.title.trim(),
    author: v.author.trim(),
    year: v.year === '' ? null : Number(v.year),
    status: v.status,
    rating: v.rating === '' ? null : Number(v.rating),
    notes: v.notes.trim() || null,
  };
}

export default function BookFormModal({ initial, onClose, onSave }) {
  const [values, setValues] = useState(() => toForm(initial));
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'Escape' && !saving) onClose();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose, saving]);

  const set = (key) => (e) =>
    setValues((prev) => ({ ...prev, [key]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!values.title.trim() || !values.author.trim()) {
      setError('Название и автор обязательны');
      return;
    }

    setSaving(true);
    try {
      await onSave(toPayload(values));
    } catch (err) {
      setError(err.message);
      setSaving(false);
    }
  };

  const handleBackdrop = (e) => {
    if (e.target === e.currentTarget && !saving) onClose();
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdrop}>
      <div className="modal" role="dialog" aria-modal="true">
        <form onSubmit={handleSubmit}>
          <h2>{initial ? 'Редактировать книгу' : 'Добавить книгу'}</h2>

          <label>
            Название *
            <input
              value={values.title}
              onChange={set('title')}
              maxLength={200}
              autoFocus
            />
          </label>

          <label>
            Автор *
            <input
              value={values.author}
              onChange={set('author')}
              maxLength={200}
            />
          </label>

          <div className="row">
            <label>
              Год
              <input
                type="number"
                value={values.year}
                onChange={set('year')}
                min={0}
                max={2100}
              />
            </label>

            <label>
              Статус
              <select value={values.status} onChange={set('status')}>
                {STATUSES.map((s) => (
                  <option key={s.value} value={s.value}>{s.label}</option>
                ))}
              </select>
            </label>

            <label>
              Оценка
              <select value={values.rating} onChange={set('rating')}>
                <option value="">—</option>
                {[1, 2, 3, 4, 5].map((n) => (
                  <option key={n} value={n}>{'★'.repeat(n)}</option>
                ))}
              </select>
            </label>
          </div>

          <label>
            Заметки
            <textarea
              value={values.notes}
              onChange={set('notes')}
              rows={3}
            />
          </label>

          {error && <div className="form-error">{error}</div>}

          <div className="modal-actions">
            <button
              type="button"
              className="btn btn-ghost"
              onClick={onClose}
              disabled={saving}
            >
              Отмена
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={saving}
            >
              {saving ? 'Сохраняем...' : 'Сохранить'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}