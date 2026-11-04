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
    ) -> list:
    return book_service.list_books(status=status_, search=search)

@router.get("/books/{book_id}", response_model=BookResponseModel)
def get_book_by_id(book_id: int = Path(...,gt=0, description="Идентификатор должен быть больше 0"),
                   book_service: BookService = Depends(get_book_service)):
    return book_service.get_book(book_id=book_id)

@router.post("/books", response_model=BookResponseModel, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreateSchema, book_service: BookService = Depends(get_book_service)):
    return book_service.create_book(payload)

@router.put("/books/{book_id}", response_model=BookResponseModel)
def update_book(payload: BookUpdateSchema,
                book_id: int = Path(..., gt=0),
                book_service: BookService = Depends(get_book_service)
                ):
    return book_service.update_book(book_id, payload)

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(..., gt=0),
                book_service: BookService = Depends(get_book_service)) -> None:
    book_service.delete_book(book_id)