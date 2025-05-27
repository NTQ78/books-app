from abc import ABC, abstractmethod
from schemas.book.book_schema import BookCreate, BookUpdate, BookResponse


class BookRepoInterface:
    @abstractmethod
    def get_books(self):
        pass

    @abstractmethod
    def get_books_with_pagination(self, page: int, limit: int):
        pass

    @abstractmethod
    def get_book_with_ID(self, book_id: str):
        pass

    @abstractmethod
    def get_books_by_user_id(self, user_id: str):
        pass

    @abstractmethod
    async def create_book(self, book: BookCreate, image: str, credentials):
        pass

    @abstractmethod
    def update_book(self, book_id: str, book_update: BookUpdate):
        pass

    @abstractmethod
    def delete_book(self, book_id: str):
        pass
