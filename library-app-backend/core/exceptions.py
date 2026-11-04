class BookNotFound(Exception):
    def __init__(self, book_id: int) -> None:
        self.book_id = book_id
        self.message = f"Book with id={book_id} not found"
        super().__init__(self.message)
        self.status_code = 404