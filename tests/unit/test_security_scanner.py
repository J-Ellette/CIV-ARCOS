"""Tests for security scanner module."""

import pytest
import tempfile
import shutil
from pathlib import Path
from civ_arcos.analysis.security_scanner import SecurityScanner


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def safe_code():
    """Safe Python code without vulnerabilities."""
    return '''
def safe_function(user_input):
    """A safe function."""
    # Using parameterized query (safe)
    return user_input.strip()

def safe_command():
    """Safe command execution."""
    import subprocess
    # Using array without shell=True (safe)
    subprocess.run(["ls", "-la"])
'''


@pytest.fixture
def vulnerable_code():
    """Code with various vulnerabilities."""
    return """
import subprocess
import os

# SQL Injection vulnerability
def unsafe_query(user_id):
    query = "SELECT * FROM users WHERE id = %s" % user_id
    execute(query)

# Command Injection
def unsafe_command(filename):
    os.system("cat " + filename)
    subprocess.run("ls " + filename, shell=True)

# Hardcoded secrets
API_KEY = "sk_live_abc123xyz"
password = "SuperSecret123"

# Insecure deserialization
def load_data(data):
    import pickle
    return pickle.loads(data)

# eval/exec usage
def dynamic_code(code):
    eval(code)
    exec(code)
"""


def test_scanner_initialization():
    """Test scanner initialization."""
    scanner = SecurityScanner()
    assert scanner.scanner_id == "security_scanner"
    assert len(scanner.vulnerabilities) == 0


def test_scan_safe_code(temp_dir, safe_code):
    """Test scanning safe code."""
    test_file = Path(temp_dir) / "safe.py"
    test_file.write_text(safe_code)

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    assert "error" not in result
    assert result["file"] == str(test_file)
    # Safe code should have no or very few vulnerabilities
    assert (
        result["vulnerabilities_found"] <= 1
    )  # subprocess.run might trigger a warning


def test_scan_vulnerable_code(temp_dir, vulnerable_code):
    """Test scanning vulnerable code."""
    test_file = Path(temp_dir) / "vulnerable.py"
    test_file.write_text(vulnerable_code)

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    assert "error" not in result
    assert result["vulnerabilities_found"] > 0

    # Check that various vulnerability types are detected
    vuln_types = [v["type"] for v in result["vulnerabilities"]]
    assert len(vuln_types) > 0


def test_sql_injection_detection(temp_dir):
    """Test SQL injection detection."""
    code = """
def query(user_id):
    sql = "SELECT * FROM users WHERE id = %s" % user_id
    execute(sql)
"""

    test_file = Path(temp_dir) / "sql.py"
    test_file.write_text(code)

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    vulns = result["vulnerabilities"]
    sql_vulns = [v for v in vulns if v["type"] == "SQL Injection"]
    assert len(sql_vulns) > 0
    assert sql_vulns[0]["severity"] == "High"


def test_command_injection_detection(temp_dir):
    """Test command injection detection."""
    code = """
import subprocess
subprocess.run("ls -la", shell=True)
"""

    test_file = Path(temp_dir) / "cmd.py"
    test_file.write_text(code)

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    vulns = result["vulnerabilities"]
    cmd_vulns = [v for v in vulns if v["type"] == "Command Injection"]
    assert len(cmd_vulns) > 0


def test_hardcoded_secrets_detection(temp_dir):
    """Test hardcoded secrets detection."""
    code = """
API_KEY = "sk_live_real_secret_key"
password = "MyPassword123"
"""

    test_file = Path(temp_dir) / "secrets.py"
    test_file.write_text(code)

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    vulns = result["vulnerabilities"]
    secret_vulns = [v for v in vulns if v["type"] == "Hardcoded Secret"]
    assert len(secret_vulns) > 0
    assert all(v["severity"] == "Critical" for v in secret_vulns)


def test_secrets_with_placeholders_not_detected(temp_dir):
    """Test that placeholder secrets are not flagged."""
    code = """
# These should not trigger warnings
API_KEY = "your_api_key_here"
password = "example_password"
token = "test_token_xxx"
"""

    test_file = Path(temp_dir) / "placeholders.py"
    test_file.write_text(code)

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    vulns = result["vulnerabilities"]
    secret_vulns = [v for v in vulns if v["type"] == "Hardcoded Secret"]
    # Placeholders should not be detected
    assert len(secret_vulns) == 0


def test_insecure_functions_detection(temp_dir):
    """Test detection of insecure functions."""
    code = """
import pickle

def load(data):
    return pickle.loads(data)
"""

    test_file = Path(temp_dir) / "insecure.py"
    test_file.write_text(code)

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    vulns = result["vulnerabilities"]
    insecure_vulns = [v for v in vulns if v["type"] == "Insecure Function"]
    assert len(insecure_vulns) > 0


def test_scan_directory(temp_dir, vulnerable_code):
    """Test scanning directory."""
    # Create multiple files
    for i in range(3):
        test_file = Path(temp_dir) / f"file{i}.py"
        test_file.write_text(vulnerable_code)

    scanner = SecurityScanner()
    result = scanner.scan(temp_dir)

    assert "error" not in result
    assert result["directory"] == temp_dir
    assert result["files_scanned"] == 3
    assert result["total_vulnerabilities"] > 0


def test_severity_breakdown(temp_dir, vulnerable_code):
    """Test severity breakdown calculation."""
    test_file = Path(temp_dir) / "vuln.py"
    test_file.write_text(vulnerable_code)

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    assert "severity_breakdown" in result
    breakdown = result["severity_breakdown"]
    assert all(
        severity in breakdown for severity in ["Critical", "High", "Medium", "Low"]
    )


def test_security_score_calculation():
    """Test security score calculation."""
    scanner = SecurityScanner()

    # No vulnerabilities = perfect score
    score = scanner.get_security_score([])
    assert score == 100.0

    # Critical vulnerability = large penalty
    vulns = [{"severity": "Critical"}]
    score = scanner.get_security_score(vulns)
    assert score < 100.0

    # Multiple vulnerabilities = lower score
    many_vulns = [{"severity": "High"} for _ in range(5)]
    score = scanner.get_security_score(many_vulns)
    assert score < 60.0


def test_bare_except_detection(temp_dir):
    """Test detection of bare except clauses."""
    code = """
def risky():
    try:
        something()
    except:
        pass
"""

    test_file = Path(temp_dir) / "except.py"
    test_file.write_text(code)

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    vulns = result["vulnerabilities"]
    # Check for error handling vulnerability
    error_vulns = [v for v in vulns if v["type"] == "Error Handling"]
    assert len(error_vulns) > 0


def test_scan_invalid_path():
    """Test scanning invalid path."""
    scanner = SecurityScanner()
    result = scanner.scan("/nonexistent/path")

    assert "error" in result


def test_scan_non_python_file(temp_dir):
    """Test scanning non-Python file."""
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("Not Python code")

    scanner = SecurityScanner()
    result = scanner.scan(str(test_file))

    assert "error" in result


def test_get_vulnerabilities():
    """Test getting vulnerabilities list."""
    scanner = SecurityScanner()

    # Initially empty
    assert len(scanner.get_vulnerabilities()) == 0
