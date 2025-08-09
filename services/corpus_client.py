import requests
import mimetypes
from typing import Dict, Any, Optional, List
import json
from config.settings import settings

class CorpusAppError(Exception):
    """Custom exception for CorpusApp API errors"""
    pass

class CorpusClient:
    """Client for interacting with CorpusApp API"""

    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = (base_url or settings.CORPUSAPP_BASE_URL).rstrip('/')
        self.token = token or settings.CORPUSAPP_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'User-Agent': 'Vantala-Vaani/1.0'
        })

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login to get access token"""
        login_url = self.base_url + "/auth/login"

        # For login, don't use authorization header
        login_session = requests.Session()
        login_session.headers.update({
            'User-Agent': 'Vantala-Vaani/1.0',
            'Content-Type': 'application/json'
        })

        # Format phone number with country code if needed
        phone = username
        if not phone.startswith('+'):
            if phone.startswith('91'):
                phone = '+' + phone
            else:
                phone = '+91' + phone

        # Use the correct format that works
        payload = {"phone": phone, "password": password}

        try:
            print(f"  Attempting login with phone: {phone}")
            response = login_session.post(login_url, json=payload)
            print(f"  Response status: {response.status_code}")

            result = self._handle_response(response)

            # Update the session with the new token
            if 'access_token' in result:
                self.token = result['access_token']
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}'
                })

            return result

        except CorpusAppError as e:
            print(f"  Login error: {e}")
            raise

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate errors"""
        try:
            if response.status_code == 401:
                raise CorpusAppError("Authentication failed. Please check your API token.")
            elif response.status_code == 403:
                raise CorpusAppError("Permission denied. Check your API token permissions.")
            elif response.status_code == 413:
                raise CorpusAppError("File too large. Please reduce file size and try again.")
            elif response.status_code == 415:
                raise CorpusAppError("Unsupported media type. Please use a supported audio format.")
            elif response.status_code >= 500:
                raise CorpusAppError("Server error. Please try again later.")
            elif not response.ok:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', error_data.get('message', f'HTTP {response.status_code}'))
                except:
                    error_msg = f'HTTP {response.status_code}: {response.reason}'
                raise CorpusAppError(f"API error: {error_msg}")

            return response.json()
        except requests.exceptions.JSONDecodeError:
            if response.ok:
                return {"success": True, "status_code": response.status_code}
            else:
                raise CorpusAppError(f"Invalid response from server (HTTP {response.status_code})")

    def upload_media(self, file_bytes: bytes, filename: str, mime_type: str = None) -> Dict[str, Any]:
        """Upload media file to CorpusApp"""
        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(filename)
            if mime_type is None:
                mime_type = 'application/octet-stream'

        try:
            return self._upload_media_direct(file_bytes, filename, mime_type)
        except CorpusAppError as e:
            if "404" in str(e) or "405" in str(e) or "not found" in str(e).lower():
                return self._upload_media_presigned(file_bytes, filename, mime_type)
            else:
                raise

    def _upload_media_direct(self, file_bytes: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        """Direct upload using Swecha CorpusApp records endpoints"""
        # Use the correct Swecha API endpoint for uploading files
        upload_url = self.base_url + "/records/upload"

        files = {'file': (filename, file_bytes, mime_type)}

        response = self.session.post(upload_url, files=files)
        return self._handle_response(response)

    def _upload_media_presigned(self, file_bytes: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        """Presigned URL upload pattern"""
        presign_url = self.base_url + "/media/presign"
        presign_data = {
            'filename': filename,
            'content_type': mime_type,
            'size': len(file_bytes)
        }

        response = self.session.post(presign_url, json=presign_data)
        presign_result = self._handle_response(response)

        upload_url = presign_result['upload_url']
        upload_headers = presign_result.get('headers', {})

        upload_session = requests.Session()
        upload_session.headers.update(upload_headers)

        upload_response = upload_session.put(upload_url, data=file_bytes)

        if not upload_response.ok:
            raise CorpusAppError(f"Failed to upload file: HTTP {upload_response.status_code}")

        return {
            'id': presign_result.get('id'),
            'url': presign_result.get('resource_url'),
            'mime_type': mime_type,
            'size': len(file_bytes)
        }

    def create_content(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create record in Swecha CorpusApp using the records endpoint"""
        url = self.base_url + "/records/"

        # Ensure required fields are present
        if 'media_type' not in payload:
            payload['media_type'] = 'text'  # Default to text for recipe content

        if 'user_id' not in payload:
            # Extract user_id from token
            user_id = self._get_user_id_from_token()
            if user_id:
                payload['user_id'] = user_id
            else:
                raise CorpusAppError("Unable to determine user_id from token")

        response = self.session.post(url, json=payload)
        return self._handle_response(response)

    def _get_user_id_from_token(self) -> str:
        """Extract user_id from JWT token"""
        try:
            import jwt
            decoded = jwt.decode(self.token, options={"verify_signature": False})
            return decoded.get('sub')
        except Exception:
            return None

    def list_content(self, category_id: str = None, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """List records from Swecha CorpusApp"""
        url = self.base_url + "/records/"
        params = {}

        if category_id:
            params['category_id'] = category_id

        if filters:
            params.update(filters)

        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def get_content(self, record_id: str) -> Dict[str, Any]:
        """Get specific record by ID from Swecha CorpusApp"""
        url = self.base_url + "/records/" + record_id

        response = self.session.get(url)
        return self._handle_response(response)

    def test_connection(self) -> bool:
        """Test connection to CorpusApp API"""
        try:
            self.list_content()
            return True
        except Exception:
            return False

    def discover_endpoints(self) -> Dict[str, Any]:
        """Discover available Swecha CorpusApp API endpoints"""
        endpoints_to_test = {
            "records_list": ["/records/"],
            "records_upload": ["/records/upload"],
            "categories": ["/categories/"],
            "auth_login": ["/auth/login"]
        }

        discovered = {"base_url": self.base_url, "working_endpoints": {}}

        for endpoint_type, paths in endpoints_to_test.items():
            for path in paths:
                full_url = self.base_url + path
                try:
                    # For auth endpoints, don't use authorization
                    if "auth" in endpoint_type:
                        test_session = requests.Session()
                    else:
                        test_session = self.session

                    response = test_session.get(full_url)
                    if response.status_code != 404:
                        discovered["working_endpoints"][endpoint_type] = full_url
                        break
                except:
                    continue

        return discovered