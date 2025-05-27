import pytest
import io
from unittest.mock import Mock, MagicMock
from fastapi import UploadFile, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from services.user.user_service import UserService
from repositories.interfaces.user_repo_interface import UserRepoInterface
from schemas.user.user_schema import UserCreate, UserLogin, UserUpdate


class TestUserService:
    """Unit tests for UserService class"""

    @pytest.fixture
    def mock_user_repo(self):
        """Mock user repository"""
        return Mock(spec=UserRepoInterface)

    @pytest.fixture
    def user_service(self, mock_user_repo):
        """UserService instance with mocked repository"""
        return UserService(mock_user_repo)

    @pytest.fixture
    def sample_user_create(self):
        """Sample user creation data"""
        return UserCreate(
            username="testuser", email="test@example.com", password="password123"
        )

    @pytest.fixture
    def sample_user_login(self):
        """Sample user login data"""
        return UserLogin(email="test@example.com", password="password123")

    @pytest.fixture
    def sample_user_update(self):
        """Sample user update data"""
        return UserUpdate(username="updated_user", email="updated@example.com")

    @pytest.fixture
    def mock_credentials(self):
        """Mock authorization credentials"""
        return HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_token")

    @pytest.fixture
    def mock_upload_file(self):
        """Mock upload file"""
        file_content = b"fake image content"
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.jpg"
        mock_file.content_type = "image/jpeg"
        mock_file.read = Mock(return_value=file_content)
        mock_file.file = io.BytesIO(file_content)
        return mock_file

    def test_login_success(self, user_service, mock_user_repo, sample_user_login):
        """Test successful user login"""
        # Arrange
        expected_result = {
            "status_code": 200,
            "data": {"access_token": "test_token", "token_type": "bearer"},
            "error": None,
            "message": "Login successful",
        }
        mock_user_repo.login.return_value = expected_result

        # Act
        result = user_service.login(sample_user_login)

        # Assert
        mock_user_repo.login.assert_called_once_with(sample_user_login)
        assert result == expected_result
        assert result["status_code"] == 200
        assert "access_token" in result["data"]

    def test_login_invalid_credentials(
        self, user_service, mock_user_repo, sample_user_login
    ):
        """Test login with invalid credentials"""
        # Arrange
        expected_result = {
            "status_code": 401,
            "data": None,
            "error": "Invalid password",
            "message": None,
        }
        mock_user_repo.login.return_value = expected_result

        # Act
        result = user_service.login(sample_user_login)

        # Assert
        mock_user_repo.login.assert_called_once_with(sample_user_login)
        assert result == expected_result
        assert result["status_code"] == 401
        assert result["error"] == "Invalid password"

    def test_create_user_success(
        self, user_service, mock_user_repo, sample_user_create
    ):
        """Test successful user creation"""
        # Arrange
        expected_result = {
            "status_code": 200,
            "data": {
                "id": "new-user-id",
                "username": sample_user_create.username,
                "email": sample_user_create.email,
            },
            "error": None,
            "message": "User created successfully",
        }
        mock_user_repo.create_user.return_value = expected_result

        # Act
        result = user_service.create_user(sample_user_create)

        # Assert
        mock_user_repo.create_user.assert_called_once_with(sample_user_create)
        assert result == expected_result
        assert result["status_code"] == 200
        assert result["data"]["username"] == sample_user_create.username

    def test_create_user_already_exists(
        self, user_service, mock_user_repo, sample_user_create
    ):
        """Test creating user that already exists"""
        # Arrange
        expected_result = {
            "status_code": 400,
            "data": None,
            "error": "User already exists",
            "message": None,
        }
        mock_user_repo.create_user.return_value = expected_result

        # Act
        result = user_service.create_user(sample_user_create)

        # Assert
        mock_user_repo.create_user.assert_called_once_with(sample_user_create)
        assert result == expected_result
        assert result["status_code"] == 400
        assert result["error"] == "User already exists"

    def test_get_all_users_admin_success(
        self, user_service, mock_user_repo, mock_credentials
    ):
        """Test admin successfully getting all users"""
        # Arrange
        expected_result = {
            "status_code": 200,
            "data": [
                {"id": "1", "username": "user1", "email": "user1@example.com"},
                {"id": "2", "username": "user2", "email": "user2@example.com"},
            ],
            "error": None,
            "message": "Success",
        }
        mock_user_repo.get_all_users.return_value = expected_result

        # Act
        result = user_service.get_all_users(mock_credentials)

        # Assert
        mock_user_repo.get_all_users.assert_called_once_with(mock_credentials)
        assert result == expected_result
        assert result["status_code"] == 200
        assert len(result["data"]) == 2

    def test_get_all_users_non_admin(
        self, user_service, mock_user_repo, mock_credentials
    ):
        """Test non-admin user cannot get all users"""
        # Arrange
        expected_result = {
            "status_code": 401,
            "data": None,
            "error": "Invalid token",
            "message": "Only ADMIN can access",
        }
        mock_user_repo.get_all_users.return_value = expected_result

        # Act
        result = user_service.get_all_users(mock_credentials)

        # Assert
        mock_user_repo.get_all_users.assert_called_once_with(mock_credentials)
        assert result == expected_result
        assert result["status_code"] == 401
        assert "Only ADMIN can access" in result["message"]

    def test_get_profile_success(self, user_service, mock_user_repo, mock_credentials):
        """Test successfully getting user profile"""
        # Arrange
        expected_result = {
            "status_code": 200,
            "data": {
                "id": "user-123",
                "username": "testuser",
                "email": "test@example.com",
            },
            "error": None,
            "message": "Success",
        }
        mock_user_repo.get_profile.return_value = expected_result

        # Act
        result = user_service.get_profile(mock_credentials)

        # Assert
        mock_user_repo.get_profile.assert_called_once_with(mock_credentials)
        assert result == expected_result
        assert result["status_code"] == 200
        assert result["data"]["username"] == "testuser"

    def test_get_profile_invalid_token(
        self, user_service, mock_user_repo, mock_credentials
    ):
        """Test getting profile with invalid token"""
        # Arrange
        expected_result = {
            "status_code": 401,
            "data": None,
            "error": "Invalid token",
            "message": None,
        }
        mock_user_repo.get_profile.return_value = expected_result

        # Act
        result = user_service.get_profile(mock_credentials)

        # Assert
        mock_user_repo.get_profile.assert_called_once_with(mock_credentials)
        assert result == expected_result
        assert result["status_code"] == 401
        assert result["error"] == "Invalid token"

    def test_get_user_by_id_success(self, user_service, mock_user_repo):
        """Test successfully getting user by ID"""
        # Arrange
        user_id = "user-123"
        expected_result = {
            "status_code": 200,
            "data": {
                "id": user_id,
                "username": "testuser",
                "email": "test@example.com",
            },
            "error": None,
            "message": "Success",
        }
        mock_user_repo.get_user_by_id.return_value = expected_result

        # Act
        result = user_service.get_user_by_id(user_id)

        # Assert
        mock_user_repo.get_user_by_id.assert_called_once_with(user_id)
        assert result == expected_result
        assert result["status_code"] == 200
        assert result["data"]["id"] == user_id

    def test_get_user_by_id_not_found(self, user_service, mock_user_repo):
        """Test getting user by ID when user doesn't exist"""
        # Arrange
        user_id = "nonexistent"
        expected_result = {
            "status_code": 404,
            "data": None,
            "error": "User not found",
            "message": None,
        }
        mock_user_repo.get_user_by_id.return_value = expected_result

        # Act
        result = user_service.get_user_by_id(user_id)

        # Assert
        mock_user_repo.get_user_by_id.assert_called_once_with(user_id)
        assert result == expected_result
        assert result["status_code"] == 404
        assert result["error"] == "User not found"

    def test_update_user_image_success(
        self, user_service, mock_user_repo, mock_upload_file
    ):
        """Test successfully updating user image"""
        # Arrange
        user_id = "user-123"
        expected_result = {
            "status_code": 200,
            "data": None,
            "error": None,
            "message": "Image updated successfully",
        }
        mock_user_repo.update_user_image.return_value = expected_result

        # Act
        result = user_service.update_user_image(user_id, mock_upload_file)

        # Assert
        mock_user_repo.update_user_image.assert_called_once_with(
            user_id, mock_upload_file
        )
        assert result == expected_result
        assert result["status_code"] == 200
        assert "Image updated successfully" in result["message"]

    def test_update_user_image_invalid_file_type(self, user_service, mock_user_repo):
        """Test updating user image with invalid file type"""
        # Arrange
        user_id = "user-123"
        invalid_file = Mock(spec=UploadFile)
        invalid_file.filename = "test.txt"
        invalid_file.content_type = "text/plain"

        expected_result = {
            "status_code": 400,
            "data": None,
            "error": "Invalid file type",
            "message": "Allowed file types are: jpeg, png, jpg",
        }
        mock_user_repo.update_user_image.return_value = expected_result

        # Act
        result = user_service.update_user_image(user_id, invalid_file)

        # Assert
        mock_user_repo.update_user_image.assert_called_once_with(user_id, invalid_file)
        assert result == expected_result
        assert result["status_code"] == 400
        assert result["error"] == "Invalid file type"

    def test_update_user_image_user_not_found(
        self, user_service, mock_user_repo, mock_upload_file
    ):
        """Test updating image for non-existent user"""
        # Arrange
        user_id = "nonexistent"
        expected_result = {
            "status_code": 404,
            "data": None,
            "error": "User not found",
            "message": None,
        }
        mock_user_repo.update_user_image.return_value = expected_result

        # Act
        result = user_service.update_user_image(user_id, mock_upload_file)

        # Assert
        mock_user_repo.update_user_image.assert_called_once_with(
            user_id, mock_upload_file
        )
        assert result == expected_result
        assert result["status_code"] == 404
        assert result["error"] == "User not found"

    def test_update_user_success(
        self, user_service, mock_user_repo, sample_user_update, mock_credentials
    ):
        """Test successfully updating user information"""
        # Arrange
        expected_result = {
            "status_code": 200,
            "data": {
                "id": "user-123",
                "username": "updated_user",
                "email": "updated@example.com",
            },
            "error": None,
            "message": "User updated successfully",
        }
        mock_user_repo.update_user.return_value = expected_result

        # Act
        result = user_service.update_user(sample_user_update, mock_credentials)

        # Assert
        mock_user_repo.update_user.assert_called_once_with(
            sample_user_update, mock_credentials
        )
        assert result == expected_result
        assert result["status_code"] == 200
        assert result["data"]["username"] == "updated_user"

    def test_update_user_invalid_token(
        self, user_service, mock_user_repo, sample_user_update, mock_credentials
    ):
        """Test updating user with invalid token"""
        # Arrange
        expected_result = {
            "status_code": 401,
            "data": None,
            "error": "Invalid token",
            "message": None,
        }
        mock_user_repo.update_user.return_value = expected_result

        # Act
        result = user_service.update_user(sample_user_update, mock_credentials)

        # Assert
        mock_user_repo.update_user.assert_called_once_with(
            sample_user_update, mock_credentials
        )
        assert result == expected_result
        assert result["status_code"] == 401
        assert result["error"] == "Invalid token"

    def test_delete_user_success(self, user_service, mock_user_repo):
        """Test successfully deleting user"""
        # Arrange
        user_id = "user-123"
        expected_result = {
            "status_code": 200,
            "data": None,
            "error": None,
            "message": "User deleted successfully",
        }
        mock_user_repo.delete_user.return_value = expected_result

        # Act
        result = user_service.delete_user(user_id)

        # Assert
        mock_user_repo.delete_user.assert_called_once_with(user_id)
        assert result == expected_result
        assert result["status_code"] == 200
        assert result["message"] == "User deleted successfully"

    def test_delete_user_not_found(self, user_service, mock_user_repo):
        """Test deleting user that doesn't exist"""
        # Arrange
        user_id = "nonexistent"
        expected_result = {
            "status_code": 404,
            "data": None,
            "error": "User not found",
            "message": None,
        }
        mock_user_repo.delete_user.return_value = expected_result

        # Act
        result = user_service.delete_user(user_id)

        # Assert
        mock_user_repo.delete_user.assert_called_once_with(user_id)
        assert result == expected_result
        assert result["status_code"] == 404
        assert result["error"] == "User not found"

    def test_user_service_initialization(self, mock_user_repo):
        """Test UserService initialization with repository"""
        # Act
        service = UserService(mock_user_repo)

        # Assert
        assert service.user_repo == mock_user_repo
        assert isinstance(service.user_repo, UserRepoInterface)

    def test_user_service_methods_delegate_to_repo(self, user_service, mock_user_repo):
        """Test that UserService methods properly delegate to repository"""
        # Arrange
        test_data = {
            "status_code": 200,
            "data": {"test": "data"},
            "error": None,
            "message": "Success",
        }

        # Configure mocks
        mock_user_repo.login.return_value = test_data
        mock_user_repo.create_user.return_value = test_data
        mock_user_repo.get_all_users.return_value = test_data
        mock_user_repo.get_profile.return_value = test_data
        mock_user_repo.get_user_by_id.return_value = test_data
        mock_user_repo.update_user_image.return_value = test_data
        mock_user_repo.update_user.return_value = test_data
        mock_user_repo.delete_user.return_value = test_data

        # Test data
        user_login = UserLogin(email="test@example.com", password="password123")
        user_create = UserCreate(
            username="test", email="test@example.com", password="password123"
        )
        user_update = UserUpdate(username="updated")
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="token")
        upload_file = Mock(spec=UploadFile)

        # Act & Assert
        assert user_service.login(user_login) == test_data
        assert user_service.create_user(user_create) == test_data
        assert user_service.get_all_users(credentials) == test_data
        assert user_service.get_profile(credentials) == test_data
        assert user_service.get_user_by_id("user-123") == test_data
        assert user_service.update_user_image("user-123", upload_file) == test_data
        assert user_service.update_user(user_update, credentials) == test_data
        assert user_service.delete_user("user-123") == test_data

        # Verify all methods were called
        mock_user_repo.login.assert_called_once()
        mock_user_repo.create_user.assert_called_once()
        mock_user_repo.get_all_users.assert_called_once()
        mock_user_repo.get_profile.assert_called_once()
        mock_user_repo.get_user_by_id.assert_called_once()
        mock_user_repo.update_user_image.assert_called_once()
        mock_user_repo.update_user.assert_called_once()
        mock_user_repo.delete_user.assert_called_once()
