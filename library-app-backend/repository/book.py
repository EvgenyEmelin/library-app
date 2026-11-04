from core.utils import _escape_like
from models.book import BookORM
from sqlalchemy import or_, select
from sqlalchemy.orm import Session


class BookRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_books(
        self,
        status: str | None = None,
        search: str | None = None) -> list[BookORM]:
            stmt = select(BookORM).order_by(BookORM.created_at.desc())
            if status is not None:
                stmt = stmt.where(BookORM.status == status)
            if search is not None:
                pattern = f"%{_escape_like(search)}%"
                stmt = stmt.where(
                    or_(
                        BookORM.title.ilike(pattern, escape="\\"),
                        BookORM.author.ilike(pattern, escape="\\"),
                    )
                )
            return list(self.db.scalars(stmt).all())

    def get_by_id(self, book_id: int) -> BookORM | None:
        return self.db.get(BookORM, book_id)

    def add(self, book: BookORM) -> None:
        self.db.add(book)

    def delete(self, book: BookORM) -> None:
        self.db.delete(book)
