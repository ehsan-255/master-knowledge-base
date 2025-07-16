# AOS Changelog

## Version 5.0

**Release Date:** July 16, 2025

### 🚀 Major Architectural Enhancements: Flexible Autonomy
*   **Introduced the Delegation of Authority Protocol:** This is the cornerstone change for v5.0. The system now supports both `HumanInLoop` and `FullAutonomy` modes, configurable at the start of a project or on a step-by-step basis.
*   **Added `AIDeciderPlugin`:** A new specialized L3 plugin that acts as an AI agent with decision-making authority when operating in `FullAutonomy` mode.
*   **Introduced a Suite of LLM Assistant Plugins:** Formalized the role of LLMs as assistants with new plugins like `StrategicAuditLLMPlugin`, `HistoricalContextLLMPlugin`, and `RetrospectiveLLMPlugin` to augment human decision-making.
*   **Refined Triage Process:** The initial triage is now handled by a dedicated `TriageOrchestratorPlugin` for improved architectural purity, which then hands off to the `Meta-Orchestrator`.
*   **Refactored to Composable Phase Orchestrator Model:** The previous monolithic `5D-Journey-Orchestrator` has been deprecated and replaced with a more flexible and architecturally pure model.
    *   **New Components:** Introduced a minimal L2 `Meta-Orchestrator` (`Process-Router`) and distinct L2 `Phase Orchestrators` for each stage of a process (e.g., `DefinePhaseOrchestrator`).
    *   **Rationale:** This change was made to achieve a better separation of concerns in alignment with HMA principles. It enhances flexibility by allowing different process "recipes" to be executed, and it simplifies development by breaking down a large, complex component into smaller, single-responsibility units. This directly addresses architectural feedback regarding the potential rigidity and blurred responsibilities of the v4.0 model.

### 📝 Documentation Updates
*   All relevant documentation, including the Implementation Architecture, 5D Journey pseudocode, and diagrams, has been updated to reflect the new Composable Phase Orchestrator model.

## Version 4.1

**Release Date:** 2025-07-15

### 🚀 Architectural Enhancements

*   **Refactored to Composable Phase Orchestrator Model:** This is the cornerstone change for version 5.0. The previous monolithic `5D-Journey-Orchestrator` has been deprecated and replaced with a more flexible and architecturally pure model.
    *   **New Components:** Introduced a minimal L2 `Meta-Orchestrator` (`Process-Router`) and distinct L2 `Phase Orchestrators` for each stage of a process (e.g., `DefinePhaseOrchestrator`).
    *   **Rationale:** This change was made to achieve a better separation of concerns in alignment with HMA principles. It enhances flexibility by allowing different process "recipes" to be executed, and it simplifies development by breaking down a large, complex component into smaller, single-responsibility units. This directly addresses architectural feedback regarding the potential rigidity and blurred responsibilities of the v4.0 model.

### 📝 Documentation Updates

*   All relevant documentation, including the Implementation Architecture, 5D Journey pseudocode, and diagrams, has been updated to reflect the new Composable Phase Orchestrator model. 
