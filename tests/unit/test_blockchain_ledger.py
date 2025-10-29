"""
Unit tests for blockchain evidence ledger.
"""

import pytest
from civ_arcos.distributed.blockchain_ledger import (
    EvidenceLedger,
    Block,
    BlockValidator,
    Validator,
)


def test_ledger_creation():
    """Test creating an evidence ledger."""
    ledger = EvidenceLedger(difficulty=2)
    assert len(ledger.chain) == 1  # Genesis block
    assert ledger.chain[0].index == 0
    assert ledger.chain[0].previous_hash == "0"
    assert ledger.difficulty == 2


def test_genesis_block():
    """Test genesis block properties."""
    ledger = EvidenceLedger()
    genesis = ledger.chain[0]
    
    assert genesis.index == 0
    assert genesis.previous_hash == "0"
    assert len(genesis.evidence) == 1
    assert genesis.evidence[0]["type"] == "genesis"
    assert genesis.hash == genesis.calculate_hash()


def test_add_evidence_block():
    """Test adding evidence to blockchain."""
    ledger = EvidenceLedger(difficulty=1)
    
    evidence = [
        {"type": "test", "data": {"result": "passed"}},
        {"type": "coverage", "data": {"percentage": 85}},
    ]
    
    block = ledger.add_evidence_block(evidence)
    
    assert block.index == 1
    assert len(block.evidence) == 2
    assert block.previous_hash == ledger.chain[0].hash
    assert len(ledger.chain) == 2


def test_add_evidence_to_pending():
    """Test adding evidence to pending queue."""
    ledger = EvidenceLedger()
    
    ledger.add_evidence_to_pending({"type": "test", "data": {}})
    ledger.add_evidence_to_pending({"type": "security", "data": {}})
    
    assert len(ledger.pending_evidence) == 2
    
    block = ledger.add_evidence_block()
    assert len(block.evidence) == 2
    assert len(ledger.pending_evidence) == 0


def test_block_hash_calculation():
    """Test block hash calculation."""
    block = Block(
        index=1,
        timestamp="2023-01-01T00:00:00Z",
        evidence=[{"type": "test"}],
        previous_hash="prev123",
        nonce=0,
    )
    
    hash1 = block.calculate_hash()
    hash2 = block.calculate_hash()
    
    assert hash1 == hash2  # Hash should be deterministic
    assert len(hash1) == 64  # SHA256 produces 64 hex characters


def test_block_mining():
    """Test proof of work mining."""
    ledger = EvidenceLedger(difficulty=2)
    
    evidence = [{"type": "test", "data": {}}]
    block = ledger.add_evidence_block(evidence)
    
    # Block hash should start with required number of zeros
    assert block.hash.startswith("0" * ledger.difficulty)
    assert block.nonce > 0  # Should have tried some nonces


def test_validate_evidence_chain():
    """Test blockchain validation."""
    ledger = EvidenceLedger(difficulty=1)
    
    # Add several blocks
    for i in range(3):
        ledger.add_evidence_block([{"type": f"test{i}", "data": {}}])
    
    validation = ledger.validate_evidence_chain()
    assert validation["is_valid"] is True
    assert validation["total_blocks"] == 4  # Genesis + 3 new
    assert len(validation["errors"]) == 0


def test_detect_tampering():
    """Test detecting tampered blocks."""
    ledger = EvidenceLedger(difficulty=1)
    ledger.add_evidence_block([{"type": "test", "data": {}}])
    
    # Tamper with a block
    ledger.chain[1].evidence.append({"type": "fake", "data": {}})
    
    tampered = ledger.detect_tampering()
    assert len(tampered) == 1
    assert tampered[0]["block_index"] == 1


def test_get_block():
    """Test getting a block by index."""
    ledger = EvidenceLedger(difficulty=1)
    ledger.add_evidence_block([{"type": "test", "data": {}}])
    
    block = ledger.get_block(1)
    assert block is not None
    assert block.index == 1
    
    missing = ledger.get_block(999)
    assert missing is None


def test_get_latest_block():
    """Test getting the latest block."""
    ledger = EvidenceLedger(difficulty=1)
    
    latest = ledger.get_latest_block()
    assert latest.index == 0  # Genesis
    
    ledger.add_evidence_block([{"type": "test", "data": {}}])
    latest = ledger.get_latest_block()
    assert latest.index == 1


def test_search_evidence():
    """Test searching for evidence in blockchain."""
    ledger = EvidenceLedger(difficulty=1)
    
    ledger.add_evidence_block([
        {"type": "test", "data": {"name": "test1"}},
        {"type": "security", "data": {"vuln": 0}},
    ])
    ledger.add_evidence_block([
        {"type": "test", "data": {"name": "test2"}},
    ])
    
    # Search all
    all_results = ledger.search_evidence()
    assert len(all_results) >= 3  # At least our 3 evidence items
    
    # Search by type
    test_results = ledger.search_evidence("test")
    assert len(test_results) == 2
    assert all(r["evidence"]["type"] == "test" for r in test_results)


def test_search_evidence_limit():
    """Test search limit parameter."""
    ledger = EvidenceLedger(difficulty=1)
    
    for i in range(5):
        ledger.add_evidence_block([{"type": "test", "data": {"num": i}}])
    
    results = ledger.search_evidence(limit=3)
    assert len(results) <= 3


def test_get_chain_info():
    """Test getting blockchain information."""
    ledger = EvidenceLedger(difficulty=2)
    
    ledger.add_evidence_block([{"type": "test", "data": {}}])
    ledger.add_evidence_to_pending({"type": "pending", "data": {}})
    
    info = ledger.get_chain_info()
    assert info["total_blocks"] == 2  # Genesis + 1
    assert info["total_evidence"] >= 2
    assert info["pending_evidence"] == 1
    assert info["difficulty"] == 2


def test_export_chain():
    """Test exporting the blockchain."""
    ledger = EvidenceLedger(difficulty=1)
    ledger.add_evidence_block([{"type": "test", "data": {}}])
    
    exported = ledger.export_chain()
    assert len(exported) == 2  # Genesis + 1
    assert all(isinstance(b, dict) for b in exported)
    assert all("index" in b and "hash" in b for b in exported)


def test_block_validator():
    """Test block validator."""
    validator = BlockValidator(min_validators=2)
    
    v1 = validator.add_validator("v1", "pubkey1", 100.0)
    validator.add_validator("v2", "pubkey2", 100.0)  # noqa: F841
    
    assert len(validator.validators) == 2
    assert isinstance(v1, Validator)
    assert v1.stake == 100.0


def test_block_validator_duplicate():
    """Test adding duplicate validator raises error."""
    validator = BlockValidator()
    validator.add_validator("v1", "pubkey1")
    
    with pytest.raises(ValueError, match="already exists"):
        validator.add_validator("v1", "pubkey2")


def test_validate_block_structure():
    """Test validating block structure."""
    validator = BlockValidator()
    
    block = Block(
        index=1,
        timestamp="2023-01-01T00:00:00Z",
        evidence=[{"type": "test"}],
        previous_hash="prev123",
        nonce=0,
    )
    block.hash = block.calculate_hash()
    
    result = validator.validate_block(block)
    assert result["is_valid"] is True
    assert len(result["errors"]) == 0


def test_validate_block_invalid_hash():
    """Test detecting invalid block hash."""
    validator = BlockValidator()
    
    block = Block(
        index=1,
        timestamp="2023-01-01T00:00:00Z",
        evidence=[{"type": "test"}],
        previous_hash="prev123",
        nonce=0,
        hash="invalid_hash",
    )
    
    result = validator.validate_block(block)
    assert result["is_valid"] is False
    assert "Block hash mismatch" in result["errors"]


def test_validate_block_chain_link():
    """Test validating block chain linkage."""
    validator = BlockValidator()
    
    prev_block = Block(
        index=0,
        timestamp="2023-01-01T00:00:00Z",
        evidence=[{"type": "genesis"}],
        previous_hash="0",
        nonce=0,
    )
    prev_block.hash = prev_block.calculate_hash()
    
    curr_block = Block(
        index=1,
        timestamp="2023-01-01T00:01:00Z",
        evidence=[{"type": "test"}],
        previous_hash=prev_block.hash,
        nonce=0,
    )
    curr_block.hash = curr_block.calculate_hash()
    
    result = validator.validate_block(curr_block, prev_block)
    assert result["is_valid"] is True


def test_validate_block_wrong_previous_hash():
    """Test detecting wrong previous hash."""
    validator = BlockValidator()
    
    prev_block = Block(
        index=0,
        timestamp="2023-01-01T00:00:00Z",
        evidence=[{"type": "genesis"}],
        previous_hash="0",
        nonce=0,
    )
    prev_block.hash = prev_block.calculate_hash()
    
    curr_block = Block(
        index=1,
        timestamp="2023-01-01T00:01:00Z",
        evidence=[{"type": "test"}],
        previous_hash="wrong_hash",
        nonce=0,
    )
    curr_block.hash = curr_block.calculate_hash()
    
    result = validator.validate_block(curr_block, prev_block)
    assert result["is_valid"] is False
    assert "Previous hash mismatch" in result["errors"]


def test_validator_consensus():
    """Test validator consensus mechanism."""
    validator = BlockValidator(min_validators=3)
    
    # Add validators
    validator.add_validator("v1", "key1", 100.0)
    validator.add_validator("v2", "key2", 100.0)
    validator.add_validator("v3", "key3", 100.0)
    
    # Submit validations
    block_hash = "block123"
    validator.submit_validation(block_hash, "v1", True)
    validator.submit_validation(block_hash, "v2", True)
    
    # Not enough validators
    result = validator.check_consensus(block_hash)
    assert result["has_consensus"] is False
    
    # Add third validator
    validator.submit_validation(block_hash, "v3", True)
    result = validator.check_consensus(block_hash)
    assert result["has_consensus"] is True


def test_validator_consensus_with_stake():
    """Test consensus weighted by stake."""
    validator = BlockValidator(min_validators=3)
    
    # Add validators with different stakes
    validator.add_validator("v1", "key1", 100.0)
    validator.add_validator("v2", "key2", 50.0)
    validator.add_validator("v3", "key3", 50.0)
    
    block_hash = "block123"
    
    # V1 (high stake) says invalid, others say valid
    validator.submit_validation(block_hash, "v1", False)
    validator.submit_validation(block_hash, "v2", True)
    validator.submit_validation(block_hash, "v3", True)
    
    result = validator.check_consensus(block_hash)
    # 100/(100+50+50) = 0.5 valid stake, needs 0.66
    assert result["has_consensus"] is False


def test_remove_validator():
    """Test removing a validator."""
    validator = BlockValidator()
    validator.add_validator("v1", "key1")
    
    assert validator.remove_validator("v1") is True
    assert len(validator.validators) == 0
    assert validator.remove_validator("v1") is False


def test_get_evidence_by_hash():
    """Test getting evidence by its hash."""
    ledger = EvidenceLedger(difficulty=1)
    
    evidence = {"type": "test", "data": {"unique": "value123"}}
    ledger.add_evidence_block([evidence])
    
    import hashlib
    import json
    evidence_str = json.dumps(evidence, sort_keys=True)
    evidence_hash = hashlib.sha256(evidence_str.encode()).hexdigest()
    
    result = ledger.get_evidence_by_hash(evidence_hash)
    assert result is not None
    assert result["evidence"]["type"] == "test"
    assert result["block_index"] == 1


def test_block_to_dict():
    """Test converting block to dictionary."""
    block = Block(
        index=1,
        timestamp="2023-01-01T00:00:00Z",
        evidence=[{"type": "test"}],
        previous_hash="prev123",
        nonce=42,
        hash="hash123",
    )
    
    block_dict = block.to_dict()
    assert block_dict["index"] == 1
    assert block_dict["nonce"] == 42
    assert block_dict["hash"] == "hash123"
    assert isinstance(block_dict["evidence"], list)


def test_validator_to_dict():
    """Test converting validator to dictionary."""
    validator = Validator(
        validator_id="v1",
        public_key="key123",
        stake=100.0,
        reputation=0.95,
    )
    
    validator_dict = validator.to_dict()
    assert validator_dict["validator_id"] == "v1"
    assert validator_dict["stake"] == 100.0
    assert validator_dict["reputation"] == 0.95
