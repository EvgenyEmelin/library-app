from datetime import UTC, datetime, timedelta

from models.book import BookORM
from repository.book import BookRepository
from sqlalchemy.orm import Session


class TestGetBooksApi:

    def test_get_books(self,client):
        response = client.get("/api/books")
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_books_existent(self, client, repo: BookRepository, db_session: Session):

        response = client.get("/api/books")

        book_1 = BookORM(title='Книга 1', author="Пушкин", status="read")
        book_2 = BookORM(title='Книга 2', author="Пушкин", status="read")

        repo.add(book_1)
        repo.add(book_2)

        db_session.flush()

        result = repo.get_all_books()

        assert response.status_code == 200
        assert len(result) == 2
        assert result[0].title == book_1.title
        assert result[0].author == book_1.author
        assert result[0].status == book_1.status

    def test_get_books_created_at(self, client, repo: BookRepository, db_session: Session):

        now = datetime.now(UTC)

        book_1 = BookORM(title='Книга 1', author="Пушкин", status="read", created_at=now - timedelta(minutes=5))
        book_2 = BookORM(title='Книга 2', author="Лермонтов", status="want", created_at=now)

        repo.add(book_1)
        repo.add(book_2)

        db_session.flush()

        response = client.get("/api/books")
        data = response.json()

        assert data[0]["title"] == "Книга 2"
        assert data[1]["title"] == "Книга 1"


