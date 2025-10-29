"""
Example demonstrating Step 2: Automated Test Evidence Generation
Shows how to use the analysis modules and API endpoints.
"""

from civ_arcos.analysis.static_analyzer import PythonComplexityAnalyzer
from civ_arcos.analysis.security_scanner import SecurityScanner
from civ_arcos.analysis.test_generator import TestGenerator
from civ_arcos.analysis.collectors import (
    StaticAnalysisCollector,
    SecurityScanCollector,
    ComprehensiveAnalysisCollector,
)
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import EvidenceStore


def demo_static_analysis():
    """Demonstrate static code analysis."""
    print("\n=== Static Analysis Demo ===")

    analyzer = PythonComplexityAnalyzer()
    
    # Analyze this file
    results = analyzer.analyze(__file__)
    
    print(f"File: {results['file']}")
    print(f"Lines of Code: {results['lines_of_code']}")
    print(f"Functions: {results['functions']}")
    print(f"Classes: {results['classes']}")
    print(f"Complexity: {results['complexity']}")
    print(f"Maintainability Index: {results['maintainability_index']:.2f}")
    print(f"Code Smells: {len(results['code_smells'])}")


def demo_security_scan():
    """Demonstrate security vulnerability scanning."""
    print("\n=== Security Scan Demo ===")

    scanner = SecurityScanner()
    
    # Scan this file
    results = scanner.scan(__file__)
    
    print(f"File: {results['file']}")
    print(f"Vulnerabilities Found: {results['vulnerabilities_found']}")
    
    if results['vulnerabilities_found'] > 0:
        print("\nVulnerabilities:")
        for vuln in results['vulnerabilities']:
            print(f"  - {vuln['type']}: {vuln['description']} (Line {vuln['line']})")
    else:
        print("No vulnerabilities found!")
    
    # Calculate security score
    score = scanner.get_security_score(results['vulnerabilities'])
    print(f"Security Score: {score}/100")


def demo_test_generation():
    """Demonstrate test case generation."""
    print("\n=== Test Generation Demo ===")

    generator = TestGenerator(use_ai=False)
    
    # Analyze this file
    results = generator.analyze_and_suggest(__file__)
    
    print(f"File: {results['source_file']}")
    print(f"Functions Found: {results['functions_found']}")
    print(f"Classes Found: {results['classes_found']}")
    print(f"Test Suggestions: {results['total_test_suggestions']}")
    
    # Show suggestions for first item
    if results['suggestions']:
        first = results['suggestions'][0]
        print(f"\nSample suggestion for {first['name']} ({first['type']}):")
        print(f"Suggested tests: {len(first['suggested_tests'])}")
        for test in first['suggested_tests'][:3]:
            print(f"  - {test}")


def demo_evidence_collection():
    """Demonstrate evidence collection and storage."""
    print("\n=== Evidence Collection Demo ===")

    # Create temporary storage
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage
        graph = EvidenceGraph(temp_dir)
        store = EvidenceStore(graph)
        
        # Collect static analysis evidence
        collector = StaticAnalysisCollector()
        evidence_list = collector.collect(__file__)
        
        print(f"Collected {len(evidence_list)} pieces of evidence")
        
        # Store evidence
        for evidence in evidence_list:
            evidence_id = store.store_evidence(evidence)
            print(f"Stored evidence: {evidence_id}")
            print(f"  Type: {evidence.type}")
            print(f"  Checksum: {evidence.checksum[:16]}...")
            
        # Verify integrity
        for evidence in evidence_list:
            is_valid = store.verify_integrity(evidence.id)
            print(f"Integrity check for {evidence.id}: {'PASS' if is_valid else 'FAIL'}")
            
    finally:
        # Clean up
        shutil.rmtree(temp_dir)


def demo_comprehensive_analysis():
    """Demonstrate comprehensive analysis with all modules."""
    print("\n=== Comprehensive Analysis Demo ===")

    collector = ComprehensiveAnalysisCollector()
    
    # Run all analyses
    evidence_list = collector.collect(__file__, run_coverage=False)
    
    print(f"Total Evidence Collected: {len(evidence_list)}")
    
    # Group by type
    by_type = {}
    for evidence in evidence_list:
        if evidence.type not in by_type:
            by_type[evidence.type] = []
        by_type[evidence.type].append(evidence)
    
    print("\nEvidence by type:")
    for evidence_type, items in by_type.items():
        print(f"  - {evidence_type}: {len(items)}")


def main():
    """Run all demos."""
    print("="*60)
    print("CIV-ARCOS Step 2: Automated Test Evidence Generation")
    print("="*60)
    
    demo_static_analysis()
    demo_security_scan()
    demo_test_generation()
    demo_evidence_collection()
    demo_comprehensive_analysis()
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)


if __name__ == "__main__":
    main()
