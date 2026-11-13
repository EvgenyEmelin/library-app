from api.v1.books import router as book_router
from core.exceptions import BookNotFound
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(BookNotFound)
async def book_not_found_exception_handler(rq: Request, exc: BookNotFound):
    return JSONResponse(status_code=404,content={"error": exc.message})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(rq: Request, exc: RequestValidationError):
    # Сохраняем ожидаемый формат для POST /api/books
    if rq.method == "POST" and rq.url.path == "/api/books":
        return JSONResponse(
            status_code=400,
            content={"error": "Cannot create book with invalid payload"},
        )

    # Возвращаем 400 для GET /api/books/{id} и остальных ошибок валидации
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request parameters"},
    )

app.include_router(router=book_router)


