from models.book.book_model import Book
from services.response import api_response
from celery_temp.tasks import upload_image_and_update_book
from sqlalchemy.orm import Session
from middleware.auth import decode_access_token


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def get_books(self):
        try:
            db_book = self.db.query(Book).order_by(Book.create_At.desc()).all()
            if not db_book:
                return api_response(message="Books Not Found!")
            list_books = [book.to_dict() for book in db_book]
            return api_response(data=list_books)
        except Exception as e:
            return api_response(error=str(e))

    def get_books_with_pagination(self, page: int = 1, limit: int = 3):
        try:
            db_book = (
                self.db.query(Book)
                .order_by(Book.create_At.desc())
                .offset((page - 1) * limit)
                .limit(limit)
                .all()
            )
            if not db_book:
                return api_response(message="Books Not Found!")
            list_books = [book.to_dict() for book in db_book]
            return api_response(data=list_books)
        except Exception as e:
            return api_response(error=str(e))

    def get_book_with_ID(self, book_id: str):
        try:
            db_book = self.db.query(Book).filter(Book.id == book_id).first()
            if not db_book:
                return api_response(status_code=404, message="Book not Found")
            book_dict = db_book.to_dict()
            return api_response(data=book_dict, message="Success")
        except Exception as e:
            return api_response(error=str(e))

    def get_books_by_user_id(self, user_id: str):
        try:
            db_books = self.db.query(Book).filter(Book.user_id == user_id).all()
            if not db_books:
                return api_response(
                    status_code=404, message="Books not found for this user"
                )
            list_books = [book.to_dict() for book in db_books]
            return api_response(data=list_books, message="Success")
        except Exception as e:
            return api_response(error=str(e))

    async def create_book(self, book, image, credentials):
        try:
            token = credentials.credentials
            if not token:
                return api_response(
                    status_code=401,
                    error="Invalid token",
                    message="Please login to upload Books",
                )
            payload = decode_access_token(token)
            user_id = payload.get("id") if payload else None
            if not user_id:
                return api_response(
                    status_code=401,
                    error="Invalid token",
                    message="Please login to upload Books",
                )

            cover_image_url = None

            new_book = Book(
                title=book.title,
                author=book.author,
                caption=book.caption,
                summary=book.summary,
                cover_image=cover_image_url,
                user_id=user_id,
            )
            self.db.add(new_book)
            self.db.commit()
            self.db.refresh(new_book)
            if image:
                file_bytes = await image.read()
                upload_image_and_update_book.delay(new_book.id, file_bytes)
            return api_response(data=new_book.to_dict())
        except Exception as e:
            return api_response(error=str(e))
