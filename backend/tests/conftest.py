import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.mysql import Base
from main import app
from repositories.sqlalchemy.user_repo_sqlalchemy import UserRepoSqlAlchemy
from repositories.sqlalchemy.book_repo_sqlalchemy import BookRepoSqlAlchemy
from services.user.user_service import UserService
from services.book.book_service import BookService


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Database dependency for testing"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """FastAPI test client"""
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Database session for testing"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_user_repo():
    """Mock user repository"""
    return Mock(spec=UserRepoSqlAlchemy)


@pytest.fixture
def mock_book_repo():
    """Mock book repository"""
    return Mock(spec=BookRepoSqlAlchemy)


@pytest.fixture
def user_service(mock_user_repo):
    """User service with mock repository"""
    return UserService(mock_user_repo)


@pytest.fixture
def book_service(mock_book_repo):
    """Book service with mock repository"""
    return BookService(mock_book_repo)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
    }


@pytest.fixture
def sample_book_data():
    """Sample book data for testing"""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "caption": "Test Caption",
        "summary": "Test Summary",
    }


@pytest.fixture
def auth_token():
    """Mock authentication token"""
    return "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiaWQiOiJ0ZXN0LXVzZXItaWQiLCJpc0FkbWluIjpmYWxzZSwiZXhwIjoxNjk5OTk5OTk5fQ.test_signature"


@pytest.fixture
def mock_cloudinary_upload():
    """Mock Cloudinary upload function"""
    from unittest.mock import patch

    with patch("utils.cloudinary.upload_image") as mock:
        mock.return_value = (
            "https://res.cloudinary.com/test/image/upload/test_image.jpg"
        )
        yield mock


@pytest.fixture
def mock_celery_task():
    """Mock Celery tasks"""
    from unittest.mock import patch

    with patch("celery_temp.tasks.update_profile_image.delay") as mock_profile, patch(
        "celery_temp.tasks.upload_image_and_update_book.delay"
    ) as mock_book:
        yield {"profile": mock_profile, "book": mock_book}
