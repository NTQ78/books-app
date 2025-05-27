from repositories.interfaces.user_repo_interface import UserRepoInterface
from fastapi import UploadFile, File
from schemas.user.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin,
    UserUpdate,
)


class UserService:
    def __init__(self, user_repo: UserRepoInterface):
        self.user_repo = user_repo

    def login(self, user: UserLogin):
        return self.user_repo.login(user)

    def create_user(self, user: UserCreate):
        return self.user_repo.create_user(user)

    def get_all_users(self, credentials):
        return self.user_repo.get_all_users(credentials)

    def get_profile(self, credentials):
        return self.user_repo.get_profile(credentials)

    def get_user_by_id(self, user_id: str):
        return self.user_repo.get_user_by_id(user_id)

    def update_user_image(self, user_id: str, file: UploadFile = File(...)):
        return self.user_repo.update_user_image(user_id, file)

    def update_user(self, body: UserUpdate, credentials):
        return self.user_repo.update_user(body, credentials)

    def delete_user(self, user_id: str):
        return self.user_repo.delete_user(user_id)
