## Appendices

### Appendix A: Semantic Ontology Core Classes

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix f: <https://framework.org/ontology/v3#> .

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
``` 