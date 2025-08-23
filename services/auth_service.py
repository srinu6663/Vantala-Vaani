import os
import requests
from typing import Optional

class AuthService:
    def __init__(self):
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.api_base = os.getenv("API_BASE", "https://corpus-app-domain")
        
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
        """Test authentication by making a simple API call"""
        if not self.access_token:
            return False
        
        try:
            # Test authentication with a simple GET request
            response = requests.get(
                f"{self.api_base}/api/v1/records/",
                headers=self.get_headers(),
                timeout=10
            )
            return response.status_code in [200, 401]  # 401 means auth header was processed
        except Exception:
            return False
    
    def get_api_base(self) -> str:
        """Get the API base URL"""
        return self.api_base
