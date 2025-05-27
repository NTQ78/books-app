import pytest
from unittest.mock import Mock, patch
from fastapi import UploadFile

from services.book.book_service import BookService


class TestBookService:
    """Test cases cho Book Service theo nghiệp vụ"""

    def test_get_books_success(self, book_service, mock_book_repo):
        """Test lấy danh sách sách thành công"""
        # Arrange
        expected_books = [
            {
                "id": "book-1",
                "title": "Python Programming",
                "author": "John Doe",
                "caption": "Learn Python",
                "summary": "A comprehensive guide to Python",
            },
            {
                "id": "book-2",
                "title": "FastAPI Guide",
                "author": "Jane Smith",
                "caption": "Web APIs with FastAPI",
                "summary": "Building modern APIs",
            },
        ]
        mock_book_repo.get_books.return_value = expected_books

        # Act
        result = book_service.get_books()

        # Assert
        mock_book_repo.get_books.assert_called_once()
        assert result == expected_books

    def test_get_books_empty_list(self, book_service, mock_book_repo):
        """Test lấy danh sách sách khi không có sách nào"""
        # Arrange
        mock_book_repo.get_books.return_value = []

        # Act
        result = book_service.get_books()

        # Assert
        assert result == []

    def test_get_books_with_pagination_default_params(
        self, book_service, mock_book_repo
    ):
        """Test phân trang với tham số mặc định"""
        # Arrange
        expected_result = {
            "books": [{"id": "book-1", "title": "Test Book"}],
            "total": 10,
            "page": 1,
            "limit": 3,
            "total_pages": 4,
        }
        mock_book_repo.get_books_with_pagination.return_value = expected_result

        # Act
        result = book_service.get_books_with_pagination()

        # Assert
        mock_book_repo.get_books_with_pagination.assert_called_once_with(1, 3)
        assert result == expected_result

    def test_get_books_with_pagination_custom_params(
        self, book_service, mock_book_repo
    ):
        """Test phân trang với tham số tùy chỉnh"""
        # Arrange
        page, limit = 2, 5
        expected_result = {
            "books": [{"id": "book-6", "title": "Book 6"}],
            "total": 20,
            "page": 2,
            "limit": 5,
            "total_pages": 4,
        }
        mock_book_repo.get_books_with_pagination.return_value = expected_result

        # Act
        result = book_service.get_books_with_pagination(page, limit)

        # Assert
        mock_book_repo.get_books_with_pagination.assert_called_once_with(2, 5)
        assert result == expected_result

    def test_get_book_with_valid_id(self, book_service, mock_book_repo):
        """Test lấy sách với ID hợp lệ"""
        # Arrange
        book_id = "book-123"
        expected_book = {
            "id": book_id,
            "title": "Test Book",
            "author": "Test Author",
            "caption": "Test Caption",
            "summary": "Test Summary",
        }
        mock_book_repo.get_book_with_ID.return_value = expected_book

        # Act
        result = book_service.get_book_with_ID(book_id)

        # Assert
        mock_book_repo.get_book_with_ID.assert_called_once_with(book_id)
        assert result == expected_book

    def test_get_book_with_invalid_id(self, book_service, mock_book_repo):
        """Test lấy sách với ID không tồn tại"""
        # Arrange
        book_id = "nonexistent"
        mock_book_repo.get_book_with_ID.return_value = None

        # Act
        result = book_service.get_book_with_ID(book_id)

        # Assert
        mock_book_repo.get_book_with_ID.assert_called_once_with(book_id)
        assert result is None

    def test_get_books_by_user_id_success(self, book_service, mock_book_repo):
        """Test lấy sách theo user ID thành công"""
        # Arrange
        user_id = "user-123"
        expected_books = [
            {"id": "book-1", "title": "User's Book 1", "user_id": user_id},
            {"id": "book-2", "title": "User's Book 2", "user_id": user_id},
        ]
        mock_book_repo.get_books_by_user_id.return_value = expected_books

        # Act
        result = book_service.get_books_by_user_id(user_id)

        # Assert
        mock_book_repo.get_books_by_user_id.assert_called_once_with(user_id)
        assert result == expected_books

    def test_get_books_by_user_id_no_books(self, book_service, mock_book_repo):
        """Test lấy sách theo user ID khi user không có sách"""
        # Arrange
        user_id = "user-without-books"
        mock_book_repo.get_books_by_user_id.return_value = []

        # Act
        result = book_service.get_books_by_user_id(user_id)

        # Assert
        mock_book_repo.get_books_by_user_id.assert_called_once_with(user_id)
        assert result == []

    @pytest.mark.asyncio
    async def test_create_book_success_with_image(
        self, book_service, mock_book_repo, sample_book_data, mock_celery_task
    ):
        """Test tạo sách thành công với ảnh"""
        # Arrange
        book_data = Mock()
        book_data.title = sample_book_data["title"]
        book_data.author = sample_book_data["author"]
        book_data.caption = sample_book_data["caption"]
        book_data.summary = sample_book_data["summary"]

        mock_image = Mock(spec=UploadFile)
        mock_image.content_type = "image/jpeg"
        mock_image.read = Mock(return_value=b"fake image content")

        credentials = Mock()
        credentials.credentials = "valid_token"

        expected_result = {
            "id": "new-book-id",
            "title": sample_book_data["title"],
            "message": "Book created successfully",
        }
        mock_book_repo.create_book.return_value = expected_result

        # Act
        result = await book_service.create_book(book_data, mock_image, credentials)

        # Assert
        mock_book_repo.create_book.assert_called_once_with(
            book_data, mock_image, credentials
        )
        assert result == expected_result

    @pytest.mark.asyncio
    async def test_create_book_success_without_image(
        self, book_service, mock_book_repo, sample_book_data
    ):
        """Test tạo sách thành công không có ảnh"""
        # Arrange
        book_data = Mock()
        book_data.title = sample_book_data["title"]
        book_data.author = sample_book_data["author"]

        credentials = Mock()
        credentials.credentials = "valid_token"

        expected_result = {
            "id": "new-book-id",
            "title": sample_book_data["title"],
            "message": "Book created successfully",
        }
        mock_book_repo.create_book.return_value = expected_result

        # Act
        result = await book_service.create_book(book_data, None, credentials)

        # Assert
        mock_book_repo.create_book.assert_called_once_with(book_data, None, credentials)
        assert result == expected_result

    @pytest.mark.asyncio
    async def test_create_book_invalid_credentials(
        self, book_service, mock_book_repo, sample_book_data
    ):
        """Test tạo sách với credentials không hợp lệ"""
        # Arrange
        book_data = Mock()
        credentials = None

        expected_result = {
            "status_code": 401,
            "error": "Invalid token",
            "message": "Please login to upload Books",
        }
        mock_book_repo.create_book.return_value = expected_result

        # Act
        result = await book_service.create_book(book_data, None, credentials)

        # Assert
        assert result == expected_result

    def test_update_book_success(self, book_service, mock_book_repo):
        """Test cập nhật sách thành công"""
        # Arrange
        book_id = "book-123"
        book_update = {"title": "Updated Title", "author": "Updated Author"}
        expected_result = {
            "id": book_id,
            "title": "Updated Title",
            "author": "Updated Author",
            "message": "Book updated successfully",
        }
        mock_book_repo.update_book.return_value = expected_result

        # Act
        result = book_service.update_book(book_id, book_update)

        # Assert
        mock_book_repo.update_book.assert_called_once_with(book_id, book_update)
        assert result == expected_result

    def test_update_book_not_found(self, book_service, mock_book_repo):
        """Test cập nhật sách không tồn tại"""
        # Arrange
        book_id = "nonexistent"
        book_update = {"title": "New Title"}
        expected_result = {"status_code": 404, "error": "Book not found"}
        mock_book_repo.update_book.return_value = expected_result

        # Act
        result = book_service.update_book(book_id, book_update)

        # Assert
        mock_book_repo.update_book.assert_called_once_with(book_id, book_update)
        assert result == expected_result

    def test_delete_book_success(self, book_service, mock_book_repo):
        """Test xóa sách thành công"""
        # Arrange
        book_id = "book-123"
        expected_result = {"message": "Book deleted successfully"}
        mock_book_repo.delete_book.return_value = expected_result

        # Act
        result = book_service.delete_book(book_id)

        # Assert
        mock_book_repo.delete_book.assert_called_once_with(book_id)
        assert result == expected_result

    def test_delete_book_not_found(self, book_service, mock_book_repo):
        """Test xóa sách không tồn tại"""
        # Arrange
        book_id = "nonexistent"
        expected_result = {"status_code": 404, "error": "Book not found"}
        mock_book_repo.delete_book.return_value = expected_result

        # Act
        result = book_service.delete_book(book_id)

        # Assert
        mock_book_repo.delete_book.assert_called_once_with(book_id)
        assert result == expected_result

    def test_delete_book_unauthorized(self, book_service, mock_book_repo):
        """Test xóa sách không có quyền"""
        # Arrange
        book_id = "book-123"
        expected_result = {
            "status_code": 403,
            "error": "Unauthorized",
            "message": "You can only delete your own books",
        }
        mock_book_repo.delete_book.return_value = expected_result

        # Act
        result = book_service.delete_book(book_id)

        # Assert
        mock_book_repo.delete_book.assert_called_once_with(book_id)
        assert result == expected_result
