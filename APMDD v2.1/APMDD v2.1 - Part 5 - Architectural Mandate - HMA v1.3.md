--- START OF FILE APMDD v2.1 - Architectural Mandate: Hexagonal Microkernel Architecture (HMA) v1.3.md ---
# APMDD v2.1 - Architectural Mandate: Hexagonal Microkernel Architecture (HMA) v1.3
#apmdd-hma-alignment #apmdd-architecture

## 5.1. HMA Overview
#apmdd-hma-alignment
The Hexagonal Microkernel Architecture (HMA) is the mandatory architectural pattern for all APMDD v2.1 projects. It enforces strict modularity, a minimal core, and autonomous [[APMDD v2.1 - Part 8 - Glossary#Plugin|Plugins]] with explicit [[APMDD v2.1 - Part 8 - Glossary#Port|Ports]] and [[APMDD v2.1 - Part 8 - Glossary#Event|Events]]. (See [[APMDD v2.1 - Part 8 - Glossary#Hexagonal Microkernel Architecture (HMA)]]).

## 5.2. HMA Core Principles
#apmdd-hma-alignment
- Minimal, stable core
- All business logic in replaceable [[APMDD v2.1 - Part 8 - Glossary#Plugin|Plugins]]
- Explicit, technology-agnostic [[APMDD v2.1 - Part 8 - Glossary#Port|Ports]] for all interactions
- Event-driven communication between core and plugins
- Strict boundaries and isolation between plugins

## 5.3. HMA Structure
#apmdd-hma-alignment
- **Core:** Minimal, responsible for plugin lifecycle, event routing, and enforcing boundaries
- **Plugins:** Autonomous, encapsulate business capabilities, communicate only via ports/events
- **Orchestrator Plugins:** Specialized plugins for workflow coordination (see [[APMDD v2.1 - Part 8 - Glossary#Orchestrator Plugin]])

## 5.4. HMA in the APMDD Lifecycle
#apmdd-hma-alignment #apmdd-lifecycle-phase
- HMA structure defined in PIM phase (see [[APMDD v2.1 - Part 3 - Lifecycle - Integrating MDA and Agile Practices]])
- Plugin boundaries, ports, and events specified in PIM/PSM
- Implementation and testing of plugins in PSM

## 5.5. HMA Compliance & Governance
#apmdd-hma-alignment #apmdd-governance
- Automated checks for HMA compliance (see [[APMDD v2.1 - Part 7 - Governance, Quality & Testing#7.4. Automated Governance & Enforcement|Automated Governance & Enforcement]])
- Architect reviews and validates all plugin boundaries and interfaces
- Plugins must be independently testable and replaceable

## 5.6. HMA and Security
#apmdd-hma-alignment #apmdd-governance
- Enforce trust boundaries between core and plugins
- Apply least privilege principles
- Isolate plugins to minimize blast radius (see [[APMDD v2.1 - Part 7 - Governance, Quality & Testing#7.5. Security by Design Principles within APMDD/HMA|Security by Design]])

## 5.7. HMA and Observability
#apmdd-hma-alignment #apmdd-testing
- All plugins and core must support tracing, metrics, and logging
- Observability is a design requirement (see [[APMDD v2.1 - Part 7 - Governance, Quality & Testing#7.6. Observability by Design|Observability by Design]])

## 5.8. Summary
#apmdd-hma-alignment
HMA v1.3 is the architectural backbone of APMDD v2.1, ensuring modularity, governability, and scalability for AI-led development. For modeling notations and strategy, see [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]].

--- END OF FILE APMDD v2.1 - Architectural Mandate: Hexagonal Microkernel Architecture (HMA) v1.3.md ---