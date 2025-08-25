import streamlit as st
import os
from typing import Optional

class FileHandler:
    def __init__(self):
        # File size limits in MB (load from environment or use defaults)
        self.MAX_AUDIO_SIZE = int(os.getenv("MAX_AUDIO_SIZE_MB", 50))  # Default 50MB
        self.MAX_VIDEO_SIZE = int(os.getenv("MAX_VIDEO_SIZE_MB", 100))  # Default 100MB
        self.MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE_MB", 10))  # Default 10MB

        # Supported file types
        self.AUDIO_TYPES = ['mp3', 'wav', 'm4a']
        self.VIDEO_TYPES = ['mp4', 'mov', 'avi']
        self.IMAGE_TYPES = ['jpg', 'jpeg', 'png', 'webp']

    def validate_file(self, uploaded_file, media_type: str) -> bool:
        """Validate uploaded file based on type and size"""
        if not uploaded_file:
            return False

        # Get file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()

        # Check file type
        if media_type == "audio":
            if file_extension not in self.AUDIO_TYPES:
                st.error(f"Unsupported audio format. Please use: {', '.join(self.AUDIO_TYPES)}")
                return False

            # Check file size (convert bytes to MB)
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > self.MAX_AUDIO_SIZE:
                st.error(f"Audio file too large. Maximum size: {self.MAX_AUDIO_SIZE}MB")
                return False

        elif media_type == "video":
            if file_extension not in self.VIDEO_TYPES:
                st.error(f"Unsupported video format. Please use: {', '.join(self.VIDEO_TYPES)}")
                return False

            # Check file size (convert bytes to MB)
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > self.MAX_VIDEO_SIZE:
                st.error(f"Video file too large. Maximum size: {self.MAX_VIDEO_SIZE}MB")
                return False

        elif media_type == "image":
            if file_extension not in self.IMAGE_TYPES:
                st.error(f"Unsupported image format. Please use: {', '.join(self.IMAGE_TYPES)}")
                return False

            # Check file size (convert bytes to MB)
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > self.MAX_IMAGE_SIZE:
                st.error(f"Image file too large. Maximum size: {self.MAX_IMAGE_SIZE}MB")
                return False

        return True

    def get_file_info(self, uploaded_file) -> dict:
        """Get information about the uploaded file"""
        if not uploaded_file:
            return {}

        file_size_mb = uploaded_file.size / (1024 * 1024)

        return {
            "name": uploaded_file.name,
            "size_mb": round(file_size_mb, 2),
            "type": uploaded_file.type,
            "extension": uploaded_file.name.split('.')[-1].lower()
        }
