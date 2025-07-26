"""
Project configuration for Vantala Vaani
Contains project-wide settings and paths.
"""

from pathlib import Path

# Project Information
PROJECT_NAME = "వంటల వాణి (Vantala Vaani)"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = "Bilingual Telugu-English recipe collection and ML preprocessing system"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"

# Data Files
RECIPES_CSV = DATA_DIR / "recipes.csv"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RAW_DATA_DIR = DATA_DIR / "raw"

# Ensure directories exist
for dir_path in [DATA_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR]:
    dir_path.mkdir(exist_ok=True)
