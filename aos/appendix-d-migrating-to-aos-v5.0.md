### Appendix D: Migrating to AOS v5.0

**Overview:**
This appendix provides a practical migration and integration strategy for organizations moving from legacy project-management systems—or from earlier versions of AOS such as v4.0—to Antifragile OS (AOS) **v5.0**. The recommended approach is the *Strangler-Fig* pattern, which enables incremental adoption and minimizes risk.

#### The Strangler-Fig Pattern
- **Inventory and Map Legacy Artifacts:**
  - Catalog existing project/process artifacts and map them to AOS layers (Strategic, Orchestration, Execution).
- **Wrap Legacy Assets with Adapters:**
  - Develop adapters for legacy BPMN/DMN assets to emit PDP stubs into AOS.
- **Phased Migration:**
  - Route legacy traffic through adapters while gradually introducing new PDPs and retiring old artifacts as their value diminishes.
- **Migration Toolkit:**
  - Provide scripts, guides, and checklists to facilitate the transition.

#### Key Steps
1. **Assessment:** Identify all legacy processes and their criticality.
2. **Adapter Development:** Build technical bridges to allow legacy and AOS systems to coexist.
3. **Pilot Migration:** Select a non-critical process for initial migration.
4. **Incremental Rollout:** Expand migration scope as confidence grows, using metrics to monitor progress.
5. **Retirement:** Decommission legacy components only after successful AOS adoption.

This approach ensures business continuity, reduces risk, and enables organizations to realize AOS v5.0 benefits without disruptive "big-bang" transitions.

---

#### Migrating from AOS v5.0 to v5.0
The primary change in v5.0 is the introduction of the **Delegation of Authority Protocol**. Existing v5.0 projects will default to `HumanInLoop` mode, preserving the previous workflow. To leverage the new autonomy features, the `delegation_policy` attribute must be added to the PDPs and the new suite of LLM assistant and decider plugins must be deployed and registered with the HMA Core.

#### Migrating from the Monolithic Orchestrator (v4.0)

Teams migrating from **AOS v4.0** to **v5.0** must be aware of the change in the orchestration model.

- **Legacy Orchestrator:** The single `5D-Journey-Orchestrator` is now deprecated.
- **New Model:** Projects are now routed by the `Meta-Orchestrator` (`Process-Router`) to a series of `Phase Orchestrators`.
- **Migration Action:** Any custom integrations or monitoring that targeted the old orchestrator must be updated to target the new event-driven flow (`aos.phase.completed.v1` event) and the new set of L2 plugins. 
