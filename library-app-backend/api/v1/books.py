from typing import Literal

from api.deps import get_book_service
from fastapi import APIRouter, Depends, Path, Query, status
from schemas.book import BookCreateSchema, BookResponseModel, BookUpdateSchema
from service.book import BookService

router = APIRouter(prefix="/api", tags=["books"])

@router.get('/books', response_model=list[BookResponseModel])
def get_books(
    status_: Literal["want", "reading", "read"] | None = Query(default=None, alias="status"),
    search: str | None = Query(default=None, max_length=200),
    book_service: BookService = Depends(get_book_service)
    ) -> list[BookResponseModel]:
    return book_service.list_books()