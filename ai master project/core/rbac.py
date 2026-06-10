"""
Role-Based Access Control (RBAC) System
Manages user roles and permissions for different dashboard features
"""

from enum import Enum
from typing import List, Dict, Set
from datetime import datetime
import json

class UserRole(str, Enum):
    """User roles in the system"""
    ADMIN = "admin"
    STAFF = "staff"
    VIEWER = "viewer"


class Permission(str, Enum):
    """System permissions"""
    # Dashboard
    VIEW_DASHBOARD = "view_dashboard"
    VIEW_METRICS = "view_metrics"
    VIEW_ANALYTICS = "view_analytics"
    VIEW_LOGS = "view_logs"
    
    # Executor
    EXECUTE_CODE = "execute_code"
    VIEW_EXECUTION = "view_execution"
    MANAGE_EXECUTION = "manage_execution"
    
    # Settings
    VIEW_SETTINGS = "view_settings"
    MANAGE_SETTINGS = "manage_settings"
    MANAGE_USERS = "manage_users"
    
    # System
    SYSTEM_ADMIN = "system_admin"


class RolePermissions:
    """Define permissions for each role"""
    
    PERMISSIONS = {
        UserRole.ADMIN: {
            Permission.VIEW_DASHBOARD,
            Permission.VIEW_METRICS,
            Permission.VIEW_ANALYTICS,
            Permission.VIEW_LOGS,
            Permission.EXECUTE_CODE,
            Permission.VIEW_EXECUTION,
            Permission.MANAGE_EXECUTION,
            Permission.VIEW_SETTINGS,
            Permission.MANAGE_SETTINGS,
            Permission.MANAGE_USERS,
            Permission.SYSTEM_ADMIN,
        },
        UserRole.STAFF: {
            Permission.VIEW_DASHBOARD,
            Permission.VIEW_METRICS,
            Permission.VIEW_ANALYTICS,
            Permission.VIEW_LOGS,
            Permission.EXECUTE_CODE,
            Permission.VIEW_EXECUTION,
            Permission.VIEW_SETTINGS,
        },
        UserRole.VIEWER: {
            Permission.VIEW_DASHBOARD,
            Permission.VIEW_METRICS,
            Permission.VIEW_ANALYTICS,
            Permission.VIEW_LOGS,
        },
    }


class User:
    """User model with role and permissions"""
    
    def __init__(self, username: str, role: UserRole, password_hash: str = None):
        self.username = username
        self.role = role
        self.password_hash = password_hash
        self.created_at = datetime.now()
        self.last_login = None
        self.is_active = True
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission"""
        return permission in RolePermissions.PERMISSIONS.get(self.role, set())
    
    def has_any_permission(self, permissions: List[Permission]) -> bool:
        """Check if user has any of the permissions"""
        user_perms = RolePermissions.PERMISSIONS.get(self.role, set())
        return any(perm in user_perms for perm in permissions)
    
    def has_all_permissions(self, permissions: List[Permission]) -> bool:
        """Check if user has all permissions"""
        user_perms = RolePermissions.PERMISSIONS.get(self.role, set())
        return all(perm in user_perms for perm in permissions)
    
    def to_dict(self):
        return {
            "username": self.username,
            "role": self.role.value,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active,
        }


class AuthManager:
    """Manage user authentication and authorization"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self._init_default_users()
    
    def _init_default_users(self):
        """Initialize default users for demo"""
        self.users["admin"] = User("admin", UserRole.ADMIN)
        self.users["staff"] = User("staff", UserRole.STAFF)
        self.users["viewer"] = User("viewer", UserRole.VIEWER)
    
    def get_user(self, username: str) -> User:
        """Get user by username"""
        return self.users.get(username)
    
    def create_user(self, username: str, role: UserRole) -> User:
        """Create new user"""
        if username in self.users:
            raise ValueError(f"User {username} already exists")
        user = User(username, role)
        self.users[username] = user
        return user
    
    def delete_user(self, username: str) -> bool:
        """Delete user"""
        if username in self.users:
            del self.users[username]
            return True
        return False
    
    def update_user_role(self, username: str, new_role: UserRole) -> bool:
        """Update user role"""
        user = self.get_user(username)
        if user:
            user.role = new_role
            return True
        return False
    
    def list_users(self) -> List[Dict]:
        """List all users"""
        return [user.to_dict() for user in self.users.values()]


# Global auth manager instance
auth_manager = AuthManager()
