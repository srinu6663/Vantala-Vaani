# 🚀 FoodVault - Streamlit Cloud Deployment Guide

## 📋 Pre-Deployment Checklist

✅ **Project Structure Ready**

- Main app: `app.py`
- Dependencies: `requirements.txt`
- Configuration: `.streamlit/config.toml`
- Environment template: `.env.example`

✅ **Dependencies Included**

- `streamlit>=1.48.1`
- `python-dotenv>=1.1.1`
- `requests>=2.32.5`

## 🌐 Deploy to Streamlit Cloud

### Step 1: Prepare Your Repository

1. **Push to GitHub:**

   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Ensure your repository contains:**
   - ✅ `app.py` (main application file)
   - ✅ `requirements.txt` (dependencies)
   - ✅ `.streamlit/config.toml` (Streamlit configuration)
   - ✅ All service and utility files

### Step 2: Deploy on Streamlit Cloud

1. **Visit Streamlit Cloud:**

   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App:**

   - Click "New app"
   - Select your GitHub repository
   - Choose branch: `main`
   - Main file path: `app.py`
   - App URL: Choose a custom name (e.g., `foodvault-recipes`)

3. **Configure Environment Variables:**
   Click "Advanced settings" and add these secrets:

   ```
   ACCESS_TOKEN = "your_current_access_token_here"
   API_BASE = "https://api.corpus.swecha.org"
   CATEGORY_ID = "833299f6-ff1c-4fde-804f-6d3b3877c76e"
   USER_ID = "bd591c5f-62fc-4bc5-a28f-af20429bcfaf"
   DEVELOPMENT_MODE = "false"
   MAX_AUDIO_SIZE_MB = "50"
   MAX_VIDEO_SIZE_MB = "100"
   ```

4. **Deploy:**
   - Click "Deploy!"
   - Wait for the deployment to complete (usually 2-3 minutes)

### Step 3: Update Environment Variables

Since your tokens expire, you'll need to update them regularly:

1. **Go to your Streamlit Cloud dashboard**
2. **Click on your app → Settings → Secrets**
3. **Update the `ACCESS_TOKEN` value with a fresh token**
4. **Save changes** (app will automatically restart)

## 🔄 Token Management for Production

### Option 1: Manual Updates (Recommended for Streamlit Cloud)

1. **Get fresh token locally:**

   ```bash
   python refresh_token.py
   ```

2. **Copy the new token from your `.env` file**

3. **Update Streamlit Cloud secrets:**
   - Dashboard → Your App → Settings → Secrets
   - Update `ACCESS_TOKEN` value
   - Save (app restarts automatically)

### Option 2: Automated Token Refresh (Advanced)

For production environments, you could:

- Set up a webhook to trigger token refresh
- Use a scheduled job to update Streamlit secrets via API
- Implement token refresh within the app itself

## 🌟 Your App URLs

After deployment, your app will be available at:

- **Public URL:** `https://your-app-name.streamlit.app`
- **Custom domain:** (available with Streamlit for Teams)

## 🛠 Post-Deployment

### Monitor Your App:

- **Logs:** Available in Streamlit Cloud dashboard
- **Usage:** Monitor resource usage and performance
- **Updates:** Push code changes to trigger automatic redeployment

### Update Your App:

```bash
# Make changes to your code
git add .
git commit -m "Update feature X"
git push origin main
# App automatically redeploys on Streamlit Cloud
```

## 🔧 Troubleshooting

### Common Issues:

1. **Authentication Errors:**

   - Check if `ACCESS_TOKEN` is set in Streamlit secrets
   - Verify token is not expired
   - Ensure token format is correct (no extra quotes)

2. **Module Import Errors:**

   - Verify all dependencies are in `requirements.txt`
   - Check file paths are relative to project root

3. **File Upload Issues:**
   - Streamlit Cloud has file size limits
   - Verify `MAX_AUDIO_SIZE_MB` and `MAX_VIDEO_SIZE_MB` settings

## 📞 Support

- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **Community:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **Status:** [status.streamlit.io](https://status.streamlit.io)

---

🎉 **Your FoodVault app is now ready for the world!**
