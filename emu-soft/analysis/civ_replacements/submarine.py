"""Submarine - Subprocess runner

Process manager for development tasks.
Wrapper around Python's subprocess module with enhanced error handling.
"""

import subprocess
import sys
from typing import Any, Dict, List, Optional, Union


class SubmarineResult:
    """Result of a subprocess execution"""
    
    def __init__(self, returncode: int, stdout: str, stderr: str, command: List[str]):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.command = command
    
    @property
    def success(self) -> bool:
        """Check if command succeeded"""
        return self.returncode == 0


class Submarine:
    """
    Submarine: Process manager
    
    Provides utilities to run commands using subprocess.
    """
    
    def __init__(self):
        """Initialize Submarine"""
        self.history: List[SubmarineResult] = []
        self.count = 0
    
    def run(self, 
            command: Union[str, List[str]], 
            capture_output: bool = True,
            text: bool = True,
            check: bool = False,
            timeout: Optional[float] = None,
            cwd: Optional[str] = None,
            env: Optional[Dict[str, str]] = None,
            shell: bool = False) -> SubmarineResult:
        """
        Run a command and return the result.
        
        Args:
            command: Command to run (string or list of arguments)
            capture_output: Whether to capture stdout/stderr
            text: Return output as text (not bytes)
            check: Raise exception on non-zero exit code
            timeout: Timeout in seconds
            cwd: Working directory for command
            env: Environment variables
            shell: Whether to run through shell
            
        Returns:
            SubmarineResult with command output and status
        """
        # Convert string command to list if shell=False
        if isinstance(command, str) and not shell:
            command = command.split()
        
        try:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=text,
                check=check,
                timeout=timeout,
                cwd=cwd,
                env=env,
                shell=shell
            )
            
            stdout = result.stdout if result.stdout else ""
            stderr = result.stderr if result.stderr else ""
            returncode = result.returncode
            
        except subprocess.CalledProcessError as e:
            stdout = e.stdout if e.stdout else ""
            stderr = e.stderr if e.stderr else ""
            returncode = e.returncode
            if check:
                raise
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout.decode() if e.stdout else ""
            stderr = e.stderr.decode() if e.stderr else ""
            returncode = -1
            if check:
                raise
        except Exception as e:
            stdout = ""
            stderr = str(e)
            returncode = -1
            if check:
                raise
        
        cmd_list = command if isinstance(command, list) else [command]
        sub_result = SubmarineResult(returncode, stdout, stderr, cmd_list)
        self.history.append(sub_result)
        self.count += 1
        
        return sub_result
    
    def call(self, command: Union[str, List[str]], **kwargs) -> int:
        """
        Run command and return exit code (like subprocess.call).
        
        Args:
            command: Command to run
            **kwargs: Additional arguments for subprocess
            
        Returns:
            Exit code of the command
        """
        result = self.run(command, **kwargs)
        return result.returncode
    
    def check_output(self, command: Union[str, List[str]], **kwargs) -> str:
        """
        Run command and return output (like subprocess.check_output).
        
        Args:
            command: Command to run
            **kwargs: Additional arguments for subprocess
            
        Returns:
            stdout of the command
            
        Raises:
            subprocess.CalledProcessError: If command fails
        """
        result = self.run(command, check=True, **kwargs)
        return result.stdout
    
    def popen(self, 
              command: Union[str, List[str]],
              stdin=None,
              stdout=None, 
              stderr=None,
              **kwargs) -> subprocess.Popen:
        """
        Start a process (like subprocess.Popen).
        
        Args:
            command: Command to run
            stdin: Input pipe
            stdout: Output pipe
            stderr: Error pipe
            **kwargs: Additional arguments for Popen
            
        Returns:
            Popen object
        """
        if isinstance(command, str):
            command = command.split()
        
        return subprocess.Popen(
            command,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            **kwargs
        )
    
    def get_history(self) -> List[SubmarineResult]:
        """Get command execution history"""
        return self.history
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results"""
        return {
            'executed': self.count,
            'history': [
                {
                    'command': ' '.join(r.command),
                    'returncode': r.returncode,
                    'success': r.success
                }
                for r in self.history
            ]
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics"""
        successful = sum(1 for r in self.history if r.success)
        failed = self.count - successful
        
        return {
            'total_executed': self.count,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / self.count if self.count > 0 else 0
        }
    
    def clear_history(self):
        """Clear execution history"""
        self.history.clear()
        self.count = 0
