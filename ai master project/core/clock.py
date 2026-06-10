"""
Digital Clock Module
Display current time in different time zones with real-time updates
"""

from datetime import datetime, timezone
import pytz
from typing import Dict, List, Any


class WorldClock:
    """Display world clocks for multiple time zones"""
    
    # Common time zones
    COMMON_TIMEZONES = {
        "UTC": "UTC",
        "WIB": "Asia/Jakarta",  # Western Indonesia Time
        "WITA": "Asia/Makassar",  # Central Indonesia Time
        "WIT": "Asia/Jayapura",  # Eastern Indonesia Time
        "PST": "US/Pacific",
        "EST": "US/Eastern",
        "CST": "US/Central",
        "GMT": "Europe/London",
        "CET": "Europe/Paris",
        "IST": "Asia/Kolkata",
        "SGT": "Asia/Singapore",
        "HKT": "Asia/Hong_Kong",
        "JST": "Asia/Tokyo",
        "AEST": "Australia/Sydney",
    }
    
    def __init__(self):
        self.selected_timezones = ["UTC", "WIB", "EST", "GMT", "IST", "JST"]
    
    def get_time_in_timezone(self, tz_name: str) -> Dict[str, Any]:
        """Get current time in specific timezone"""
        try:
            if tz_name in self.COMMON_TIMEZONES:
                tz_str = self.COMMON_TIMEZONES[tz_name]
            else:
                tz_str = tz_name
            
            tz = pytz.timezone(tz_str)
            now = datetime.now(tz)
            
            return {
                "timezone": tz_name,
                "tz_full_name": tz_str,
                "time": now.strftime("%H:%M:%S"),
                "date": now.strftime("%Y-%m-%d"),
                "datetime": now.isoformat(),
                "offset": now.strftime("%z"),
                "day_name": now.strftime("%A"),
                "unix_timestamp": int(now.timestamp()),
            }
        except Exception as e:
            return {
                "error": str(e),
                "timezone": tz_name,
            }
    
    def get_all_world_times(self) -> List[Dict[str, Any]]:
        """Get current time in all major timezones"""
        times = []
        for tz_abbr in self.COMMON_TIMEZONES:
            times.append(self.get_time_in_timezone(tz_abbr))
        return times
    
    def get_selected_times(self) -> List[Dict[str, Any]]:
        """Get time in selected timezones"""
        times = []
        for tz in self.selected_timezones:
            times.append(self.get_time_in_timezone(tz))
        return times
    
    def set_selected_timezones(self, timezones: List[str]):
        """Set which timezones to display"""
        valid_tzs = []
        for tz in timezones:
            if tz in self.COMMON_TIMEZONES:
                valid_tzs.append(tz)
        
        if valid_tzs:
            self.selected_timezones = valid_tzs
            return True
        return False
    
    def add_timezone(self, tz_name: str):
        """Add timezone to selected list"""
        if tz_name not in self.selected_timezones:
            if tz_name in self.COMMON_TIMEZONES or self._is_valid_timezone(tz_name):
                self.selected_timezones.append(tz_name)
                return True
        return False
    
    def remove_timezone(self, tz_name: str):
        """Remove timezone from selected list"""
        if tz_name in self.selected_timezones:
            self.selected_timezones.remove(tz_name)
            return True
        return False
    
    def get_available_timezones(self) -> Dict[str, str]:
        """Get list of available timezones"""
        return self.COMMON_TIMEZONES.copy()
    
    def _is_valid_timezone(self, tz_name: str) -> bool:
        """Check if timezone string is valid"""
        try:
            pytz.timezone(tz_name)
            return True
        except:
            return False
    
    def get_time_difference(self, tz1: str, tz2: str) -> Dict[str, Any]:
        """Calculate time difference between two timezones"""
        try:
            time1 = self.get_time_in_timezone(tz1)
            time2 = self.get_time_in_timezone(tz2)
            
            if "error" in time1 or "error" in time2:
                return {"error": "Invalid timezone"}
            
            ts1 = time1["unix_timestamp"]
            ts2 = time2["unix_timestamp"]
            
            diff_hours = (ts2 - ts1) / 3600
            
            return {
                "tz1": tz1,
                "tz2": tz2,
                "time1": time1["time"],
                "time2": time2["time"],
                "difference_hours": diff_hours,
                "difference_readable": f"{int(diff_hours)} hours" if diff_hours != int(diff_hours) else f"{int(diff_hours)} hours",
            }
        except Exception as e:
            return {"error": str(e)}


# Global clock instance
world_clock = WorldClock()
