## Appendices

### Appendix A: Semantic Ontology Core Classes

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix f: <https://framework.org/ontology/v4#> .

f:ProjectDefinitionPacket a owl:Class ;
    rdfs:label "Project Definition Packet" ;
    rdfs:comment "Immutable digital twin of a project or sub-project" .

f:StrategicContext a owl:Class ;
    rdfs:label "Strategic Context" ;
    rdfs:comment "Wardley Map position and primary constraint" .

f:AntifragileStrategy a owl:Class ;
    rdfs:label "Antifragile Strategy" ;
    rdfs:comment "Approach that gains from disorder" .

f:hasParentPDP a owl:ObjectProperty ;
    rdfs:domain f:ProjectDefinitionPacket ;
    rdfs:range f:ProjectDefinitionPacket ;
    rdfs:comment "Links child PDP to parent in fractal hierarchy" .

f:gainsFromVolatility a owl:ObjectProperty ;
    rdfs:domain f:AntifragileStrategy ;
    rdfs:range f:VolatilitySource ;
    rdfs:comment "Identifies sources of beneficial disorder" .

f:Successful a owl:Class ;
    rdfs:subClassOf f:ProjectOutcome ;
    rdfs:label "Successful Outcome" .

f:ProjectOutcome a owl:Class ;
    rdfs:label "Project Outcome" .

f:SuccessCriterion a owl:Class ;
    rdfs:label "Success Criterion" ;
    rdfs:comment "A specific, measurable, achievable, relevant, and time-bound success condition for a project." .

f:InheritanceMap a owl:Class ;
    rdfs:label "Inheritance Map" ;
    rdfs:comment "An artifact that explicitly documents the propagation of strategic context and constraints from a parent PDP to its children." .

f:PreMortemAnalysis a owl:Class ;
    rdfs:label "Pre-Mortem Analysis" ;
    rdfs:comment "An artifact capturing the results of a workshop designed to identify potential project failure modes before they occur." .

f:DelegationPolicy a owl:Class ;
    rdfs:label "Delegation of Authority Policy" ;
    rdfs:comment "Defines whether a human or an AI agent is the final authority for decision gates in the AOS process." .
```

# --- Additions for Problem & Tool Ontologies (C-1) ---

@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

f:Problem a owl:Class ;
    rdfs:label "Problem Instance" ;
    rdfs:comment "Represents a problem or sub-problem tackled by AOS." .

f:problem_domain a owl:DatatypeProperty ;
    rdfs:domain f:Problem ;
    rdfs:range xsd:string ;
    rdfs:comment "Domain of the problem (technical, business, social, etc.)." .

f:problem_complexity a owl:DatatypeProperty ;
    rdfs:domain f:Problem ;
    rdfs:range xsd:string ;
    rdfs:comment "Cynefin complexity classification." .

f:problem_nature a owl:DatatypeProperty ;
    rdfs:domain f:Problem ;
    rdfs:range xsd:string ;
    rdfs:comment "Nature such as invention, optimisation, analysis." .

f:Tool a owl:Class ;
    rdfs:label "Problem-Solving Tool" ;
    rdfs:comment "Any technique or capability plugin that can be applied to a problem." .

f:tool_phase_fit a owl:DatatypeProperty ;
    rdfs:domain f:Tool ;
    rdfs:range xsd:string ;
    rdfs:comment "Primary 5D Journey phase where the tool is usually invoked." .

f:tool_mechanism a owl:DatatypeProperty ;
    rdfs:domain f:Tool ;
    rdfs:range xsd:string ;
    rdfs:comment "Core mechanism, e.g., root_cause, contradiction_resolution." . 
