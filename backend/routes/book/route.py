from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    status,
    File,
    UploadFile,
    Form,
)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.response import api_response
from services.cloudinary import upload_image

from sqlalchemy.orm import Session
from database.mysql import SessionLocal
from models.book.model import Book

from schemas.book.schemas import BookCreate, BookUpdate, BookResponse
from middleware.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    check_Admin,
)

from celery_temp.tasks import upload_image_and_update_book

router = APIRouter(prefix="/products", tags=["Books API"])
bearer_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET ALL BOOK
@router.get("/")
def get_books(db: Session = Depends(get_db)):
    try:
        db_book = db.query(Book).order_by(Book.create_At.desc()).all()
        if not db_book:
            return api_response(message="Books Not Found!")
        list_books = []
        for book in db_book:
            book_dict = book.to_dict()
            list_books.append(book_dict)

        return api_response(data=list_books)

    except Exception as e:
        return api_response(error=e)


# GET BOOK WITH PANIGATION
@router.get("/pagination")
def get_books_with_pagination(
    page: int = 1,
    limit: int = 3,
    db: Session = Depends(get_db),
):
    try:

        db_book = (
            db.query(Book)
            .order_by(Book.create_At.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        if not db_book:
            return api_response(message="Books Not Found!")
        list_books = []
        for book in db_book:
            book_dict = book.to_dict()
            list_books.append(book_dict)

        return api_response(data=list_books)

    except Exception as e:
        return api_response(error=e)


# GET BOOK WITH ID
@router.get("/book/{book_id}")
def get_book_with_ID(book_id: str, db: Session = Depends(get_db)):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return api_response(status_code=404, message="Book not Found")
        book_dict = db_book.to_dict()
        return api_response(data=book_dict, message="Success")
    except Exception as e:
        return api_response(error=e)


# GET BOOK WITH USER_ID
@router.get("/user/{user_id}")
def get_books_by_user_id(user_id: str, db: Session = Depends(get_db)):
    try:

        db_books = db.query(Book).filter(Book.user_id == user_id).all()
        if not db_books:
            return api_response(
                status_code=404, message="Books not found for this user"
            )
        list_books = [book.to_dict() for book in db_books]
        return api_response(data=list_books, message="Success")
    except Exception as e:
        return api_response(error=str(e))


# Create Product
@router.post("/")
async def create_book(
    book: BookCreate = Depends(BookCreate.as_form),
    image: UploadFile = File(None),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
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
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        if image:
            file_bytes = await image.read()

            upload_image_and_update_book.delay(new_book.id, file_bytes)
        return api_response(data=new_book.to_dict())

    except Exception as e:
        return api_response(error=str(e))
