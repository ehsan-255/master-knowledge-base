# The Scribe Engine: Final Architecture & Design Blueprint

## 1. Vision & Guiding Principles

Scribe is an event-driven automation engine designed to be the central nervous system for a plain-text knowledge base. After careful analysis of all proposals, we are adopting a pragmatic, layered architecture that prioritizes **stability, operability, and extensibility.**

Our guiding principle remains the elegant loop: **Observe → Trigger → Act**.

This blueprint finalizes the design by making key architectural decisions that provide a clear path forward, balancing the simplicity of the original concept with the resilience required for complex, automated environments.

## 2. The Final Core Architecture

We will implement a **decoupled, single-process, multi-threaded model** for Scribe V1. This provides exceptional performance for single-machine operation and avoids the complexity of external dependencies like Kafka or a dedicated database, while a clean interface design prepares it for future scaling.

```
                                      ┌──────────────────────────────────────────┐
                                      │              Scribe Engine               │
                                      │                                          │
┌───────────────┐                     │   ┌────────────────┐   ┌───────────────┐ │
│ File System   ├─(File Events)───────► │  The Watcher     ├─► │   Event Bus   ├─►
└───────────────┘                     │   (Producer)       │   │ (Queue)       │ │
                                      │   └────────────────┘   └───────────────┘ │
                                      │           ▲                  │           │
                                      │           │ (Hot Reload)     │ (Events)  │
                                      │           │                  ▼           │
┌───────────────┐                     │   ┌────────────────┐   ┌───────────────┐ │
│ config.json   ├─(Config Updates)────┤   │ Config Manager │   │  Engine Core  │ │
└───────────────┘                     │   └────────────────┘   │   (Worker)    │ │
                                      │           │            └───────┬───────┘ │
                                      │           │ (Rules)            │ (Action)│
                                      │           │                    ▼           │
                                      │   ┌────────────────┐   ┌───────────────┐ │
                                      │   │  Rule Engine   │◄───┤Action Dispatch├─► External Systems
                                      │   └────────────────┘   │ (Plugin System) │   (Git, APIs, etc.)
                                      │                        └───────────────┘ │
                                      └──────────────────────────────────────────┘
```

### Key Component Decisions:

1.  **Event Bus:** We will use Python's native, thread-safe `queue.Queue`. It is robust, in-memory, and perfectly suited for the single-process model. It acts as the critical shock absorber for event bursts.
2.  **Configuration:** We will use a single `config.json` file. Its integrity will be enforced on load and hot-reload by a **JSON Schema**, providing safety and clarity without the overhead of a custom DSL.
3.  **Extensibility:** We will implement a **Python-based Plugin System**. Actions will be individual Python classes discovered at runtime from a dedicated `actions/` directory. This is developer-friendly and powerful enough for V1.

## 3. The Three Pillars of Implementation

This architecture will be built upon three pillars that ensure it is not just functional, but production-ready.

### Pillar 1: Reliability & Resilience (It must not fail)

*   **Crash-Safe Writes:** All file modifications will use the atomic **`write-temp -> fsync -> rename`** pattern. This guarantees that a power loss or crash will never leave a file in a corrupted, partially-written state.
*   **Circuit Breaker:** The `Action Dispatcher` will be wrapped in a Circuit Breaker. If a specific rule or action fails consecutively *N* times (e.g., due to a malformed file or a dead API), the breaker will "open" for that rule, preventing it from running for a configured timeout. Offending events will be moved to a **quarantine directory** for manual inspection. This isolates failures and allows the rest of the engine to continue functioning.
*   **Idempotent Actions:** The core action plugins (`update_field`, `add_line`, etc.) will be designed to be idempotent where possible, meaning running them multiple times has the same effect as running them once.

### Pillar 2: Operability & Observability (We must see what it's doing)

*   **Structured Logging:** All logs will be emitted as **JSON lines** (`structlog`). This is non-negotiable. Each log entry will include context like `rule_name`, `file_path`, and `duration_ms`, making logs machine-parsable and ready for ingestion into systems like Grafana Loki or an ELK stack.
*   **Health Check Endpoint:** A lightweight HTTP server will run on a dedicated port (e.g., `:9468`) exposing a `/health` endpoint. This endpoint will return a JSON object with the engine's status (`status`, `queue_size`, `uptime_seconds`), making it trivial to monitor with any standard tool or integrate with orchestrators like Kubernetes.
*   **Prometheus Metrics:** The server will also expose a `/metrics` endpoint with key operational metrics in Prometheus format (e.g., `scribe_events_processed_total`, `scribe_action_duration_seconds`, `scribe_queue_depth`).

### Pillar 3: Extensibility & Safety (It must be easy and safe to extend)

*   **Hot-Reloading Configuration:** The `Config Manager` will use the same `watchdog` observer to monitor `config.json`. A change to the rules will trigger a safe, atomic reload of the configuration in the running engine, **without requiring a restart**.
*   **Sandboxed Command Execution:** The `run_command` action will be heavily restricted. It will execute commands with a scrubbed environment (allowing only `PATH`, etc.), enforce a strict timeout, and validate the command against an **allow-list** in `config.json`.
*   **Rule Validation:** On startup and hot-reload, the `config.json` will be validated against a formal **JSON Schema**. Invalid rules will prevent the engine from starting or the reload from completing, ensuring configuration errors are caught immediately.

## 4. The Finalized `config.json` Schema

This schema provides the power and safety needed for V1.

```json
{
  "engine_settings": {
    "log_level": "INFO",
    "quarantine_path": "scribe/quarantine/",
    "pause_file": ".engine-pause"
  },
  "security": {
    "allowed_commands": [
      "git",
      "/usr/local/bin/my-custom-script.sh"
    ],
    "restricted_paths": ["/etc/", "/root/", ".git/"]
  },
  "rules": [
    {
      "name": "Timestamp High-Priority Tasks",
      "id": "RULE-001",
      "enabled": true,
      "priority": 10, // Lower numbers run first
      "file_glob": "**/tasks/*.md",
      "trigger_pattern": "^(> \\[!TASK\\].*priority: high.*)$",
      "actions": [
        {
          "type": "update_structured_field",
          "field": "updated",
          "value_template": "{timestamp_utc_iso}"
        }
      ],
      "error_handling": {
        "max_retries": 2,
        "retry_delay_seconds": 5
      }
    }
  ]
}
```

## 5. The Action Plugin Contract

Creating a new action will be simple and standardized. A developer will create a new file in `actions/` and implement a class that inherits from a base class.

```python
# actions/base_action.py
from abc import ABC, abstractmethod

class BaseAction(ABC):
    @abstractmethod
    def execute(self, line: str, match: re.Match, file_path: str, **kwargs) -> str:
        """
        Executes the action.
        Returns the modified line or original line.
        """
        pass

# actions/add_tag_action.py
class AddTagAction(BaseAction):
    def execute(self, line: str, match: re.Match, file_path: str, **kwargs) -> str:
        tag_to_add = kwargs.get('tag')
        if not tag_to_add:
            return line # No tag configured for this action
        
        if f"tags: " in line:
            # Safely append to existing tags
            return line.replace("tags: ", f"tags: {tag_to_add}, ")
        else:
            # Add new tags field
            return f"{line.strip()} | tags: {tag_to_add}"
```

## 6. The Development Roadmap

This architecture will be delivered in clear, incremental phases.

*   **Phase 1: The Resilient Core (MVP)**
    *   **Goal:** Build a rock-solid, observable engine.
    *   **Features:** Implement the core Producer-Consumer loop, `config.json` loading, structured logging, the health endpoint, and crash-safe writes. Implement 3-4 essential actions (`update_field`, `run_command`).
    *   **Outcome:** A stable, trustworthy tool that can be deployed and monitored safely.

*   **Phase 2: The Extensible Platform**
    *   **Goal:** Make Scribe powerful and easy to extend.
    *   **Features:** Implement the full Action Plugin discovery system, JSON Schema validation, config hot-reloading, the Circuit Breaker, and the security sandbox for commands.
    *   **Outcome:** A platform that power-users can safely and dynamically configure to automate complex workflows.

*   **Phase 3: The Intelligent Engine (Future)**
    *   **Goal:** Introduce advanced capabilities, preparing for scale.
    *   **Features:** This is where we explore swapping the `EventBus` with a Redis/Kafka adapter, introducing AI/LLM-driven actions (`summarize`, `ai_enhance`), and building semantic triggers based on vector embeddings.
    *   **Outcome:** Scribe evolves from a rule-based engine to a context-aware knowledge operations platform.

This final blueprint provides a robust, pragmatic, and exciting path forward. It delivers immediate value with a stable core while laying the perfect foundation for the powerful, intelligent system we envision.