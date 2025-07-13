# Hexagonal Microkernel Architecture (HMA) Specification

_Version 1.3 (C4-Inspired Edition)_

**(Companion document to the AI-Powered Model-Driven Development (APMDD) Methodology v2.0)**

---

**Table of Contents (Revised for C4-Inspired Structure)**

## Part LP - LLM Primers
- [[HMA v1.3 - Part LP - Story Guide]]
- [[HMA v1.3 - Part LP - Fact Sheet]]

**Part 1: HMA Overview and Architectural Context (Analogous to C4 Level 1 - System Context)**
*   [[HMA v1.3 - Part 1 - Overview and Context#Abstract|Abstract]]
*   [[HMA v1.3 - Part 1 - Overview and Context#1. Introduction to HMA|1. Introduction to HMA]]
    *   [[HMA v1.3 - Part 1 - Overview and Context#1.1 Purpose of the HMA Specification|1.1 Purpose of the HMA Specification]]
    *   [[HMA v1.3 - Part 1 - Overview and Context#1.2 Relationship to APMDD Methodology|1.2 Relationship to APMDD Methodology]]
    *   [[HMA v1.3 - Part 1 - Overview and Context#1.3 Core Problems HMA Solves|1.3 Core Problems HMA Solves]]
*   [[HMA v1.3 - Part 1 - Overview and Context#2. HMA Core Philosophy and Guiding Architectural Principles|2. HMA Core Philosophy and Guiding Architectural Principles]]
    *   [[HMA v1.3 - Part 1 - Overview and Context#2.1 Synthesizing Hexagonal, Microkernel, and EDA|2.1 Synthesizing Hexagonal, Microkernel, and EDA]]
    *   [[HMA v1.3 - Part 1 - Overview and Context#2.2 Key HMA Architectural Principles (APMDD Aligned)|2.2 Key HMA Architectural Principles (APMDD Aligned)]]
*   [[HMA v1.3 - Part 1 - Overview and Context#3. Foundational HMA Concepts at a Glance|3. Foundational HMA Concepts at a Glance]]
    *   [[HMA v1.3 - Part 1 - Overview and Context#3.1 Core|3.1 Core]]
    *   [[HMA v1.3 - Part 1 - Overview and Context#3.2 Plugin (Capability & Orchestrator)|3.2 Plugin (Capability & Orchestrator)]]
    *   [[HMA v1.3 - Part 1 - Overview and Context#3.3 Port & Adapter|3.3 Port & Adapter]]
    *   [[HMA v1.3 - Part 1 - Overview and Context#3.4 Event & Event Bus|3.4 Event & Event Bus]]

**Part 2: HMA High-Level Structure: Layers & Major Zones (Analogous to C4 Level 2 - Containers)**
*   [[HMA v1.3 - Part 2 - High-Level Structure#4. HMA Macro-Architecture: The Layered Reference Model|4. HMA Macro-Architecture: The Layered Reference Model]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#4.1 Overview of L0-L4 Layers|4.1 Overview of L0-L4 Layers]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#4.2 Diagram: HMA Layered Reference Model & Major Zones|4.2 Diagram: HMA Layered Reference Model & Major Zones]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#4.3 Interaction Flow Between Layers|4.3 Interaction Flow Between Layers]]
*   [[HMA v1.3 - Part 2 - High-Level Structure#5. The HMA Microkernel Core Zone (L2): Role & Responsibilities|5. The HMA Microkernel Core Zone (L2): Role & Responsibilities]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#5.1 Core's Minimalist Mandate|5.1 Core's Minimalist Mandate]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#5.2 Core's Boundaries and Interactions with other Zones|5.2 Core's Boundaries and Interactions with other Zones]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#5.3 Diagram: Core Zone Context|5.3 Diagram: Core Zone Context]]
*   [[HMA v1.3 - Part 2 - High-Level Structure#6. HMA Plugins Zone (L3 Capability & L2 Orchestrator): Autonomy & Roles|6. HMA Plugins Zone (L3 Capability & L2 Orchestrator): Autonomy & Roles]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#6.1 L3 Capability Plugins: Encapsulating Business Logic|6.1 L3 Capability Plugins: Encapsulating Business Logic]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#6.2 L2 Orchestrator Plugins: Coordinating Complex Workflows|6.2 L2 Orchestrator Plugins: Coordinating Complex Workflows]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#6.3 Plugin Zone Boundaries and Interactions|6.3 Plugin Zone Boundaries and Interactions]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#6.4 Diagram: Plugin Zone Context|6.4 Diagram: Plugin Zone Context]]
*   [[HMA v1.3 - Part 2 - High-Level Structure#7. Primary HMA Interaction Patterns (High-Level)|7. Primary HMA Interaction Patterns (High-Level)]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#7.1 Direct Synchronous Request/Response (via Core to Plugin)|7.1 Direct Synchronous Request/Response (via Core to Plugin)]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#7.2 Asynchronous Event-Driven Communication|7.2 Asynchronous Event-Driven Communication]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#7.3 Orchestrated Multi-Plugin Workflows|7.3 Orchestrated Multi-Plugin Workflows]]
    *   [[HMA v1.3 - Part 2 - High-Level Structure#7.4 Diagram: Key Interaction Patterns Overview|7.4 Diagram: Key Interaction Patterns Overview]]

**Part 3: HMA Internal Components & Key Interfaces (Analogous to C4 Level 3 - Components)**
*   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#8. Deeper Dive: Microkernel Core Components (L2)|8. Deeper Dive: Microkernel Core Components (L2)]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#8.1 Request Router/Dispatcher Component|8.1 Request Router/Dispatcher Component]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#8.2 Plugin Lifecycle Manager Component|8.2 Plugin Lifecycle Manager Component]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#8.3 Control Plane Service Components|8.3 Control Plane Service Components]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#8.4 Diagram: Core Internal Components|8.4 Diagram: Core Internal Components]]
*   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9. Deeper Dive: Generic Plugin Components (L3 & L2 Orchestrator)|9. Deeper Dive: Generic Plugin Components (L3 & L2 Orchestrator)]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9.1 Defining Ports (Inbound/Outbound)|9.1 Defining Ports (Inbound/Outbound)]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9.2 Implementing Adapters (Driving/Driven)|9.2 Implementing Adapters (Driving/Driven)]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9.3 Encapsulating Internal Logic and State|9.3 Encapsulating Internal Logic and State]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9.4 Plugin's Interaction with L4 Infrastructure (via its Adapters)|9.4 Plugin's Interaction with L4 Infrastructure (via its Adapters)]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9.5 Diagram: Generic Plugin Internal Structure|9.5 Diagram: Generic Plugin Internal Structure]]
*   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#10. Standard HMA Port Types & Their Purpose|10. Standard HMA Port Types & Their Purpose]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#10.1 PluginExecutionPort|10.1 PluginExecutionPort]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#10.2 CredBrokerQueryPort|10.2 CredBrokerQueryPort]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#10.3 EventBusPort|10.3 EventBusPort]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#10.4 ObservabilityPort|10.4 ObservabilityPort]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#10.5 Other Common Port Types|10.5 Other Common Port Types]]
*   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#11. HMA Plugin Lifecycle Management (Detailed)|11. HMA Plugin Lifecycle Management (Detailed)]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#11.1 Plugin States and Transitions|11.1 Plugin States and Transitions]]
    *   [[HMA v1.3 - Part 3 - Internal Components and Interfaces#11.2 Technical Compliance for Plugins|11.2 Technical Compliance for Plugins]]

**Part 4: HMA Detailed Specifications, Standards, & Implementation Guidance (Analogous to C4 Level 4 - Code/Classes)**
*   [[HMA v1.3 - Part 4 - Detailed Specifications and Standards#12. Port & API Design Standards|12. Port & API Design Standards]]
    *   [[HMA v1.3 - Part 4 - Detailed Specifications and Standards#12.1 Interface Contract Rules|12.1 Interface Contract Rules]]
    *   [[HMA v1.3 - Part 4 - Detailed Specifications and Standards#12.2 Versioning Strategies|12.2 Versioning Strategies]]
*   [[HMA v1.3 - Part 4 - Detailed Specifications and Standards#13. Event Design & Schema Standards|13. Event Design & Schema Standards]]
    *   [[HMA v1.3 - Part 4 - Detailed Specifications and Standards#13.1 Event Payload Structure and Schemas|13.1 Event Payload Structure and Schemas]]
    *   [[HMA v1.3 - Part 4 - Detailed Specifications and Standards#13.2 Standard Event Metadata|13.2 Standard Event Metadata]]
    *   [[HMA v1.3 - Part 4 - Detailed Specifications and Standards#13.3 Event Versioning|13.3 Event Versioning]]
*   [[HMA v1.3 - Part 4 - Detailed Specifications and Standards#14. HMA Naming Conventions|14. HMA Naming Conventions]]
*   [[HMA v1.3 - Part 4 - Detailed Specifications and Standards#15. Rule Syntax (RFC 2119)|15. Rule Syntax (RFC 2119)]]

**Part 5: Applying Cross-Cutting HMA Concerns**
*   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#16. HMA Observability Implementation|16. HMA Observability Implementation]]
    *   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#16.1 Observability Principles in HMA|16.1 Observability Principles in HMA]]
    *   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#16.2 Observability Requirements (Tracing, Metrics, Logging)|16.2 Observability Requirements (Tracing, Metrics, Logging)]]
    *   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#16.3 Conceptual Data Flow & Instrumentation|16.3 Conceptual Data Flow & Instrumentation]]
*   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#17. HMA Security Implementation|17. HMA Security Implementation]]
    *   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#17.1 Trust Boundaries in HMA|17.1 Trust Boundaries in HMA]]
    *   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#17.2 Mandatory Security Controls|17.2 Mandatory Security Controls]]
    *   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#17.3 Threat Model Considerations for HMA Structures|17.3 Threat Model Considerations for HMA Structures]]
*   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#18. HMA Enforcement Mechanisms & Tooling|18. HMA Enforcement Mechanisms & Tooling]]
    *   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#18.1 Static Analysis (hma-lint Concept)|18.1 Static Analysis (hma-lint Concept)]]
    *   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#18.2 Runtime Policy Enforcement|18.2 Runtime Policy Enforcement]]
    *   [[HMA v1.3 - Part 5 - Cross-Cutting Concerns#18.3 Plugin Registry Validation|18.3 Plugin Registry Validation]]

**Part 6: Supporting Information**
*   [[HMA v1.3 - Part 6 - Supporting Information#19. HMA Glossary|19. HMA Glossary]]
*   [[HMA v1.3 - Part 6 - Supporting Information#20. HMA Comparative Analysis & Trade-offs|20. HMA Comparative Analysis & Trade-offs]]
    *   [[HMA v1.3 - Part 6 - Supporting Information#20.1 HMA vs. Alternatives (Architectural Focus)|20.1 HMA vs. Alternatives (Architectural Focus)]]
    *   [[HMA v1.3 - Part 6 - Supporting Information#20.2 Key HMA v1.3 Trade-offs|20.2 Key HMA v1.3 Trade-offs]]
*   [[HMA v1.3 - Part 6 - Supporting Information#21. Appendices (Illustrative Examples)|21. Appendices (Illustrative Examples)]]
    *   [[HMA v1.3 - Part 6 - Supporting Information#21.1 Appendix A: Example Interaction Flow - RAG Query (Illustrative)|21.1 Appendix A: Example Interaction Flow - RAG Query (Illustrative)]]
    *   [[HMA v1.3 - Part 6 - Supporting Information#21.2 Appendix B: HMA Implementation Examples (Diagrams)|21.2 Appendix B: HMA Implementation Examples (Diagrams)]]
*   [[HMA v1.3 - Part 6 - Supporting Information#22. HMA Diagram Index|22. HMA Diagram Index]]

---

**End of Table of Contents**
