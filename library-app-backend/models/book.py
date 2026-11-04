from datetime import datetime

from sqlalchemy import CheckConstraint, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class BookORM(Base):
    __tablename__ = "books"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="want")
    rating: Mapped[int | None] = mapped_column(nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


    __table_args__ = (
        CheckConstraint("year > 0 AND year < 2100", name="check_book_year_range"),
        CheckConstraint("status IN ('want', 'reading', 'read')", name="check_book_status_enum"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_book_rating_range"),
    )
