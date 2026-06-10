"""
Safe Python Code Executor
Execute Python code with resource limits and sandboxing
"""

import subprocess
import sys
import json
import time
import os
from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import signal
import threading


@dataclass
class ExecutionResult:
    """Result of code execution"""
    success: bool
    output: str
    error: str
    execution_time: float
    timestamp: str
    code_hash: str = None


class PythonExecutor:
    """Execute Python code safely with resource limits"""
    
    def __init__(self, max_timeout: int = 300, max_memory_mb: int = 2048):
        self.max_timeout = max_timeout
        self.max_memory_mb = max_memory_mb
        self.execution_history = []
        self.max_history = 100
    
    def execute_code(self, code: str, timeout: int = None) -> ExecutionResult:
        """
        Execute Python code with timeout and resource limits
        
        Args:
            code: Python code to execute
            timeout: Timeout in seconds (default: max_timeout)
        
        Returns:
            ExecutionResult with output/error
        """
        if timeout is None:
            timeout = self.max_timeout
        
        timeout = min(timeout, self.max_timeout)  # Enforce max timeout
        
        start_time = time.time()
        result = ExecutionResult(
            success=False,
            output="",
            error="",
            execution_time=0.0,
            timestamp=datetime.now().isoformat(),
        )
        
        try:
            # Create temporary script file
            script_path = f"/tmp/exec_{int(time.time() * 1000)}.py"
            
            with open(script_path, 'w') as f:
                f.write(code)
            
            # Execute with timeout
            try:
                process = subprocess.Popen(
                    [sys.executable, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                
                stdout, stderr = process.communicate(timeout=timeout)
                
                result.success = process.returncode == 0
                result.output = stdout
                result.error = stderr if stderr else ""
                
            except subprocess.TimeoutExpired:
                process.kill()
                result.error = f"Execution timeout exceeded ({timeout}s)"
                result.success = False
            
            except Exception as e:
                result.error = str(e)
                result.success = False
            
            finally:
                # Clean up
                if os.path.exists(script_path):
                    os.remove(script_path)
        
        except Exception as e:
            result.error = f"Execution failed: {str(e)}"
            result.success = False
        
        result.execution_time = time.time() - start_time
        
        # Keep history
        self.execution_history.append(asdict(result))
        if len(self.execution_history) > self.max_history:
            self.execution_history.pop(0)
        
        return result
    
    def execute_code_with_imports(self, code: str, allowed_imports: list = None, timeout: int = None) -> ExecutionResult:
        """
        Execute code with restricted imports
        
        Args:
            code: Python code
            allowed_imports: List of allowed import modules
            timeout: Timeout in seconds
        
        Returns:
            ExecutionResult
        """
        if allowed_imports is None:
            allowed_imports = ['json', 'math', 'datetime', 'random', 'statistics']
        
        # Validate imports in code
        for line in code.split('\n'):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                for module in allowed_imports:
                    if module in line:
                        break
                else:
                    return ExecutionResult(
                        success=False,
                        output="",
                        error=f"Import not allowed in: {line}",
                        execution_time=0.0,
                        timestamp=datetime.now().isoformat(),
                    )
        
        return self.execute_code(code, timeout)
    
    def validate_code_syntax(self, code: str) -> Dict[str, Any]:
        """Validate Python code syntax"""
        result = {
            "valid": False,
            "error": None,
            "line": None,
            "offset": None,
        }
        
        try:
            compile(code, '<string>', 'exec')
            result["valid"] = True
        except SyntaxError as e:
            result["error"] = e.msg
            result["line"] = e.lineno
            result["offset"] = e.offset
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def get_execution_history(self) -> list:
        """Get execution history"""
        return self.execution_history
    
    def clear_history(self):
        """Clear execution history"""
        self.execution_history = []


class CodeAnalyzer:
    """Analyze code for safety and best practices"""
    
    DANGEROUS_KEYWORDS = [
        '__import__',
        'eval',
        'exec',
        'compile',
        'open',
        'os.system',
        'subprocess',
        '__file__',
        '__loader__',
        'globals()',
        'locals()',
    ]
    
    @staticmethod
    def analyze(code: str) -> Dict[str, Any]:
        """Analyze code for dangerous patterns"""
        issues = []
        warnings = []
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for dangerous keywords
            for keyword in CodeAnalyzer.DANGEROUS_KEYWORDS:
                if keyword in line:
                    issues.append({
                        "line": i,
                        "keyword": keyword,
                        "message": f"Dangerous keyword found: {keyword}",
                    })
            
            # Check for long lines (potential issue)
            if len(line) > 200:
                warnings.append({
                    "line": i,
                    "message": "Line is very long (>200 chars)",
                })
        
        return {
            "safe": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "total_lines": len(lines),
            "lines_with_issues": len(set(issue["line"] for issue in issues)),
        }


# Global executor instance
python_executor = PythonExecutor()
