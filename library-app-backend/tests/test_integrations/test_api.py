from datetime import UTC, datetime, timedelta

import pytest
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


        book_1 = BookORM(title='Книга 1', author="Пушкин", status="read")
        repo.add(book_1)
        db_session.flush()

        response = client.get("/api/books")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1

        assert data[0]["title"] == book_1.title
        assert data[0]["author"] == book_1.author
        assert data[0]["status"] == book_1.status
        assert data[0]["created_at"] is not None


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



class TestGetBookById:

    def test_book_by_id_success(self, client):

        payload = {
        "title": "Книга 1",
        "author": "Пушкин",
        "status": "read"
    }
    
        create_response = client.post("/api/books", json=payload)

        assert create_response.status_code == 201

        book_id = create_response.json()["id"]
        response = client.get(f"/api/books/{book_id}")

        assert response.status_code == 200

        data = response.json()
        assert data["id"] == book_id
        assert data["title"] == payload["title"]
        assert data["author"] == payload["author"]
        assert data["status"] == payload["status"]

    def test_book_by_id_does_not_exist(self, client):
        book_id = 999999

        response = client.get(f"/api/books/{book_id}")

        assert response.status_code == 404

        assert response.json() == {"error" : f"Book with id={book_id} not found"}

    @pytest.mark.parametrize("book_id", ["abc", 0, -1])
    def test_bok_by_id_not_valid(self, client, book_id):

        response = client.get(f"/api/books/{book_id}")

        assert response.status_code == 400

class TestPostBook:

    def test_post_book_valid(self, client):
        payload = {"title":"Книга 1", "author": "Пушкин", "status": "want"}

        response = client.post("/api/books", json=payload)

        assert response.status_code == 201

        data = response.json()

        assert data["id"] is not None
        assert data["created_at"] is not None
        assert data["updated_at"] is not None

    @pytest.mark.parametrize("payload, expected_status",(
            [{"title": "", "rating": 5, "year": 100, "status": "want"}, 400],
            [{"title": " ", "rating": 5, "year": 100, "status": "want"}, 400],
            [{"title": "test", "rating": 7, "year": 100, "status": "want"}, 400],
            [{"title": "test", "rating": 5, "year": -1, "status": "want"}, 400],
            [{"title": "test", "rating": 5, "year": 100, "status": "foo"}, 400],
            [{}, 400],
    ))
    def test_post_book_not_valid(self, client, payload, expected_status):

        response = client.post("/api/books", json=payload)

        assert response.status_code == expected_status
        assert "error" in response.json()

    def test_post_book_invalid_json(self, client):
        response = client.post(
            "/api/books",
            content="{",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 400

    def test_post_book_extra_field_ignored(self, client):
        payload = {
            "title": "Книга 1",
            "author": "Пушкин",
            "status": "want",
            "extra_field": "ignored_value",
        }

        response = client.post("/api/books", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert "extra_field" not in data
        assert data["title"] == "Книга 1"





    


