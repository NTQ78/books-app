from fastapi import UploadFile, File
from models.user.user_model import User
from models.profile.profile_model import Profile
from utils.response import api_response
from celery_temp.tasks import update_profile_image
from middleware.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    check_admin,
)


class UserService:
    def __init__(self, db):
        self.db = db

    def login(self, user):
        try:
            db_user = self.db.query(User).filter(User.email == user.email).first()

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

            return api_response(
                data={"access_token": token_access, "token_type": "bearer"}
            )
        except Exception as e:
            return api_response(status_code=500, error=str(e))

    def create_user(self, user):
        try:
            if self.db.query(User).filter(User.email == user.email).first():
                return api_response(status_code=400, error="User already exists")

            hashed_password = get_password_hash(user.password)
            new_user = User(
                username=user.username,
                email=user.email,
                password=hashed_password,
            )
            self.db.add(new_user)
            self.db.flush()  # Ensure new_user.id is available

            new_profile = Profile(profile_id=new_user.id)
            self.db.add(new_profile)
            self.db.commit()
            self.db.refresh(new_user)

            return api_response(
                data=new_user.to_dict(), message="User created successfully"
            )
        except Exception as e:
            self.db.rollback()
            return api_response(status_code=500, error=str(e))

    def get_all_users(self, credentials):
        try:
            is_admin = check_admin(credentials.credentials)
            if not is_admin:
                return api_response(
                    status_code=401,
                    error="Invalid token",
                    message="Only ADMIN can access",
                )
            users = (
                self.db.query(User)
                .join(User.profile)
                .order_by(Profile.create_At.desc())
                .all()
            )

            user_list = []
            for user in users:
                user_dict = user.to_dict()
                user_list.append(user_dict)
            return api_response(data=user_list)
        except Exception as e:
            return api_response(status_code=500, error=str(e))
        finally:
            self.db.close()

    def get_profile(self, credentials):
        try:
            token = credentials.credentials
            payload = decode_access_token(token)
            if not payload or "sub" not in payload:
                return api_response(
                    status_code=401, error="Invalid token", message="Invalid token"
                )
            email = payload["sub"]
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                return api_response(status_code=404, error="User not found")
            user_dict = user.to_dict()
            # user_dict.pop("books", None)
            return api_response(data=user_dict, message="Success")

        except Exception as e:
            return api_response(status_code=500, error=str(e))

    def get_user_by_id(self, user_id: str):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return api_response(status_code=404, error="User not found")
            user_dict = user.to_dict()

            return api_response(data=user_dict, message="Success")
        except Exception as e:
            return api_response(status_code=500, error=str(e))

    async def update_user_image(self, user_id: str, file: UploadFile):
        try:
            if file:
                file_bytes = await file.read()
                update_profile_image.delay(user_id, file_bytes)
            else:
                return api_response(message=f"Please update your image!!.")

            return api_response(message="Image updated successfully")
        except Exception as e:
            self.db.rollback()
            return api_response(status_code=500, error=str(e))
        finally:
            self.db.close()

    def update_user(self, body, credentials):
        try:
            token = credentials.credentials
            payload = decode_access_token(token)
            if not payload or "id" not in payload:
                return api_response(
                    status_code=401, error="Invalid token", message="Invalid token"
                )
            user_id = payload["id"]
            user = self.db.query(User).filter(User.id == user_id).first()

            if not user:
                return api_response(status_code=404, error="User not found")
            if body.email is not None:
                # Check if new email already exists for another user
                existing_email = (
                    self.db.query(User)
                    .filter(User.email == body.email, User.id != user.id)
                    .first()
                )
                if existing_email:
                    return api_response(
                        status_code=400,
                        error="Email already exists",
                        message="Email already exists, please use another email",
                    )

            for key, value in body.dict(exclude_unset=True).items():
                if key == "profile":
                    continue
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)

            if body.profile is not None:
                for key, value in body.profile.dict(exclude_unset=True).items():
                    if hasattr(user.profile, key) and value is not None:
                        setattr(user.profile, key, value)

            self.db.commit()
            self.db.refresh(user)

            return api_response(
                message="User updated successfully", data=user.to_dict()
            )
        except Exception as e:
            self.db.rollback()
            return api_response(status_code=500, error=str(e))
        finally:
            self.db.close()

    def delete_user(self, user_id: str):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return api_response(status_code=404, error="User not found")
            self.db.delete(user)
            self.db.commit()
            return api_response(message="User deleted successfully")
        except Exception as e:
            self.db.rollback()
            return api_response(status_code=500, error=str(e))
        finally:
            self.db.close()
