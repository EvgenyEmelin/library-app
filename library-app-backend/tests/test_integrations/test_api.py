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
    def test_book_by_id_not_valid(self, client, book_id):

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

    @pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"title": "", "author": "A"}, 400),
        ({"title": " ", "author": "A"}, 400),
        ({"title": "T", "author": ""}, 400),
        ({"title": "T", "author": "A", "rating": 7}, 400),
        ({"title": "T", "author": "A", "rating": 0}, 400),
        ({"title": "T", "author": "A", "year": -1}, 400),
        ({"title": "T", "author": "A", "year": 3000}, 400),
        ({"title": "T", "author": "A", "status": "foo"}, 400),
        ({}, 400),
    ],
)
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

class TestPutBook:

    def test_update_book_valid(self, client):
        payload = {
                    "title": "Книга 1",
                    "author": "Пушкин",
                    "status": "want",
                }
        response_create = client.post("/api/books", json=payload)


        assert response_create.status_code == 201

        book_id = response_create.json()["id"]


        payload_update = {
        "title": "Книга новая",
        "author": "Автор",
        "status": "read",
    }

        response_update = client.put(f"/api/books/{book_id}", json=payload_update)

        assert response_update.status_code == 200

        data = response_update.json()

        assert data["id"] == book_id
        assert data["title"] == payload_update["title"]
        assert data["author"] == payload_update["author"]
        assert data["status"] == payload_update["status"]

    def test_update_book_not_valid(self, client):
        book_id = 999999

        payload_update = {
                "title": "Книга новая",
                "author": "Автор",
                "status": "read",
        }

        response_update = client.put(f"/api/books/{book_id}", json=payload_update)

        assert response_update.status_code == 404
        assert response_update.json() == {"error": f"Book with id={book_id} not found"}

    def test_update_book_empty(self, client):
        create = client.post("/api/books", json={"title": "X", "author": "Y"})
        book_id = create.json()["id"]
        response_update = client.put(f"/api/books/{book_id}", json={})
        assert response_update.status_code == 400

    def test_update_book_updated_at_gt_created_at(self, client):
        payload = {
                    "title": "Книга 1",
                    "author": "Пушкин",
                    "status": "want",
                }
        response_create = client.post("/api/books", json=payload)
        assert response_create.status_code == 201

        assert response_create.status_code == 201
        book_id = response_create.json()["id"]
        created_at = response_create.json()["created_at"]

        payload_update = {
                       "title": "Книга 1",
                       "author": "Пушкин",
                       "status": "want",
                }
        response_update = client.put(f"/api/books/{book_id}", json=payload_update)
        assert response_update.status_code == 200
        
        updated_data = response_update.json()

        assert updated_data["created_at"] == created_at
        assert updated_data["updated_at"] > created_at

    def test_update_book_wrong_id(self, client):
        book_id = "abc"

        payload_update = {
                       "title": "Книга 1",
                       "author": "Пушкин",
                       "status": "want",
                }

        response_update = client.put(f"/api/books/{book_id}", json=payload_update)

        assert response_update.status_code == 400

class TestDeleteBook:
    def test_delete_book_valid(self, client):

        payload = {
            "title": "Книга для удаления",
            "author": "Пушкин",
            "status": "want",
        }
        response_create = client.post("/api/books", json=payload)
        assert response_create.status_code == 201
        book_id = response_create.json()["id"]

        response_delete = client.delete(f"/api/books/{book_id}")
        assert response_delete.status_code == 204
        assert response_delete.content == b""


        response_get = client.get(f"/api/books/{book_id}")
        assert response_get.status_code == 404

    def test_delete_book_not_found(self, client):
        book_id = 999999
        response = client.delete(f"/api/books/{book_id}")

        assert response.status_code == 404
        assert response.json() == {"error": f"Book with id={book_id} not found"}

    @pytest.mark.parametrize("book_id", ["abc", 0, -1])
    def test_delete_book_invalid_id(self, client, book_id):
        response = client.delete(f"/api/books/{book_id}")

        assert response.status_code == 400




