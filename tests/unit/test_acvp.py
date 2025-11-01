"""Tests for ACVP Client."""

import pytest
from civ_arcos.compliance.acvp import (
    ACVPClient,
    AlgorithmType,
    ValidationStatus,
    create_acvp_client,
)


def test_acvp_client_creation():
    """Test ACVP client can be created."""
    client = create_acvp_client()
    assert client is not None
    assert isinstance(client, ACVPClient)


def test_generate_sha_test_vectors():
    """Test generating SHA test vectors."""
    client = ACVPClient()
    
    vectors = client.generate_test_vectors(AlgorithmType.SHA, count=5)
    
    assert len(vectors) == 5
    assert all(v.algorithm == AlgorithmType.SHA for v in vectors)
    assert all(v.test_id.startswith("SHA_TEST_") for v in vectors)


def test_validate_sha():
    """Test SHA validation."""
    client = ACVPClient()
    
    # Test data
    data = b"test data"
    
    result = client.validate_sha(data, variant="SHA256")
    
    assert result.algorithm == AlgorithmType.SHA
    assert result.status == ValidationStatus.PASS
    assert result.actual_output is not None
    assert len(result.actual_output) == 64  # SHA256 produces 64 hex characters


def test_validate_sha_with_expected():
    """Test SHA validation with expected hash."""
    client = ACVPClient()
    
    data = b"test"
    # Pre-calculated SHA256 of "test"
    expected = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
    
    result = client.validate_sha(data, expected_hash=expected, variant="SHA256")
    
    assert result.status == ValidationStatus.PASS
    assert result.actual_output.lower() == expected.lower()


def test_validate_sha_mismatch():
    """Test SHA validation with mismatched hash."""
    client = ACVPClient()
    
    data = b"test"
    wrong_hash = "0" * 64
    
    result = client.validate_sha(data, expected_hash=wrong_hash, variant="SHA256")
    
    assert result.status == ValidationStatus.FAIL
    assert result.error_message == "Hash mismatch"


def test_validate_hmac():
    """Test HMAC validation."""
    client = ACVPClient()
    
    key = b"secret key"
    data = b"message"
    
    result = client.validate_hmac(key, data, variant="SHA256")
    
    assert result.algorithm == AlgorithmType.HMAC
    assert result.status == ValidationStatus.PASS
    assert result.actual_output is not None


def test_run_test_suite():
    """Test running complete test suite."""
    client = ACVPClient()
    
    results = client.run_test_suite(AlgorithmType.SHA)
    
    assert len(results) > 0
    assert all(r.algorithm == AlgorithmType.SHA for r in results)
    assert all(r.status in [ValidationStatus.PASS, ValidationStatus.FAIL] for r in results)


def test_certification_report():
    """Test generating certification report."""
    client = ACVPClient()
    
    # Run test suite first (no count parameter - uses default)
    client.run_test_suite(AlgorithmType.SHA)
    
    report = client.generate_certification_report(
        AlgorithmType.SHA,
        compliance_level="FIPS_140_2"
    )
    
    assert report.algorithm == AlgorithmType.SHA
    assert report.total_tests > 0
    assert report.passed_tests >= 0
    assert report.compliance_level == "FIPS_140_2"
    assert isinstance(report.certified, bool)


def test_export_test_session():
    """Test exporting test session data."""
    client = ACVPClient()
    
    # Run some tests
    client.generate_test_vectors(AlgorithmType.SHA, count=3)
    client.run_test_suite(AlgorithmType.SHA)
    
    session_data = client.export_test_session()
    
    assert 'acvpVersion' in session_data
    assert 'testVectors' in session_data
    assert 'validationResults' in session_data
    assert 'summary' in session_data
    assert session_data['summary']['totalTests'] > 0


def test_multiple_sha_variants():
    """Test different SHA variants."""
    client = ACVPClient()
    
    data = b"test"
    
    sha256_result = client.validate_sha(data, variant="SHA256")
    sha512_result = client.validate_sha(data, variant="SHA512")
    
    assert sha256_result.status == ValidationStatus.PASS
    assert sha512_result.status == ValidationStatus.PASS
    assert len(sha256_result.actual_output) == 64  # 256 bits / 4 bits per hex char
    assert len(sha512_result.actual_output) == 128  # 512 bits / 4 bits per hex char


def test_unsupported_algorithm_variant():
    """Test unsupported algorithm variant."""
    client = ACVPClient()
    
    data = b"test"
    result = client.validate_sha(data, variant="SHA999")
    
    assert result.status == ValidationStatus.ERROR
    assert "Unsupported" in result.error_message
