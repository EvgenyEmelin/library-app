from repository.book import BookRepository
from schemas.book import BookResponseModel
from sqlalchemy.orm import Session


class BookService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.book_repository =  BookRepository(db)

    def list_books(self) -> list[BookResponseModel]:
        book_orm = self.book_repository.get_all_books()
        return [BookResponseModel.model_validate(book) for book in book_orm]
