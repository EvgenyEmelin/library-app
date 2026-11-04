from core.exceptions import BookNotFound
from models.book import BookORM
from repository.book import BookRepository
from schemas.book import BookCreateSchema, BookUpdateSchema
from sqlalchemy.orm import Session


class BookService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.book_repository =  BookRepository(db)

    def list_books(
        self,
        status: str | None = None,
        search: str | None = None
 )-> list[BookORM]:

        search = search.strip() if search else None
        if search == "":
            search = None
        return self.book_repository.get_all_books(status = status, search = search)

    def get_book(self,
                 book_id: int) -> BookORM:
        book = self.book_repository.get_by_id(book_id=book_id)
        if book is None:
            raise BookNotFound(book_id)
        return book

    def create_book(self,
                    data: BookCreateSchema) -> BookORM:
        book = BookORM(**data.model_dump())
        self.book_repository.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update_book(self,
                    book_id: int,
                    data: BookUpdateSchema) -> BookORM:
        book = self.get_book(book_id)
        for f,v in data.model_dump().items():
            setattr(book, f, v)
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete_book(self,
                    book_id: int) -> None:
        book = self.get_book(book_id)
        self.book_repository.delete(book)
        self.db.commit()
