"""
Analytics and Logging Module
Track execution logs, performance metrics, and user activities
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, asdict, field
import json
import sqlite3
from pathlib import Path


@dataclass
class LogEntry:
    """Single log entry"""
    timestamp: str
    level: str  # INFO, WARNING, ERROR, DEBUG
    module: str
    message: str
    user: str = None
    data: Dict = field(default_factory=dict)


class Logger:
    """Application logger"""
    
    LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
    }
    
    def __init__(self, min_level: str = "INFO"):
        self.min_level = min_level
        self.logs: List[LogEntry] = []
        self.max_logs = 1000
    
    def _log(self, level: str, module: str, message: str, user: str = None, data: Dict = None):
        """Internal logging method"""
        if self.LEVELS.get(level, 0) < self.LEVELS.get(self.min_level, 0):
            return
        
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level,
            module=module,
            message=message,
            user=user,
            data=data or {},
        )
        
        self.logs.append(entry)
        
        # Keep only recent logs
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
        
        # Print to console
        self._print_log(entry)
    
    def _print_log(self, entry: LogEntry):
        """Print log to console"""
        timestamp = entry.timestamp
        level = entry.level
        module = entry.module
        message = entry.message
        
        print(f"[{timestamp}] {level:8} | {module:20} | {message}")
    
    def debug(self, module: str, message: str, user: str = None, data: Dict = None):
        self._log("DEBUG", module, message, user, data)
    
    def info(self, module: str, message: str, user: str = None, data: Dict = None):
        self._log("INFO", module, message, user, data)
    
    def warning(self, module: str, message: str, user: str = None, data: Dict = None):
        self._log("WARNING", module, message, user, data)
    
    def error(self, module: str, message: str, user: str = None, data: Dict = None):
        self._log("ERROR", module, message, user, data)
    
    def get_logs(self, level: str = None, module: str = None, limit: int = 100) -> List[Dict]:
        """Get logs with optional filtering"""
        filtered_logs = self.logs
        
        if level:
            filtered_logs = [l for l in filtered_logs if l.level == level]
        
        if module:
            filtered_logs = [l for l in filtered_logs if l.module == module]
        
        # Return most recent first
        return [asdict(l) for l in filtered_logs[-limit:][::-1]]
    
    def get_logs_by_time(self, hours: int = 1) -> List[Dict]:
        """Get logs from last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        filtered = [
            l for l in self.logs
            if datetime.fromisoformat(l.timestamp) > cutoff
        ]
        return [asdict(l) for l in filtered[::-1]]


class AnalyticsTracker:
    """Track analytics and statistics"""
    
    def __init__(self):
        self.execution_count = 0
        self.successful_executions = 0
        self.failed_executions = 0
        self.total_execution_time = 0.0
        self.user_activity: Dict[str, int] = {}
        self.module_stats: Dict[str, Dict] = {}
        self.start_time = datetime.now()
    
    def record_execution(self, user: str, success: bool, execution_time: float, module: str = "unknown"):
        """Record code execution"""
        self.execution_count += 1
        
        if success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1
        
        self.total_execution_time += execution_time
        
        # Track user activity
        if user not in self.user_activity:
            self.user_activity[user] = 0
        self.user_activity[user] += 1
        
        # Track module stats
        if module not in self.module_stats:
            self.module_stats[module] = {
                "count": 0,
                "success": 0,
                "total_time": 0.0,
                "avg_time": 0.0,
            }
        
        stats = self.module_stats[module]
        stats["count"] += 1
        if success:
            stats["success"] += 1
        stats["total_time"] += execution_time
        stats["avg_time"] = stats["total_time"] / stats["count"]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get analytics statistics"""
        uptime = datetime.now() - self.start_time
        
        return {
            "uptime_seconds": uptime.total_seconds(),
            "total_executions": self.execution_count,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "success_rate": (
                self.successful_executions / self.execution_count * 100
                if self.execution_count > 0 else 0
            ),
            "total_execution_time": self.total_execution_time,
            "average_execution_time": (
                self.total_execution_time / self.execution_count
                if self.execution_count > 0 else 0
            ),
            "user_activity": self.user_activity,
            "module_stats": self.module_stats,
        }
    
    def get_user_stats(self, user: str) -> Dict[str, Any]:
        """Get stats for specific user"""
        user_executions = [
            l for l in logger.logs if l.user == user and "execution" in l.message.lower()
        ]
        
        return {
            "user": user,
            "total_executions": len(user_executions),
            "last_execution": user_executions[-1].timestamp if user_executions else None,
        }
    
    def reset_statistics(self):
        """Reset all statistics"""
        self.execution_count = 0
        self.successful_executions = 0
        self.failed_executions = 0
        self.total_execution_time = 0.0
        self.user_activity = {}
        self.module_stats = {}
        self.start_time = datetime.now()


# Global instances
logger = Logger()
analytics = AnalyticsTracker()
