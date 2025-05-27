from repositories.interfaces.book_repo_interface import BookRepoInterface


class BookService:
    def __init__(self, book_repo: BookRepoInterface):
        self.book_repo = book_repo

    def get_books(self):
        return self.book_repo.get_books()

    def get_books_with_pagination(self, page: int = 1, limit: int = 3):
        return self.book_repo.get_books_with_pagination(page, limit)

    def get_book_with_ID(self, book_id: str):
        return self.book_repo.get_book_with_ID(book_id)

    def get_books_by_user_id(self, user_id: str):
        return self.book_repo.get_books_by_user_id(user_id)

    async def create_book(self, book, image, credentials):
        return await self.book_repo.create_book(book, image, credentials)

    def update_book(self, book_id: str, book_update):
        return self.book_repo.update_book(book_id, book_update)

    def delete_book(self, book_id: str):
        return self.book_repo.delete_book(book_id)
