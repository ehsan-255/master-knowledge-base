# Option Stub Policy

**Version:** 1.0
**Applies to:** AOS v4.0

---

## 1. The Challenge of Maintaining Optionality

A core tenet of antifragility is the maintenance of strategic options. However, the overhead of creating and maintaining a full Project Digital Twin (PDP) for every potential option can be prohibitive, discouraging the very practice the framework intends to promote.

This policy addresses Critique #12 (Antifragile Optionality vs. Digital Twins) from `aos-upgrade.md` by introducing a low-cost mechanism for representing and managing strategic options.

## 2. "Option Stubs": Lightweight Placeholders

AOS v4.0 introduces the concept of an **"Option Stub"** (or a "Lightweight PDP"). This is a minimal, lightweight artifact that acts as a placeholder for a strategic option that has been identified but not yet pursued.

## 3. Structure of an Option Stub

An Option Stub is not a full PDP. It contains only the decision-critical metadata required to evaluate the option at a strategic level, such as:

*   **`optionId`**: A unique identifier.
*   **`description`**: A brief, plain-language summary of the option.
*   **`triggerConditions`**: The specific conditions under which this option might be activated.
*   **`estimatedCost`**: A rough order of magnitude cost to implement.
*   **`potentialPayoff`**: The potential benefit or value if activated.
*   **`confidenceScore`**: A score representing the confidence in the estimated costs and payoffs.

## 4. Lifecycle: Instantiation on Activation

Option Stubs are managed within the Knowledge Graph as distinct entities. A full, heavyweight PDP is only created and instantiated from an Option Stub if and when a formal decision is made to activate that option.

This "instantiate on activation" approach provides the best of both worlds:

*   **Maintains Optionality:** Allows the system to track dozens or hundreds of potential strategic paths at a very low administrative and computational cost.
*   **Ensures Traceability:** When an option is activated, the newly created PDP is explicitly linked back to its originating Option Stub, preserving the full strategic lineage. 