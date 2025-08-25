import os
import requests
from typing import Optional

class AuthService:
    def __init__(self):
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.api_base = os.getenv("API_BASE", "https://api.corpus.swecha.org")

    def get_headers(self) -> dict:
        """Get authentication headers for API requests"""
        if not self.access_token:
            raise ValueError("ACCESS_TOKEN not found in environment variables")

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_multipart_headers(self) -> dict:
        """Get authentication headers for multipart requests"""
        if not self.access_token:
            raise ValueError("ACCESS_TOKEN not found in environment variables")

        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def is_authenticated(self) -> bool:
        """Test authentication by checking if access token exists"""
        # For development: just check if token exists
        if not self.access_token:
            return False

        # For development mode, return True if token exists
        # TODO: In production, validate token with actual API call
        return True

        # Optional: Try to validate with API if available (commented out for dev)
        # try:
        #     response = requests.get(
        #         f"{self.api_base}/api/v1/records/",
        #         headers=self.get_headers(),
        #         timeout=5
        #     )
        #     return response.status_code in [200, 401]
        # except Exception:
        #     return bool(self.access_token)

    def get_api_base(self) -> str:
        """Get the API base URL"""
        return self.api_base
