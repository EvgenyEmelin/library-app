from api.v1.books import router as book_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(router=book_router)
