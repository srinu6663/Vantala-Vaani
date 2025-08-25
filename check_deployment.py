#!/usr/bin/env python3
"""
Deployment Preparation Script for FoodVault
Validates and prepares the project for Streamlit Cloud deployment
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a required file exists"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_requirements():
    """Check if requirements.txt contains necessary packages"""
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        print(f"❌ {req_file} not found")
        return False

    with open(req_file, 'r') as f:
        content = f.read().lower()

    required_packages = ['streamlit', 'python-dotenv', 'requests']
    missing_packages = []

    for package in required_packages:
        if package not in content:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages in requirements.txt: {', '.join(missing_packages)}")
        return False
    else:
        print("✅ All required packages found in requirements.txt")
        return True

def check_env_variables():
    """Check if environment variables are properly configured"""
    env_example = ".env.example"
    if not os.path.exists(env_example):
        print("❌ .env.example not found")
        return False

    with open(env_example, 'r') as f:
        content = f.read()

    required_vars = ['ACCESS_TOKEN', 'API_BASE', 'CATEGORY_ID', 'USER_ID']
    missing_vars = []

    for var in required_vars:
        if var not in content:
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing environment variables in .env.example: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ All required environment variables found in .env.example")
        return True

def main():
    """Main deployment check function"""
    print("🚀 FoodVault - Deployment Readiness Check")
    print("=" * 50)

    all_good = True

    # Check essential files
    essential_files = [
        ("app.py", "Main application file"),
        ("requirements.txt", "Python dependencies"),
        (".streamlit/config.toml", "Streamlit configuration"),
        (".env.example", "Environment variables template"),
        ("services/auth_service.py", "Authentication service"),
        ("services/record_service.py", "Record service"),
        ("utils/file_handler.py", "File handler utility"),
        ("utils/logger.py", "Logger utility"),
    ]

    print("\n📁 Checking Essential Files:")
    for file_path, description in essential_files:
        if not check_file_exists(file_path, description):
            all_good = False

    print("\n📦 Checking Dependencies:")
    if not check_requirements():
        all_good = False

    print("\n🔧 Checking Environment Configuration:")
    if not check_env_variables():
        all_good = False

    print("\n" + "=" * 50)

    if all_good:
        print("🎉 SUCCESS! Your project is ready for Streamlit Cloud deployment!")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Go to share.streamlit.io")
        print("3. Create a new app from your repository")
        print("4. Configure environment variables in Streamlit Cloud")
        print("5. Deploy!")
        print("\nSee DEPLOYMENT_GUIDE.md for detailed instructions.")
    else:
        print("❌ ISSUES FOUND! Please fix the above issues before deploying.")
        print("Check the missing files and requirements.")

    return 0 if all_good else 1

if __name__ == "__main__":
    exit(main())
