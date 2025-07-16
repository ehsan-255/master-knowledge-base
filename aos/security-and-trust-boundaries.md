# AOS Security and Trust Boundaries

**Version:** 1.0
**Applies to:** AOS v5.0

---

## 1. Principle: Security by Design

The Antifragile OS (AOS) implements the Hexagonal Microkernel Architecture (HMA) security model, which is based on the principle of "Security by Design." This means security is not an afterthought but is woven into the architecture through clearly defined trust boundaries and mandatory security controls.

This document outlines the security framework for a compliant AOS v5.0 implementation.

## 2. HMA Trust Boundaries

AOS defines several trust boundaries that dictate where security controls are most critical. Traffic crossing these boundaries MUST be appropriately secured.

*   **Zone 0 (Internet) -> Zone 1 (L1 Adapters):** Untrusted. All traffic MUST undergo authentication, authorization, and strict input validation here.
*   **Zone 1 (L1 Adapters) -> Zone 2 (Core):** Semi-trusted. The Core MUST re-validate data from adapters to protect itself.
*   **Zone 2 (Core) -> Zone 3 (Plugins):** Semi-trusted. The Core treats plugins as isolated, semi-trusted components. All interaction is strictly mediated by ports.
*   **Zone 3 (Plugin) -> Zone 3 (Plugin):** Untrusted. Direct communication between plugins is forbidden. Asynchronous communication via the Event Bus is the standard, where each plugin is a distinct security principal.
*   **Zones 2/3 (Core/Plugins) -> Zone 4 (Infrastructure):** Untrusted. All calls to databases, APIs, or other infrastructure MUST use secure, brokered credentials.

## 3. Mandatory Security Controls

The following controls are REQUIRED for any AOS implementation.

*   **Secure Communication:**
    *   **TLS:** Mandatory for all external network traffic.
    *   **mTLS (Mutual TLS):** Recommended for all internal communication between components (Core-to-Plugin, Plugin-to-Infrastructure) to ensure mutual authentication.

*   **Centralized Credential Management:**
    *   Plugins MUST obtain all credentials exclusively through the Core's **`CredBrokerQueryPort`**.
    *   Static secrets (passwords, API keys) are forbidden in plugin code or configuration. They must be stored in a secure backend like HashiCorp Vault, managed by the Credential Broker.

*   **Plugin Runtime Isolation:**
    *   Plugins MUST run in strongly isolated environments (e.g., separate containers with strict network policies).
    *   This limits the "blast radius" if a single plugin is compromised, preventing it from affecting the Core or other plugins.

*   **Principle of Least Privilege:**
    *   Plugins MUST operate with the minimum permissions necessary. This is enforced by providing narrowly-scoped credentials from the `CredentialBroker`.

*   **Code Signing & Verification (Recommended):**
    *   Plugin artifacts SHOULD be cryptographically signed. The Core's Plugin Lifecycle Manager SHOULD verify signatures before activation to ensure code integrity. 
