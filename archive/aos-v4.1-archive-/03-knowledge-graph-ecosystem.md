## Part III: The Knowledge Graph Ecosystem

### 4.1 Graph Architecture

```python
class EnterpriseKnowledgeGraph:
    """
    Queryable semantic graph connecting all projects, learnings, and strategic assets

    Implements solution from Critique 19 (Scalability Issues): Adds GraphLifecyclePolicy for data tiers and PDP Summary nodes for aggregation.
    Implements solution from Critique 34 (KG Corruption) and Critique 17 (AI Perfection):
    - All patterns have a validation_status: [Hypothesized, Tested, Validated, Deprecated].
    - All AI-generated artifacts must include source_attribution (Citable AI principle).
    - All data entering the KG must pass SHACL validation gates.
    - The recommendation engine only recommends Validated patterns by default.
    """
    def __init__(self):
        self.core_graph = SemanticGraph("core"); self.context_graphs = {};
        self.reasoner = OWLReasoner()
        self.query_engine = SPARQLEngine()
        self.federated_query = FederatedSPARQLEngine(["remote_graph1", "remote_graph2"]);
        self.graph_lifecycle_policy = GraphLifecyclePolicy()  # hot/warm/cold tiers
    
    def add_pdp(self, pdp: ImmutablePDP):
        """Add a PDP and all its relationships to the graph"""
        # Create PDP Summary node for aggregation
        summary_node = self.create_pdp_summary(pdp)
        self.graph.add_node(summary_node.id, summary_node.to_jsonld())
        
        # Add full PDP node to appropriate tier
        self.graph.add_node(pdp.id, pdp.to_jsonld(), tier='hot')
        
        # Connect to strategic elements
        self.link_to_wardley_components(pdp)
        self.link_to_constraints(pdp)
        self.link_to_capabilities(pdp)
        
        # Connect to organizational elements
        self.link_to_teams(pdp)
        self.link_to_technologies(pdp)
        self.link_to_business_outcomes(pdp)
        
        # Extract and store patterns
        patterns = self.extract_patterns(pdp)
        for pattern in patterns:
            pattern['validation_status'] = pattern.get('validation_status', 'Hypothesized')
            pattern['source_attribution'] = pattern.get('source_attribution', 'AI-generated, human-validated')
            self.store_patterns([pattern])
        # Enforce SHACL validation gate
        if not self.reasoner.validate(pdp):
            raise ValueError('PDP failed SHACL validation and cannot be added to the knowledge graph.')
        overlaps = self.detect_overlaps(patterns); IF overlaps: FLAG_FOR_REVIEW(overlaps);
    
    def strategic_query(self, sparql: str) -> QueryResult:
        """Execute strategic queries across the enterprise"""
        return self.federated_query.execute(sparql)
    
    def recommend_approach(self, new_problem: str, exploration_factor: float = 0.2) -> 'Recommendations':
        """
        AI-powered recommendation based on historical patterns.
        Implements solutions for Critique 44 (Bias), 45 (Homogenization), and 6 (Hasty Generalization).
        - Uses an epsilon-greedy style "exploration bonus" to test novel patterns.
        - Promotes "Strategic Diversity" by presenting alternatives, not just the "best" one.
        """
        # With probability epsilon (exploration_factor), recommend a novel/experimental pattern
        if random.random() < exploration_factor:
            experimental_patterns = self.find_patterns_by_status(['Hypothesized', 'Tested'])
            if experimental_patterns:
                return self.generate_recommendations({
                    'primary': None,
                    'experimental': random.choice(experimental_patterns),
                    'alternatives': []
                })

        # Otherwise, exploit known successful patterns
        similar_projects = self.find_similar_projects(new_problem)
        all_patterns = self.analyze_success_patterns(similar_projects)
        
        validated_patterns = [p for p in all_patterns if p.get('validation_status') == 'Validated']
        
        if not validated_patterns:
            return self.generate_recommendations({'primary': None, 'experimental': None, 'alternatives': []})
            
IF self.detect_drift(): self.trigger_retraining();
            
        # Select the best validated pattern as primary, and others as alternatives
        primary_recommendation = max(validated_patterns, key=lambda p: p.get('success_score', 0))
        alternative_recommendations = [p for p in validated_patterns if p != primary_recommendation]
        
        return self.generate_recommendations({
            'primary': primary_recommendation,
            'alternatives': alternative_recommendations,
            'experimental': None
        })

    def create_pdp_summary(self, pdp: ImmutablePDP) -> PDPSummary:
        """Create summary node for PDP aggregation"""
        return PDPSummary(pdp)  # Implementation details omitted
```

### 4.2 Strategic Query Examples

```
```

### 4.3 Problem & Tool Ontologies  <!-- NEW INTEGRATION C-1 -->

AOS v4.1 now formalises two lightweight ontologies that live inside the Enterprise Knowledge Graph:

* **Problem Ontology** – captures key attributes required for intelligent plugin selection.
  - `f:problem_domain` (e.g., technical, business, social)
  - `f:problem_complexity` (clear, complicated, complex, chaotic)
  - `f:problem_nature` (invention, optimisation, diagnosis, design, analysis)
  - `f:primary_constraints` (array of constraint IRIs)

* **Tool Ontology** – describes any technique, capability plugin or external service.
  - `f:tool_phase_fit` (define, diagnose, design, develop, deliver)
  - `f:tool_mechanism` (root_cause, contradiction_resolution, brainstorming, etc.)
  - `f:required_inputs`
  - `f:preferred_complexity`

These classes allow the Rule-Based Adapter (see Implementation Architecture) to run SPARQL queries such as:  
`SELECT ?tool WHERE { ?tool f:tool_phase_fit "design" ; f:tool_mechanism "contradiction_resolution" . }`

All existing PDPs SHOULD be back-filled with `problem_domain`, `problem_complexity`, and `problem_nature` properties during normal evolution.

### LLM Provenance Metadata  <!-- LLM INTEGRATION -->

Each node produced by an LLM-driven plugin MUST include:

| Property | Description |
|----------|-------------|
| `f:generatedByModel` | model identifier (e.g., gpt-4o, llama3-8b-local) |
| `f:promptHash` | SHA-256 hash of the system+user prompt to guarantee reproducibility |
| `f:promptTokenCount` / `f:completionTokenCount` | usage metrics for cost tracking |
| `f:temperature` | sampling temperature used |
| `f:llmLatencyMs` | round-trip latency captured via ObservabilityPort |

These properties satisfy audit requirements and enable future cost/quality analytics.
