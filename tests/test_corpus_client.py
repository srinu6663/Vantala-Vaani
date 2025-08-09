import pytest
import responses
import json
from services.corpus_client import CorpusClient, CorpusAppError

class TestCorpusClient:
    """Test CorpusApp client functionality"""

    def setup_method(self):
        """Setup test client"""
        self.client = CorpusClient("https://test-corpus.com/api", "test-token")

    @responses.activate
    def test_create_content_success(self):
        """Test successful content creation"""
        # Mock the API response
        responses.add(
            responses.POST,
            "https://test-corpus.com/api/v1/content",
            json={"id": "content-123", "status": "created"},
            status=201
        )

        payload = {
            "category_id": "food-category",
            "title": "Test Recipe",
            "content": {"text_te": "Cook something delicious"}
        }

        result = self.client.create_content(payload)
        assert result["id"] == "content-123"
        assert result["status"] == "created"

    @responses.activate
    def test_create_content_auth_error(self):
        """Test authentication error"""
        responses.add(
            responses.POST,
            "https://test-corpus.com/api/v1/content",
            json={"error": "Unauthorized"},
            status=401
        )

        payload = {"title": "Test"}

        with pytest.raises(CorpusAppError) as exc_info:
            self.client.create_content(payload)

        assert "Authentication failed" in str(exc_info.value)

    @responses.activate
    def test_upload_media_direct_success(self):
        """Test successful direct media upload"""
        responses.add(
            responses.POST,
            "https://test-corpus.com/api/v1/media",
            json={"id": "media-123", "url": "https://cdn.example.com/media-123.mp3"},
            status=201
        )

        file_bytes = b"fake audio content"
        result = self.client._upload_media_direct(file_bytes, "test.mp3", "audio/mpeg")

        assert result["id"] == "media-123"
        assert "media-123.mp3" in result["url"]

    @responses.activate
    def test_upload_media_presigned_success(self):
        """Test successful presigned media upload"""
        # Mock presign request
        responses.add(
            responses.POST,
            "https://test-corpus.com/api/v1/media/presign",
            json={
                "upload_url": "https://s3.example.com/upload-url",
                "resource_url": "https://cdn.example.com/resource-url",
                "headers": {"Content-Type": "audio/mpeg"},
                "id": "media-456"
            },
            status=200
        )

        # Mock presigned upload
        responses.add(
            responses.PUT,
            "https://s3.example.com/upload-url",
            status=200
        )

        file_bytes = b"fake audio content"
        result = self.client._upload_media_presigned(file_bytes, "test.mp3", "audio/mpeg")

        assert result["id"] == "media-456"
        assert result["url"] == "https://cdn.example.com/resource-url"

    @responses.activate
    def test_list_content_success(self):
        """Test successful content listing"""
        responses.add(
            responses.GET,
            "https://test-corpus.com/api/v1/content",
            json={
                "items": [
                    {"id": "content-1", "title": "Recipe 1"},
                    {"id": "content-2", "title": "Recipe 2"}
                ],
                "total": 2
            },
            status=200
        )

        result = self.client.list_content()
        assert len(result["items"]) == 2
        assert result["total"] == 2

    @responses.activate
    def test_get_content_success(self):
        """Test successful content retrieval"""
        responses.add(
            responses.GET,
            "https://test-corpus.com/api/v1/content/content-123",
            json={
                "id": "content-123",
                "title": "Test Recipe",
                "category_id": "food-category"
            },
            status=200
        )

        result = self.client.get_content("content-123")
        assert result["id"] == "content-123"
        assert result["title"] == "Test Recipe"

    @responses.activate
    def test_file_too_large_error(self):
        """Test file too large error"""
        responses.add(
            responses.POST,
            "https://test-corpus.com/api/v1/media",
            json={"error": "File too large"},
            status=413
        )

        with pytest.raises(CorpusAppError) as exc_info:
            self.client._upload_media_direct(b"content", "test.mp3", "audio/mpeg")

        assert "File too large" in str(exc_info.value)

    @responses.activate
    def test_unsupported_media_type_error(self):
        """Test unsupported media type error"""
        responses.add(
            responses.POST,
            "https://test-corpus.com/api/v1/media",
            json={"error": "Unsupported media type"},
            status=415
        )

        with pytest.raises(CorpusAppError) as exc_info:
            self.client._upload_media_direct(b"content", "test.exe", "application/octet-stream")

        assert "Unsupported media type" in str(exc_info.value)

    @responses.activate
    def test_server_error(self):
        """Test server error handling"""
        responses.add(
            responses.POST,
            "https://test-corpus.com/api/v1/content",
            json={"error": "Internal server error"},
            status=500
        )

        with pytest.raises(CorpusAppError) as exc_info:
            self.client.create_content({"title": "Test"})

        assert "Server error" in str(exc_info.value)

    @responses.activate
    def test_test_connection_success(self):
        """Test successful connection test"""
        responses.add(
            responses.GET,
            "https://test-corpus.com/api/v1/content",
            json={"items": []},
            status=200
        )

        assert self.client.test_connection() is True

    @responses.activate
    def test_test_connection_failure(self):
        """Test failed connection test"""
        responses.add(
            responses.GET,
            "https://test-corpus.com/api/v1/content",
            json={"error": "Unauthorized"},
            status=401
        )

        assert self.client.test_connection() is False
