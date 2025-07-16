# AOS Implementation Profiles

**Version:** 1.0
**Applies to:** AOS v4.1

---

## 1. The Principle of Proportionality

A one-size-fits-all methodology creates an impractical resource burden for smaller projects and lacks sufficient governance for large-scale programs. AOS v4.1 adopts the **Principle of Proportionality**, where the level of rigor, documentation, and tooling is proportional to the scale and complexity of the problem.

This is achieved through Implementation Profiles, which directly addresses Critique #18 (Resource Bottlenecks) by making the framework accessible and practical for all scales of work.

## 2. Phase 0: Triage & Scoping

Before the 5D Journey begins, every new initiative enters a mandatory "Phase 0: Triage & Scoping". During this phase, a quick assessment of the project's scale, risk, and uncertainty is performed to select one of three implementation profiles.

## 3. The Three Profiles

*   ### **AOS-Lite**
    *   **Use Case:** Small, simple tasks, proofs-of-concept, or projects in the "Clear" Cynefin domain.
    *   **PDP:** Uses a simplified, single-file "PDP-Lite" template that may bypass heavyweight analysis sections.
    *   **HMA Mapping:** Deploys a minimal HMA instance. It may use a single, combined Orchestrator/Capability plugin and an embedded database to reduce overhead.
    *   **Goal:** Rapid execution with minimal process overhead.

*   ### **AOS-Standard**
    *   **Use Case:** The default profile for significant, complex projects that require the full analytical and adaptive power of AOS.
    *   **PDP:** Uses the complete, unabridged PDP v4.1 specification.
    *   **HMA Mapping:** Deploys the full HMA architecture with a distinct Core, multiple L2 Orchestrator plugins for the 5D journey, and a suite of L3 Capability Plugins.
    *   **Goal:** Robust, resilient, and antifragile project delivery.

*   ### **AOS-Enterprise**
    *   **Use Case:** Large-scale, strategic programs of work that consist of multiple interconnected projects.
    *   **PDP:** Utilizes the full PDP v4.1 specification, but also introduces a new "Portfolio PDP" artifact that aggregates status and metrics from child PDPs.
    *   **HMA Mapping:** Deploys a federated HMA architecture. Includes additional plugins for enterprise concerns like advanced portfolio reporting, cross-project dependency management, and enterprise-wide risk aggregation.
    *   **Goal:** Strategic alignment and governance across a portfolio of complex initiatives. 
