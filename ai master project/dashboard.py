"""
Main Dashboard Application
Streamlit-based admin dashboard with monitoring, analytics, and code execution
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from core.rbac import auth_manager, UserRole, Permission
from core.monitoring import system_monitor
from core.executor import python_executor, CodeAnalyzer
from core.analytics import logger, analytics
from core.clock import world_clock

# Page configuration
st.set_page_config(
    page_title="AI Admin Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .status-good { color: #00d084; font-weight: bold; }
    .status-warning { color: #ffa500; font-weight: bold; }
    .status-danger { color: #ff4444; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)


def init_session():
    """Initialize session state"""
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False


def login_page():
    """Login page"""
    st.title("🔐 AI Master Dashboard - Login")
    
    with st.form("login_form"):
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="admin")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = auth_manager.get_user(username)
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = user
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    st.info("Demo users: admin, staff, viewer (all with password: admin)")


def dashboard_page():
    """Main dashboard"""
    user = st.session_state.current_user
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 Navigation")
        page = st.radio("Select Page", [
            "📊 Dashboard",
            "⏰ World Clock",
            "💻 Code Executor",
            "📈 Analytics",
            "🔍 System Logs",
            "👥 User Management" if user.has_permission(Permission.MANAGE_USERS) else None,
            "⚙️ Settings" if user.has_permission(Permission.MANAGE_SETTINGS) else None,
        ])
        page = [p for p in [page] if p is not None][0]
        
        st.divider()
        st.write(f"**User:** {user.username}")
        st.write(f"**Role:** {user.role.value.upper()}")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    # Main content
    if page == "📊 Dashboard":
        dashboard_home()
    elif page == "⏰ World Clock":
        world_clock_page()
    elif page == "💻 Code Executor":
        code_executor_page(user)
    elif page == "📈 Analytics":
        analytics_page()
    elif page == "🔍 System Logs":
        logs_page()
    elif page == "👥 User Management":
        user_management_page()
    elif page == "⚙️ Settings":
        settings_page()


def dashboard_home():
    """Home dashboard page"""
    st.title("📊 Admin Dashboard")
    
    # Get metrics
    metrics = system_monitor.get_system_metrics()
    resource_check = system_monitor.check_resource_limits()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "CPU Usage",
            f"{metrics.cpu_percent:.1f}%",
            delta="⚠️" if resource_check["cpu_exceeded"] else "✅",
            delta_color="inverse" if resource_check["cpu_exceeded"] else "off"
        )
    
    with col2:
        st.metric(
            "Memory Usage",
            f"{metrics.memory_percent:.1f}%",
            delta="⚠️" if resource_check["memory_exceeded"] else "✅",
            delta_color="inverse" if resource_check["memory_exceeded"] else "off"
        )
    
    with col3:
        st.metric(
            "Disk Usage",
            f"{metrics.disk_percent:.1f}%",
            delta=f"{metrics.disk_free_gb:.1f}GB free"
        )
    
    with col4:
        st.metric(
            "Active Processes",
            metrics.process_count,
            delta="processes"
        )
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 System Metrics History")
        history = system_monitor.get_metrics_history()
        if history:
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['cpu_percent'],
                mode='lines',
                name='CPU %',
                line=dict(color='#667eea', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['memory_percent'],
                mode='lines',
                name='Memory %',
                line=dict(color='#764ba2', width=2)
            ))
            fig.update_layout(height=300, hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔥 Top Processes")
        top_procs = system_monitor.get_top_processes(5)
        if top_procs:
            proc_data = []
            for p in top_procs:
                proc_data.append({
                    "Process": p.name,
                    "CPU %": f"{p.cpu_percent:.1f}",
                    "Memory MB": f"{p.memory_mb:.1f}",
                })
            st.dataframe(pd.DataFrame(proc_data), use_container_width=True)


def world_clock_page():
    """World clock page"""
    st.title("⏰ World Clock")
    
    # Clock display
    col1, col2, col3 = st.columns(3)
    
    times = world_clock.get_selected_times()
    
    for idx, time_data in enumerate(times):
        if idx % 3 == 0:
            container = col1
        elif idx % 3 == 1:
            container = col2
        else:
            container = col3
        
        with container:
            st.markdown(f"### 🕐 {time_data['timezone']}")
            st.markdown(f"**Time:** `{time_data['time']}`")
            st.markdown(f"**Date:** {time_data['date']}")
            st.markdown(f"**Day:** {time_data['day_name']}")
            st.markdown(f"**Offset:** {time_data['offset']}")
    
    st.divider()
    
    # Timezone customization
    st.subheader("⚙️ Customize Timezones")
    available = world_clock.get_available_timezones()
    
    selected = st.multiselect(
        "Select timezones to display:",
        list(available.keys()),
        default=world_clock.selected_timezones
    )
    
    if st.button("Update Timezones"):
        world_clock.set_selected_timezones(selected)
        st.success("Timezones updated!")
        st.rerun()


def code_executor_page(user):
    """Code executor page"""
    if not user.has_permission(Permission.EXECUTE_CODE):
        st.error("❌ You don't have permission to execute code")
        return
    
    st.title("💻 Python Code Executor")
    
    # Resource check
    resource_check = system_monitor.check_resource_limits()
    if not resource_check["can_execute"]:
        st.warning("⚠️ System resources are at limit. Code execution might be slow.")
    
    # Code editor
    code = st.text_area(
        "Enter Python code:",
        height=300,
        placeholder="# Write your Python code here\nprint('Hello World')"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        execute_btn = st.button("▶️ Execute Code", use_container_width=True)
    
    with col2:
        analyze_btn = st.button("🔍 Analyze Code", use_container_width=True)
    
    if analyze_btn and code:
        st.subheader("Code Analysis")
        analysis = CodeAnalyzer.analyze(code)
        
        if analysis["safe"]:
            st.success("✅ Code appears safe to execute")
        else:
            st.error(f"❌ Found {len(analysis['issues'])} issues")
            for issue in analysis["issues"]:
                st.warning(f"Line {issue['line']}: {issue['message']}")
        
        if analysis["warnings"]:
            for warning in analysis["warnings"]:
                st.info(f"Line {warning['line']}: {warning['message']}")
    
    if execute_btn and code:
        st.subheader("Execution Result")
        
        with st.spinner("Executing code..."):
            result = python_executor.execute_code(code)
            analytics.record_execution(user.username, result.success, result.execution_time)
        
        if result.success:
            st.success("✅ Execution successful")
            if result.output:
                st.code(result.output, language="text")
        else:
            st.error("❌ Execution failed")
            if result.error:
                st.code(result.error, language="text")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Execution Time", f"{result.execution_time:.3f}s")
        with col2:
            st.metric("Status", "Success" if result.success else "Failed")
        with col3:
            st.metric("Timestamp", result.timestamp)


def analytics_page():
    """Analytics page"""
    st.title("📈 Analytics & Statistics")
    
    stats = analytics.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Executions", stats["total_executions"])
    with col2:
        st.metric("Successful", stats["successful_executions"])
    with col3:
        st.metric("Failed", stats["failed_executions"])
    with col4:
        st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("User Activity")
        if stats["user_activity"]:
            user_df = pd.DataFrame([
                {"User": k, "Executions": v}
                for k, v in stats["user_activity"].items()
            ])
            fig = px.bar(user_df, x="User", y="Executions")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Module Statistics")
        if stats["module_stats"]:
            module_df = pd.DataFrame([
                {"Module": k, "Count": v["count"], "Success": v["success"]}
                for k, v in stats["module_stats"].items()
            ])
            fig = px.bar(module_df, x="Module", y=["Count", "Success"], barmode="group")
            st.plotly_chart(fig, use_container_width=True)


def logs_page():
    """System logs page"""
    st.title("🔍 System Logs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        level_filter = st.selectbox("Filter by level:", ["ALL", "DEBUG", "INFO", "WARNING", "ERROR"])
    with col2:
        limit = st.slider("Number of logs:", 10, 100, 50)
    
    if level_filter == "ALL":
        logs_data = logger.get_logs(limit=limit)
    else:
        logs_data = logger.get_logs(level=level_filter, limit=limit)
    
    if logs_data:
        logs_df = pd.DataFrame(logs_data)
        st.dataframe(logs_df, use_container_width=True)
    else:
        st.info("No logs found")


def user_management_page():
    """User management page"""
    st.title("👥 User Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Users")
        users = auth_manager.list_users()
        if users:
            st.dataframe(pd.DataFrame(users), use_container_width=True)
    
    with col2:
        st.subheader("Add User")
        new_username = st.text_input("Username")
        new_role = st.selectbox("Role", [r.value for r in UserRole])
        
        if st.button("Create User"):
            try:
                auth_manager.create_user(new_username, UserRole(new_role))
                st.success(f"User {new_username} created!")
                st.rerun()
            except ValueError as e:
                st.error(str(e))


def settings_page():
    """Settings page"""
    st.title("⚙️ Settings")
    
    st.subheader("Resource Limits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_cpu = st.slider(
            "Max CPU %:",
            0.0,
            100.0,
            system_monitor.MAX_CPU_PERCENT,
            1.0
        )
        system_monitor.MAX_CPU_PERCENT = max_cpu
    
    with col2:
        max_mem = st.slider(
            "Max Memory %:",
            0.0,
            100.0,
            system_monitor.MAX_MEMORY_PERCENT,
            1.0
        )
        system_monitor.MAX_MEMORY_PERCENT = max_mem
    
    st.subheader("Execution Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_timeout = st.slider(
            "Max Timeout (seconds):",
            10,
            600,
            python_executor.max_timeout,
            10
        )
        python_executor.max_timeout = max_timeout
    
    with col2:
        max_memory = st.slider(
            "Max Memory (MB):",
            256,
            4096,
            python_executor.max_memory_mb,
            256
        )
        python_executor.max_memory_mb = max_memory
    
    if st.button("Save Settings"):
        st.success("✅ Settings saved!")


def main():
    """Main application"""
    init_session()
    
    if not st.session_state.authenticated:
        login_page()
    else:
        dashboard_page()


if __name__ == "__main__":
    main()
