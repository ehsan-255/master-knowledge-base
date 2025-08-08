# ADR-001: NATS Message Broker Adoption

## Status
**Accepted** - July 24, 2025

## Context

The Scribe engine previously used a simplistic in-memory `queue.Queue` for inter-component communication. This approach had several limitations:

1. **Scalability**: In-memory queues don't scale across processes or machines
2. **Reliability**: No persistence or delivery guarantees
3. **Observability**: Limited visibility into message flow
4. **HMA Compliance**: HMA v2.2 recommends production-grade message brokers (Tier 2)

The HMA v2.2 specification recommends NATS as a Tier 2 technology for message-oriented middleware.

## Decision

We will adopt **NATS** as the primary message broker for the Scribe engine, replacing the legacy in-memory queue system.

### Implementation Details

1. **Library**: Use `nats-py` client library
2. **Adapter**: Implement `NatsEventBusAdapter` that implements the `EventBusPort` interface
3. **Configuration**: NATS server URL configurable via `config.json`
4. **Fallback**: Maintain backward compatibility methods for legacy tests
5. **Event Structure**: Use HMA-compliant event format with versioning

### Technology Tier Justification

- **Tier**: 2 (Recommended)
- **Category**: Message-Oriented Middleware
- **HMA Compliance**: Full compliance with HMA v2.2 messaging patterns
- **Alternative Considered**: Apache Kafka (heavier, more complex for our use case)

## Consequences

### Positive
- ✅ **Scalability**: Supports distributed deployments
- ✅ **Reliability**: Built-in message persistence and delivery guarantees
- ✅ **Performance**: High-throughput, low-latency messaging
- ✅ **Observability**: Rich metrics and monitoring capabilities
- ✅ **HMA Compliance**: Meets Tier 2 recommendations
- ✅ **Cloud Native**: Integrates well with Kubernetes environments

### Negative
- ❌ **Complexity**: Requires NATS server deployment and management
- ❌ **Dependencies**: External service dependency (can be mitigated with clustering)
- ❌ **Learning Curve**: Team needs to understand NATS concepts and operations

### Migration Impact
- Legacy `queue.Queue` usage replaced with NATS subjects
- Event publishing/subscribing patterns remain the same through port abstraction
- Backward compatibility maintained for existing tests
- Configuration changes required for production deployments

## Implementation Status

- ✅ `NatsEventBusAdapter` implemented in `core/adapters/nats_adapter.py`
- ✅ Integration with engine factory and startup/shutdown lifecycle
- ✅ HMA-compliant event structure with OTEL telemetry
- ✅ Connection management with auto-reconnect capabilities
- ✅ Backward compatibility methods for legacy tests

## Related ADRs
- ADR-002: Ports and Adapters Architecture
- ADR-005: HMA v2.2 Compliance Strategy