import requests
import json
from typing import Tuple, Optional
from services.auth_service import AuthService
import os

class RecordService:
    def __init__(self):
        self.auth_service = AuthService()
        self.category_id = os.getenv("CATEGORY_ID", "833299f6-ff1c-4fde-804f-6d3b3877c76e")
        self.api_base = self.auth_service.get_api_base()
    
    def submit_text_recipe(self, content: str, recipe_name: str = "", cuisine_type: str = "", 
                          cooking_time: str = "", difficulty: str = "") -> Tuple[bool, str, Optional[str]]:
        """Submit a text recipe to the API"""
        try:
            # Prepare the payload
            payload = {
                "category_id": self.category_id,
                "media_type": "text",
                "content": content
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
                payload["metadata"] = json.dumps(metadata)
            
            # Make the API request
            response = requests.post(
                f"{self.api_base}/api/v1/records/",
                headers=self.auth_service.get_headers(),
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                response_data = response.json()
                record_id = response_data.get("id", "Unknown")
                return True, f"Text recipe submitted successfully!", record_id
            elif response.status_code == 401:
                return False, "Authentication failed. Please check your access token.", None
            elif response.status_code == 400:
                error_detail = response.json().get("detail", "Bad request")
                return False, f"Invalid data: {error_detail}", None
            else:
                return False, f"Submission failed with status code: {response.status_code}", None
                
        except requests.exceptions.Timeout:
            return False, "Request timed out. Please try again.", None
        except requests.exceptions.ConnectionError:
            return False, "Connection error. Please check your internet connection.", None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None
    
    def submit_media_recipe(self, uploaded_file, media_type: str, recipe_name: str = "", 
                           cuisine_type: str = "", cooking_time: str = "", 
                           difficulty: str = "") -> Tuple[bool, str, Optional[str]]:
        """Submit an audio or video recipe to the API"""
        try:
            # Prepare the multipart form data
            files = {
                'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }
            
            data = {
                'category_id': self.category_id,
                'media_type': media_type
            }
            
            # Add metadata if provided
            if recipe_name:
                data['recipe_name'] = recipe_name
            if cuisine_type:
                data['cuisine_type'] = cuisine_type
            if cooking_time:
                data['cooking_time'] = cooking_time
            if difficulty and difficulty != "Not specified":
                data['difficulty'] = difficulty
            
            # Make the API request
            response = requests.post(
                f"{self.api_base}/api/v1/records/upload",
                headers=self.auth_service.get_multipart_headers(),
                files=files,
                data=data,
                timeout=120  # Longer timeout for file uploads
            )
            
            if response.status_code == 201:
                response_data = response.json()
                record_id = response_data.get("id", "Unknown")
                return True, f"{media_type.capitalize()} recipe uploaded successfully!", record_id
            elif response.status_code == 401:
                return False, "Authentication failed. Please check your access token.", None
            elif response.status_code == 400:
                error_detail = response.json().get("detail", "Bad request")
                return False, f"Invalid file or data: {error_detail}", None
            elif response.status_code == 413:
                return False, "File too large. Please use a smaller file.", None
            else:
                return False, f"Upload failed with status code: {response.status_code}", None
                
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
