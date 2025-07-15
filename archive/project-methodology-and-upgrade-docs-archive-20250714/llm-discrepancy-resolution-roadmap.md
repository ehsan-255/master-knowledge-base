# Roadmap for LLM-Based Discrepancy Resolution in AOS V4.0

## 1. Hierarchical Roadmap
### Phase 1: PDP Schema Remediation (Foundational)
- Discrepancy: Critique Point 1 - Add Interaction Model.
- Discrepancy: Critique Point 11 - Add dual-domain support.
- Discrepancy: Critique Point 32 - Add fields for multiple hypotheses.

### Phase 2: 5D Journey Process Remediation (Depends on Phase 1)
- Discrepancy: Critique Point 1 - Add Integration Validation sub-phase.
- Discrepancy: Critique Point 11 - Implement hybrid responses.
- Discrepancy: Critique Point 25 - Add de-duplication logic.
- Discrepancy: Critique Point 26 - Parameterize limits.
- Discrepancy: Critique Point 32 - Implement parallel exploratory PDPs.

### Phase 3: Knowledge Graph Remediation (Parallel to Phase 2, Depends on Phase 1)
- Discrepancy: Critique Point 25 - Add overlap detection.
- Discrepancy: Critique Point 27 - Implement federated model.
- Discrepancy: Critique Point 29 - Add drift detection.
- Discrepancy: Critique Point 34 - Add trust scores.

### Phase 4: Metrics Remediation (Parallel to Phases 2-3)
- Discrepancy: Critique Point 30 - Add confidence intervals.

### Phase 5: HMA Integration (Depends on All Previous)
- Discrepancy: Missing federated graph.
- Discrepancy: Incomplete plugin lifecycle.
- Discrepancy: No security mechanisms.

## 2. Granular Task Decomposition
Each task includes atomic steps: read the file, specify exact edit location, provide precise code/markdown to insert, and reference the critique solution.

### Phase 1 Tasks
- **Task 1.1 (Critique 1)**: Use read_file on aos/02-pdp-digital-twin.md (entire file). Then edit_file to add 'interaction_model' object in the 'solution_architecture' section of the JSON-LD schema, after the 'antifragile_features' array. Insert: '"interaction_model": {"@type": "InteractionModel", "interactions": [{"from": "component1", "to": "component2", "type": "data_flow"}], "synergy_score": 0.85},'.
- **Task 1.2 (Critique 11)**: Use read_file on aos/02-pdp-digital-twin.md (entire file). Then edit_file to modify 'domain' in 'complexity_assessment' to support dual values, change to '"domain": {"@type": "CynefinDomain", "primary": "cynefin:Complex", "secondary": "cynefin:Complicated", "probability": 0.6},' after line 149.
- **Task 1.3 (Critique 32)**: Use read_file on aos/02-pdp-digital-twin.md (entire file). Then edit_file to add array 'hypotheses' in 'problem_definition', after 'hypothesis', insert: '"hypotheses": [{"belief": "Alt hypothesis 1", "confidence": 0.7}, {"belief": "Alt hypothesis 2", "confidence": 0.5}],'.

### Phase 2 Tasks
- **Task 2.1 (Critique 1)**: Use read_file on aos/03-enhanced-5d-journey.md (entire file). Then edit_file to add sub-phase in DESIGN procedure after line 69: 'integration_validation = orchestrator.invoke("L3-Integration-Validator-Plugin", {"action": "VALIDATE_SYNERGY", "params": synthesized_solutions}); IF integration_validation.score < 0.8: ESCALATE_FOR_REVIEW;'.
- **Task 2.2 (Critique 11)**: Use read_file on aos/03-enhanced-5d-journey.md (entire file). Then edit_file to modify DIAGNOSE after line 32: 'IF pdp.complexity_assessment.secondary: hybrid_response = GENERATE_HYBRID(pdp.complexity_assessment.primary, pdp.complexity_assessment.secondary); pdp.update({"response_type": hybrid_response});'.
- **Task 2.3 (Critique 25)**: Use read_file on aos/03-enhanced-5d-journey.md (entire file). Then edit_file to add after line 65 in DESIGN: 'deduped_solutions = orchestrator.invoke("L3-DeDuplication-Plugin", {"action": "DETECT_OVERLAPS", "params": solutions});'.
- **Task 2.4 (Critique 26)**: Use read_file on aos/05-implementation-architecture.md (lines 190-243 for config). Then edit_file to change 'adaptation_limit: 3' to 'adaptation_limit: "= ceil(log10(work_items)) * domain_factor"' after line 214.
- **Task 2.5 (Critique 32)**: Use read_file on aos/03-enhanced-5d-journey.md (entire file). Then edit_file to add in DEFINE after line 18: 'FOR hypothesis IN constraint_hypothesis.top_n(3): child_pdp = CREATE_EXPLORATORY_PDP(hypothesis); orchestrator.publish_event("ExploreHypothesis", {"pdp": child_pdp});'.

### Phase 3 Tasks
- **Task 3.1 (Critique 25)**: Use read_file on aos/04-knowledge-graph-ecosystem.md (entire file). Then edit_file to add after line 38 in add_pdp: 'overlaps = self.detect_overlaps(patterns); IF overlaps: FLAG_FOR_REVIEW(overlaps);'.
- **Task 3.2 (Critique 27)**: Use read_file on aos/04-knowledge-graph-ecosystem.md (entire file). Then edit_file to modify init to 'self.core_graph = SemanticGraph("core"); self.context_graphs = {};', and in add_pdp: 'IF is_core: self.core_graph.add(...); ELSE: self.get_context_graph(domain).add(...);' after line 10.
- **Task 3.3 (Critique 29)**: Use read_file on aos/04-knowledge-graph-ecosystem.md (entire file). Then edit_file to add in recommend_approach after line 66: 'IF self.detect_drift(): self.trigger_retraining();'.
- **Task 3.4 (Critique 34)**: Use read_file on aos/04-knowledge-graph-ecosystem.md (entire file). Then edit_file to add 'pattern["trust_score"] = 1.0 if audited else decay_score(pattern); IF pattern["trust_score"] < 0.7: IGNORE_PATTERN;' after line 41.

### Phase 4 Tasks
- **Task 4.1 (Critique 30)**: Use read_file on aos/06-metrics-and-evolution.md (entire file). Then edit_file to add to each metric, e.g., after 'target: "> 0.8"': ', "confidence_interval": "[0.75, 0.85]"' for all in sections 6.0-6.2.

### Phase 5 Tasks
- **Task 5.1 (HMA Discrepancy)**: Use read_file on aos/04-knowledge-graph-ecosystem.md (entire file). Then edit_file to add 'self.federated_query = FederatedSPARQLEngine(["remote_graph1", "remote_graph2"]);' in init, and modify strategic_query to use federated_query after line 53.
- **Task 5.2 (HMA Discrepancy)**: Use read_file on aos/05-implementation-architecture.md (entire file). Then edit_file to add lifecycle in HMA section after line 230: 'core.register_plugin(plugin_id, version); core.activate_plugin(plugin_id); core.deactivate_plugin(plugin_id);'.
- **Task 5.3 (HMA Discrepancy)**: Use read_file on aos/05-implementation-architecture.md (entire file). Then edit_file to add after line 230: '"security": {"credential_broker": "Centralized", "trust_boundaries": ["L2-Core", "L3-Plugins"]},'.

## 3. Task Dependencies
- Phase 1 must complete before Phases 2, 3, 5 (schema used in processes/KG/HMA).
- Phase 4 is independent but should follow Phase 1 for consistency.
- Phase 5 depends on all others for full integration.

## 4. Final Ordered Action Sequence
1. Execute Task 1.1
2. Execute Task 1.2
3. Execute Task 1.3
4. Execute Task 2.1
5. Execute Task 2.2
6. Execute Task 2.3
7. Execute Task 2.4
8. Execute Task 2.5
9. Execute Task 3.1
10. Execute Task 3.2
11. Execute Task 3.3
12. Execute Task 3.4
13. Execute Task 4.1
14. Execute Task 5.1
15. Execute Task 5.2
16. Execute Task 5.3
17. Verify all changes: Use read_file on each modified file (aos/02-pdp-digital-twin.md, aos/03-enhanced-5d-journey.md, aos/04-knowledge-graph-ecosystem.md, aos/05-implementation-architecture.md, aos/06-metrics-and-evolution.md) and confirm all added elements match specifications.
18. Run validations: Use grep_search for key terms (e.g., 'interaction_model', 'trust_score') to ensure presence; If any missing, reapply edits. 