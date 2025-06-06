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
from sqlalchemy.orm import Session
from database.mysql import SessionLocal
from schemas.book.book_schema import BookCreate, BookUpdate, BookResponse
from services.book.book_service import BookService
from repositories.sqlalchemy.book_repo_sqlalchemy import BookRepoSqlAlchemy


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
    repo = BookRepoSqlAlchemy(db)
    book_service = BookService(repo)
    return book_service.get_books()


# GET BOOK WITH PANIGATION
@router.get("/pagination")
def get_books_with_pagination(
    page: int = 1,
    limit: int = 3,
    db: Session = Depends(get_db),
):
    repo = BookRepoSqlAlchemy(db)
    book_service = BookService(repo)
    return book_service.get_books_with_pagination(page, limit)


# GET BOOK WITH ID
@router.get("/book/{book_id}")
def get_book_with_ID(book_id: str, db: Session = Depends(get_db)):
    repo = BookRepoSqlAlchemy(db)
    book_service = BookService(repo)
    return book_service.get_book_with_ID(book_id)


# GET BOOK WITH USER_ID
@router.get("/user/{user_id}")
def get_books_by_user_id(user_id: str, db: Session = Depends(get_db)):
    repo = BookRepoSqlAlchemy(db)
    book_service = BookService(repo)
    return book_service.get_books_by_user_id(user_id)


# Create Product
@router.post("/")
async def create_book(
    book: BookCreate = Depends(BookCreate.as_form),
    image: UploadFile = File(None),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):

    repo = BookRepoSqlAlchemy(db)
    book_service = BookService(repo)
    return await book_service.create_book(book, image, credentials)
