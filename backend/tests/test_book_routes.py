import pytest
import json
import io
from unittest.mock import patch, Mock

from fastapi import status
from fastapi.testclient import TestClient


class TestBookRoutes:
    """Integration tests cho Book Routes theo nghiệp vụ"""

    def test_get_books_success(self, client):
        """Test API lấy tất cả sách thành công"""
        # Arrange
        expected_books = [
            {
                "id": "book-1",
                "title": "Python Programming",
                "author": "John Doe",
                "caption": "Learn Python",
                "summary": "A comprehensive guide",
            },
            {
                "id": "book-2",
                "title": "FastAPI Guide",
                "author": "Jane Smith",
                "caption": "Web APIs",
                "summary": "Building modern APIs",
            },
        ]

        with patch(
            "services.book.book_service.BookService.get_books"
        ) as mock_get_books:
            mock_get_books.return_value = expected_books

            # Act
            response = client.get("/products/")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["title"] == "Python Programming"

    def test_get_books_empty_list(self, client):
        """Test API lấy sách khi không có sách nào"""
        # Arrange
        with patch(
            "services.book.book_service.BookService.get_books"
        ) as mock_get_books:
            mock_get_books.return_value = []

            # Act
            response = client.get("/products/")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data == []

    def test_get_books_with_pagination_default(self, client):
        """Test API phân trang với tham số mặc định"""
        # Arrange
        expected_result = {
            "books": [
                {"id": "book-1", "title": "Book 1"},
                {"id": "book-2", "title": "Book 2"},
            ],
            "total": 10,
            "page": 1,
            "limit": 3,
            "total_pages": 4,
        }

        with patch(
            "services.book.book_service.BookService.get_books_with_pagination"
        ) as mock_pagination:
            mock_pagination.return_value = expected_result

            # Act
            response = client.get("/products/pagination")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["page"] == 1
            assert data["limit"] == 3
            assert len(data["books"]) == 2

    def test_get_books_with_pagination_custom_params(self, client):
        """Test API phân trang với tham số tùy chỉnh"""
        # Arrange
        expected_result = {
            "books": [{"id": "book-6", "title": "Book 6"}],
            "total": 20,
            "page": 2,
            "limit": 5,
            "total_pages": 4,
        }

        with patch(
            "services.book.book_service.BookService.get_books_with_pagination"
        ) as mock_pagination:
            mock_pagination.return_value = expected_result

            # Act
            response = client.get("/products/pagination?page=2&limit=5")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["page"] == 2
            assert data["limit"] == 5

    def test_get_books_with_pagination_invalid_params(self, client):
        """Test API phân trang với tham số không hợp lệ"""
        # Arrange - page âm
        with patch(
            "services.book.book_service.BookService.get_books_with_pagination"
        ) as mock_pagination:
            mock_pagination.return_value = {
                "status_code": 400,
                "error": "Invalid pagination parameters",
            }

            # Act
            response = client.get("/products/pagination?page=-1&limit=5")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["status_code"] == 400

    def test_get_book_by_id_success(self, client):
        """Test API lấy sách theo ID thành công"""
        # Arrange
        book_id = "book-123"
        expected_book = {
            "id": book_id,
            "title": "Test Book",
            "author": "Test Author",
            "caption": "Test Caption",
            "summary": "Test Summary",
            "cover_image": "https://example.com/image.jpg",
        }

        with patch(
            "services.book.book_service.BookService.get_book_with_ID"
        ) as mock_get_book:
            mock_get_book.return_value = expected_book

            # Act
            response = client.get(f"/products/book/{book_id}")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == book_id
            assert data["title"] == "Test Book"

    def test_get_book_by_id_not_found(self, client):
        """Test API lấy sách theo ID không tồn tại"""
        # Arrange
        book_id = "nonexistent"

        with patch(
            "services.book.book_service.BookService.get_book_with_ID"
        ) as mock_get_book:
            mock_get_book.return_value = {"status_code": 404, "error": "Book not found"}

            # Act
            response = client.get(f"/products/book/{book_id}")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["status_code"] == 404

    def test_get_books_by_user_id_success(self, client):
        """Test API lấy sách theo user ID thành công"""
        # Arrange
        user_id = "user-123"
        expected_books = [
            {"id": "book-1", "title": "User's Book 1", "user_id": user_id},
            {"id": "book-2", "title": "User's Book 2", "user_id": user_id},
        ]

        with patch(
            "services.book.book_service.BookService.get_books_by_user_id"
        ) as mock_get_books:
            mock_get_books.return_value = expected_books

            # Act
            response = client.get(f"/products/user/{user_id}")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert all(book["user_id"] == user_id for book in data)

    def test_get_books_by_user_id_no_books(self, client):
        """Test API lấy sách theo user ID khi user không có sách"""
        # Arrange
        user_id = "user-without-books"

        with patch(
            "services.book.book_service.BookService.get_books_by_user_id"
        ) as mock_get_books:
            mock_get_books.return_value = {
                "status_code": 404,
                "error": "Books not found for this user",
            }

            # Act
            response = client.get(f"/products/user/{user_id}")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["status_code"] == 404

    def test_create_book_success_with_image(self, client, auth_token, sample_book_data):
        """Test API tạo sách thành công với ảnh"""
        # Arrange
        test_image = io.BytesIO(b"fake image content")

        with patch("services.book.book_service.BookService.create_book") as mock_create:
            mock_create.return_value = {
                "status_code": 201,
                "data": {
                    "id": "new-book-id",
                    "title": sample_book_data["title"],
                    "author": sample_book_data["author"],
                },
                "message": "Book created successfully",
            }

            # Act
            response = client.post(
                "/products/",
                data={
                    "title": sample_book_data["title"],
                    "author": sample_book_data["author"],
                    "caption": sample_book_data["caption"],
                    "summary": sample_book_data["summary"],
                },
                files={"image": ("test.jpg", test_image, "image/jpeg")},
                headers={"Authorization": auth_token},
            )

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Book created successfully"

    def test_create_book_success_without_image(
        self, client, auth_token, sample_book_data
    ):
        """Test API tạo sách thành công không có ảnh"""
        # Arrange
        with patch("services.book.book_service.BookService.create_book") as mock_create:
            mock_create.return_value = {
                "status_code": 201,
                "data": {"id": "new-book-id", "title": sample_book_data["title"]},
                "message": "Book created successfully",
            }

            # Act
            response = client.post(
                "/products/",
                data={
                    "title": sample_book_data["title"],
                    "author": sample_book_data["author"],
                    "caption": sample_book_data["caption"],
                    "summary": sample_book_data["summary"],
                },
                headers={"Authorization": auth_token},
            )

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Book created successfully"

    def test_create_book_unauthorized(self, client, sample_book_data):
        """Test API tạo sách không có token"""
        # Act
        response = client.post(
            "/products/",
            data={
                "title": sample_book_data["title"],
                "author": sample_book_data["author"],
                "caption": sample_book_data["caption"],
                "summary": sample_book_data["summary"],
            },
        )

        # Assert
        assert response.status_code == 403  # FastAPI security dependency

    def test_create_book_invalid_token(self, client, sample_book_data):
        """Test API tạo sách với token không hợp lệ"""
        # Arrange
        with patch("services.book.book_service.BookService.create_book") as mock_create:
            mock_create.return_value = {
                "status_code": 401,
                "error": "Invalid token",
                "message": "Please login to upload Books",
            }

            # Act
            response = client.post(
                "/products/",
                data={
                    "title": sample_book_data["title"],
                    "author": sample_book_data["author"],
                    "caption": sample_book_data["caption"],
                    "summary": sample_book_data["summary"],
                },
                headers={"Authorization": "Bearer invalid_token"},
            )

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["status_code"] == 401

    def test_create_book_invalid_file_type(self, client, auth_token, sample_book_data):
        """Test API tạo sách với file type không hợp lệ"""
        # Arrange
        test_file = io.BytesIO(b"not an image")

        with patch("services.book.book_service.BookService.create_book") as mock_create:
            mock_create.return_value = {
                "status_code": 400,
                "error": "Invalid file type",
                "message": "Only JPEG and PNG files are allowed",
            }

            # Act
            response = client.post(
                "/products/",
                data={
                    "title": sample_book_data["title"],
                    "author": sample_book_data["author"],
                    "caption": sample_book_data["caption"],
                    "summary": sample_book_data["summary"],
                },
                files={"image": ("test.txt", test_file, "text/plain")},
                headers={"Authorization": auth_token},
            )

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["status_code"] == 400

    def test_create_book_file_too_large(self, client, auth_token, sample_book_data):
        """Test API tạo sách với file quá lớn"""
        # Arrange
        large_file = io.BytesIO(b"x" * (6 * 1024 * 1024))  # 6MB

        with patch("services.book.book_service.BookService.create_book") as mock_create:
            mock_create.return_value = {
                "status_code": 400,
                "error": "File size exceeds the limit",
                "message": "File size should be less than 5MB",
            }

            # Act
            response = client.post(
                "/products/",
                data={
                    "title": sample_book_data["title"],
                    "author": sample_book_data["author"],
                    "caption": sample_book_data["caption"],
                    "summary": sample_book_data["summary"],
                },
                files={"image": ("large.jpg", large_file, "image/jpeg")},
                headers={"Authorization": auth_token},
            )

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["status_code"] == 400

    def test_input_validation_missing_required_fields(self, client, auth_token):
        """Test validation với dữ liệu thiếu trường bắt buộc"""
        # Arrange - missing title
        incomplete_data = {
            "author": "Test Author",
            "caption": "Test Caption",
            "summary": "Test Summary",
        }

        # Act
        response = client.post(
            "/products/", data=incomplete_data, headers={"Authorization": auth_token}
        )

        # Assert
        assert response.status_code == 422  # Validation error

    def test_input_validation_empty_strings(self, client, auth_token):
        """Test validation với chuỗi rỗng"""
        # Arrange
        invalid_data = {
            "title": "",  # Empty title
            "author": "Test Author",
            "caption": "Test Caption",
            "summary": "Test Summary",
        }

        # Act
        response = client.post(
            "/products/", data=invalid_data, headers={"Authorization": auth_token}
        )

        # Assert

        assert response.status_code == 422 or (
            response.status_code == 200 and response.json().get("status_code") == 400
        )

    def test_endpoint_performance(self, client):
        """Test hiệu suất của endpoint lấy sách"""
        import time

        # Arrange
        with patch(
            "services.book.book_service.BookService.get_books"
        ) as mock_get_books:
            mock_get_books.return_value = [
                {"id": f"book-{i}", "title": f"Book {i}"} for i in range(50)
            ]

            # Act
            start_time = time.time()
            response = client.get("/products/")
            end_time = time.time()

            # Assert
            response_time = end_time - start_time
            assert response_time < 2.0  # API phải trả về trong vòng 2 giây
            assert response.status_code == 200

    def test_concurrent_requests(self, client):
        """Test xử lý requests đồng thời"""
        import threading
        import time

        results = []

        def make_request():
            with patch(
                "services.book.book_service.BookService.get_books"
            ) as mock_get_books:
                mock_get_books.return_value = [{"id": "book-1", "title": "Book 1"}]
                response = client.get("/products/")
                results.append(response.status_code)

        # Tạo 10 threads đồng thời
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)

        # Chạy tất cả threads
        for thread in threads:
            thread.start()

        # Đợi tất cả threads hoàn thành
        for thread in threads:
            thread.join()

        # Assert tất cả requests đều thành công
        assert len(results) == 10
        assert all(status == 200 for status in results)
