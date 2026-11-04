from api.v1.books import router as book_router
from core.exceptions import BookNotFound
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(BookNotFound)
async def book_not_found_exception_handler(rq: Request, exc: BookNotFound):
    return JSONResponse(status_code=404,content={"error": exc.message})

app.include_router(router=book_router)


