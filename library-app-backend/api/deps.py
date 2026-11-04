from db.session import get_db
from fastapi import Depends
from service.book import BookService
from sqlalchemy.orm import Session


def get_book_service(db: Session = Depends(get_db)):
    return BookService(db)