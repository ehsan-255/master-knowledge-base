# Architecture Decision Records (ADRs)

## Overview

This directory contains Architecture Decision Records (ADRs) documenting significant technology and architectural decisions made in the Scribe engine. These ADRs ensure transparency and provide context for future maintenance and evolution.

## ADR Format

Each ADR follows the standard template:

1. **Status**: Proposed, Accepted, Deprecated, Superseded
2. **Context**: The issue motivating this decision
3. **Decision**: The change we're proposing or have agreed to implement
4. **Consequences**: What becomes easier or more difficult to do because of this change

## ADR Index

| ID | Title | Status | Date |
|----|--------|--------|------|
| ADR-001 | [NATS Message Broker Adoption](ADR-001-nats-message-broker.md) | Accepted | 2025-07-24 |
| ADR-002 | [Ports and Adapters Architecture](ADR-002-ports-and-adapters.md) | Accepted | 2025-07-24 |
| ADR-003 | [SHACL to JSON Schema Bridge](ADR-003-shacl-json-bridge.md) | Accepted | 2025-07-24 |
| ADR-004 | [Python Async/Await for Concurrency](ADR-004-python-async-concurrency.md) | Accepted | 2025-07-24 |
| ADR-005 | [HMA v2.2 Compliance Strategy](ADR-005-hma-compliance-strategy.md) | Accepted | 2025-07-24 |

## HMA v2.2 Compliance

These ADRs document compliance with the Hexagonal Microkernel Architecture (HMA) v2.2 specification and justify technology choices within the three-tier framework:

- **Tier 1 (Mandatory)**: OpenTelemetry, mTLS, JSON Schema
- **Tier 2 (Recommended)**: NATS, Kubernetes, Vault, Structured Logging
- **Tier 3 (Alternative)**: SHACL, Custom implementations with compliance bridges