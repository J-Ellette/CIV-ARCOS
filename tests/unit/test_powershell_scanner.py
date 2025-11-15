"""Tests for PowerShell security scanner module."""

import pytest
import tempfile
import shutil
from pathlib import Path
from civ_arcos.analysis.powershell_scanner import (
    PowerShellScanner,
    PowerShellSecurityRule,
    PowerShellViolation,
    analyze_powershell_script,
    analyze_powershell_repository,
)


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def safe_powershell():
    """Safe PowerShell code without vulnerabilities."""
    return """
# Safe PowerShell script
$userName = Read-Host -Prompt "Enter your name"
Write-Host "Hello, $userName"

# Using secure hash algorithm
$hash = Get-FileHash -Path "file.txt" -Algorithm SHA256

# Safe credential handling
$securePassword = Read-Host -AsSecureString -Prompt "Enter password"
$credentials = New-Object System.Management.Automation.PSCredential("user", $securePassword)

# Using HTTPS
$result = Invoke-RestMethod -Uri "https://api.example.com/data" -Method Get
"""


@pytest.fixture
def vulnerable_powershell():
    """PowerShell code with various vulnerabilities."""
    return """
# Insecure hash algorithm (MD5)
$hash = Get-FileHash -Path "file.txt" -Algorithm MD5

# Hardcoded credentials
$password = ConvertTo-SecureString "MyPassword123" -AsPlainText -Force

# Dangerous Invoke-Expression with user input
$command = $args[0]
Invoke-Expression $command

# Disabled certificate validation
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

# Unencrypted HTTP
$data = Invoke-WebRequest -Uri "http://insecure-api.example.com/data"

# SQL injection risk
$userId = $args[0]
$query = "SELECT * FROM Users WHERE Id = " + $userId

# Command injection risk
$fileName = $args[0]
Start-Process "cmd.exe" -ArgumentList "/c type $fileName"

# Weak random generation
$random = Get-Random -Minimum 1 -Maximum 100

# Exposed API key (fake for testing)
$apiKey = "test_FAKE_example_key_1234567890"

# Execution policy bypass
Set-ExecutionPolicy Bypass -Scope Process
"""


def test_scanner_initialization():
    """Test scanner initialization."""
    scanner = PowerShellScanner()
    assert scanner.use_powershield_cli is True
    assert len(scanner.rules) > 0
    assert all(isinstance(rule, PowerShellSecurityRule) for rule in scanner.rules)


def test_scanner_initialization_without_cli():
    """Test scanner initialization without CLI."""
    scanner = PowerShellScanner(use_powershield_cli=False)
    assert scanner.use_powershield_cli is False
    assert scanner.powershield_available is False
    assert len(scanner.rules) > 0


def test_scan_safe_script(temp_dir, safe_powershell):
    """Test scanning safe PowerShell code."""
    test_file = Path(temp_dir) / "safe.ps1"
    test_file.write_text(safe_powershell)
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_script(str(test_file))
    
    assert result["success"] is True
    assert result["total_violations"] == 0
    assert result["summary"]["critical"] == 0
    assert result["summary"]["high"] == 0
    assert result["summary"]["medium"] == 0
    assert result["summary"]["low"] == 0
    assert result["scanner"] == "built-in"


def test_scan_vulnerable_script(temp_dir, vulnerable_powershell):
    """Test scanning vulnerable PowerShell code."""
    test_file = Path(temp_dir) / "vulnerable.ps1"
    test_file.write_text(vulnerable_powershell)
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_script(str(test_file))
    
    assert result["success"] is True
    assert result["total_violations"] > 0
    assert len(result["violations"]) > 0
    
    # Check for expected vulnerabilities
    violation_names = [v["name"] for v in result["violations"]]
    
    # Should detect at least some of these vulnerabilities
    expected_vulnerabilities = [
        "InsecureHashAlgorithms",
        "HardcodedCredentials",
        "DangerousInvokeExpression",
        "DisabledCertValidation",
        "UnencryptedHttp",
        "SqlInjectionRisk",
        "CommandInjectionRisk",
        "WeakRandomGeneration",
        "ExposedSecrets",
        "ExecutionPolicyBypass",
    ]
    
    # At least some expected vulnerabilities should be found
    found_vulnerabilities = [v for v in expected_vulnerabilities if v in violation_names]
    assert len(found_vulnerabilities) > 0


def test_scan_insecure_hash():
    """Test detection of insecure hash algorithms."""
    code = """
$hash1 = Get-FileHash -Path "file.txt" -Algorithm MD5
$hash2 = Get-FileHash -Path "file2.txt" -Algorithm SHA1
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] >= 2
    
    # Check that both MD5 and SHA1 are detected
    violation_snippets = [v["code_snippet"] for v in result["violations"]]
    assert any("MD5" in snippet for snippet in violation_snippets)
    assert any("SHA1" in snippet for snippet in violation_snippets)


def test_scan_hardcoded_credentials():
    """Test detection of hardcoded credentials."""
    code = """
$password = ConvertTo-SecureString "MyPassword123" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("user", $password)
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] >= 1
    assert any(v["name"] == "HardcodedCredentials" for v in result["violations"])


def test_scan_invoke_expression():
    """Test detection of dangerous Invoke-Expression usage."""
    code = """
$userInput = Read-Host "Enter command"
Invoke-Expression $userInput
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] >= 1
    assert any(v["name"] == "DangerousInvokeExpression" for v in result["violations"])


def test_scan_disabled_cert_validation():
    """Test detection of disabled certificate validation."""
    code = """
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
$response = Invoke-WebRequest -Uri "https://example.com"
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] >= 1
    assert any(v["name"] == "DisabledCertValidation" for v in result["violations"])


def test_scan_unencrypted_http():
    """Test detection of unencrypted HTTP usage."""
    code = """
$data = Invoke-RestMethod -Uri "http://api.example.com/data"
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] >= 1
    assert any(v["name"] == "UnencryptedHttp" for v in result["violations"])


def test_scan_sql_injection():
    """Test detection of SQL injection vulnerabilities."""
    code = """
$userId = $args[0]
$query = "SELECT * FROM users WHERE id = " + $userId
Execute-SqlCommand $query
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] >= 1
    assert any(v["name"] == "SqlInjectionRisk" for v in result["violations"])


def test_scan_command_injection():
    """Test detection of command injection vulnerabilities."""
    code = """
$fileName = $args[0]
$result = Start-Process "cmd.exe" "/c type $fileName"
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] >= 1
    assert any(v["name"] == "CommandInjectionRisk" for v in result["violations"])


def test_scan_exposed_secrets():
    """Test detection of exposed secrets."""
    # Using fake patterns that look like secrets but aren't real
    code = """
$apiKey = "test_live_FAKE1234567890abcdefghijklmnopqrstu"
$token = "fake_token_1234567890abcdefghijklmnopqrstuvwx"
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] >= 1
    assert any(v["name"] == "ExposedSecrets" for v in result["violations"])


def test_scan_execution_policy_bypass():
    """Test detection of execution policy bypass."""
    code = """
Set-ExecutionPolicy Bypass -Scope Process -Force
Set-ExecutionPolicy Unrestricted -Scope CurrentUser
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] >= 1
    assert any(v["name"] == "ExecutionPolicyBypass" for v in result["violations"])


def test_scan_directory(temp_dir, safe_powershell, vulnerable_powershell):
    """Test scanning a directory of PowerShell scripts."""
    # Create multiple test files
    safe_file = Path(temp_dir) / "safe.ps1"
    safe_file.write_text(safe_powershell)
    
    vuln_file = Path(temp_dir) / "vulnerable.ps1"
    vuln_file.write_text(vulnerable_powershell)
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_directory(temp_dir)
    
    assert result["success"] is True
    assert result["files_scanned"] == 2
    assert len(result["files"]) == 2
    assert result["total_violations"] > 0
    
    # Check summary aggregation
    assert "summary" in result
    assert all(key in result["summary"] for key in ["critical", "high", "medium", "low"])


def test_scan_nonexistent_file():
    """Test scanning a nonexistent file."""
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_script("/nonexistent/file.ps1")
    
    assert result["success"] is False
    assert "error" in result


def test_scan_nonexistent_directory():
    """Test scanning a nonexistent directory."""
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_directory("/nonexistent/directory")
    
    assert result["success"] is False
    assert "error" in result


def test_violation_to_dict():
    """Test PowerShellViolation to_dict method."""
    violation = PowerShellViolation(
        rule_id="PS001",
        name="TestViolation",
        message="Test message",
        severity="High",
        line_number=10,
        code_snippet="$test = 'value'",
        file_path="/test/file.ps1"
    )
    
    result = violation.to_dict()
    
    assert result["rule_id"] == "PS001"
    assert result["name"] == "TestViolation"
    assert result["message"] == "Test message"
    assert result["severity"] == "High"
    assert result["line_number"] == 10
    assert result["code_snippet"] == "$test = 'value'"
    assert result["file_path"] == "/test/file.ps1"


def test_analyze_powershell_script_helper(temp_dir, safe_powershell):
    """Test analyze_powershell_script helper function."""
    test_file = Path(temp_dir) / "test.ps1"
    test_file.write_text(safe_powershell)
    
    result = analyze_powershell_script(str(test_file))
    
    assert result["success"] is True
    assert "violations" in result
    assert "summary" in result


def test_analyze_powershell_repository_helper(temp_dir, safe_powershell):
    """Test analyze_powershell_repository helper function."""
    test_file = Path(temp_dir) / "test.ps1"
    test_file.write_text(safe_powershell)
    
    result = analyze_powershell_repository(temp_dir)
    
    assert result["success"] is True
    assert result["files_scanned"] >= 1
    assert "summary" in result


def test_severity_levels():
    """Test that all severity levels are properly represented."""
    scanner = PowerShellScanner(use_powershield_cli=False)
    
    # Check that rules have various severity levels
    severities = [rule.severity for rule in scanner.rules]
    assert "Critical" in severities
    assert "High" in severities
    assert "Medium" in severities


def test_rule_ids_are_unique():
    """Test that all rule IDs are unique."""
    scanner = PowerShellScanner(use_powershield_cli=False)
    
    rule_ids = [rule.rule_id for rule in scanner.rules]
    assert len(rule_ids) == len(set(rule_ids))


def test_all_rules_have_patterns():
    """Test that all rules have patterns defined."""
    scanner = PowerShellScanner(use_powershield_cli=False)
    
    for rule in scanner.rules:
        assert rule.pattern is not None
        assert len(rule.pattern) > 0


def test_scan_with_multiple_extensions(temp_dir, safe_powershell):
    """Test scanning PowerShell files with different extensions."""
    # Create files with different PowerShell extensions
    ps1_file = Path(temp_dir) / "script.ps1"
    ps1_file.write_text(safe_powershell)
    
    psm1_file = Path(temp_dir) / "module.psm1"
    psm1_file.write_text(safe_powershell)
    
    psd1_file = Path(temp_dir) / "manifest.psd1"
    psd1_file.write_text(safe_powershell)
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_directory(temp_dir)
    
    assert result["success"] is True
    assert result["files_scanned"] == 3


def test_scan_empty_content():
    """Test scanning empty content."""
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content("")
    
    assert result["success"] is True
    assert result["total_violations"] == 0


def test_scan_content_with_comments_only():
    """Test scanning content with only comments."""
    code = """
# This is a comment
# Another comment
# Yet another comment
"""
    
    scanner = PowerShellScanner(use_powershield_cli=False)
    result = scanner.scan_content(code)
    
    assert result["success"] is True
    assert result["total_violations"] == 0
