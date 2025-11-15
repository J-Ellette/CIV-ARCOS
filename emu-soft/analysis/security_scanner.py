"""
Security scanning module for SAST (Static Application Security Testing).
Implements basic security checks without external dependencies.
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List


class SecurityScanner:
    """
    Security scanner for detecting common vulnerabilities.
    Implements SAST checks for injection, XSS, hardcoded secrets, etc.
    """

    def __init__(self):
        """Initialize security scanner."""
        self.scanner_id = "security_scanner"
        self.vulnerabilities: List[Dict[str, Any]] = []

        # Patterns for detecting security issues
        self.secret_patterns = [
            (
                r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]+['\"]",
                "Hardcoded Password",
            ),
            (r"(?i)(api[_-]?key|apikey)\s*=\s*['\"][^'\"]+['\"]", "Hardcoded API Key"),
            (r"(?i)(secret|token)\s*=\s*['\"][^'\"]+['\"]", "Hardcoded Secret"),
            (r"(?i)aws_secret_access_key\s*=\s*['\"][^'\"]+['\"]", "AWS Secret Key"),
            (r"(?i)(private[_-]?key)\s*=\s*['\"][^'\"]+['\"]", "Private Key"),
        ]

    def scan(self, source_path: str) -> Dict[str, Any]:
        """
        Scan source code for security vulnerabilities.

        Args:
            source_path: Path to source file or directory

        Returns:
            Dictionary with security findings
        """
        self.vulnerabilities.clear()

        path = Path(source_path)

        if path.is_file():
            return self._scan_file(path)
        elif path.is_dir():
            return self._scan_directory(path)
        else:
            return {"error": "Invalid path"}

    def _scan_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan a single file for vulnerabilities."""
        if file_path.suffix != ".py":
            return {"error": "Not a Python file"}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()

            # Run various security checks
            self._check_sql_injection(source_code, str(file_path))
            self._check_command_injection(source_code, str(file_path))
            self._check_hardcoded_secrets(source_code, str(file_path))
            self._check_insecure_functions(source_code, str(file_path))
            self._check_xss_vulnerabilities(source_code, str(file_path))

            # Parse AST for deeper analysis
            try:
                tree = ast.parse(source_code, filename=str(file_path))
                self._check_ast_vulnerabilities(tree, str(file_path))
            except SyntaxError:
                pass

            return {
                "file": str(file_path),
                "vulnerabilities_found": len(self.vulnerabilities),
                "vulnerabilities": self.vulnerabilities.copy(),
                "severity_breakdown": self._calculate_severity_breakdown(
                    self.vulnerabilities
                ),
            }

        except Exception as e:
            return {"error": f"Failed to scan {file_path}: {str(e)}"}

    def _scan_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Scan all Python files in a directory."""
        total_vulnerabilities = 0
        files_scanned = 0
        all_vulnerabilities = []

        for py_file in dir_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            result = self._scan_file(py_file)
            if "error" not in result:
                files_scanned += 1
                total_vulnerabilities += result.get("vulnerabilities_found", 0)
                all_vulnerabilities.extend(result.get("vulnerabilities", []))

        return {
            "directory": str(dir_path),
            "files_scanned": files_scanned,
            "total_vulnerabilities": total_vulnerabilities,
            "vulnerabilities": all_vulnerabilities,
            "severity_breakdown": self._calculate_severity_breakdown(
                all_vulnerabilities
            ),
        }

    def _check_sql_injection(self, source_code: str, file_path: str) -> None:
        """Check for potential SQL injection vulnerabilities."""
        # Look for string formatting in SQL queries
        sql_patterns = [
            r"['\"].*?%s.*?['\"]\s*%\s*\w+",  # "query %s" % var
            r"execute\s*\(['\"].*?%s.*?['\"]\s*%",
            r"execute\s*\(['\"].*?\{.*?\}.*?['\"]\s*\.format",
            r"execute\s*\(f['\"].*?\{.*?\}.*?['\"]",
            r"execute\s*\(.*?\+.*?\)",
        ]

        for pattern in sql_patterns:
            matches = re.finditer(pattern, source_code, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                line_num = source_code[: match.start()].count("\n") + 1
                self.vulnerabilities.append(
                    {
                        "type": "SQL Injection",
                        "severity": "High",
                        "file": file_path,
                        "line": line_num,
                        "description": "Potential SQL injection via string formatting",
                        "recommendation": "Use parameterized queries with placeholders",
                    }
                )

    def _check_command_injection(self, source_code: str, file_path: str) -> None:
        """Check for command injection vulnerabilities."""
        # Look for shell=True or unsafe command execution
        patterns = [
            (
                r"subprocess\.\w+\(.*?shell\s*=\s*True.*?\)",
                "Command injection via shell=True",
            ),
            (r"os\.system\(", "Unsafe command execution with os.system"),
            (r"eval\(", "Dangerous use of eval()"),
            (r"exec\(", "Dangerous use of exec()"),
        ]

        for pattern, description in patterns:
            matches = re.finditer(pattern, source_code, re.IGNORECASE)
            for match in matches:
                line_num = source_code[: match.start()].count("\n") + 1
                self.vulnerabilities.append(
                    {
                        "type": "Command Injection",
                        "severity": "High",
                        "file": file_path,
                        "line": line_num,
                        "description": description,
                        "recommendation": "Avoid shell=True and use parameterized commands",
                    }
                )

    def _check_hardcoded_secrets(self, source_code: str, file_path: str) -> None:
        """Check for hardcoded secrets and credentials."""
        for pattern, secret_type in self.secret_patterns:
            matches = re.finditer(pattern, source_code)
            for match in matches:
                # Skip if it's a placeholder or example
                matched_text = match.group(0)
                if any(
                    placeholder in matched_text.lower()
                    for placeholder in [
                        "example",
                        "test",
                        "dummy",
                        "placeholder",
                        "xxx",
                        "your_",
                        "here",
                    ]
                ):
                    continue

                line_num = source_code[: match.start()].count("\n") + 1
                self.vulnerabilities.append(
                    {
                        "type": "Hardcoded Secret",
                        "severity": "Critical",
                        "file": file_path,
                        "line": line_num,
                        "description": f"{secret_type} found in source code",
                        "recommendation": "Use environment variables or secure vaults",
                    }
                )

    def _check_insecure_functions(self, source_code: str, file_path: str) -> None:
        """Check for use of insecure functions."""
        insecure_functions = [
            (r"pickle\.loads?\(", "Insecure deserialization", "Medium"),
            (r"yaml\.load\(", "Unsafe YAML loading", "Medium"),
            (r"marshal\.loads?\(", "Insecure deserialization", "Medium"),
            (r"input\(.*?\)", "Use of input() can be unsafe", "Low"),
        ]

        for pattern, description, severity in insecure_functions:
            matches = re.finditer(pattern, source_code)
            for match in matches:
                line_num = source_code[: match.start()].count("\n") + 1
                self.vulnerabilities.append(
                    {
                        "type": "Insecure Function",
                        "severity": severity,
                        "file": file_path,
                        "line": line_num,
                        "description": description,
                        "recommendation": "Use safe alternatives or validate input",
                    }
                )

    def _check_xss_vulnerabilities(self, source_code: str, file_path: str) -> None:
        """Check for potential XSS vulnerabilities."""
        # Look for unsafe HTML rendering
        xss_patterns = [
            (r"\.innerHTML\s*=", "Potential XSS via innerHTML"),
            (r"document\.write\(", "Potential XSS via document.write"),
            (r"dangerouslySetInnerHTML", "Potential XSS in React"),
        ]

        for pattern, description in xss_patterns:
            matches = re.finditer(pattern, source_code, re.IGNORECASE)
            for match in matches:
                line_num = source_code[: match.start()].count("\n") + 1
                self.vulnerabilities.append(
                    {
                        "type": "XSS",
                        "severity": "Medium",
                        "file": file_path,
                        "line": line_num,
                        "description": description,
                        "recommendation": "Sanitize user input and use safe rendering methods",
                    }
                )

    def _check_ast_vulnerabilities(self, tree: ast.AST, file_path: str) -> None:
        """Check for vulnerabilities using AST analysis."""
        for node in ast.walk(tree):
            # Check for assert statements (shouldn't be used for validation)
            if isinstance(node, ast.Assert):
                line_num = getattr(node, "lineno", 0)
                self.vulnerabilities.append(
                    {
                        "type": "Insecure Validation",
                        "severity": "Low",
                        "file": file_path,
                        "line": line_num,
                        "description": "Using assert for validation (disabled with -O flag)",
                        "recommendation": "Use explicit if statements for validation",
                    }
                )

            # Check for bare except clauses
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    line_num = getattr(node, "lineno", 0)
                    self.vulnerabilities.append(
                        {
                            "type": "Error Handling",
                            "severity": "Low",
                            "file": file_path,
                            "line": line_num,
                            "description": "Bare except clause can hide errors",
                            "recommendation": "Catch specific exceptions",
                        }
                    )

    def _calculate_severity_breakdown(
        self, vulnerabilities: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """Calculate severity breakdown."""
        breakdown = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

        for vuln in vulnerabilities:
            severity = vuln.get("severity", "Low")
            breakdown[severity] = breakdown.get(severity, 0) + 1

        return breakdown

    def get_security_score(self, vulnerabilities: List[Dict[str, Any]]) -> float:
        """
        Calculate security score (0-100) based on vulnerabilities.

        Args:
            vulnerabilities: List of vulnerabilities

        Returns:
            Security score (higher is better)
        """
        if not vulnerabilities:
            return 100.0

        # Weight by severity
        severity_weights = {"Critical": 20, "High": 10, "Medium": 5, "Low": 2}

        total_penalty = sum(
            severity_weights.get(v.get("severity", "Low"), 2) for v in vulnerabilities
        )

        # Cap at 0
        score = max(0, 100 - total_penalty)
        return round(score, 2)

    def get_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Get all found vulnerabilities."""
        return self.vulnerabilities.copy()
