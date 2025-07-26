#!/usr/bin/env python3
"""
Streamlit App Entry Point for Vantala Vaani
This is the main entry point for Streamlit Cloud deployment.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    # Import and run the main recipe collection app
    from src.core.recipe_collection import main

    if __name__ == "__main__":
        main()
except ImportError as e:
    import streamlit as st
    st.error(f"Import error: {e}")
    st.info("Please ensure all dependencies are installed.")
except Exception as e:
    import streamlit as st
    st.error(f"Application error: {e}")
    st.info("There was an issue loading the application.")
