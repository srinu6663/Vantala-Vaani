# PowerShell script to set up Windows Task Scheduler for daily token refresh
# Run this script as Administrator to create the scheduled task

$TaskName = "FoodVault-TokenRefresh"
$ScriptPath = "d:\Projects\back up\FoodVault\refresh_token.bat"
$LogPath = "d:\Projects\back up\FoodVault\token_refresh.log"

Write-Host "Setting up daily token refresh task..." -ForegroundColor Green

try {
    # Check if task already exists
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

    if ($ExistingTask) {
        Write-Host "Task already exists. Removing old task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Create a new scheduled task action
    $Action = New-ScheduledTaskAction -Execute $ScriptPath

    # Create a trigger for daily execution at 6:00 PM
    $Trigger = New-ScheduledTaskTrigger -Daily -At "18:00"

    # Create task settings
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    # Create the principal (run with highest privileges)
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

    # Register the scheduled task
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Daily refresh of access token for FoodVault app"

    Write-Host "✅ Successfully created scheduled task: $TaskName" -ForegroundColor Green
    Write-Host "📅 The task will run daily at 6:00 PM" -ForegroundColor Cyan
    Write-Host "📁 Logs will be saved to: $LogPath" -ForegroundColor Cyan

    # Test the task
    Write-Host "`nWould you like to test the task now? (y/n): " -ForegroundColor Yellow -NoNewline
    $TestResponse = Read-Host

    if ($TestResponse -eq "y" -or $TestResponse -eq "Y") {
        Write-Host "Running test..." -ForegroundColor Yellow
        Start-ScheduledTask -TaskName $TaskName
        Start-Sleep -Seconds 3

        if (Test-Path $LogPath) {
            Write-Host "`nLatest log entries:" -ForegroundColor Cyan
            Get-Content $LogPath -Tail 5
        }
    }

    Write-Host "`n✅ Setup completed successfully!" -ForegroundColor Green
    Write-Host "You can manage this task in Task Scheduler (taskschd.msc)" -ForegroundColor Gray

} catch {
    Write-Host "❌ Error setting up scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure you're running PowerShell as Administrator" -ForegroundColor Yellow
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
