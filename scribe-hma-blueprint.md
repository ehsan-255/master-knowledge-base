# **The Scribe Engine - Final Architecture & Design Blueprint (HMA-Aligned)**

## 1. Executive Vision: Scribe as an HMA Implementation

Scribe will be engineered as a premier, lightweight implementation of the **Hexagonal Microkernel Architecture (HMA)**. Its purpose is to serve as a resilient, event-driven automation engine for plain-text knowledge and code repositories.

The engine's design is anchored by HMA's core principle, which we will rigorously enforce: a simple, powerful loop of **Observe → Trigger → Act**, executed within a framework that prioritizes stability, operability, and secure extensibility.

This blueprint finalizes the architecture, making decisive choices on technology and methodology to resolve all identified ambiguities and mitigate risks. It is the single source of truth for Scribe's development.

## 2. Final Architecture: Scribe Mapped to HMA

Scribe will be a **single-process, multi-threaded application**. This model provides the necessary performance and resilience for its intended use case without incurring the operational overhead of a distributed system.

```mermaid
%%{ init: { 'theme': 'base', 'themeVariables': { 'fontSize': '12px' } } }%%
graph TD
    subgraph L1_Interface [L1: Interface Zone]
        A[File System Events] -->|Driving Adapter| B(Watcher / Producer Thread)
    end

    subgraph L2_Core [L2: Microkernel Core Zone]
        B --> C{Event Bus<br>(Thread-Safe Queue)}
        C --> D(Engine Core / Worker Thread)
        
        subgraph L2_ControlPlane [L2 Control Plane Services]
            E(Config Manager<br>w/ Hot-Reload)
            F(Plugin Loader)
            G(Circuit Breaker Service)
        end
        
        D -- Uses --> E
        D -- Uses --> F
        D -- Uses --> G
    end

    subgraph L3_Plugins [L3: Capability Plugin Zone]
        H(Action Dispatcher)
        I[Action Plugins<br>(e.g., UpdateTimestampAction)]
    end
    
    subgraph L4_Infrastructure [L4: Infrastructure Zone]
        J[Target Files]
        K[External Commands]
    end

    D -- Dispatches to --> H
    F -- Loads --> I
    H -- Executes --> I
    I -- Driven Adapter --> J
    I -- Driven Adapter --> K
    
    style L1_Interface fill:#eafaf1,stroke:#1abc9c
    style L2_Core fill:#d6eaf8,stroke:#3498db
    style L3_Plugins fill:#d5f5e3,stroke:#2ecc71
    style L4_Infrastructure fill:#f4ecf7,stroke:#af7ac5
    style L2_ControlPlane fill:#ebf5fb,stroke:#3498db,stroke-dasharray: 3 3
```

| HMA Concept | Scribe Implementation | Location (`repo-tree.md`) |
| :--- | :--- | :--- |
| **L1 Driving Adapter** | The **Watcher (Producer) Thread**, using `watchdog` to listen for file system events. | `tools/scribe/watcher.py` |
| **L2 Microkernel Core** | The **Engine Core (Worker) Thread**, which orchestrates the entire process. | `tools/scribe/engine.py` |
| **L2 Control Plane** | **Config Manager**, **Plugin Loader**, and **Circuit Breaker Service**. | `tools/scribe/core/` |
| **Event Bus** | A thread-safe `queue.Queue` for in-process event buffering. | `tools/scribe/engine.py` |
| **L3 Capability Plugin** | An **Action** class (e.g., `UpdateTimestampAction`) inheriting from `BaseAction`. | `tools/scribe/actions/` |
| **Port (Interface)** | The abstract `BaseAction` class defining the `execute()` contract. | `tools/scribe/actions/base.py` |
| **L4 Driven Adapter** | The implementation logic within each specific `Action` plugin's `execute()` method. | `tools/scribe/actions/*.py` |

## 3. Component Deep Dive & Risk Mitigation

This section provides concrete technical solutions to the identified implementation challenges.

### 3.1. Multi-Threading & Synchronization (Risk Area 1)

*   **Challenge:** Race conditions and graceful shutdown.
*   **Final Decision & Methodology:**
    1.  **Thread-Safe Queue:** The communication channel between the Watcher (Producer) and Engine (Consumer) **MUST** be Python's `queue.Queue`, which is inherently thread-safe and handles all locking internally.
    2.  **Graceful Shutdown:** A single `threading.Event` object, named `shutdown_event`, will be used.
        *   The main thread will catch `KeyboardInterrupt` (`Ctrl+C`) and call `shutdown_event.set()`.
        *   The Watcher's `watchdog` loop and the Worker's `while` loop **MUST** check `if shutdown_event.is_set()` on each iteration to allow for a clean exit.
        *   The Worker's `queue.get()` call **MUST** use a timeout (e.g., `queue.get(timeout=1)`) so it can periodically check the `shutdown_event` instead of blocking indefinitely.

    ```python
    # worker.py snippet
    def run(self):
        while not self.shutdown_event.is_set():
            try:
                event = self.queue.get(timeout=1)
                # ... process event ...
            except queue.Empty:
                continue # Loop continues, checking shutdown_event
    ```

### 3.2. Security Sandboxing (Risk Area 2)

*   **Challenge:** Vague definitions of "whitelisting" and "scrubbing."
*   **Final Decision & Methodology:**
    1.  **Command Structure:** The `run_command` action in `config.json` **MUST** accept a list of strings, not a single string. This allows direct use with `subprocess.run()` without `shell=True`, preventing shell injection.
    2.  **Command Whitelisting:** The first element of the command list (the executable) **MUST** be validated against the `security.allowed_commands` list in `config.json`. The check will be against the executable name only (e.g., `git`), not the full path.
    3.  **Environment Scrubbing:** The `subprocess.run` call **MUST** use a minimal, allow-listed environment. The default will be an empty environment, with an optional `allowed_env_vars` key in the action's config to specify which variables to pass through (e.g., `["PATH"]`).

    ```python
    # actions/run_command_action.py snippet
    def execute(self, ..., command: list, allowed_env_vars: list = None):
        executable = command[0]
        if executable not in self.config.security.allowed_commands:
            raise SecurityError(f"Command '{executable}' is not in the allow-list.")

        env = {}
        if allowed_env_vars:
            for var in allowed_env_vars:
                if var in os.environ:
                    env[var] = os.environ[var]
        
        subprocess.run(command, env=env, check=True, capture_output=True)
    ```

### 3.3. Circuit Breaker State Management (Risk Area 3)

*   **Challenge:** Complex state logic and unclear scope.
*   **Final Decision & Methodology:**
    1.  **Scope:** The Circuit Breaker will operate on a **per-rule ID basis**. A dictionary will hold a `CircuitBreaker` instance for each `rule.id`.
    2.  **State Machine:** The implementation will follow the classic `CLOSED -> OPEN -> HALF_OPEN` state machine.
    3.  **Configuration:** The `config.json` will define `failure_threshold` (e.g., 3) and `recovery_timeout_seconds` (e.g., 60) within each rule's `error_handling` block.
    4.  **Logic:**
        *   **CLOSED:** Normal operation. On failure, increment failure count. If count > threshold, move to `OPEN` and record the time.
        *   **OPEN:** Immediately reject calls. After `recovery_timeout_seconds` has passed, move to `HALF_OPEN`.
        *   **HALF_OPEN:** Allow exactly one call to pass through. If it succeeds, reset failure count and move to `CLOSED`. If it fails, move back to `OPEN` and reset the recovery timer.

### 3.4. Atomic File Operations (Risk Area 4)

*   **Challenge:** Platform-specific implementation and testing power loss.
*   **Final Decision & Methodology:**
    1.  **Pattern:** The `atomic_write` utility **MUST** use the `write-temp -> os.fsync -> os.rename` pattern. The temporary file will be created in the same directory as the target file to ensure the `rename` is an atomic operation on POSIX-compliant filesystems.
    2.  **Testing:** We will not attempt to simulate literal power loss. Instead, the test suite in `test-environment/` **MUST** include a test that **injects an exception** between the temporary file write and the final `os.rename`. The test will then assert that the original file remains unmodified and the temporary file is cleaned up. This validates the core safety guarantee of the pattern.

### 3.5. Hot-Reloading Configuration

*   **Challenge:** Atomicity and handling invalid configurations.
*   **Final Decision & Methodology:**
    1.  **Mechanism:** The `ConfigManager` will run its own `watchdog` observer on `config.json`.
    2.  **Atomic Swap:** On detection of a change, the manager will:
        a. Load the new configuration into a *temporary dictionary*.
        b. Validate this temporary dictionary against the `config.schema.json` using `jsonschema`.
        c. If validation fails, it will log a critical error and **discard the temporary config**, keeping the old, valid configuration active.
        d. If validation succeeds, it will acquire a `threading.Lock` and atomically replace the main configuration object with the new one (`self.config = new_config`). The lock ensures the worker thread never reads a partially updated config.

### 3.6. Plugin System & Discovery

*   **Challenge:** Securely loading dynamic code.
*   **Final Decision & Methodology:**
    1.  **Discovery:** The `PluginLoader` will iterate through `.py` files in the `tools/scribe/actions/` directory.
    2.  **Loading:** It will use `importlib.util.spec_from_file_location` and `importlib.util.module_from_spec` to load each file as a module.
    3.  **Validation:** It will use `inspect.getmembers` to find classes within the module that are a subclass of `BaseAction` but are not `BaseAction` itself.
    4.  **Error Handling:** The entire loading process for a single file **MUST** be wrapped in a `try...except` block. If a plugin file has syntax errors or fails to load for any reason, the engine will log the error and skip that plugin, without crashing.

### 3.7. Performance & Observability Testing

*   **Challenge:** Vague test definitions.
*   **Final Decision & Methodology:**
    1.  **Test Location:** All performance and soak tests will be located in and run from `test-environment/`.
    2.  **Soak Test (`soak_test.py`):** This script will perform the 24-hour test. It will first create a burst of 5,000 files, then enter a loop that randomly modifies one of the files every 500ms.
    3.  **Success Criteria:**
        *   The Scribe process does not exit with an error code.
        *   A separate monitoring script will use `psutil` to record Scribe's memory usage every minute. A successful test shows stable memory usage (no linear growth).
        *   The structured logs will be piped to a file. A post-processing script will calculate the average `duration_ms` for `rule_executed` events, which must remain below a defined threshold (e.g., 50ms).
    4.  **Observability Test (`observability_test.py`):** This test will trigger at least 5 different rules and assert that the corresponding JSON logs are created and contain the correct `rule_id`, `file_path`, and `status` fields. It will also `curl` the `/health` endpoint and validate the JSON response schema.

## 4. Finalized `config.json` Structure

This structure will be validated by `config/config.schema.json`.

```json
{
  "engine_settings": {
    "log_level": "INFO",
    "quarantine_path": "archive/scribe/quarantine/",
    "pause_file": ".engine-pause"
  },
  "security": {
    "allowed_commands": [
      "git",
      "make",
      "npm"
    ],
    "restricted_paths": [
      ".git/",
      ".vscode/",
      "node_modules/"
    ]
  },
  "rules": [
    {
      "id": "RULE-001",
      "name": "Update Task Timestamp on State Change",
      "enabled": true,
      "file_glob": "**/tasks/*.md",
      "trigger_pattern": "^(> \\[!TASK\\].*?\\| state: (\\w+).*)$",
      "actions": [
        {
          "type": "update_structured_field",
          "params": {
            "field": "updated",
            "value_template": "{timestamp_utc_iso}"
          }
        }
      ],
      "error_handling": {
        "circuit_breaker": {
          "failure_threshold": 3,
          "recovery_timeout_seconds": 60
        }
      }
    }
  ]
}
```

## 5. Plugin (Action) Contract

The `BaseAction` class in `tools/scribe/actions/base.py` defines the formal Port contract.

```python
# tools/scribe/actions/base.py
from abc import ABC, abstractmethod
import re

class BaseAction(ABC):
    """The abstract Port for all Scribe actions."""

    @abstractmethod
    def execute(self, file_content: str, match: re.Match, file_path: str, params: dict) -> str:
        """
        Executes the action.

        Args:
            file_content: The full content of the file being processed.
            match: The regex match object that triggered the rule.
            file_path: The path to the file being processed.
            params: A dictionary of parameters from the rule's action config.

        Returns:
            The modified file content.
        """
        pass
```

## 6. Repository & Execution Instructions

1.  **Location:** The Scribe engine's source code **MUST** reside entirely within `tools/scribe/`.
2.  **Configuration:** The primary configuration file **MUST** be `config/config.json`. The schema **MUST** be `config/config.schema.json`.
3.  **Testing:** All tests, test files, and test outputs **MUST** be located within `test-environment/`.
4.  **Execution:**
    *   To run the engine, the user must first activate the Conda environment: `conda activate conda-kb`.
    *   The engine is then started via: `python tools/scribe/engine.py`.

---

### **Architectural Note: Configuration Schema Evolution Strategy for Scribe V1**

**Preamble:**
This note addresses the identified gap regarding the long-term evolution of `config.json`. While Scribe V1 will launch with a fixed schema (`config.schema.json`), future versions will inevitably require changes. This document outlines the strategy to manage these changes gracefully, ensuring backward compatibility and a clear migration path.

**1. Guiding Principle: Simplicity and Explicit Versioning**

The primary strategy is to avoid complex, implicit migration logic within the engine itself. Instead, we will rely on explicit versioning of the configuration file.

*   **Decision:** The root of `config.json` **MUST** contain a `config_version` field. The V1 schema will enforce this field with a constant value, e.g., `"1.0"`.

    ```json
    // config.json
    {
      "config_version": "1.0",
      "engine_settings": { ... },
      "security": { ... },
      "rules": [ ... ]
    }
    ```

**2. The Migration Path for Future Versions**

When a future version of Scribe introduces a breaking change to the configuration schema (e.g., renaming a key, changing a data structure), the following protocol will be followed:

*   **Schema Versioning:** A new schema file will be created (e.g., `config.schema.v2.json`), and the Scribe engine will be updated to expect `config_version: "2.0"`.

*   **Engine Behavior:**
    *   On startup, the Scribe engine will read the `config_version` from the user's `config.json`.
    *   If the version matches the engine's expected version, it proceeds with validation against the corresponding schema.
    *   If the version is *older* than the engine's expected version, the engine **MUST NOT** attempt to run. Instead, it will:
        1.  Log a clear, user-friendly error message: `ERROR: Configuration file version '1.0' is outdated. This version of Scribe requires version '2.0'.`
        2.  Direct the user to run a dedicated migration utility: `Please run 'python tools/scribe/utils/migrate_config.py' to update your configuration.`
        3.  Exit with a non-zero status code.

*   **Migration Utility (`migrate_config.py`):**
    *   A standalone, version-aware script will be provided with Scribe to handle configuration upgrades.
    *   When run, this script will:
        1.  Read the existing `config.json`.
        2.  Create a backup of the old file (e.g., `config.json.v1.bak`).
        3.  Programmatically transform the old structure to the new structure (e.g., rename keys, restructure objects).
        4.  Update the `config_version` field to the new version.
        5.  Write the new, transformed `config.json` file.
        6.  Inform the user of the successful migration and the location of the backup.

**3. Strategy for Non-Breaking (Additive) Changes**

If a new version of Scribe adds only new, optional fields to the configuration, a full version bump may not be necessary.

*   **Decision:** The JSON Schema for V1 will be defined with `"additionalProperties": false` for most objects to enforce strictness.
*   For additive changes, a new minor version of the schema can be introduced (e.g., `config_version: "1.1"`). The engine can be designed to gracefully handle older minor versions (e.g., a `1.0` config is still valid for an engine expecting `1.1`), as the missing optional fields will simply fall back to their default values within the engine's code.

**4. Summary of Benefits of this Approach**

*   **Explicit & Safe:** The engine never guesses how to interpret an old configuration. It fails fast and provides clear instructions.
*   **Decoupled Logic:** Migration logic is kept separate in a dedicated utility, preventing the core engine from becoming bloated with legacy transformation code.
*   **User Control:** The user initiates the migration, ensuring they are aware of the changes and have a backup of their old configuration.
*   **Clear Path Forward:** This establishes a predictable and maintainable process for all future configuration changes, resolving the ambiguity.