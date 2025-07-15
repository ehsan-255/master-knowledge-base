# HMA Traceability and Context Propagation

**Version:** 1.0
**Applies to:** AOS v4.0

---

## 1. The Challenge of a Distributed System

Moving from a monolithic architecture to a distributed, plugin-based system like HMA introduces a challenge: ensuring a clear, unbroken line of sight from high-level strategic intent down to the smallest execution detail.

This document outlines the conceptual mechanisms used in AOS v4.0 to ensure end-to-end traceability and the correct propagation of context, addressing Critiques #21 (Strategy-to-Execution Gaps) and #24 (Integration and Inheritance Gaps).

## 2. The Correlation ID

Every request that enters the HMA system via an L1 Adapter is assigned a unique **`CorrelationId`**.

*   This ID is attached to all subsequent events, logs, and telemetry generated during the processing of that request.
*   It is passed from the Core to L2 Orchestrator Plugins and L3 Capability Plugins with every invocation.
*   This allows for the complete reconstruction of a request's journey across multiple distributed components, which is essential for debugging and observability.

## 3. The Inheritance Map (Context Propagation)

To ensure strategic alignment during fractal decomposition, a formal **`InheritanceMap`** is passed down from a parent PDP to its children.

*   **Mechanism:** When an L2 Orchestrator Plugin executes the `DEVELOP` phase and creates child PDPs, it is responsible for creating and attaching an `InheritanceMap` to each child.
*   **Content:** This map is an object that contains critical context from the parent, such as:
    *   `parent_pdp_id`: The ID of the parent PDP.
    *   `parent_primary_constraint`: The primary constraint identified in the parent's strategic analysis, which serves as a guiding principle for the child.
    *   `parent_value_anchors`: The high-level business KPIs the parent is aligned with.
*   **Enforcement:** The Core's Control Plane provides a service for validating these maps, and the Knowledge Graph ontology includes relationships to formally link child nodes to their parents via this inherited context. This directly implements the "Constraint Propagation" solution from Critique #8.

## 4. Bridging Artifacts and the Knowledge Graph

Traceability is not just for runtime. The Knowledge Graph itself serves as the master traceability tool.

*   **Traceability Matrices:** The graph schema will explicitly define relationships that create traceability matrices, linking strategic goals (`f:ValueAnchor`) to solution options (`aos:OptionStub`), to activated PDPs, to decomposed child PDPs, and finally to execution work items.
*   **Conflict Resolution Engine:** When an L2 Orchestrator reconciles conflicting outputs from multiple L3 plugins (Critique #22), it logs the conflict, the chosen resolution, and the rationale as a formal "ReconciliationEvent" in the Knowledge Graph, preserving a complete decision history. 