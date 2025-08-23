import os
import json
from datetime import datetime
from typing import Optional

class Logger:
    def __init__(self):
        self.log_file = "submission_logs.json"
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Create log file if it doesn't exist"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)
    
    def log_submission(self, format_type: str, recipe_name: str, status: str, record_id: Optional[str]):
        """Log a recipe submission"""
        try:
            # Read existing logs
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            # Create new log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "format": format_type,
                "recipe_name": recipe_name,
                "status": status,
                "record_id": record_id
            }
            
            # Add to logs
            logs.append(log_entry)
            
            # Keep only last 100 entries to prevent file from growing too large
            if len(logs) > 100:
                logs = logs[-100:]
            
            # Write back to file
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            # If logging fails, don't crash the app
            print(f"Logging error: {e}")
    
    def get_recent_submissions_count(self, days: int = 7) -> int:
        """Get count of submissions in the last N days"""
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            if not logs:
                return 0
            
            # Calculate cutoff date
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Count recent successful submissions
            count = 0
            for log in logs:
                try:
                    log_date = datetime.fromisoformat(log["timestamp"])
                    if log_date >= cutoff_date and log["status"] == "Success":
                        count += 1
                except:
                    continue
            
            return count
            
        except Exception:
            return 0
    
    def get_submission_stats(self) -> dict:
        """Get basic statistics about submissions"""
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            if not logs:
                return {"total": 0, "successful": 0, "failed": 0}
            
            total = len(logs)
            successful = sum(1 for log in logs if log["status"] == "Success")
            failed = total - successful
            
            return {
                "total": total,
                "successful": successful,
                "failed": failed
            }
            
        except Exception:
            return {"total": 0, "successful": 0, "failed": 0}
