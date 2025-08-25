# FoodVault Token Auto-Refresh Setup

## 🔄 Automated Access Token Refresh

Your FoodVault app now has an automated token refresh system that will generate a new access token daily and update your `.env` file automatically.

## 📁 Files Created

1. **`refresh_token.py`** - Main Python script that fetches new tokens
2. **`refresh_token.bat`** - Windows batch script to run the Python script
3. **`setup_scheduler.ps1`** - PowerShell script for automated scheduling

## ✅ What's Already Working

- ✅ Token refresh script is working perfectly
- ✅ Your `.env` file is being updated automatically
- ✅ Backup files are created before each update
- ✅ Comprehensive logging is enabled

## 🕐 Setting Up Daily Automation

### Option 1: Windows Task Scheduler (Recommended)

1. **Open Task Scheduler as Administrator:**

   - Press `Win + R`, type `taskschd.msc`, press Enter
   - Right-click and select "Run as administrator"

2. **Create New Task:**

   - Click "Create Basic Task..." in the right panel
   - Name: `FoodVault Token Refresh`
   - Description: `Daily refresh of access token for FoodVault app`

3. **Set Trigger:**

   - When: `Daily`
   - Start date: Today
   - Time: `6:00 PM` (or any time you prefer)
   - Recur every: `1 days`

4. **Set Action:**

   - Action: `Start a program`
   - Program/script: `d:\Projects\back up\FoodVault\refresh_token.bat`
   - Start in: `d:\Projects\back up\FoodVault`

5. **Finish and Test:**
   - Check "Open the Properties dialog" before clicking Finish
   - In Properties, go to "General" tab and check "Run with highest privileges"
   - Click OK to save

### Option 2: Manual Daily Execution

Simply run this command daily:

```batch
cd "d:\Projects\back up\FoodVault"
refresh_token.bat
```

### Option 3: Quick PowerShell Setup (Run as Administrator)

```powershell
# Open PowerShell as Administrator and run:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& "d:\Projects\back up\FoodVault\setup_scheduler.ps1"
```

## 📊 Monitoring

- **Log File:** `token_refresh.log` - Contains execution history
- **Backup Files:** `.env.backup` - Created before each update
- **Manual Test:** Run `refresh_token.bat` to test manually

## 🔧 Configuration

The script uses these credentials (stored in `refresh_token.py`):

- Phone: `+916305877795`
- Password: `Srinu@2006`
- API URL: `https://api.corpus.swecha.org/api/v1/auth/login`

## 🛠 Troubleshooting

### If the token refresh fails:

1. Check your internet connection
2. Verify the API is accessible
3. Check the log file for error details
4. Manually run `refresh_token.py` to see detailed output

### If credentials change:

Edit `refresh_token.py` and update the `PHONE` and `PASSWORD` variables.

## 📝 Usage Example

```bash
# Manual token refresh
cd "d:\Projects\back up\FoodVault"
python refresh_token.py

# Check the logs
type token_refresh.log

# Verify new token in .env
type .env
```

## 🎯 Next Steps

1. **Set up the Task Scheduler** (recommended) or choose your preferred automation method
2. **Test the automation** by running the task manually
3. **Monitor the logs** to ensure everything works correctly
4. **Your app will now have fresh tokens daily** - no more authentication errors!

---

**Note:** The token refresh script is designed to be robust and will try multiple authentication formats to ensure compatibility with the API.
