"""
Blockchain Evidence Ledger implementation.
Provides immutable evidence records with cryptographic proof of authenticity.
"""

import hashlib
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field


@dataclass
class Block:
    """Represents a block in the evidence blockchain."""

    index: int
    timestamp: str
    evidence: List[Dict[str, Any]]
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "evidence": self.evidence,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }

    def calculate_hash(self) -> str:
        """
        Calculate the hash of the block.

        Returns:
            SHA256 hash of block contents
        """
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "evidence": self.evidence,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


@dataclass
class Validator:
    """Represents a validator node in the network."""

    validator_id: str
    public_key: str
    stake: float = 0.0
    reputation: float = 1.0
    joined_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert validator to dictionary."""
        return {
            "validator_id": self.validator_id,
            "public_key": self.public_key,
            "stake": self.stake,
            "reputation": self.reputation,
            "joined_at": self.joined_at,
        }


class BlockValidator:
    """
    Validator for blockchain blocks.
    Ensures blocks are properly formed and evidence is valid.
    """

    def __init__(self, min_validators: int = 3):
        """
        Initialize block validator.

        Args:
            min_validators: Minimum number of validators required
        """
        self.min_validators = min_validators
        self.validators: Dict[str, Validator] = {}
        self.pending_validations: Dict[str, List[Dict[str, Any]]] = {}

    def add_validator(
        self,
        validator_id: str,
        public_key: str,
        stake: float = 0.0,
    ) -> Validator:
        """
        Add a validator to the network.

        Args:
            validator_id: Unique identifier for validator
            public_key: Public key for validation
            stake: Amount staked by validator

        Returns:
            Created validator
        """
        if validator_id in self.validators:
            raise ValueError(f"Validator {validator_id} already exists")

        validator = Validator(
            validator_id=validator_id,
            public_key=public_key,
            stake=stake,
        )
        self.validators[validator_id] = validator
        return validator

    def remove_validator(self, validator_id: str) -> bool:
        """Remove a validator from the network."""
        if validator_id in self.validators:
            del self.validators[validator_id]
            return True
        return False

    def validate_block(
        self, block: Block, previous_block: Optional[Block] = None
    ) -> Dict[str, Any]:
        """
        Validate a block's structure and contents.

        Args:
            block: Block to validate
            previous_block: Previous block in chain (if any)

        Returns:
            Dictionary with validation result
        """
        errors = []

        # Check block hash
        calculated_hash = block.calculate_hash()
        if block.hash != calculated_hash:
            errors.append("Block hash mismatch")

        # Check previous hash matches
        if previous_block:
            if block.previous_hash != previous_block.hash:
                errors.append("Previous hash mismatch")
            if block.index != previous_block.index + 1:
                errors.append("Block index not sequential")

        # Check evidence is present
        if not block.evidence:
            errors.append("Block has no evidence")

        # Check timestamp is valid
        try:
            datetime.fromisoformat(block.timestamp.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            errors.append("Invalid timestamp format")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
        }

    def submit_validation(
        self, block_hash: str, validator_id: str, is_valid: bool
    ) -> None:
        """
        Submit a validation vote for a block.

        Args:
            block_hash: Hash of block being validated
            validator_id: ID of validator submitting vote
            is_valid: Whether block is considered valid
        """
        if validator_id not in self.validators:
            raise ValueError(f"Validator {validator_id} not registered")

        if block_hash not in self.pending_validations:
            self.pending_validations[block_hash] = []

        validation = {
            "validator_id": validator_id,
            "is_valid": is_valid,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.pending_validations[block_hash].append(validation)

    def check_consensus(self, block_hash: str) -> Dict[str, Any]:
        """
        Check if consensus has been reached for a block.

        Args:
            block_hash: Hash of block to check

        Returns:
            Dictionary with consensus status
        """
        if block_hash not in self.pending_validations:
            return {
                "has_consensus": False,
                "reason": "No validations submitted",
                "votes": 0,
            }

        validations = self.pending_validations[block_hash]
        if len(validations) < self.min_validators:
            return {
                "has_consensus": False,
                "reason": f"Insufficient validators ({len(validations)}/{self.min_validators})",
                "votes": len(validations),
            }

        # Calculate weighted consensus based on stake
        total_stake = sum(
            self.validators[v["validator_id"]].stake
            for v in validations
            if v["validator_id"] in self.validators
        )
        valid_stake = sum(
            self.validators[v["validator_id"]].stake
            for v in validations
            if v["is_valid"] and v["validator_id"] in self.validators
        )

        # If no stake, use simple majority
        if total_stake == 0:
            valid_votes = sum(1 for v in validations if v["is_valid"])
            agreement = valid_votes / len(validations)
        else:
            agreement = valid_stake / total_stake

        has_consensus = agreement >= 0.66  # 2/3 majority

        return {
            "has_consensus": has_consensus,
            "agreement": agreement,
            "votes": len(validations),
            "validations": validations,
        }


class EvidenceLedger:
    """
    Blockchain ledger for immutable evidence records.
    Implements distributed validation and cryptographic proof.
    """

    def __init__(self, difficulty: int = 2):
        """
        Initialize evidence ledger.

        Args:
            difficulty: Mining difficulty (number of leading zeros required)
        """
        self.chain: List[Block] = []
        self.pending_evidence: List[Dict[str, Any]] = []
        self.validators: BlockValidator = BlockValidator()
        self.difficulty = difficulty

        # Create genesis block
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        """Create the genesis (first) block in the chain."""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            evidence=[{"type": "genesis", "data": "CIV-ARCOS Evidence Ledger"}],
            previous_hash="0",
            nonce=0,
        )
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def add_evidence_to_pending(self, evidence: Dict[str, Any]) -> None:
        """
        Add evidence to pending queue for next block.

        Args:
            evidence: Evidence to add
        """
        self.pending_evidence.append(evidence)

    def add_evidence_block(
        self, evidence_batch: Optional[List[Dict[str, Any]]] = None
    ) -> Block:
        """
        Create and add a new block with evidence.

        Args:
            evidence_batch: Optional batch of evidence to include.
                           If None, uses pending evidence.

        Returns:
            Created and added block
        """
        if evidence_batch is None:
            evidence_batch = self.pending_evidence
            self.pending_evidence = []

        if not evidence_batch:
            raise ValueError("No evidence to add to block")

        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now(timezone.utc).isoformat(),
            evidence=evidence_batch,
            previous_hash=previous_block.hash,
            nonce=0,
        )

        # Mine the block (proof of work)
        self._mine_block(new_block)

        # Validate before adding
        validation_result = self.validators.validate_block(new_block, previous_block)
        if not validation_result["is_valid"]:
            raise ValueError(f"Block validation failed: {validation_result['errors']}")

        self.chain.append(new_block)
        return new_block

    def _mine_block(self, block: Block) -> None:
        """
        Mine a block by finding a valid hash with required difficulty.

        Args:
            block: Block to mine
        """
        target = "0" * self.difficulty
        while True:
            block.hash = block.calculate_hash()
            if block.hash.startswith(target):
                break
            block.nonce += 1

    def validate_evidence_chain(self) -> Dict[str, Any]:
        """
        Validate the entire evidence chain.

        Returns:
            Dictionary with validation result
        """
        errors = []

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Validate current block
            validation_result = self.validators.validate_block(
                current_block, previous_block
            )
            if not validation_result["is_valid"]:
                errors.append(
                    {
                        "block_index": i,
                        "errors": validation_result["errors"],
                    }
                )

        return {
            "is_valid": len(errors) == 0,
            "total_blocks": len(self.chain),
            "errors": errors,
        }

    def get_block(self, index: int) -> Optional[Block]:
        """
        Get a block by its index.

        Args:
            index: Index of block to retrieve

        Returns:
            Block if found, None otherwise
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain."""
        return self.chain[-1]

    def search_evidence(
        self, evidence_type: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search for evidence in the blockchain.

        Args:
            evidence_type: Optional filter by evidence type
            limit: Maximum number of results

        Returns:
            List of evidence entries
        """
        results = []
        for block in reversed(self.chain):
            for evidence in block.evidence:
                if evidence_type is None or evidence.get("type") == evidence_type:
                    results.append(
                        {
                            "evidence": evidence,
                            "block_index": block.index,
                            "block_hash": block.hash,
                            "timestamp": block.timestamp,
                        }
                    )
                    if len(results) >= limit:
                        return results
        return results

    def get_chain_info(self) -> Dict[str, Any]:
        """Get information about the blockchain."""
        total_evidence = sum(len(block.evidence) for block in self.chain)
        return {
            "total_blocks": len(self.chain),
            "total_evidence": total_evidence,
            "pending_evidence": len(self.pending_evidence),
            "latest_block_hash": self.chain[-1].hash if self.chain else None,
            "difficulty": self.difficulty,
            "validators": len(self.validators.validators),
        }

    def detect_tampering(self) -> List[Dict[str, Any]]:
        """
        Detect any tampering in the blockchain.

        Returns:
            List of tampered blocks
        """
        tampered = []
        for i, block in enumerate(self.chain):
            calculated_hash = block.calculate_hash()
            if block.hash != calculated_hash:
                tampered.append(
                    {
                        "block_index": i,
                        "stored_hash": block.hash,
                        "calculated_hash": calculated_hash,
                    }
                )
        return tampered

    def export_chain(self) -> List[Dict[str, Any]]:
        """Export the entire blockchain as a list of dictionaries."""
        return [block.to_dict() for block in self.chain]

    def get_evidence_by_hash(self, evidence_hash: str) -> Optional[Dict[str, Any]]:
        """
        Get evidence by its hash.

        Args:
            evidence_hash: Hash of evidence to find

        Returns:
            Evidence and block info if found, None otherwise
        """
        for block in self.chain:
            for evidence in block.evidence:
                # Calculate evidence hash
                evidence_str = json.dumps(evidence, sort_keys=True)
                ev_hash = hashlib.sha256(evidence_str.encode()).hexdigest()
                if ev_hash == evidence_hash:
                    return {
                        "evidence": evidence,
                        "block_index": block.index,
                        "block_hash": block.hash,
                        "timestamp": block.timestamp,
                    }
        return None
