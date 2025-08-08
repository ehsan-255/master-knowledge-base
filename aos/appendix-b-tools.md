### Appendix B: Tool Ecosystem

```yaml
recommended_tools:
  strategic_layer:
    - name: "OnlineWardleyMaps"
      purpose: "Collaborative Wardley Mapping"
    - name: "TOC Thinking Processes"
      purpose: "Constraint analysis tools"
      
  semantic_infrastructure:
    - name: "Apache Jena"
      purpose: "RDF/SPARQL processing"
    - name: "TopBraid"
      purpose: "SHACL validation"
      
  orchestration:
    - name: "Camunda"
      purpose: "BPMN orchestration"
    - name: "Kogito"
      purpose: "Cloud-native business automation"
      
  knowledge_graph:
    - name: "Neo4j"
      purpose: "Graph database"
    - name: "Stardog"
      purpose: "Semantic graph with reasoning"

  taxonomy:
    - name: "Generic Problem-Solving Toolkit"
      purpose: "Starter library of lightweight L3 plugins implementing classic techniques such as 5-Whys, Fishbone Diagram, SCAMPER, Decision Matrix, Impact/Effort Matrix, Critical Path Method, etc."
    - name: "RequirementsClarifier-LLM"
      purpose: "Uses an LLM Q&A chain to refine acceptance criteria; returns JSON patch for PDP."
    - name: "Brainstorm-LLM"
      purpose: "LLM generates SCAMPER and mind-map option lists tagged with novelty scores."
    - name: "DecisionMatrix-LLM"
      purpose: "LLM reasons over candidate options, fills a weighted decision matrix, and justifies scores."
    - name: "WBS-LLM"
      purpose: "LLM converts clarified requirements into a work-breakdown structure (max depth 3)."
    - name: "CodeStub-LLM"
      purpose: "LLM scaffolds boilerplate code or scripts requested by other plugins; output verified by linter."
    - name: "AIDeciderPlugin"
      purpose: "Acts as an autonomous AI agent to make decisions at governance gates when operating in FullAutonomy mode."
    - name: "TriageAnalysisLLMPlugin"
      purpose: "Parses unstructured user requests to infer initial project parameters and recommend a profile."
    - name: "StrategicAuditLLMPlugin"
      purpose: "Audits generated strategic artifacts against the initial problem statement for inconsistencies."
    - name: "HistoricalContextLLMPlugin"
      purpose: "Queries the Knowledge Graph for historical precedents to augment human sense-making."
    - name: "RetrospectiveLLMPlugin"
      purpose: "Generates a concise project summary from the final PDP's telemetry and event log."
    - name: "WorstCaseSimulationPlugin"
      purpose: "Runs probabilistic worst-case simulations (e.g., Monte Carlo) for volatility sources to quantify risks and losses."
    - name: "MetricsAuditorPlugin"
      purpose: "LLM-based auditing of metrics for objectivity and tamper-proof verification."
``` 
