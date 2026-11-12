import re
from datetime import UTC, datetime, timedelta
from tkinter import W

import pytest
from core.exceptions import BookNotFound
from repository.book import BookORM, BookRepository
from schemas.book import BookCreateSchema, BookUpdateSchema
from service.book import BookService
from sqlalchemy.orm import Session


class TestGetBookService:


    def test_get_book_success(self, service: BookService, repo: BookRepository, db_session: Session):
        book = BookORM(id=1,title='Книга 1', author="Пушкин", status="read")

        repo.add(book)
        db_session.flush()

        result = service.get_book(book.id)

        assert result is not None
        assert result.id == book.id
        assert result.title == book.title
        assert result.author == book.author
        assert result.status == book.status

    def test_get_book_not_found(self, service: BookService, db_session: Session):
        not_valid_id = 9999

        with pytest.raises(BookNotFound) as exp:
            service.get_book(not_valid_id)

        assert str(not_valid_id) in str(exp.value)

class TestCreateBookService:

    def test_create_book_success(self, service: BookService, repo: BookRepository, db_session: Session):
        book_schema = BookCreateSchema(title='Книга 1', author='Пушкин', status='read')

        result = service.create_book(book_schema)

        assert result.id is not None
        assert result.created_at is not None
        assert result.title == book_schema.title
        assert result.author == book_schema.author
        assert result.status == book_schema.status

    def test_create_book_without_notes(self, service: BookService, repo: BookRepository, db_session: Session):
        book_schema = BookCreateSchema(title='Книга 1', author='Пушкин', status='read', notes="")

        result = service.create_book(book_schema)

        assert result.notes is None

class TestUpdateBookService:

    def test_update_book(self, service: BookService, repo: BookRepository, db_session: Session):

        book = BookORM(id=1,title='Книга 1', author="Пушкин", status="read")
        book_update_data = BookUpdateSchema(title="Книга 12", author="Булгаков")

        repo.add(book)
        db_session.flush()

        created_at = book.created_at
        old_time = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=1)

        result = service.update_book(book.id, data=book_update_data)

        assert result.title == book_update_data.title
        assert result.author == book_update_data.author
        assert result.created_at == created_at
        assert result.updated_at > old_time

    def test_update_status(self, service: BookService, repo: BookRepository, db_session: Session):
        book = BookORM(id=1,title='Книга 1', author="Пушкин", status="read")
        book_update_data = BookUpdateSchema(title="Книга 12", author="Булгаков")

        repo.add(book)
        db_session.flush()

        result = service.update_book(book.id, data=book_update_data)

        assert result.status == book_update_data.status

    def test_update_non_existent(self, service: BookService):
        wrong_id = 99999
        book_update_data = BookUpdateSchema(title="Книга 12", author="Булгаков")

        with pytest.raises(BookNotFound) as exp:
            service.update_book(wrong_id, book_update_data)

        assert str(wrong_id) in str(exp.value)

class TestDeleteBookService:

    def test_delete_book(self, service: BookService, repo: BookRepository, db_session: Session):

        book = BookORM(id=1,title='Книга 1', author="Пушкин", status="read")

        repo.add(book)
        db_session.flush()
        book_id = book.id
        service.delete_book(book_id)

        with pytest.raises(BookNotFound) as exp:
            service.delete_book(book_id)

        assert str(book_id) in str(exp.value)

    def test_delete_book_non_existent(self, service: BookService):

        wrong_id = 9999

        with pytest.raises(BookNotFound) as exp:
            service.delete_book(wrong_id)

        assert str(wrong_id) in str(exp.value)

class TestListBookService:

    def test_list_books(self, service: BookService, repo: BookRepository, db_session: Session):
        book_1 = BookORM(title='Книга 1', author="Пушкин", status="read")
        book_2 = BookORM(title='Книга 2', author="Гоголь", status="read")
        book_3 = BookORM(title='Книга 3', author="Толстой", status="read")

        repo.add(book_1)
        repo.add(book_2)
        repo.add(book_3)

        db_session.flush()

        result = service.list_books(search=" ")

        assert len(result) == 3

    def test_list_books_search(self, service: BookService, repo: BookRepository, db_session: Session):
        book_1 = BookORM(title='Книга 1', author="Пушкин", status="read")
        book_2 = BookORM(title='Книга 2', author="Гоголь", status="read")

        repo.add(book_1)
        repo.add(book_2)

        db_session.flush()

        result = service.list_books(search="пуш")

        assert len(result) == 1
        assert result[0].author == "Пушкин"
