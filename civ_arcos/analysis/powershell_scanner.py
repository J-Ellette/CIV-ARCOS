"""
PowerShell Script Security Scanner Module

Integrates PowerShield scanning capabilities for PowerShell scripts.
Provides security analysis, vulnerability detection, and best practice checks.
"""

import re
import subprocess
import json
import tempfile
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


class PowerShellSecurityRule:
    """Represents a PowerShell security rule."""
    
    def __init__(
        self,
        rule_id: str,
        name: str,
        description: str,
        severity: str,
        pattern: str = None,
        check_function: callable = None
    ):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.severity = severity  # Critical, High, Medium, Low
        self.pattern = pattern
        self.check_function = check_function


class PowerShellViolation:
    """Represents a security violation found in PowerShell code."""
    
    def __init__(
        self,
        rule_id: str,
        name: str,
        message: str,
        severity: str,
        line_number: int,
        code_snippet: str,
        file_path: str = ""
    ):
        self.rule_id = rule_id
        self.name = name
        self.message = message
        self.severity = severity
        self.line_number = line_number
        self.code_snippet = code_snippet
        self.file_path = file_path
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert violation to dictionary."""
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "message": self.message,
            "severity": self.severity,
            "line_number": self.line_number,
            "code_snippet": self.code_snippet,
            "file_path": self.file_path
        }


class PowerShellScanner:
    """
    PowerShell Script Security Scanner
    
    Analyzes PowerShell scripts for security vulnerabilities and coding issues.
    Can use PowerShield CLI if available, or built-in pattern matching.
    """
    
    def __init__(self, use_powershield_cli: bool = True):
        """
        Initialize PowerShell scanner.
        
        Args:
            use_powershield_cli: If True, try to use PowerShield CLI for analysis
        """
        self.use_powershield_cli = use_powershield_cli
        self.powershield_available = self._check_powershield_available()
        self.rules = self._initialize_rules()
        
    def _check_powershield_available(self) -> bool:
        """Check if PowerShield CLI is available."""
        if not self.use_powershield_cli:
            return False
            
        try:
            # Check if pwsh (PowerShell Core) is available
            result = subprocess.run(
                ["pwsh", "-Version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def _initialize_rules(self) -> List[PowerShellSecurityRule]:
        """Initialize security rules for PowerShell scanning."""
        rules = []
        
        # Rule 1: Insecure Hash Algorithms
        rules.append(PowerShellSecurityRule(
            rule_id="PS001",
            name="InsecureHashAlgorithms",
            description="Detects usage of cryptographically weak hash algorithms (MD5, SHA1)",
            severity="High",
            pattern=r"Get-FileHash\s+.*-Algorithm\s+(MD5|SHA1|SHA-1)"
        ))
        
        # Rule 2: Hardcoded Credentials
        rules.append(PowerShellSecurityRule(
            rule_id="PS002",
            name="HardcodedCredentials",
            description="Detects hardcoded credentials in scripts",
            severity="Critical",
            pattern=r"(ConvertTo-SecureString\s+.*-AsPlainText|-Password\s+['\"][\w@!#$%^&*()]+['\"])"
        ))
        
        # Rule 3: Invoke-Expression with User Input
        rules.append(PowerShellSecurityRule(
            rule_id="PS003",
            name="DangerousInvokeExpression",
            description="Detects potentially dangerous use of Invoke-Expression",
            severity="Critical",
            pattern=r"Invoke-Expression\s+\$"
        ))
        
        # Rule 4: Disabled Certificate Validation
        rules.append(PowerShellSecurityRule(
            rule_id="PS004",
            name="DisabledCertValidation",
            description="Detects disabled SSL/TLS certificate validation",
            severity="High",
            pattern=r"ServerCertificateValidationCallback.*\$true"
        ))
        
        # Rule 5: Unencrypted Network Communication
        rules.append(PowerShellSecurityRule(
            rule_id="PS005",
            name="UnencryptedHttp",
            description="Detects use of unencrypted HTTP instead of HTTPS",
            severity="Medium",
            pattern=r"http://(?!localhost|127\.0\.0\.1)"
        ))
        
        # Rule 6: SQL Injection Risk
        rules.append(PowerShellSecurityRule(
            rule_id="PS006",
            name="SqlInjectionRisk",
            description="Detects potential SQL injection vulnerabilities",
            severity="High",
            pattern=r"(SELECT|INSERT|UPDATE|DELETE).*\+\s*\$"
        ))
        
        # Rule 7: Command Injection Risk
        rules.append(PowerShellSecurityRule(
            rule_id="PS007",
            name="CommandInjectionRisk",
            description="Detects potential command injection vulnerabilities",
            severity="High",
            pattern=r"(Start-Process|Invoke-Command).*['\"].*\$"
        ))
        
        # Rule 8: Insecure Deserialization
        rules.append(PowerShellSecurityRule(
            rule_id="PS008",
            name="InsecureDeserialization",
            description="Detects insecure deserialization patterns",
            severity="High",
            pattern=r"(Import-Clixml|ConvertFrom-Json)\s+\$"
        ))
        
        # Rule 9: Weak Random Number Generation
        rules.append(PowerShellSecurityRule(
            rule_id="PS009",
            name="WeakRandomGeneration",
            description="Detects use of weak random number generation",
            severity="Medium",
            pattern=r"Get-Random(?!\s+-Secure)"
        ))
        
        # Rule 10: Exposed Secrets
        rules.append(PowerShellSecurityRule(
            rule_id="PS010",
            name="ExposedSecrets",
            description="Detects potential exposed API keys, tokens, or secrets",
            severity="Critical",
            pattern=r"\$\w+\s*=\s*['\"]([a-zA-Z0-9_-]{30,}|sk_live_|ghp_|glpat-)['\"]"
        ))
        
        # Rule 11: Dangerous Modules
        rules.append(PowerShellSecurityRule(
            rule_id="PS011",
            name="DangerousModules",
            description="Detects import of potentially dangerous modules",
            severity="Medium",
            pattern=r"Import-Module\s+.*(Win32|System\.Management|ActiveDirectory)"
        ))
        
        # Rule 12: Execution Policy Bypass
        rules.append(PowerShellSecurityRule(
            rule_id="PS012",
            name="ExecutionPolicyBypass",
            description="Detects attempts to bypass execution policy",
            severity="High",
            pattern=r"Set-ExecutionPolicy\s+(Bypass|Unrestricted)"
        ))
        
        return rules
    
    def scan_script(self, script_path: str) -> Dict[str, Any]:
        """
        Scan a PowerShell script file for security vulnerabilities.
        
        Args:
            script_path: Path to PowerShell script (.ps1, .psm1, .psd1)
            
        Returns:
            Dictionary containing scan results
        """
        if not os.path.exists(script_path):
            return {
                "success": False,
                "error": f"Script file not found: {script_path}"
            }
        
        # Try PowerShield CLI first if available
        if self.powershield_available:
            try:
                result = self._scan_with_powershield(script_path)
                if result["success"]:
                    return result
            except Exception as e:
                # Fall back to built-in scanner
                pass
        
        # Use built-in pattern-based scanner
        return self._scan_with_patterns(script_path)
    
    def scan_content(self, content: str, file_name: str = "script.ps1") -> Dict[str, Any]:
        """
        Scan PowerShell script content for security vulnerabilities.
        
        Args:
            content: PowerShell script content
            file_name: Name for the script (for reporting)
            
        Returns:
            Dictionary containing scan results
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.ps1',
            delete=False,
            encoding='utf-8'
        ) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            result = self.scan_script(tmp_path)
            # Update file paths in violations to use the provided name
            if result.get("success") and result.get("violations"):
                for violation in result["violations"]:
                    violation["file_path"] = file_name
            return result
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_path)
            except (OSError, FileNotFoundError):
                # Ignore cleanup errors - file may already be deleted
                pass
    
    def _scan_with_powershield(self, script_path: str) -> Dict[str, Any]:
        """
        Scan using PowerShield CLI.
        
        Args:
            script_path: Path to PowerShell script
            
        Returns:
            Dictionary containing scan results
        """
        # Note: This would require PowerShield to be installed
        # For now, this is a placeholder that would call PowerShield
        # In production, you would either:
        # 1. Bundle PowerShield with CIV-ARCOS
        # 2. Require it as a dependency
        # 3. Provide installation instructions
        
        try:
            # Example of how to call PowerShield (requires it to be in PATH or bundled)
            # Using list arguments to prevent shell injection
            result = subprocess.run(
                ["pwsh", "-Command", "./powershield.ps1", "analyze", script_path, "-Format", "json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                # Parse PowerShield JSON output
                data = json.loads(result.stdout)
                return self._convert_powershield_results(data)
            
        except (subprocess.SubprocessError, json.JSONDecodeError, OSError) as e:
            # Log specific error types for debugging
            pass
        
        return {"success": False, "error": "PowerShield scan failed"}
    
    def _scan_with_patterns(self, script_path: str) -> Dict[str, Any]:
        """
        Scan using built-in pattern matching.
        
        Args:
            script_path: Path to PowerShell script
            
        Returns:
            Dictionary containing scan results
        """
        violations = []
        
        try:
            with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Check each line against each rule
            for line_num, line in enumerate(lines, start=1):
                for rule in self.rules:
                    if rule.pattern and re.search(rule.pattern, line, re.IGNORECASE):
                        violation = PowerShellViolation(
                            rule_id=rule.rule_id,
                            name=rule.name,
                            message=rule.description,
                            severity=rule.severity,
                            line_number=line_num,
                            code_snippet=line.strip(),
                            file_path=script_path
                        )
                        violations.append(violation.to_dict())
            
            # Calculate summary
            summary = {
                "critical": sum(1 for v in violations if v["severity"] == "Critical"),
                "high": sum(1 for v in violations if v["severity"] == "High"),
                "medium": sum(1 for v in violations if v["severity"] == "Medium"),
                "low": sum(1 for v in violations if v["severity"] == "Low")
            }
            
            return {
                "success": True,
                "file_path": script_path,
                "violations": violations,
                "total_violations": len(violations),
                "summary": summary,
                "scanner": "built-in"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error scanning script: {str(e)}"
            }
    
    def _convert_powershield_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert PowerShield results to standard format.
        
        Args:
            data: PowerShield JSON output
            
        Returns:
            Standardized results dictionary
        """
        # This would convert PowerShield's output format to our standard format
        # Implementation depends on PowerShield's actual JSON structure
        return {
            "success": True,
            "violations": data.get("violations", []),
            "total_violations": data.get("total_violations", 0),
            "summary": data.get("summary", {}),
            "scanner": "powershield"
        }
    
    def scan_directory(self, directory: str) -> Dict[str, Any]:
        """
        Scan all PowerShell scripts in a directory.
        
        Args:
            directory: Directory path to scan
            
        Returns:
            Dictionary containing aggregated scan results
        """
        if not os.path.isdir(directory):
            return {
                "success": False,
                "error": f"Directory not found: {directory}"
            }
        
        results = {
            "success": True,
            "directory": directory,
            "files_scanned": 0,
            "total_violations": 0,
            "summary": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "files": []
        }
        
        # Find all PowerShell files
        ps_extensions = ['.ps1', '.psm1', '.psd1']
        ps_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in ps_extensions):
                    ps_files.append(os.path.join(root, file))
        
        # Scan each file
        for ps_file in ps_files:
            file_result = self.scan_script(ps_file)
            if file_result.get("success"):
                results["files"].append(file_result)
                results["files_scanned"] += 1
                results["total_violations"] += file_result.get("total_violations", 0)
                
                # Aggregate summary
                file_summary = file_result.get("summary", {})
                for severity in ["critical", "high", "medium", "low"]:
                    results["summary"][severity] += file_summary.get(severity, 0)
        
        return results


def analyze_powershell_repository(repo_path: str) -> Dict[str, Any]:
    """
    Analyze a repository for PowerShell security issues.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Analysis results dictionary
    """
    scanner = PowerShellScanner()
    return scanner.scan_directory(repo_path)


def analyze_powershell_script(script_path: str) -> Dict[str, Any]:
    """
    Analyze a single PowerShell script.
    
    Args:
        script_path: Path to PowerShell script
        
    Returns:
        Analysis results dictionary
    """
    scanner = PowerShellScanner()
    return scanner.scan_script(script_path)
