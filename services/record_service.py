import requests
import json
import uuid
from typing import Tuple, Optional
from services.auth_service import AuthService
import os

class RecordService:
    def __init__(self):
        self.auth_service = AuthService()
        self.category_id = os.getenv("CATEGORY_ID", "833299f6-ff1c-4fde-804f-6d3b3877c76e")
        self.user_id = os.getenv("USER_ID", "bd591c5f-62fc-4bc5-a28f-af20429bcfaf")
        self.api_base = self.auth_service.get_api_base()

    def submit_media_recipe(self, uploaded_file, media_type: str, recipe_name: str = "",
                           cuisine_type: str = "", cooking_time: str = "",
                           difficulty: str = "") -> Tuple[bool, str, Optional[str]]:
        """Submit an audio or video recipe to the API using chunked upload"""
        try:
            # Generate a unique upload UUID
            upload_uuid = str(uuid.uuid4())

            # Step 1: Upload chunk using the chunk endpoint (multipart format)
            file_content = uploaded_file.getvalue()

            # Prepare multipart data for chunk upload
            chunk_files = {
                'chunk': ('chunk_0', file_content, 'application/octet-stream')
            }

            chunk_data = {
                'upload_uuid': upload_uuid,
                'filename': uploaded_file.name,
                'total_chunks': '1',
                'chunk_index': '0'
            }

            chunk_headers = {
                "Authorization": f"Bearer {self.auth_service.access_token}"
                # No Content-Type - let requests handle multipart
            }

            # Upload the chunk
            chunk_response = requests.post(
                f"{self.api_base}/api/v1/records/upload/chunk",
                headers=chunk_headers,
                files=chunk_files,
                data=chunk_data,
                timeout=60
            )

            if chunk_response.status_code not in [200, 201]:
                return False, f"Chunk upload failed: {chunk_response.text}", None

            # Step 2: Create the record (JSON format)
            record_payload = {
                'category_id': self.category_id,
                'media_type': media_type,
                'title': recipe_name if recipe_name else f"Traditional {media_type.capitalize()} Recipe",
                'language': 'hindi',
                'release_rights': 'creator',
                'user_id': self.user_id,
                'upload_uuid': upload_uuid,
                'filename': uploaded_file.name,
                'total_chunks': 1
            }

            # Add metadata if provided
            metadata = {}
            if recipe_name:
                metadata["recipe_name"] = recipe_name
            if cuisine_type:
                metadata["cuisine_type"] = cuisine_type
            if cooking_time:
                metadata["cooking_time"] = cooking_time
            if difficulty and difficulty != "Not specified":
                metadata["difficulty"] = difficulty

            if metadata:
                record_payload["metadata"] = json.dumps(metadata)

            record_headers = {
                "Authorization": f"Bearer {self.auth_service.access_token}"
                # Let requests handle Content-Type for form data
            }

            # Convert record payload to form data format
            record_form_data = {
                'category_id': self.category_id,
                'media_type': media_type,
                'title': recipe_name if recipe_name else f"Traditional {media_type.capitalize()} Recipe",
                'language': 'hindi',
                'release_rights': 'creator',
                'user_id': self.user_id,
                'upload_uuid': upload_uuid,
                'filename': uploaded_file.name,
                'total_chunks': '1'  # Convert to string for form data
            }

            # Add metadata if provided (keep as JSON string in form data)
            if metadata:
                record_form_data["metadata"] = json.dumps(metadata)

            # Create the record using form data
            record_response = requests.post(
                f"{self.api_base}/api/v1/records/upload",
                headers=record_headers,
                data=record_form_data,  # Use data instead of json
                timeout=60
            )

            if record_response.status_code == 201:
                response_data = record_response.json()
                record_id = response_data.get("id", "Unknown")
                return True, f"{media_type.capitalize()} recipe uploaded successfully!", record_id
            elif record_response.status_code == 401:
                return False, "Authentication failed. Please check your access token.", None
            elif record_response.status_code == 400:
                error_detail = record_response.json().get("detail", "Bad request")
                return False, f"Invalid file or data: {error_detail}", None
            elif record_response.status_code == 413:
                return False, "File too large. Please use a smaller file.", None
            elif record_response.status_code == 500:
                return False, "Server error: The CorpusApp API is currently experiencing issues. Please try again later or contact support.", None
            else:
                return False, f"Upload failed with status code: {record_response.status_code}", None

        except requests.exceptions.Timeout:
            return False, "Upload timed out. Please try with a smaller file or check your connection.", None
        except requests.exceptions.ConnectionError:
            return False, "Connection error. Please check your internet connection.", None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None

    def verify_submission(self, record_id: str) -> Tuple[bool, dict]:
        """Verify that a record was successfully submitted"""
        try:
            response = requests.get(
                f"{self.api_base}/api/v1/records/{record_id}",
                headers=self.auth_service.get_headers(),
                timeout=10
            )

            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {}

        except Exception:
            return False, {}
