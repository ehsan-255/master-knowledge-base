# AOS Naming Conventions

**Version:** 1.0
**Applies to:** AOS v5.0

---

## 1. Principle: Consistency and Clarity

To ensure consistency, improve readability, and support automated governance, the Antifragile OS (AOS) adopts the mandatory naming conventions specified by the Hexagonal Microkernel Architecture (HMA).

Adherence to these conventions is not optional; it is a requirement for all components and artifacts within an AOS implementation and will be enforced by static analysis tools (`aos-lint`).

## 2. Naming Convention Rules

> **HMA Alignment:**  All rules in this document map 1-for-1 to the definitive table in *HMA v1.3 Part 4 §14*.  If any discrepancy exists, **the HMA specification is authoritative**.

| Element Type                       | Convention                                                               | Example                                                     |
| :--------------------------------- | :----------------------------------------------------------------------- | :---------------------------------------------------------- |
| **Core Components (Logic)**        | PascalCase                                                               | `RequestRouter`, `PluginLifecycleManager`                   |
| **Plugins (L3 Capability)**        | PascalCase, suffixed `Plugin`                                            | `DataAnalysisPlugin`, `UserManagementPlugin`                |
| **Plugins (L2 Orchestrator)**      | PascalCase, suffixed `Orchestrator` or `OrchestratorPlugin`              | `OrderProcessingOrchestrator`                               |
| **Ports (Interfaces)**             | PascalCase, suffixed `Port`                                              | `RequestPort`, `PluginExecutionPort`, `CredBrokerQueryPort` |
| **Adapters (L1 Driving, L4 Driven)** | PascalCase, suffixed `Adapter`                                           | `RestApiAdapter`, `PostgresUserRepositoryAdapter`           |
| **Events (Object/Class Name)**     | PascalCase, Past Tense, suffixed `Event`                                 | `OrderCreatedEvent`, `AnalysisCompletedEvent`               |
| **Event Types (in metadata)**      | dot.case, hierarchical, versioned                                        | `aos.order.created.v1`, `plugin.status.changed.v1`          |
| **Metric Names**                   | snake_case, hierarchical, with units                                     | `aos.core.router.requests.total`, `plugin.db.calls.ms`      |
| **Configuration / Env Vars**       | SCREAMING_SNAKE_CASE                                                     | `AOS_DATABASE_URL`, `PLUGIN_RETRY_COUNT`                    |
| **Package/Module Names**           | `lowercase_snake_case` or `lowercasekebab-case`                          | `aos_core/routing`, `data-analysis-plugin`                  | 
