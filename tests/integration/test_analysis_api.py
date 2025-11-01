"""Integration tests for analysis API endpoints."""

import pytest
import json
import tempfile
import shutil
import threading
import time
import urllib.request
from pathlib import Path
from civ_arcos.api import app


@pytest.fixture
def server():
    """Start test server in background thread."""
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=8889), daemon=True
    )
    server_thread.start()
    time.sleep(1)  # Give server time to start
    yield "http://127.0.0.1:8889"
    # Server will be cleaned up automatically when thread terminates


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_code_file(temp_dir):
    """Create a sample Python file for testing."""
    code = '''
def add(a, b):
    """Add two numbers."""
    return a + b

class Calculator:
    """Simple calculator."""
    
    def __init__(self):
        self.result = 0
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b
'''

    code_file = Path(temp_dir) / "sample.py"
    code_file.write_text(code)
    return str(code_file)


def make_post_request(url, data):
    """Make a POST request with JSON data."""
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode()), response.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode()), e.code


def test_static_analysis_endpoint(server, sample_code_file):
    """Test static analysis API endpoint."""
    url = f"{server}/api/analysis/static"
    data = {"source_path": sample_code_file}

    result, status = make_post_request(url, data)

    assert status == 200
    assert result["success"] is True
    assert result["evidence_collected"] > 0
    assert "results" in result
    assert "complexity" in result["results"]


def test_security_scan_endpoint(server, sample_code_file):
    """Test security scan API endpoint."""
    url = f"{server}/api/analysis/security"
    data = {"source_path": sample_code_file}

    result, status = make_post_request(url, data)

    assert status == 200
    assert result["success"] is True
    assert result["evidence_collected"] >= 1
    assert "scan_results" in result


def test_test_suggestions_endpoint(server, sample_code_file):
    """Test test suggestions API endpoint."""
    url = f"{server}/api/analysis/tests"
    data = {"source_path": sample_code_file, "use_ai": False}

    result, status = make_post_request(url, data)

    assert status == 200
    assert result["success"] is True
    assert result["evidence_collected"] > 0
    assert "suggestions" in result
    assert result["suggestions"]["total_test_suggestions"] > 0


def test_comprehensive_analysis_endpoint(server, sample_code_file):
    """Test comprehensive analysis API endpoint."""
    url = f"{server}/api/analysis/comprehensive"
    data = {"source_path": sample_code_file, "run_coverage": False}

    result, status = make_post_request(url, data)

    assert status == 200
    assert result["success"] is True
    assert result["evidence_collected"] > 0
    assert "results" in result

    # Should have multiple types of evidence
    results = result["results"]
    assert "static_analysis" in results
    assert "security_scan" in results or "security_score" in results
    assert "test_suggestions" in results


def test_static_analysis_missing_path(server):
    """Test static analysis with missing source_path."""
    url = f"{server}/api/analysis/static"
    data = {}

    result, status = make_post_request(url, data)

    assert status == 400
    assert "error" in result


def test_api_root_shows_new_endpoints(server):
    """Test that API root shows new analysis endpoints."""
    with urllib.request.urlopen(f"{server}/") as response:
        data = json.loads(response.read().decode())

    endpoints = data["endpoints"]
    assert "POST /api/analysis/static" in endpoints
    assert "POST /api/analysis/security" in endpoints
    assert "POST /api/analysis/tests" in endpoints
    assert "POST /api/analysis/comprehensive" in endpoints
    assert "POST /api/analysis/powershell" in endpoints


def test_powershell_analysis_with_content(server):
    """Test PowerShell analysis API endpoint with content."""
    url = f"{server}/api/analysis/powershell"
    
    # PowerShell script with vulnerabilities
    ps_code = """
# Insecure hash algorithm
$hash = Get-FileHash -Path "file.txt" -Algorithm MD5

# Hardcoded credential
$password = ConvertTo-SecureString "MyPassword" -AsPlainText -Force

# Unencrypted HTTP
$data = Invoke-WebRequest -Uri "http://example.com/api"
"""
    
    data = {"content": ps_code}
    result, status = make_post_request(url, data)
    
    assert status == 200
    assert result["success"] is True
    assert "evidence_collected" in result
    assert "results" in result
    
    # Check scan results
    scan_results = result["results"]
    assert scan_results["success"] is True
    assert "violations" in scan_results
    assert "total_violations" in scan_results
    assert "summary" in scan_results
    
    # Should detect some vulnerabilities
    assert scan_results["total_violations"] > 0


def test_powershell_analysis_with_file(server, temp_dir):
    """Test PowerShell analysis API endpoint with file."""
    # Create a PowerShell test file
    ps_file = Path(temp_dir) / "test.ps1"
    ps_file.write_text("""
# Safe PowerShell script
$name = Read-Host -Prompt "Enter name"
Write-Host "Hello, $name"
""")
    
    url = f"{server}/api/analysis/powershell"
    data = {"source_path": str(ps_file)}
    
    result, status = make_post_request(url, data)
    
    assert status == 200
    assert result["success"] is True
    assert "evidence_collected" in result
    assert "results" in result


def test_powershell_analysis_missing_input(server):
    """Test PowerShell analysis API without required input."""
    url = f"{server}/api/analysis/powershell"
    data = {}  # No source_path or content
    
    result, status = make_post_request(url, data)
    
    assert status == 400
    assert "error" in result


def test_powershell_analysis_vulnerability_detection(server):
    """Test that PowerShell scanner detects specific vulnerabilities."""
    url = f"{server}/api/analysis/powershell"
    
    # Script with multiple known vulnerabilities
    ps_code = """
# MD5 hash
$hash = Get-FileHash -Path "file.txt" -Algorithm MD5

# Hardcoded API key (fake for testing)
$apiKey = "test_fake_EXAMPLE1234567890abcdefghijklmnopq"

# Invoke-Expression with variable
Invoke-Expression $userInput

# SQL injection
$query = "SELECT * FROM users WHERE id = " + $userId

# Execution policy bypass
Set-ExecutionPolicy Bypass -Scope Process
"""
    
    data = {"content": ps_code}
    result, status = make_post_request(url, data)
    
    assert status == 200
    scan_results = result["results"]
    
    # Check that multiple violations are detected
    assert scan_results["total_violations"] >= 4
    
    # Check severity summary
    summary = scan_results["summary"]
    assert summary["critical"] > 0 or summary["high"] > 0


def test_powershell_analysis_safe_script(server):
    """Test PowerShell analysis with safe script."""
    url = f"{server}/api/analysis/powershell"
    
    # Safe PowerShell script
    ps_code = """
# Safe script using best practices
$userName = Read-Host -Prompt "Enter name"
Write-Host "Hello, $userName"

# Using secure hash
$hash = Get-FileHash -Path "file.txt" -Algorithm SHA256

# Using HTTPS
$result = Invoke-RestMethod -Uri "https://api.example.com" -Method Get

# Safe credential handling
$securePassword = Read-Host -AsSecureString -Prompt "Password"
"""
    
    data = {"content": ps_code}
    result, status = make_post_request(url, data)
    
    assert status == 200
    scan_results = result["results"]
    
    # Should have no or very few violations
    assert scan_results["total_violations"] == 0 or scan_results["total_violations"] <= 1
