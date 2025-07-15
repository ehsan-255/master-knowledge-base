# AOS Changelog

## Version 4.1

**Release Date:** 2025-07-15

### 🚀 Architectural Enhancements

*   **Refactored to Composable Phase Orchestrator Model:** This is the cornerstone change for version 4.1. The previous monolithic `5D-Journey-Orchestrator` has been deprecated and replaced with a more flexible and architecturally pure model.
    *   **New Components:** Introduced a minimal L2 `Meta-Orchestrator` (`Process-Router`) and distinct L2 `Phase Orchestrators` for each stage of a process (e.g., `DefinePhaseOrchestrator`).
    *   **Rationale:** This change was made to achieve a better separation of concerns in alignment with HMA principles. It enhances flexibility by allowing different process "recipes" to be executed, and it simplifies development by breaking down a large, complex component into smaller, single-responsibility units. This directly addresses architectural feedback regarding the potential rigidity and blurred responsibilities of the v4.0 model.

### 📝 Documentation Updates

*   All relevant documentation, including the Implementation Architecture, 5D Journey pseudocode, and diagrams, has been updated to reflect the new Composable Phase Orchestrator model. 