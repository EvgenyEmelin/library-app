from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db
from service.book import BookService


def get_book_service(db: Session = Depends(get_db)):
    return BookService(db)
