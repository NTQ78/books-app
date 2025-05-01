from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.mysql import SessionLocal
from schemas.user.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin,
    UserUpdate,
)
from services.user.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users API"])
bearer_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# SIGN IN
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.login(user)


# SIGN UP
@router.post("/create")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user)


# GET ALL USERS
@router.get("/")
def get_all_users(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.get_all_users(credentials)


# PROFILE
@router.get("/profile")
def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.get_profile(credentials)


# GET USER BY ID
@router.get("/{user_id}")
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_user_by_id(user_id)


# UPDATE USER IMAGE
@router.put("/upload_image/{user_id}")
async def update_user_image(
    user_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return await user_service.update_user_image(user_id, file)


# UPDATE USER
@router.put("/profile")
async def update_user(
    body: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.update_user(body, credentials)


# DELETE USER
@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.delete_user(user_id)
