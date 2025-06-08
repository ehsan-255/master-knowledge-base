# PROJECT EXECUTION ROADMAP

>**THE "*🚨 MANDATORY* ROADMAP PROGRESS MANAGEMENT PROTOCOL" *MUST* BE FOLLOWED AND UPDATED AT ALL TIMES TO ENSURE THE PROGRESS IS ACTIVELY TRACKED AND WORK CAN BE RESUMED FROM THE SAME POINT WITHOUT CAUSING ANY CONFUSION AND REDUNDANCY, THE PROGRESS MUST BE UPDATED CONTINUOUSLY WITHOUT ANY EXCEPTION**

>**UPDATE THE CHECKLIST CONTINUOUSLY AT ALL TIMES WITHOUT ANY EXCEPTION**

⬜ ## PROJECT OVERVIEW

**Brief Description:** To develop, test, and deploy the "Scribe" automation engine as a robust, production-ready tool, strictly adhering to the Hexagonal Microkernel Architecture (HMA). The project covers core architecture, reliability features, observability, and a secure plugin system, culminating in a stable V1 release.

---

⬜ ## PHASE 1: The Resilient Core (MVP)
- **Brief Description:** Establish a rock-solid, observable engine foundation. The goal is a stable, trustworthy tool that can be deployed and monitored safely, forming the bedrock for all future enhancements.

---

⬜ **🏁 PHASE 1 EXIT CONDITIONS**: [Phase 1 Completion Criteria]
⬜ **CONDITION 1**: Core engine runs for 24 hours under a simulated load test (5,000+ events) with no memory leaks or crashes.
⬜ **CONDITION 2**: Core features of Phase 1 are documented with code examples in the main `tools/scribe/README.md`.
⬜ **CONDITION 3**: Health endpoint and structured logs are validated in the `test-environment` and are fully operational.

---

⬜ ### STEP 1.1: Core Architecture & Event Loop
- **Brief Description:** Implement the fundamental single-process, multi-threaded architecture with a decoupled producer-consumer model, adhering to HMA principles.

---

⬜ **🏁 STEP 1.1 EXIT CONDITIONS**: [Step 1.1 Completion Criteria]
⬜ **CONDITION 1**: File system events are successfully captured and placed into the in-memory queue within 50ms of file save.
⬜ **CONDITION 2**: The worker thread successfully consumes events from the queue and logs them in the correct JSON format.

---

⬜ #### TASK 1.1.1: Project Scaffolding
- **Brief Description:** Set up the initial project structure, dependencies, and version control within the existing repository.
⬜ ###### ACTION 1.1.1.1: Create Scribe Directory Structure
- 🎬 Create the required directory structure inside `tools/scribe/` (`core/`, `actions/`) and `test-environment/scribe-tests/`.
⬜ ###### ACTION 1.1.1.2: Initialize Scribe Dependencies
- 🎬 Add initial dependencies (`watchdog`, `structlog`, `pyyaml`, `jsonschema`, `psutil`) to a `requirements.txt` file for the `conda-kb` environment.

---

⬜ #### TASK 1.1.2: Implement Producer-Consumer Loop
- **Brief Description:** Code the core event handling mechanism with graceful shutdown.
⬜ ###### ACTION 1.1.2.1: Implement Watcher (Producer) Thread
- 🎬 Write the `Watcher` class using `watchdog` to observe target directories and push events to a shared `queue.Queue`, respecting the `shutdown_event`.
⬜ ###### ACTION 1.1.2.2: Implement Worker (Consumer) Thread
- 🎬 Write the `Worker` class that runs in a separate thread, pulling events from the queue with a timeout, and respecting the `shutdown_event`.
⬜ ###### ACTION 1.1.2.3: Implement Main Orchestrator
- 🎬 Write the main `tools/scribe/engine.py` script to initialize and start the watcher and worker threads, handling `KeyboardInterrupt` to trigger the graceful shutdown.

---

⬜ #### TASK 1.1.3: Unit & Integration Testing for Event Loop
- **Brief Description:** Verify the core event pipeline works as expected.
⬜ ###### ACTION 1.1.3.1: Write Unit Tests for Watcher & Worker
- 🎬 Create unit tests in `test-environment/scribe-tests/` that verify the watcher queues events correctly and the worker consumes them, in isolation.
⬜ ###### ACTION 1.1.3.2: Write Integration Test for Event Flow
- 🎬 Create an integration test that simulates a file creation and verifies it flows from the watcher, through the queue, to the worker successfully.

---

⬜ ### STEP 1.2: Foundational Reliability & Observability
- **Brief Description:** Integrate the essential features that make the engine stable and transparent.

---

⬜ **🏁 STEP 1.2 EXIT CONDITIONS**: [Step 1.2 Completion Criteria]
⬜ **CONDITION 1**: A test confirms that a simulated interruption during a file write does not result in a corrupted file.
⬜ **CONDITION 2**: Logs for at least 5 different event types are captured and validated against the JSON log schema.
⬜ **CONDITION 3**: The `/health` endpoint is accessible via `curl` and returns a `200 OK` with a valid JSON payload.

---

⬜ #### TASK 1.2.1: Implement Crash-Safe File Writes
- **Brief Description:** Ensure file modifications are atomic to prevent data corruption.
⬜ ###### ACTION 1.2.1.1: Create Atomic Write Utility
- 🎬 Write a helper function `atomic_write(filepath, data)` that implements the `write-to-temporary-file -> os.fsync -> os.rename` pattern.

---

⬜ #### TASK 1.2.2: Implement Structured Logging
- **Brief Description:** Configure `structlog` for machine-parsable JSON log output.
⬜ ###### ACTION 1.2.2.1: Configure Structlog Processor Chain
- 🎬 Set up the `structlog` pipeline to add timestamps, log levels, and bind context, outputting everything as a JSON object to `stdout`.

---

⬜ #### TASK 1.2.3: Implement Health Check Endpoint
- **Brief Description:** Create a simple HTTP server to expose engine status.
⬜ ###### ACTION 1.2.3.1: Write Minimal HTTP Server
- 🎬 Use Python's built-in `http.server` in a separate thread to serve a `/health` endpoint.
⬜ ###### ACTION 1.2.3.2: Expose Engine Metrics
- 🎬 Pass the `event_queue` and other state information to the health server to report `queue_size`, `uptime`, and `status`.

---

⬜ #### TASK 1.2.4: Integration Testing for Reliability
- **Brief Description:** Verify the reliability and observability features work together.
⬜ ###### ACTION 1.2.4.1: Write Test for Atomic Write
- 🎬 Create a test that injects an exception between the temp-file write and the rename, asserting the original file remains untouched.
⬜ ###### ACTION 1.2.4.2: Write Test for Health Endpoint
- 🎬 Create a test that starts the engine and makes an HTTP request to the `/health` endpoint, validating the response code and payload structure.

---

⬜ ## PHASE 2: The Extensible Platform
- **Brief Description:** Transform the core engine into a powerful, configurable, and safe platform that users can easily extend.

---

⬜ **🏁 PHASE 2 EXIT CONDITIONS**: [Phase 2 Completion Criteria]
⬜ **CONDITION 1**: A new custom action plugin is added by dropping a Python file into the `actions/` directory, and it is discovered and executed successfully via a rule.
⬜ **CONDITION 2**: An invalid `config.json` change prevents the engine from starting or reloading, logging a clear validation error.
⬜ **CONDITION 3**: A test demonstrates that a rule configured to fail consistently is disabled by the circuit breaker after 3 attempts and the offending event is quarantined.

---

⬜ ### STEP 2.1: Rule Engine & Configuration Management
- **Brief Description:** Build the system that reads, validates, and executes rules from the configuration file.

---

⬜ **🏁 STEP 2.1 EXIT CONDITIONS**: [Step 2.1 Completion Criteria]
⬜ **CONDITION 1**: A change to a rule's `trigger_pattern` in `config.json` is detected and applied by the running engine within 5 seconds, without a restart.
⬜ **CONDITION 2**: A rule with an invalid regex pattern is rejected with a descriptive error message on load.

---

⬜ #### TASK 2.1.1: Implement Config Loader & Validator
- **Brief Description:** Safely load and validate the `config.json` file.
⬜ ###### ACTION 2.1.1.1: Define JSON Schema
- 🎬 Create a `config/config.schema.json` file that formally defines the structure, types, and required fields for all rules and settings.
⬜ ###### ACTION 2.1.1.2: Write Config Manager
- 🎬 Create a `ConfigManager` class that loads `config.json`, validates it against the schema using the `jsonschema` library, and provides access to the configuration.
⬜ ###### ACTION 2.1.1.3: Implement Hot-Reloading
- 🎬 Use a `watchdog` observer within the `ConfigManager` to monitor `config.json` for changes and trigger a safe, atomic reload.

---

⬜ #### TASK 2.1.2: Implement Rule Processor
- **Brief Description:** Create the logic that matches file content against rule triggers.
⬜ ###### ACTION 2.1.2.1: Develop Rule Matching Logic
- 🎬 Write the `RuleProcessor` that takes a file path and content, iterates through the loaded rules, and uses pre-compiled regex from `re.finditer` to match `trigger_pattern` against the content.

---

⬜ ### STEP 2.2: Action Plugin System & Security
- **Brief Description:** Develop the plugin architecture for actions and implement critical security guardrails.

---

⬜ **🏁 STEP 2.2 EXIT CONDITIONS**: [Step 2.2 Completion Criteria]
⬜ **CONDITION 1**: The `run_command` action fails with a security error when attempting to execute a command not present in the `security.allowed_commands` list.
⬜ **CONDITION 2**: The circuit breaker correctly quarantines a file that causes a rule to fail repeatedly.

---

⬜ #### TASK 2.2.1: Build Plugin System
- **Brief Description:** Create the mechanism for discovering and dispatching to action plugins.
⬜ ###### ACTION 2.2.1.1: Define BaseAction Class
- 🎬 Create an abstract base class `BaseAction` in `tools/scribe/actions/base.py` with an `execute()` method that all plugins must implement.
⬜ ###### ACTION 2.2.1.2: Implement Plugin Loader
- 🎬 Write a `PluginLoader` that dynamically imports all Python modules from the `actions/` directory and registers any classes that inherit from `BaseAction`.
⬜ ###### ACTION 2.2.1.3: Implement Action Dispatcher
- 🎬 Create an `ActionDispatcher` that, given a rule's action configuration, finds the corresponding loaded plugin and calls its `execute()` method.

---

⬜ #### TASK 2.2.2: Implement Security Sandboxing
- **Brief Description:** Harden the engine against malicious configuration.
⬜ ###### ACTION 2.2.2.1: Implement Command Whitelisting
- 🎬 In the `run_command` action, check the command against the `security.allowed_commands` list from the config before execution.
⬜ ###### ACTION 2.2.2.2: Implement Environment Scrubbing
- 🎬 Ensure the `subprocess.run` call for the `run_command` action uses a minimal, clean environment (`env={...}`).

---

⬜ #### TASK 2.2.3: Implement Circuit Breaker
- **Brief Description:** Add a failure isolation mechanism to the engine.
⬜ ###### ACTION 2.2.3.1: Write Circuit Breaker Class
- 🎬 Create a `CircuitBreaker` class that tracks failures on a per-rule ID basis and manages `CLOSED`, `OPEN`, and `HALF_OPEN` states.
⬜ ###### ACTION 2.2.3.2: Integrate Breaker into Action Dispatcher
- 🎬 Wrap the action execution logic in the dispatcher with the circuit breaker, so that exceptions increment the failure count and can trip the breaker.
⬜ ###### ACTION 2.2.3.3: Implement Quarantine Logic
- 🎬 When the breaker opens, move the offending event/file to the configured quarantine directory.

---

⬜ **🏁 PROJECT EXIT CONDITIONS**: [Final Completion Criteria for Entire Project]
⬜ **CONDITION 1**: All features specified in Phase 1 and Phase 2 are implemented and pass all unit and integration tests.
⬜ **CONDITION 2**: A comprehensive `README.md` is created in `tools/scribe/`, detailing installation, configuration, and how to create a new action plugin.
⬜ **CONDITION 3**: The final V1 application is packaged (e.g., as a Python wheel) and ready for distribution.

---

## STATUS LEGEND

⬜ **NOT STARTED**
🔄 **IN PROGRESS**
✅ **COMPLETED**
❌ **BLOCKED**

**NOTE:** ***🔄 IN PROGRESS and ❌ BLOCKED statuses must be applied to all the affected parent branches all the way up to the project level***

---

## EXECUTION PROTOCOL

### **SEQUENTIAL PROGRESSION**

- **PHASES**: Must complete 1 → 2 → 3...
- **STEPS**: Must complete 1.1 → 1.2 → 1.3...
- **TASKS**: Must complete 1.1.1 → 1.1.2 → 1.1.3...
- **NO PARALLEL EXECUTION** unless explicitly planned

### **COMPLETION STANDARDS**

- **100% COMPLETION REQUIRED** before advancing
- **ZERO TOLERANCE** for partial completion
- **EXIT CONDITIONS** must be verified and checked off

### **BLOCKED PROGRESS PROTOCOL**
If progress is blocked,

1. **TAKE A STEP BACK**, review and analyze the plan from a different perspective, then craft an alternative strategy and try again. IF resolved, continue, ELSE, GOTO 2
2. **GO BACKWARDS STEP BY STEP**, review and analyze the plan meticulously at each step, and try to identify the flaw in the plan or where the problem was introduced (go back until the previous 100% checkpoint)
2.1 **IF A SOLUTION IS FOUND**, apply and continue
2.2 **ELSE IF NO SOLUTION IS FOUND**, mark the plan as **❌ BLOCKED** and execute the **FAILURE PROTOCOL**

### **FAILURE PROTOCOL**
If progress is blocked,

1. **IMMEDIATELY STOP** all progression
2. **DOCUMENT** blocking issue with specific details
2.1 **ADD** a one-liner note to the plan
2.2 **UPDATE** the progress report with specific details
2.3 **ENSURE** the specific item and all the affected parent branches are marked as **❌ BLOCKED**

## **🚨 MANDATORY** ROADMAP PROGRESS MANAGEMENT PROTOCOL

>**THIS PROTOCOL IS *MANDATORY* AND *MUST* BE FOLLOWED AT ALL TIMES**

### **PROGRESS TRACKING OPTIONS**

#### **OPTION B: SEPARATE PROGRESS CHECKLIST** (for longer roadmaps)
- **GENERATE** separate progress checklist file with tree-structure matching roadmap ToC
- **UPDATE** status checkboxes in the separate checklist
- **ADD** one-liner notes to the checklist items (NOT the roadmap)
- **MAINTAIN** separate detailed progress tracker document

### **MANDATORY UPDATES**

1. **STATUS TRACKING**: Update checkboxes continuously (refer to status legend)
2. **ONE-LINER NOTES**: Add important execution points (roadmap OR checklist based on option chosen)
3. **DETAILED PROGRESS**: Update progress tracker document after each completion