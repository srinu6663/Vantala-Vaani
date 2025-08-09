#!/usr/bin/env python3
"""
Quick deployment helper for Vantala Vaani
"""

import subprocess
import sys

def run_command(cmd, description):
    """Run a command and print results"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 Vantala Vaani Deployment Helper")
    print("=" * 40)

    # Check git status
    print("\n📋 Current Project Status:")
    run_command("git status --porcelain", "Checking git status")

    # Show remote if exists
    run_command("git remote -v", "Checking git remotes")

    print("\n📝 Next Steps for Streamlit Cloud Deployment:")
    print("1. Create a GitHub repository:")
    print("   - Go to https://github.com/new")
    print("   - Name: vantala-vaani")
    print("   - Make it PUBLIC")
    print("   - Don't initialize with README")

    print("\n2. Add GitHub remote (replace USERNAME):")
    print("   git remote add origin https://github.com/USERNAME/vantala-vaani.git")

    print("\n3. Push to GitHub:")
    print("   git push -u origin main")

    print("\n4. Deploy to Streamlit Cloud:")
    print("   - Go to https://share.streamlit.io/")
    print("   - Sign in with GitHub")
    print("   - Click 'New app'")
    print("   - Select your repository")
    print("   - Main file: app.py")

    print("\n5. Add these secrets in Streamlit Cloud:")
    print("   CORPUSAPP_BASE_URL = \"https://api.corpus.swecha.org/api/v1\"")
    print("   CORPUSAPP_TOKEN = \"your_token_from_env_file\"")
    print("   CATEGORY_ID_FOOD = \"833299f6-ff1c-4fde-804f-6d3b3877c76e\"")
    print("   ALLOWED_AUDIO_TYPES = \"mp3,wav,m4a,aac,ogg,flac\"")
    print("   MAX_UPLOAD_MB = \"50\"")

    print("\n🎉 Your app will be live at: https://your-app-name.streamlit.app/")

if __name__ == "__main__":
    main()
