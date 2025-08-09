import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    def __init__(self):
        # Try Streamlit secrets first, then environment variables
        try:
            import streamlit as st
            # Use Streamlit secrets in cloud deployment
            self.CORPUSAPP_BASE_URL = st.secrets.get("CORPUSAPP_BASE_URL", os.getenv("CORPUSAPP_BASE_URL", ""))
            self.CORPUSAPP_TOKEN = st.secrets.get("CORPUSAPP_TOKEN", os.getenv("CORPUSAPP_TOKEN", ""))
            self.CATEGORY_ID_FOOD = st.secrets.get("CATEGORY_ID_FOOD", os.getenv("CATEGORY_ID_FOOD", "833299f6-ff1c-4fde-804f-6d3b3877c76e"))
            self.ALLOWED_AUDIO_TYPES = st.secrets.get("ALLOWED_AUDIO_TYPES", os.getenv("ALLOWED_AUDIO_TYPES", "mp3,wav,m4a,aac,ogg,flac")).split(",")
            self.MAX_UPLOAD_MB = int(st.secrets.get("MAX_UPLOAD_MB", os.getenv("MAX_UPLOAD_MB", "50")))
        except:
            # Fallback to environment variables for local development
            self.CORPUSAPP_BASE_URL = os.getenv("CORPUSAPP_BASE_URL", "")
            self.CORPUSAPP_TOKEN = os.getenv("CORPUSAPP_TOKEN", "")
            self.CATEGORY_ID_FOOD = os.getenv("CATEGORY_ID_FOOD", "833299f6-ff1c-4fde-804f-6d3b3877c76e")
            self.ALLOWED_AUDIO_TYPES = os.getenv("ALLOWED_AUDIO_TYPES", "mp3,wav,m4a,aac,ogg,flac").split(",")
            self.MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "50"))

    def validate(self) -> bool:
        """Validate that required settings are present"""
        return bool(self.CORPUSAPP_BASE_URL and self.CORPUSAPP_TOKEN)

    def get_missing_vars(self) -> List[str]:
        """Return list of missing required environment variables"""
        missing = []
        if not self.CORPUSAPP_BASE_URL:
            missing.append("CORPUSAPP_BASE_URL")
        if not self.CORPUSAPP_TOKEN:
            missing.append("CORPUSAPP_TOKEN")
        return missing

settings = Settings()
