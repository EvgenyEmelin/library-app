const BASE = import.meta.env.VITE_API_URL ?? '/api';

async function readError(res) {
  try {
    const data = await res.json();
    return data?.error || `HTTP ${res.status}`;
  } catch {
    return `HTTP ${res.status}`;
  }
}

async function request(path, { signal, ...options } = {}) {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    signal,
    ...options,
  });
  if (!res.ok) throw new Error(await readError(res));
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  list({ status, search } = {}, signal) {
    const qs = new URLSearchParams();
    if (status) qs.set('status', status);
    if (search) qs.set('search', search);
    const query = qs.toString();
    return request('/books' + (query ? '?' + query : ''), { signal });
  },
  get(id, signal) {
    return request(`/books/${id}`, { signal });
  },
  create(data) {
    return request('/books', { method: 'POST', body: JSON.stringify(data) });
  },
  update(id, data) {
    return request(`/books/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  remove(id) {
    return request(`/books/${id}`, { method: 'DELETE' });
  },
};