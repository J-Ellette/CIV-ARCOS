"""
Unit tests for Quantum-Resistant Security module.
"""

import pytest
from civ_arcos.core.quantum_security import (
    QuantumResistantSecurity,
    QuantumSignature,
    LatticeKey,
)


def test_quantum_security_initialization():
    """Test creating quantum-resistant security instance."""
    qrs = QuantumResistantSecurity(security_level=256)
    assert qrs.security_level == 256
    assert len(qrs.signatures) == 0
    assert len(qrs.keys) == 0


def test_post_quantum_crypto():
    """Test post-quantum cryptography implementation."""
    qrs = QuantumResistantSecurity()
    data = b"sensitive evidence data"

    result = qrs.implement_post_quantum_crypto(data)

    assert "encrypted_data" in result
    assert "key_id" in result
    assert result["algorithm"] == "lattice-based-ntru-like"
    assert result["security_level"] == 256
    assert "timestamp" in result


def test_quantum_resistant_sign():
    """Test quantum-resistant digital signature."""
    qrs = QuantumResistantSecurity()
    data = b"evidence to sign"

    signature = qrs.quantum_resistant_sign(data)

    assert isinstance(signature, QuantumSignature)
    assert signature.signature
    assert signature.public_key
    assert signature.algorithm == "dilithium-like"
    assert signature.timestamp
    assert "key_id" in signature.metadata
    assert signature.metadata["security_level"] == 256


def test_verify_quantum_signature():
    """Test verifying quantum-resistant signature."""
    qrs = QuantumResistantSecurity()
    data = b"evidence to verify"

    # Create signature
    signature = qrs.quantum_resistant_sign(data)

    # Verify signature
    is_valid = qrs.verify_quantum_signature(data, signature)
    assert is_valid is True


def test_future_proof_authentication():
    """Test future-proof evidence authentication."""
    qrs = QuantumResistantSecurity()
    evidence_id = "test_evidence_001"
    evidence_data = {"type": "test_coverage", "value": 95.5}

    auth_proof = qrs.future_proof_authentication(evidence_id, evidence_data)

    assert auth_proof["evidence_id"] == evidence_id
    assert "signature" in auth_proof
    assert auth_proof["signature"]["algorithm"] == "dilithium-like"
    assert "integrity_hash" in auth_proof
    assert auth_proof["quantum_resistant"] is True
    assert auth_proof["security_level"] == 256


def test_quantum_enhanced_analysis():
    """Test quantum-enhanced analysis for pattern recognition."""
    qrs = QuantumResistantSecurity()
    patterns = [
        {"type": "code_quality", "score": 85, "anomaly": False},
        {"type": "security", "vulnerability": "SQL injection", "severity": "high"},
        {"type": "performance", "latency": 100, "anomaly": True},
    ]

    result = qrs.quantum_enhanced_analysis(patterns)

    assert "patterns_detected" in result
    assert "threat_analysis" in result
    assert result["optimization_quality"] == "quantum-enhanced"
    assert result["algorithm"] == "quantum-inspired"
    assert "analysis_timestamp" in result


def test_quantum_threat_detection():
    """Test quantum-enhanced threat detection."""
    qrs = QuantumResistantSecurity()
    patterns = [
        {"anomaly": True, "severity": "high"},
        {"security": "vulnerability", "type": "XSS"},
        {"normal": "operation"},
    ]

    result = qrs.quantum_enhanced_analysis(patterns)
    threat_analysis = result["threat_analysis"]

    assert "threat_level" in threat_analysis
    assert "threat_score" in threat_analysis
    assert "indicators" in threat_analysis
    assert threat_analysis["quantum_optimization_applied"] is True


def test_lattice_key_generation():
    """Test lattice-based key generation."""
    qrs = QuantumResistantSecurity()
    key = qrs._generate_lattice_key()

    assert isinstance(key, LatticeKey)
    assert key.dimension == 512
    assert key.modulus == 2048
    assert key.algorithm == "ntru-like"
    assert key.key_data
    assert key.created_at


def test_encrypt_with_reuse_key():
    """Test encryption with key reuse."""
    qrs = QuantumResistantSecurity()
    data1 = b"first data"
    data2 = b"second data"

    # First encryption creates key
    result1 = qrs.implement_post_quantum_crypto(data1)
    key_id = result1["key_id"]

    # Second encryption reuses key
    result2 = qrs.implement_post_quantum_crypto(data2, key_id=key_id)

    assert result2["key_id"] == key_id
    assert result1["encrypted_data"] != result2["encrypted_data"]


def test_sign_with_reuse_key():
    """Test signing with key reuse."""
    qrs = QuantumResistantSecurity()
    data1 = b"first message"
    data2 = b"second message"

    # First signature creates key
    sig1 = qrs.quantum_resistant_sign(data1)
    key_id = sig1.metadata["key_id"]

    # Second signature reuses key
    sig2 = qrs.quantum_resistant_sign(data2, private_key_id=key_id)

    assert sig2.metadata["key_id"] == key_id
    assert sig1.signature != sig2.signature
    assert sig1.public_key == sig2.public_key


def test_quantum_pattern_matching():
    """Test quantum pattern matching algorithm."""
    qrs = QuantumResistantSecurity()
    patterns = [
        {"complexity": 50, "features": 10},
        {"complexity": 100, "features": 20},
        {"complexity": 25, "features": 5},
    ]

    detected = qrs._quantum_pattern_matching(patterns)

    assert isinstance(detected, list)
    for pattern in detected:
        assert "pattern" in pattern
        assert "quantum_score" in pattern
        assert "confidence" in pattern
        assert 0 <= pattern["quantum_score"] <= 1
        assert 0 <= pattern["confidence"] <= 100


def test_quantum_score_calculation():
    """Test quantum score calculation."""
    qrs = QuantumResistantSecurity()
    pattern1 = {"key1": "value1", "key2": "value2"}
    pattern2 = {"key1": "value1"}

    score1 = qrs._calculate_quantum_score(pattern1)
    score2 = qrs._calculate_quantum_score(pattern2)

    assert 0 <= score1 <= 1
    assert 0 <= score2 <= 1
    # More complex pattern should typically have higher score
    assert score1 != score2


def test_signature_storage():
    """Test signature storage in quantum security."""
    qrs = QuantumResistantSecurity()
    data = b"test data"

    sig1 = qrs.quantum_resistant_sign(data)
    sig2 = qrs.quantum_resistant_sign(data)

    # Both signatures should be stored
    assert len(qrs.signatures) == 2


def test_key_storage():
    """Test key storage in quantum security."""
    qrs = QuantumResistantSecurity()
    data = b"test data"

    result1 = qrs.implement_post_quantum_crypto(data)
    result2 = qrs.implement_post_quantum_crypto(data)

    # Both keys should be stored
    assert len(qrs.keys) == 2


def test_derive_public_key():
    """Test public key derivation from private key."""
    qrs = QuantumResistantSecurity()
    private_key = qrs._generate_lattice_key()

    public_key = qrs._derive_public_key(private_key)

    assert isinstance(public_key, str)
    assert len(public_key) == 64  # SHA256 hex digest


def test_security_levels():
    """Test different security levels."""
    qrs128 = QuantumResistantSecurity(security_level=128)
    qrs256 = QuantumResistantSecurity(security_level=256)
    qrs512 = QuantumResistantSecurity(security_level=512)

    assert qrs128.security_level == 128
    assert qrs256.security_level == 256
    assert qrs512.security_level == 512


def test_empty_pattern_analysis():
    """Test quantum analysis with empty patterns."""
    qrs = QuantumResistantSecurity()
    patterns = []

    result = qrs.quantum_enhanced_analysis(patterns)

    assert "patterns_detected" in result
    assert len(result["patterns_detected"]) == 0
    assert "threat_analysis" in result


def test_large_data_encryption():
    """Test encryption with large data."""
    qrs = QuantumResistantSecurity()
    large_data = b"x" * 10000

    result = qrs.implement_post_quantum_crypto(large_data)

    assert "encrypted_data" in result
    assert result["encrypted_data"]


def test_multiple_authentications():
    """Test multiple evidence authentications."""
    qrs = QuantumResistantSecurity()

    auth1 = qrs.future_proof_authentication("ev1", {"data": "test1"})
    auth2 = qrs.future_proof_authentication("ev2", {"data": "test2"})

    assert auth1["evidence_id"] != auth2["evidence_id"]
    assert auth1["integrity_hash"] != auth2["integrity_hash"]
