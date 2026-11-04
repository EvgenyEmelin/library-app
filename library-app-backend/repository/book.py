from models.book import BookORM
from sqlalchemy import select
from sqlalchemy.orm import Session


class BookRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, book_id: int) -> BookORM | None:
        return self.db.get(BookORM, book_id)

    def get_all_books(self) -> list[BookORM]:
        stmt = select(BookORM).order_by(BookORM.created_at.desc())
        return list(self.db.scalars(stmt).all())