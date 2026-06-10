"""
System Monitoring Module
Real-time monitoring of CPU, RAM, disk, and process metrics
"""

import psutil
import time
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, asdict
import json


@dataclass
class SystemMetrics:
    """Container for system metrics"""
    timestamp: str
    cpu_percent: float
    cpu_count: int
    memory_percent: float
    memory_available_gb: float
    memory_used_gb: float
    disk_percent: float
    disk_free_gb: float
    process_count: int
    boot_time: str


@dataclass
class ProcessMetrics:
    """Container for process metrics"""
    pid: int
    name: str
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    status: str
    create_time: str


class SystemMonitor:
    """Monitor system resources and metrics"""
    
    # Resource limits for safe execution
    MAX_CPU_PERCENT = 80.0
    MAX_MEMORY_PERCENT = 85.0
    MAX_EXECUTION_TIME = 300  # 5 minutes
    MAX_MEMORY_MB = 2048  # 2GB
    
    def __init__(self, history_size: int = 100):
        self.history_size = history_size
        self.metrics_history: List[SystemMetrics] = []
        self.process_history: Dict[int, List[ProcessMetrics]] = {}
        self.start_time = datetime.now()
    
    def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        
        metrics = SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_percent=cpu_percent,
            cpu_count=cpu_count,
            memory_percent=memory.percent,
            memory_available_gb=memory.available / (1024**3),
            memory_used_gb=memory.used / (1024**3),
            disk_percent=disk.percent,
            disk_free_gb=disk.free / (1024**3),
            process_count=len(psutil.pids()),
            boot_time=boot_time.isoformat(),
        )
        
        # Keep history
        self.metrics_history.append(metrics)
        if len(self.metrics_history) > self.history_size:
            self.metrics_history.pop(0)
        
        return metrics
    
    def get_top_processes(self, limit: int = 10) -> List[ProcessMetrics]:
        """Get top processes by CPU and memory usage"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'memory_percent', 'status', 'create_time']):
                try:
                    info = proc.info
                    proc_metrics = ProcessMetrics(
                        pid=info['pid'],
                        name=info['name'],
                        cpu_percent=info['cpu_percent'] or 0.0,
                        memory_mb=info['memory_info'].rss / (1024**2) if info['memory_info'] else 0,
                        memory_percent=info['memory_percent'] or 0.0,
                        status=info['status'],
                        create_time=datetime.fromtimestamp(info['create_time']).isoformat(),
                    )
                    processes.append(proc_metrics)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error getting processes: {e}")
        
        # Sort by CPU usage first, then memory
        processes.sort(key=lambda x: (x.cpu_percent, x.memory_mb), reverse=True)
        return processes[:limit]
    
    def check_resource_limits(self) -> Dict[str, any]:
        """Check if system resources exceed limits"""
        metrics = self.get_system_metrics()
        
        return {
            "cpu_exceeded": metrics.cpu_percent > self.MAX_CPU_PERCENT,
            "memory_exceeded": metrics.memory_percent > self.MAX_MEMORY_PERCENT,
            "cpu_percent": metrics.cpu_percent,
            "memory_percent": metrics.memory_percent,
            "memory_available_mb": metrics.memory_available_gb * 1024,
            "can_execute": (metrics.cpu_percent <= self.MAX_CPU_PERCENT and 
                          metrics.memory_percent <= self.MAX_MEMORY_PERCENT),
        }
    
    def get_metrics_history(self) -> List[Dict]:
        """Get metrics history as dict"""
        return [asdict(m) for m in self.metrics_history]
    
    def get_uptime(self) -> Dict[str, any]:
        """Get system uptime information"""
        uptime = datetime.now() - self.start_time
        
        return {
            "monitor_uptime_seconds": uptime.total_seconds(),
            "monitor_uptime_readable": str(uptime),
            "start_time": self.start_time.isoformat(),
        }
    
    def get_system_info(self) -> Dict[str, any]:
        """Get detailed system information"""
        import platform
        
        return {
            "platform": platform.system(),
            "platform_version": platform.release(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "cpu_count_physical": psutil.cpu_count(logical=False),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "total_memory_gb": psutil.virtual_memory().total / (1024**3),
            "total_disk_gb": psutil.disk_usage('/').total / (1024**3),
        }


# Global monitor instance
system_monitor = SystemMonitor()
