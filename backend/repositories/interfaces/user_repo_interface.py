from abc import ABC, abstractmethod
from schemas.user.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin,
    UserUpdate,
)


class UserRepoInterface(ABC):
    @abstractmethod
    def login(self, user: UserLogin):
        pass

    @abstractmethod
    def create_user(self, user: UserCreate):
        pass

    @abstractmethod
    def get_all_users(self, credentials):
        pass

    @abstractmethod
    def get_profile(self, credentials):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str):
        pass

    @abstractmethod
    def update_user_image(self, user_id: str, file):
        pass

    @abstractmethod
    def update_user(self, body: UserUpdate, credentials):
        pass

    @abstractmethod
    def delete_user(self, user_id: str):
        pass
