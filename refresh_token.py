#!/usr/bin/env python3
"""
Token Refresh Script for FoodVault App
Automatically fetches a new access token and updates the .env file
"""

import requests
import os
import re
from datetime import datetime
from pathlib import Path

# Configuration
API_URL = "https://api.corpus.swecha.org/api/v1/auth/login"
PHONE = "+916305877795"
PASSWORD = "Srinu@2006"
ENV_FILE_PATH = Path(__file__).parent / ".env"

def log_message(message):
    """Log messages with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_new_access_token():
    """Fetch a new access token from the API"""
    try:
        log_message("Requesting new access token...")

        # Try different request formats that are commonly used
        # Format 1: JSON body
        response = requests.post(
            API_URL,
            json={
                "phone": PHONE,
                "password": PASSWORD
            },
            headers={
                "Content-Type": "application/json"
            },
            timeout=30
        )

        if not response.ok:
            # Format 2: Form data (if JSON doesn't work)
            log_message("JSON request failed, trying form data...")
            response = requests.post(
                API_URL,
                data={
                    "username": PHONE,  # Some APIs use 'username' instead of 'phone'
                    "password": PASSWORD
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                timeout=30
            )

        if not response.ok:
            # Format 3: Alternative field names
            log_message("Form data failed, trying alternative format...")
            response = requests.post(
                API_URL,
                json={
                    "username": PHONE,
                    "password": PASSWORD
                },
                headers={
                    "Content-Type": "application/json"
                },
                timeout=30
            )

        if response.ok:
            response_data = response.json()
            log_message(f"API Response: {response_data}")

            # Try different possible token field names
            token = (response_data.get("access_token") or
                    response_data.get("token") or
                    response_data.get("accessToken") or
                    response_data.get("jwt"))

            if token:
                log_message("Successfully obtained new access token")
                return token
            else:
                log_message(f"Token not found in response. Available keys: {list(response_data.keys())}")
                return None
        else:
            log_message(f"Failed to get token. Status: {response.status_code}, Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        log_message(f"Network error while fetching token: {e}")
        return None
    except Exception as e:
        log_message(f"Unexpected error while fetching token: {e}")
        return None

def update_env_file(new_token):
    """Update the ACCESS_TOKEN in the .env file"""
    try:
        if not ENV_FILE_PATH.exists():
            log_message(f"Error: .env file not found at {ENV_FILE_PATH}")
            return False

        # Read the current .env file
        with open(ENV_FILE_PATH, 'r', encoding='utf-8') as file:
            content = file.read()

        # Create backup
        backup_path = ENV_FILE_PATH.with_suffix('.env.backup')
        with open(backup_path, 'w', encoding='utf-8') as backup_file:
            backup_file.write(content)
        log_message(f"Created backup at {backup_path}")

        # Replace the ACCESS_TOKEN line
        # Pattern to match ACCESS_TOKEN line with any quote style
        pattern = r'^ACCESS_TOKEN\s*=\s*["\']?[^"\'\r\n]*["\']?'
        replacement = f'ACCESS_TOKEN="{new_token}"'

        updated_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

        # Write the updated content back
        with open(ENV_FILE_PATH, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        log_message("Successfully updated .env file with new access token")
        return True

    except Exception as e:
        log_message(f"Error updating .env file: {e}")
        return False

def main():
    """Main function to refresh the access token"""
    log_message("Starting token refresh process...")

    # Get new access token
    new_token = get_new_access_token()

    if new_token:
        # Update the .env file
        if update_env_file(new_token):
            log_message("Token refresh completed successfully!")

            # Log the first and last few characters of the token for verification
            masked_token = f"{new_token[:10]}...{new_token[-10:]}" if len(new_token) > 20 else new_token
            log_message(f"New token: {masked_token}")
        else:
            log_message("Failed to update .env file")
            return 1
    else:
        log_message("Failed to obtain new access token")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()

    # If running interactively, wait for user input
    if hasattr(os, 'getenv') and not os.getenv('AUTOMATED_RUN'):
        input("Press Enter to exit...")

    exit(exit_code)
