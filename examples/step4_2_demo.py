"""
Step 4.2 Demo: Advanced ARCOS Methodologies

Demonstrates the integration of:
- CertGATE (Fragments, ArgTL, ACQL)
- CLARISSA (Reasoning Engine)
- A-CERT (Architecture Mapping)
- CAID-tools (Dependency Tracking)
"""

from civ_arcos.assurance import (
    FragmentLibrary,
    ArgTLEngine,
    ACQLEngine,
    ACQLQuery,
    QueryType,
    ReasoningEngine,
    ArchitectureMapper,
    DependencyTracker,
    ResourceType,
    DependencyType,
)


def main():
    print("=" * 60)
    print("Step 4.2: Advanced ARCOS Methodologies Demo")
    print("=" * 60)

    # 1. Create Fragments (CertGATE)
    print("\n1. Creating Assurance Case Fragments...")
    library = FragmentLibrary()

    auth_fragment = library.create_from_pattern("component_security", "AuthModule")
    api_fragment = library.create_from_pattern("component_quality", "APIModule")
    db_fragment = library.create_from_pattern("component_quality", "DatabaseModule")

    print(f"   ✓ Created 3 fragments")
    print(f"   - Auth: {len(auth_fragment.nodes)} nodes")
    print(f"   - API: {len(api_fragment.nodes)} nodes")
    print(f"   - DB: {len(db_fragment.nodes)} nodes")

    # 2. Link Evidence
    print("\n2. Linking Evidence...")
    for evidence_type in list(auth_fragment.required_evidence_types)[:2]:
        auth_fragment.link_evidence(f"evidence_{evidence_type}", evidence_type)

    assessment = auth_fragment.assess_strength()
    print(f"   ✓ Auth fragment strength: {assessment['strength_score']:.2f}")
    print(f"   ✓ Completeness: {assessment['completeness_score']:.2f}")

    # 3. Compose Fragments (ArgTL)
    print("\n3. Composing Fragments with ArgTL...")
    engine = ArgTLEngine(library)

    composed = engine.compose(
        [auth_fragment.fragment_id, api_fragment.fragment_id, db_fragment.fragment_id],
        "system_assurance",
        "hierarchical",
    )

    print(f"   ✓ Composed fragment created")
    print(f"   ✓ Total nodes: {len(composed.nodes)}")

    # Link fragments
    engine.link_fragments(
        api_fragment.fragment_id, db_fragment.fragment_id, "Database API interface"
    )
    print(f"   ✓ Linked API → Database")

    # 4. Query with ACQL
    print("\n4. Querying with ACQL...")
    acql = ACQLEngine()

    # Check completeness
    completeness = acql.execute_query(
        ACQLQuery(QueryType.COMPLETENESS), fragment=composed
    )
    print(
        f"   ✓ Completeness check: {'✓ PASS' if completeness['complete'] else '✗ FAIL'}"
    )

    # Check for weaknesses
    weaknesses = acql.execute_query(
        ACQLQuery(QueryType.WEAKNESSES), fragment=composed
    )
    print(f"   ✓ Found {weaknesses['weakness_count']} weaknesses")

    # 5. Reason about the Case (CLARISSA)
    print("\n5. Reasoning with CLARISSA...")
    reasoning = ReasoningEngine()

    # Create evidence context
    context = {
        "test_coverage": 88.0,
        "tests_pass": True,
        "branch_coverage": 82.0,
        "static_scan_complete": True,
        "critical_issues": 0,
        "high_issues": 1,
    }

    # Assemble case for reasoning
    case = engine.assemble_case(
        [composed.fragment_id], "system_case", "System Assurance Case"
    )

    result = reasoning.reason_about_case(case, context)
    print(f"   ✓ Applicable theories: {len(result['applicable_theories'])}")
    print(f"   ✓ Active defeaters: {len(result['active_defeaters'])}")
    print(f"   ✓ Confidence score: {result['confidence_score']:.2f}")
    print(f"   ✓ Indefeasible: {result['indefeasible']}")

    # Risk estimation
    risk = reasoning.estimate_risk(case, context)
    print(f"   ✓ Risk level: {risk['risk_level']}")

    # 6. Track Dependencies (CAID-tools)
    print("\n6. Tracking Dependencies...")
    tracker = DependencyTracker()

    # Register resources
    auth_res = tracker.register_resource(
        ResourceType.FRAGMENT, "AuthModule", "auth_fragment", "arcos"
    )
    api_res = tracker.register_resource(
        ResourceType.FRAGMENT, "APIModule", "api_fragment", "arcos"
    )
    db_res = tracker.register_resource(
        ResourceType.FRAGMENT, "DatabaseModule", "db_fragment", "arcos"
    )

    # Link dependencies
    tracker.link_resources(api_res, db_res, DependencyType.REQUIRES, "API uses DB")
    tracker.link_resources(
        auth_res, api_res, DependencyType.VALIDATES, "Auth validates API"
    )

    # Impact analysis
    impact = tracker.generate_impact_analysis(db_res)
    print(f"   ✓ Database changes impact {impact['impacted_count']} resources")

    stats = tracker.get_statistics()
    print(f"   ✓ Tracked: {stats['total_resources']} resources, {stats['total_dependencies']} dependencies")

    # 7. Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"✓ Created {len(library.fragments)} fragments from patterns")
    print(f"✓ Composed into system with {len(composed.nodes)} argument nodes")
    print(f"✓ ACQL found {weaknesses['weakness_count']} weaknesses to address")
    print(f"✓ Reasoning engine confidence: {result['confidence_score']:.2f}")
    print(f"✓ Risk level: {risk['risk_level']}")
    print(f"✓ Tracked {stats['total_resources']} resources with {stats['total_dependencies']} dependencies")
    print("\n🎉 Step 4.2 Advanced ARCOS Methodologies - COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
