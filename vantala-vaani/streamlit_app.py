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

# Import and run the main recipe collection app
from src.core.recipe_collection import main

if __name__ == "__main__":
    main()
