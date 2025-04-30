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
from models.user.model import User
from models.profile.model import Profile
from schemas.user.schemas import UserCreate, UserResponse, UserLogin, UserUpdate
from middleware.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    check_Admin,
)
from services.cloudinary import upload_image, delete_image
from services.response import api_response


from celery_temp.tasks import update_profile_image

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
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()

        if not db_user:
            return api_response(status_code=404, error="User not found")
        if not verify_password(user.password, db_user.password):
            return api_response(status_code=401, error="Invalid password")

        token_access = create_access_token(
            data={
                "sub": db_user.email,
                "id": db_user.id,
                "isAdmin": db_user.profile.isAdmin if db_user.profile else False,
            }
        )

        return api_response(data={"access_token": token_access, "token_type": "bearer"})
    except Exception as e:
        return api_response(status_code=500, error=str(e))


# SIGN UP
@router.post("/create")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )

    try:
        existing_email = db.query(User).filter(User.email == user.email).first()
        if existing_email:
            return api_response(
                status_code=400,
                error="Email already exists",
                message="Email already exists, please use another email",
            )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        new_profile = Profile(profile_id=new_user.id)
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        user_dict = new_user.to_dict()
        return api_response(data=user_dict)
    except Exception as e:
        return api_response(status_code=500, error=str(e))


# GET ALL USERS
@router.get("/")
async def get_users(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    try:
        is_admin = check_Admin(credentials.credentials)
        if is_admin is None:
            return api_response(
                status_code=401, error="Invalid token", message="Only ADMIN can access"
            )
        users = (
            db.query(User).join(User.profile).order_by(Profile.create_At.desc()).all()
        )

        user_list = []
        for user in users:
            user_dict = user.to_dict()
            user_list.append(user_dict)
        return api_response(data=user_list)
    except Exception as e:
        return api_response(status_code=500, error=str(e))
    finally:
        db.close()


# PROFILE
@router.get("/profile")
async def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return api_response(
            status_code=401, error="Invalid token", message="Invalid token"
        )
    email = payload["sub"]
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise api_response(status_code=404, message="User not found")

    user_dict = user.to_dict()
    return api_response(data=user_dict)


# GET USER BY ID
@router.get("/{user_id}")
async def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return api_response(status_code=404, error="User not found")
        user_dict = user.to_dict()
        return api_response(data=user_dict)
    except Exception as e:
        return api_response(status_code=500, error=str(e))
    finally:
        db.close()


# UPDATE USER IMAGE
@router.put("/upload_image/{user_id}")
async def update_user_image(
    user_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        if file:
            file_bytes = await file.read()
            update_profile_image.delay(user_id, file_bytes)
        else:
            return api_response(message=f"Please update your image!!.")

        return api_response(message=f"Profile updated with new image.")
    except Exception as e:
        return api_response(status_code=500, error=str(e))


# UPDATE USER
@router.put("/profile")
async def update_user(
    body: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    try:

        token = credentials.credentials
        payload = decode_access_token(token)
        if not payload or "sub" not in payload:
            return api_response(
                status_code=401, error="Invalid token", message="Invalid token"
            )
        email = payload["sub"]
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return api_response(status_code=404, error="User not found")
        if body.username is not None:
            user.username = body.username
        if body.email is not None:
            # Check if new email already exists for another user
            existing_email = (
                db.query(User)
                .filter(User.email == body.email, User.id != user.id)
                .first()
            )
            if existing_email:
                return api_response(
                    status_code=400,
                    error="Email already exists",
                    message="Email already exists, please use another email",
                )
            user.email = body.email
        if body.isAdmin is not None:
            user.profile.isAdmin = body.isAdmin
        if body.isAuthor is not None:
            user.profile.isAuthor = body.isAuthor
        db.commit()
        db.refresh(user)
        # Remove field books
        user_dict = user.to_dict()
        user_dict.pop("books", None)

        return api_response(message="Update Success!", data=user_dict)
    except Exception as e:
        return api_response(status_code=500, error=str(e))


# DELETE USER
@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return api_response(status_code=404, error="User not found")
        db.delete(user)
        db.commit()
        return api_response(message="User deleted successfully")
    except Exception as e:
        return api_response(error=str(e))
