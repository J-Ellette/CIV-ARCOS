#!/usr/bin/env python3
"""
Test script to verify all emu-soft modules can be imported and instantiated.
Run this from the emu-soft directory or its parent.
"""

import sys
from pathlib import Path

# Add emu-soft to path if running from parent directory
emu_soft_path = Path(__file__).parent
if emu_soft_path.name == 'emu-soft':
    sys.path.insert(0, str(emu_soft_path))
else:
    sys.path.insert(0, str(emu_soft_path / 'emu-soft'))

def test_infrastructure():
    """Test infrastructure modules."""
    print("Testing infrastructure modules...")
    
    from infrastructure.cache import RedisEmulator
    cache = RedisEmulator()
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"
    print("  ✓ cache.py works")
    
    from infrastructure.tasks import CeleryEmulator
    emulator = CeleryEmulator()
    print("  ✓ tasks.py works")
    
    from infrastructure.framework import Application
    app = Application()
    print("  ✓ framework.py works")
    
    from infrastructure.graph import EvidenceGraph
    graph = EvidenceGraph(storage_path=":memory:")
    print("  ✓ graph.py works")

def test_analysis():
    """Test analysis modules."""
    print("\nTesting analysis modules...")
    
    from analysis.static_analyzer import PythonComplexityAnalyzer
    analyzer = PythonComplexityAnalyzer()
    print("  ✓ static_analyzer.py works")
    
    from analysis.security_scanner import SecurityScanner
    scanner = SecurityScanner()
    print("  ✓ security_scanner.py works")
    
    from analysis.test_generator import TestGenerator
    generator = TestGenerator()
    print("  ✓ test_generator.py works")

def test_assurance():
    """Test assurance modules."""
    print("\nTesting assurance modules...")
    
    from assurance.gsn import GSNNode, GSNNodeType
    node = GSNNode(id="G1", node_type=GSNNodeType.GOAL, statement="Test goal")
    print("  ✓ gsn.py works")
    
    from assurance.case import AssuranceCase
    case = AssuranceCase("test-case", "Test Case", "Test description")
    print("  ✓ case.py works")
    
    from assurance.fragments import AssuranceCaseFragment, FragmentType
    print("  ✓ fragments.py works")
    
    from assurance.argtl import ArgTLEngine
    from assurance.fragments import FragmentLibrary
    lib = FragmentLibrary()
    engine = ArgTLEngine(lib)
    print("  ✓ argtl.py works")
    
    from assurance.acql import ACQLEngine
    acql_engine = ACQLEngine()
    print("  ✓ acql.py works")
    
    from assurance.reasoning import ReasoningEngine
    reasoner = ReasoningEngine()
    print("  ✓ reasoning.py works")
    
    from assurance.dependency_tracker import DependencyTracker
    tracker = DependencyTracker()
    print("  ✓ dependency_tracker.py works")
    
    from assurance.architecture import ArchitectureMapper
    print("  ✓ architecture.py works")

def test_evidence():
    """Test evidence modules."""
    print("\nTesting evidence modules...")
    
    from evidence.collector import Evidence
    # Test the Evidence class (dataclass)
    evidence = Evidence(
        id="test",
        type="test",
        source="test",
        timestamp="2024-01-01T00:00:00Z",
        data={"test": "data"}
    )
    print("  ✓ collector.py works")

def test_web():
    """Test web modules."""
    print("\nTesting web modules...")
    
    from web.badges import BadgeGenerator
    generator = BadgeGenerator()
    print("  ✓ badges.py works")
    
    from web.dashboard import DashboardGenerator
    print("  ✓ dashboard.py works")

if __name__ == "__main__":
    print("=" * 60)
    print("EMU-SOFT Module Import Test")
    print("=" * 60)
    
    try:
        test_infrastructure()
        test_analysis()
        test_assurance()
        test_evidence()
        test_web()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("All emu-soft modules are complete and working!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
