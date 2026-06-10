# 🚀 AI Master Project - Advanced Admin Dashboard

Sistem monitoring, analytics, dan code execution dengan admin dashboard yang comprehensive dengan role-based access control.

## ✨ Fitur Utama

### 📊 Dashboard Admin
- **Real-time System Monitoring**: CPU, RAM, Disk usage tracking
- **Process Monitor**: Top 10 processes by resource usage
- **Performance Charts**: Interactive Plotly visualizations
- **System Uptime & Info**: Detailed system information

### 💻 Python Code Executor
- **Safe Code Execution**: Sandboxed execution dengan timeout & resource limits
- **Code Analysis**: Deteksi dangerous keywords & patterns
- **Execution History**: Track semua code execution dengan analytics
- **Resource Management**: Max timeout: 5 menit, Max memory: 2GB

### 📈 Analytics & Logging
- **Execution Statistics**: Success rate, avg execution time
- **User Activity Tracking**: Monitor activity per user
- **Module Statistics**: Performance stats per module
- **System Logging**: DEBUG, INFO, WARNING, ERROR levels

### ⏰ World Clock
- **Multiple Timezones**: 14+ timezones support
- **Real-time Updates**: Automatic timezone conversion
- **Timezone Customization**: Select preferred timezones
- **Time Difference Calculator**: Calculate timezone differences

### 👥 Role-Based Access Control (RBAC)
3 built-in roles dengan different permissions:
- **Admin**: Full access ke semua fitur
- **Staff**: Access ke dashboard, executor, analytics
- **Viewer**: Read-only access ke dashboard & analytics

### ⚙️ Advanced Settings
- **Resource Limits**: Customize CPU/Memory thresholds
- **Execution Settings**: Timeout & memory limits
- **User Management**: Create/delete users & manage roles

## 📦 Instalasi

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone Repository**
```bash
git clone https://github.com/FachriAditya2010/ai-project.git
cd "ai-project/ai master project"
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run Dashboard**
```bash
streamlit run dashboard.py
```

Dashboard akan tersedia di `http://localhost:8501`

## 🔐 Default Credentials

| Username | Password | Role   |
|----------|----------|--------|
| admin    | admin    | Admin  |
| staff    | admin    | Staff  |
| viewer   | admin    | Viewer |

## 📁 Project Structure

```
ai master project/
├── dashboard.py              # Main Streamlit dashboard
├── requirements.txt          # Python dependencies
├── core/
│   ├── rbac.py              # Role-Based Access Control
│   ├── monitoring.py        # System monitoring & resource limits
│   ├── executor.py          # Safe Python code executor
│   ├── analytics.py         # Logging & analytics
│   └── clock.py             # World clock with timezones
├── agent/                    # Original AI agent modules
│   ├── core.py
│   ├── llm.py
│   ├── tools.py
│   └── sandbox.py
└── workspace/               # Working directory
```

## 🎯 Usage Examples

### 1. Monitor System Resources
- Buka Dashboard tab untuk melihat real-time system metrics
- Charts otomatis update setiap beberapa detik

### 2. Execute Python Code
- Go to "Code Executor" page
- Input Python code
- Click "Analyze Code" untuk security check
- Click "Execute Code" untuk run

### 3. Check Analytics
- View execution statistics & trends
- Monitor user activity
- Track module performance

### 4. View World Clock
- Select preferred timezones
- See real-time time di berbagai timezone
- Calculate time differences antar timezone

### 5. Manage Users (Admin Only)
- Add new users dengan specific roles
- Assign different permission levels
- Remove users jika diperlukan

## 🔧 Resource Limits

Default resource limits untuk code execution:
- **Max CPU**: 80%
- **Max Memory**: 85%
- **Max Execution Time**: 5 minutes
- **Max Memory per Process**: 2GB

Dapat di-customize melalui Settings page.

## 📊 Core Modules

### rbac.py
```python
from core.rbac import auth_manager, UserRole, Permission

# Get user
user = auth_manager.get_user("admin")

# Check permission
if user.has_permission(Permission.EXECUTE_CODE):
    # User can execute code
```

### monitoring.py
```python
from core.monitoring import system_monitor

# Get metrics
metrics = system_monitor.get_system_metrics()
print(f"CPU: {metrics.cpu_percent}%")

# Get top processes
processes = system_monitor.get_top_processes(10)
```

### executor.py
```python
from core.executor import python_executor

# Execute code
result = python_executor.execute_code("print('Hello')")
print(result.output)

# Analyze code
analysis = CodeAnalyzer.analyze(code)
print(f"Safe: {analysis['safe']}")
```

### analytics.py
```python
from core.analytics import analytics, logger

# Log
logger.info("module", "Message", user="admin")

# Record execution
analytics.record_execution("admin", True, 0.5)

# Get stats
stats = analytics.get_statistics()
```

### clock.py
```python
from core.clock import world_clock

# Get time in timezone
time_data = world_clock.get_time_in_timezone("WIB")
print(f"Current time: {time_data['time']}")

# Get time difference
diff = world_clock.get_time_difference("WIB", "EST")
```

## 🚀 Deployment

### Local Development
```bash
streamlit run dashboard.py
```

### Production (Heroku)
1. Create `Procfile`:
```
web: streamlit run dashboard.py --logger.level=error
```

2. Deploy:
```bash
git push heroku main
```

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "dashboard.py"]
```

## 📋 Checklist Fitur

- [x] Admin Dashboard dengan real-time monitoring
- [x] System metrics visualization
- [x] Python code executor dengan safety checks
- [x] Code analysis & dangerous keyword detection
- [x] Analytics & execution statistics
- [x] System logging (DEBUG, INFO, WARNING, ERROR)
- [x] World clock dengan multiple timezones
- [x] Role-Based Access Control (3 roles)
- [x] User management
- [x] Resource limits configuration
- [x] Process monitoring
- [x] Execution history tracking

## 🔐 Security Features

- ✅ Sandboxed code execution
- ✅ Timeout protection (5 min max)
- ✅ Memory limits (2GB max)
- ✅ Dangerous keyword detection
- ✅ Role-based permissions
- ✅ User authentication
- ✅ Activity logging
- ✅ Resource monitoring

## 🐛 Troubleshooting

### Dashboard tidak muncul
```bash
streamlit run dashboard.py --logger.level=error
```

### Import error
```bash
pip install --upgrade -r requirements.txt
```

### Memory issues
Reduce metrics history size di monitoring.py atau adjust resource limits

## 📝 License

MIT License

## 👨‍💻 Author

**FachriAditya2010** - AI & Full-stack Developer

## 🤝 Contributing

Contributions welcome! Please create issue atau PR.

---

**Made with ❤️ using Python, Streamlit, and Plotly**
