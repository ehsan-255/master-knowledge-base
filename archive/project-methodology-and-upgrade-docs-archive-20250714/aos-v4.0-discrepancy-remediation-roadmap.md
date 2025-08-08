# AOS V4.0 Discrepancy Remediation & HMA Adoption Roadmap

> Version: 2025-07-14
> Author: LLM Analyst
> Purpose: Eliminate all gaps identified in the 2025-07-14 discrepancy report and achieve full compliance with **aos-upgrade.md** requirements and **HMA v1.3** architecture.

---

## 0. Reading Guide

* **Task IDs**: `T-n` are top-level tasks, `T-n.m` are subtasks.
* **Dependencies**: A task **must not** start until all tasks in its *Dependencies* list are **Completed**.
* **Deliverables**: Each task specifies concrete file edits, code additions, or artefacts to be produced.
* **LLM Execution**: Designed for direct execution by an LLM with access to repository editing tools (read, grep, edit).

---

## 1. Roadmap Overview (Hierarchical)

### Phase 1 – HMA Foundation (Core Architecture)  
*Goal*: Provide missing Hexagonal Microkernel Architecture scaffolding so higher-level remedies can rely on stable infrastructure.

| ID | Title | Dependencies |
| --- | ----- | ------------ |
| T-1 | Define HMA Ports & Adapters | – |
| T-2 | Implement Plugin Lifecycle Manager | T-1 |
| T-3 | Implement Event Bus Interface & Message Taxonomy | T-1 |
| T-4 | Integrate Cross-Cutting Concerns (Observability, Security, Tenancy) | T-1 |
| T-5 | Embed Formal HMA Diagrams & Traceability Matrices | T-1, T-2, T-3, T-4 |
| T-6 | Add HMA Compliance Test Suite | T-1 … T-5 |

### Phase 2 – Human-AI Collaboration Enhancements  
*Goal*: Close gaps around autonomy, dissent, and graceful degradation.

| ID | Title | Dependencies |
| --- | ----- | ------------ |
| T-7 | Add Graceful Degradation Ladder & Autonomy Switch Logic | T-2, T-3 |
| T-8 | Add `IntuitiveDissonanceFlag` Metadata & Workflow | T-7 |
| T-9 | Capture & Replay Human Rationale / Skills-Building Hooks | T-8 |

### Phase 3 – Methodology & Template Upgrades  
*Goal*: Deliver missing process artefacts required by aos-upgrade.md.

| ID | Title | Dependencies |
| --- | ----- | ------------ |
| T-10 | Provide Emergent Response Templates Library | – |
| T-11 | Finalise Option Stub Threshold Rules & Activation Logic | T-1 |

### Phase 4 – Metrics & Evidence Framework  
*Goal*: Strengthen measurement credibility and AI accountability.

| ID | Title | Dependencies |
| --- | ----- | ------------ |
| T-12 | Implement Balanced Scorecard Metric Pairs & SHACL Rules | – |
| T-13 | Add `source_attribution` ("Citable AI") Metadata to PDP Schema | – |

### Phase 5 – Scalability & Governance Enhancements  
*Goal*: Address remaining governance, volatility, and reconciliation issues.

| ID | Title | Dependencies |
| --- | ----- | ------------ |
| T-14 | Define Tiered Implementation Profiles (`AOS-Lite`, `Standard`, `Strategic`) | – |
| T-15 | Implement Volatility Classification System & Harm-Mitigation Protocols | – |
| T-16 | Build Formal Reconciliation Engine (Decision Logic) | T-1, T-3 |
| T-17 | Add Threshold-Based Adaptation Triggers in Cybernetic Controller | T-12 |

---

## 2. Granular Task Breakdown & Instructions

Below, each top-level task is decomposed into atomic **Operational Steps** ready for LLM execution.

### T-1  Define HMA Ports & Adapters

1. **Locate target files**: `aos/05-implementation-architecture.md`, create `aos/hma-core-spec.md`.
2. **Add Port Definitions**: Insert subsections defining `PluginExecutionPort`, `EventBusPort`, `CredBrokerQueryPort`, etc., mirroring HMA v1.3 Part 3 §10.
3. **Add Adapter Examples**: Provide one driving adapter and one driven adapter code snippet (Python pseudo-code) per port.
4. **Update Traceability**: Link each new port back to HMA spec section using markdown anchor.
5. **Validation**: Grep for each port name to confirm presence.

### T-2  Implement Plugin Lifecycle Manager

1. **Create** `aos/hma-plugin-lifecycle.py` with class `PluginLifecycleManager` implementing `register_plugin`, `activate_plugin`, `deactivate_plugin`, `upgrade_plugin` per HMA v1.3 Part 3 §8.2.
2. **Edit** `aos/05-implementation-architecture.md` to reference the new manager and embed code sample.
3. **Add unit tests** in `test-environment/scribe-tests/` validating lifecycle state transitions.

### T-3  Implement Event Bus Interface & Message Taxonomy

1. **Create** `aos/event_bus.py` exposing `publish(event)`, `subscribe(topic)`, `unsubscribe(topic)`.
2. **Define** message schema & topic taxonomy in `aos/event-bus-spec.md` (align with HMA Part 2 §7.2).
3. **Integrate** EventBusPort stub into Port definitions (depends on T-1).
4. **Add example asynchronous workflow** in `aos/05-implementation-architecture.md`.

### T-4  Integrate Cross-Cutting Concerns

1. **Observability**: Add logging, tracing, metrics providers to `aos/05-implementation-architecture.md` and update config YAML with `observability` block.
2. **Security**: Expand existing `credential_broker` section with role-based access and token rotation strategy.
3. **Tenancy**: Add multi-tenant isolation section and sample adapter.
4. **Reference** HMA Part 5 cross-cutting checklist.

### T-5  Embed Formal HMA Diagrams & Traceability

1. **Generate Mermaid diagrams** mapping AOS components to HMA L0–L4 layers; store in `aos/diagrams/`.
2. **Insert diagram embeds** in `aos/05-implementation-architecture.md`.
3. **Create traceability matrix** (`aos/hma-traceability.md`) linking each AOS file / component to the corresponding HMA element.

### T-6  Add HMA Compliance Test Suite

1. **Create** `tools/validation/hma_compliance_tests.py` checking:
   * Port definitions present
   * Plugins declare required ports
   * Lifecycle manager callable
2. **Add pytest entry** inside `test-environment/run_all_tests.py`.
3. **Document** usage in `README.md`.

### T-7  Add Graceful Degradation Ladder

1. **Edit** `aos/05-implementation-architecture.md` – add subsection “Graceful Degradation Ladder”.
2. **Define** autonomy levels (L0 Manual ↔ L4 Fully Autonomous) and triggering rules.
3. **Insert** decision table (DMN XML) mapping Cynefin domain & confidence to autonomy level.
4. **Update** orchestrator code to read autonomy level and route tasks.

### T-8  Add `IntuitiveDissonanceFlag`

1. **Update PDP JSON-LD schema** (`aos/02-pdp-digital-twin.md`) – add field `intuitive_dissonance_flag` boolean, default `false`.
2. **Add** logging when flag raised; require second-human approval via synergy matrix.
3. **Add SHACL shape** enforcing flag review.

### T-9  Capture & Replay Human Rationale

1. **Extend** PDP schema with `override_rationale` text.
2. **Create** `tools/analysis/rationale_extractor.py` – aggregates rationales for model retraining.
3. **Update** documentation to schedule quarterly skills-building sessions.

### T-10  Provide Emergent Response Templates

1. **Add directory** `aos/emergent-response-templates/` with markdown templates (sense-act-learn loop).
2. **Link** templates from `aos/03-enhanced-5d-journey.md` and update table of contents.

### T-11  Option Stub Threshold Rules

1. **Edit** `aos/02-pdp-digital-twin.md` – add fields `activation_threshold`, `cost_benefit_ratio`.
2. **Create** decision logic in `tools/builder/option_stub_manager.py` to instantiate full PDP when threshold reached.

### T-12  Balanced Scorecard Metric Pairs & SHACL

1. **Define** `stability_index`, `innovation_index` metric pair in `aos/06-metrics-and-evolution.md`.
2. **Add** SHACL shapes in `standards/registry/scorecard_shapes.ttl` enforcing metric pair presence.
3. **Update** telemetry block in PDP examples.

### T-13  Add `source_attribution` Metadata ("Citable AI")

1. **Edit** PDP schema to include `source_attribution` (array of URI strings).
2. **Update** AI generation scripts to inject source links.
3. **Add** SHACL shape verifying non-empty attribution.

### T-14  Tiered Implementation Profiles

1. **Create** `aos/implementation-profiles.md` detailing `AOS-Lite`, `AOS-Standard`, `AOS-Strategic`.
2. **Add** decision table selecting profile in Phase 0 Triage (`aos/00-introduction.md`).
3. **Provide** minimal PDP-Lite template in `templates/`.

### T-15  Volatility Classification & Mitigation

1. **Add** volatility taxonomy and classification algorithm in `aos/03-enhanced-5d-journey.md`.
2. **Create** `tools/analysis/volatility_classifier.py`.
3. **Embed** harm-mitigation protocol and crisis-response escalation path.

### T-16  Formal Reconciliation Engine

1. **Add** `tools/orchestrator/reconciliation_engine.py` that merges conflicting outputs using priority rules.
2. **Create** DMN table `reconciliation.dmn.xml` for rule set.
3. **Wire** engine into Orchestrator plugin.

### T-17  Threshold-Based Adaptation Triggers

1. **Define** KPI deviation thresholds in `aos/06-metrics-and-evolution.md`.
2. **Update** cybernetic controller code to monitor, emit `AdaptationTrigger` event (requires Event Bus from T-3).
3. **Add** SHACL shape verifying trigger configuration per PDP.

---

## 3. Consolidated Execution Order

1. T-1 → T-2 → T-3 → T-4 → T-5 → T-6  *(HMA foundation completed)*  
2. T-7 → T-8 → T-9  *(Human-AI collaboration)*  
3. T-10 → T-11  *(Methodology templates & option handling)*  
4. T-12 → T-13  *(Metrics & Citable AI)*  
5. T-14 → T-15 → T-16 → T-17  *(Scalability & governance)*

All tasks must pass unit tests and SHACL validation before marking **Complete**.

---

## 4. Progress Tracking Template

| Task ID | Status | Owner | Notes |
| ------- | ------ | ----- | ----- |
| T-1 | pending | | |
| … | | | |

---

*End of roadmap* 