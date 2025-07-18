"""Rate limiting for Claude Code API calls."""

import time
from pathlib import Path
from typing import Dict, Optional
import json
from datetime import datetime, timedelta


class RateLimiter:
    """Simple rate limiter for Claude Code API calls."""
    
    def __init__(self, cache_file: Optional[Path] = None):
        self.cache_file = cache_file or Path.home() / ".ai-code-pattern-discovery" / "rate_limit.json"
        self.cache_file.parent.mkdir(exist_ok=True)
        
        # Default limits (can be adjusted based on Claude subscription)
        self.limits = {
            "requests_per_minute": 10,
            "requests_per_hour": 100,
            "requests_per_day": 500
        }
        
        self.usage = self._load_usage()
    
    def _load_usage(self) -> Dict:
        """Load usage data from cache file."""
        if not self.cache_file.exists():
            return {"requests": []}
        
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except:
            return {"requests": []}
    
    def _save_usage(self):
        """Save usage data to cache file."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.usage, f)
        except:
            pass  # Fail silently if can't save
    
    def _clean_old_requests(self):
        """Remove requests older than 24 hours."""
        now = datetime.now()
        cutoff = now - timedelta(hours=24)
        
        self.usage["requests"] = [
            req for req in self.usage["requests"]
            if datetime.fromisoformat(req["timestamp"]) > cutoff
        ]
    
    def check_rate_limit(self) -> tuple[bool, str]:
        """Check if request can be made within rate limits."""
        self._clean_old_requests()
        
        now = datetime.now()
        requests = self.usage["requests"]
        
        # Count requests in different time windows
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        minute_count = sum(1 for req in requests if datetime.fromisoformat(req["timestamp"]) > minute_ago)
        hour_count = sum(1 for req in requests if datetime.fromisoformat(req["timestamp"]) > hour_ago)
        day_count = sum(1 for req in requests if datetime.fromisoformat(req["timestamp"]) > day_ago)
        
        # Check limits
        if minute_count >= self.limits["requests_per_minute"]:
            return False, f"Rate limit exceeded: {minute_count}/{self.limits['requests_per_minute']} requests per minute"
        
        if hour_count >= self.limits["requests_per_hour"]:
            return False, f"Rate limit exceeded: {hour_count}/{self.limits['requests_per_hour']} requests per hour"
        
        if day_count >= self.limits["requests_per_day"]:
            return False, f"Rate limit exceeded: {day_count}/{self.limits['requests_per_day']} requests per day"
        
        return True, "OK"
    
    def record_request(self, request_type: str = "pattern_analysis"):
        """Record a new request."""
        self.usage["requests"].append({
            "timestamp": datetime.now().isoformat(),
            "type": request_type
        })
        self._save_usage()
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics."""
        self._clean_old_requests()
        
        now = datetime.now()
        requests = self.usage["requests"]
        
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        minute_count = sum(1 for req in requests if datetime.fromisoformat(req["timestamp"]) > minute_ago)
        hour_count = sum(1 for req in requests if datetime.fromisoformat(req["timestamp"]) > hour_ago)
        day_count = sum(1 for req in requests if datetime.fromisoformat(req["timestamp"]) > day_ago)
        
        return {
            "minute": {"used": minute_count, "limit": self.limits["requests_per_minute"]},
            "hour": {"used": hour_count, "limit": self.limits["requests_per_hour"]},
            "day": {"used": day_count, "limit": self.limits["requests_per_day"]},
            "total_requests": len(requests)
        }
    
    def time_until_reset(self) -> Dict:
        """Get time until rate limits reset."""
        now = datetime.now()
        
        # Find the oldest request in each time window
        requests = self.usage["requests"]
        
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        minute_requests = [req for req in requests if datetime.fromisoformat(req["timestamp"]) > minute_ago]
        hour_requests = [req for req in requests if datetime.fromisoformat(req["timestamp"]) > hour_ago]
        day_requests = [req for req in requests if datetime.fromisoformat(req["timestamp"]) > day_ago]
        
        reset_times = {}
        
        if len(minute_requests) >= self.limits["requests_per_minute"]:
            oldest = min(minute_requests, key=lambda x: x["timestamp"])
            reset_time = datetime.fromisoformat(oldest["timestamp"]) + timedelta(minutes=1)
            reset_times["minute"] = max(0, (reset_time - now).total_seconds())
        
        if len(hour_requests) >= self.limits["requests_per_hour"]:
            oldest = min(hour_requests, key=lambda x: x["timestamp"])
            reset_time = datetime.fromisoformat(oldest["timestamp"]) + timedelta(hours=1)
            reset_times["hour"] = max(0, (reset_time - now).total_seconds())
        
        if len(day_requests) >= self.limits["requests_per_day"]:
            oldest = min(day_requests, key=lambda x: x["timestamp"])
            reset_time = datetime.fromisoformat(oldest["timestamp"]) + timedelta(days=1)
            reset_times["day"] = max(0, (reset_time - now).total_seconds())
        
        return reset_times