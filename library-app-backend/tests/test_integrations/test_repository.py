import datetime

import pytest
from repository.book import BookORM, BookRepository
from sqlalchemy.orm.session import Session


class TestGetAllBookRepo: ##Тесты для методы get_all_books в репозитории

    def test_get_all_books_empty(self, repo: BookRepository):
        result = repo.get_all_books()
        assert result == []

    def test_all_books_created_at_desc(self, repo: BookRepository):
        now = datetime.datetime.now(datetime.UTC)

        book_old = BookORM(title="Книга 1", author="Автор", created_at = now - datetime.timedelta(hours=2))

        book_mid = BookORM(title="Книга 2", author="Автор", created_at = now - datetime.timedelta(hours=1))

        book_new = BookORM(title="Книга 3", author="Автор", created_at = now)

        repo.add(book_old)
        repo.add(book_mid)
        repo.add(book_new)

        result = repo.get_all_books()

        assert [book.title for book in result] == ["Книга 3", "Книга 2", "Книга 1"]

    @pytest.mark.parametrize("search_char, expected_title",
                             [
                                 ("_", "file_name"),
                                 ("%", "100%")
                             ])
    def test_all_books_like(self, search_char: str, expected_title: str, repo: BookRepository):

        book = BookORM(title="Книга 1", author="Булгаков", status="read")
        wrong_book = BookORM(title="file_name", author="Булгаков", status="read")
        wrong_book2 = BookORM(title="100%", author="Булгаков", status="read")

        repo.add(book)
        repo.add(wrong_book)
        repo.add(wrong_book2)

        result = repo.get_all_books(search=search_char)

        assert len(result) == 1
        assert result[0].title == expected_title

    @pytest.mark.parametrize(
                            "filter_kwargs, expected_title",
                            [
                                ({"status": "read"}, "Мастер и Маргарита"),
                                ({"search": "булг"}, "Мастер и Маргарита"),
                                ({"search": "Мастер"}, "Мастер и Маргарита"),
                            ],
)
    def test_get_all_books_by_filter(self, filter_kwargs: dict, expected_title: str, repo: BookRepository):
        target_book = BookORM(title="Мастер и Маргарита", author="Булгаков", status="read")
        other_book = BookORM(title="Капитанская дочка", author="Пушкин", status="want")
        repo.add(target_book)
        repo.add(other_book)
        result = repo.get_all_books(**filter_kwargs)
        assert len(result) == 1
        assert result[0].title == expected_title

    def test_get_all_books_combined_search_and_status(self, repo: BookRepository):

        only_search_match = BookORM(title="Book X", author="Булгаков", status="want")
        only_status_match = BookORM(title="Other", author="Булгаков", status="read")
        both_match = BookORM(title="Target X", author="Булгаков", status="read")

        repo.add(only_search_match)
        repo.add(only_status_match)
        repo.add(both_match)

        result = repo.get_all_books(search="x", status="read")

        assert len(result) == 1
        assert result[0].title == "Target X"
        assert result[0].status == "read"


class TestGetByIdRepo: ##Тесты для методы get_by_id в репозитории

    @pytest.mark.parametrize(
    "book_id, is_found",
    [
        pytest.param(1, True, id="existing_id"),
        pytest.param(999, False, id="non_existent_id"),
        pytest.param(0, False, id="zero_id"),
    ],
    )
    def test_get_by_id(self, book_id: int, is_found: bool, repo: BookRepository):
        book = BookORM(id="1", title="Book", author="Пушкин", status="read")
        repo.add(book)

        result = repo.get_by_id(book_id=book_id)

        if is_found:
            assert result is not None
            assert result.title == "Book"
            assert result.author == "Пушкин"
            assert result.status == "read"
        else:
            assert result is None

class TestAddRepo: ##Тесты для методы add в репозитории

    def test_add(self, repo: BookRepository, db_session: Session):

        book = BookORM(title="Book", author="Пушкин", status="read")

        repo.add(book)

        db_session.flush()

        result = repo.get_by_id(book.id)

        assert book.id is not None
        assert result is not None
        assert book.id == result.id

class TestDeleteRepo: ##Тесты для методы delete в репозитории

    def test_delete(self, repo: BookRepository, db_session: Session):

        book = BookORM(title="Book", author="Пушкин", status="read")

        repo.add(book)

        db_session.flush()
        book_id = book.id
        assert book_id is not None
        repo.delete(book)
        db_session.flush()

        result = repo.get_by_id(book_id)

        assert result is None


