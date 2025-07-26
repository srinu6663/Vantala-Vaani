#!/usr/bin/env python3
"""
Test script for Recipe Collection App
Run this to verify that all dependencies are installed correctly.
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        'streamlit',
        'pandas',
        'googletrans',
        'requests'
    ]

    print("Testing module imports...")
    failed_imports = []

    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - FAILED: {e}")
            failed_imports.append(module)

    return failed_imports

def test_utilities():
    """Test utility functions"""
    print("\nTesting utility functions...")

    try:
        from utils import RecipeUtils
        recipe_utils = RecipeUtils()

        # Test language detection
        english_text = "This is English text"
        telugu_text = "ఇది తెలుగు వచనం"

        assert recipe_utils.detect_language(english_text) == 'english'
        assert recipe_utils.detect_language(telugu_text) == 'telugu'
        print("✅ Language detection - OK")

        # Test validation
        errors = recipe_utils.validate_recipe_input("Test Recipe", "Test ingredients", "Test steps")
        print("✅ Recipe validation - OK")

    except Exception as e:
        print(f"❌ Utility functions - FAILED: {e}")
        return False

    return True

def main():
    """Main test function"""
    print("Recipe Collection App - Dependency Test")
    print("=" * 50)

    # Test imports
    failed_imports = test_imports()

    if failed_imports:
        print(f"\n❌ Some modules failed to import: {failed_imports}")
        print("Please install missing dependencies using:")
        print("pip install -r requirements.txt")
        return False

    # Test utilities
    if not test_utilities():
        return False

    print("\n✅ All tests passed! The application should work correctly.")
    print("\nTo run the application:")
    print("streamlit run recipe_collection.py")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
