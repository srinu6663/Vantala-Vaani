# 🚀 Deploying Vantala Vaani to Streamlit Cloud

## Prerequisites

1. **GitHub Account**: You need a GitHub account to host your code
2. **Streamlit Cloud Account**: Sign up at https://share.streamlit.io/
3. **Swecha CorpusApp API Token**: Your authentication token

## Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository
```bash
# In your project directory (d:\Projects\Food\)
git init
git add .
git commit -m "Initial commit: Vantala Vaani food recipe uploader"
```

### 1.2 Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository named `vantala-vaani` (or your preferred name)
3. Make it **Public** (required for free Streamlit Cloud)
4. Don't initialize with README (you already have files)

### 1.3 Push to GitHub
```bash
# Replace USERNAME with your GitHub username
git remote add origin https://github.com/USERNAME/vantala-vaani.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

### 2.1 Connect to Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click "New app"

### 2.2 Configure Your App
- **Repository**: Select your `vantala-vaani` repository
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL**: Choose a custom URL (e.g., `your-username-vantala-vaani`)

### 2.3 Add Secrets
Before deploying, click "Advanced settings" → "Secrets" and add:

```toml
# Copy your secrets here
CORPUSAPP_BASE_URL = "https://api.corpus.swecha.org/api/v1"
CORPUSAPP_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTQ4MzY3NDAsInN1YiI6ImJkNTkxYzVmLTYyZmMtNGJjNS1hMjhmLWFmMjA0MjliY2ZhZiJ9.-sjqDDo1g29UQWqrWnfE1USB9SQYonjAk20onHBtNiM"
CATEGORY_ID_FOOD = "833299f6-ff1c-4fde-804f-6d3b3877c76e"
ALLOWED_AUDIO_TYPES = "mp3,wav,m4a,aac,ogg,flac"
MAX_UPLOAD_MB = "50"
```

**⚠️ Important**: Replace `CORPUSAPP_TOKEN` with your actual token from the `.env` file.

### 2.4 Deploy
Click "Deploy!" and wait for the app to build and start.

## Step 3: Verify Deployment

Your app will be available at: `https://your-app-name.streamlit.app/`

Test the following:
- ✅ App loads without errors
- ✅ Environment variables are loaded
- ✅ Text recipe submission works
- ✅ Audio file upload works

## 🔧 Troubleshooting

### Common Issues:

1. **ModuleNotFoundError**
   - Check that all dependencies are in `requirements.txt`
   - Ensure no relative imports are broken

2. **Configuration Errors**
   - Verify all secrets are added correctly in Streamlit Cloud
   - Check secret names match exactly (case-sensitive)

3. **API Errors**
   - Verify your CorpusApp token is still valid
   - Check if your token has expired

### Checking Logs:
- Click "Manage app" in Streamlit Cloud
- View the logs to see any error messages

## 🔄 Updating Your App

To update your deployed app:

```bash
# Make your changes
git add .
git commit -m "Update: description of changes"
git push
```

Streamlit Cloud will automatically redeploy when you push to the main branch.

## 🔐 Security Notes

- ✅ Secrets are encrypted in Streamlit Cloud
- ✅ Your `.env` file is ignored by git (in `.gitignore`)
- ✅ Never commit API tokens to your repository
- ✅ Use the `secrets.toml.example` file for sharing configuration templates

## 📱 Sharing Your App

Once deployed, share your app URL with users:
- `https://your-app-name.streamlit.app/`

Users can submit food recipes directly through the web interface without needing any technical setup!

---

## 🎉 Congratulations!

Your Vantala Vaani food recipe uploader is now live on the internet and ready to collect food recipes for the Swecha CorpusApp! 🍽️🌐
