# PROJECT EXECUTION ROADMAP

>**THE "*🚨 MANDATORY* ROADMAP PROGRESS MANAGEMENT PROTOCOL" *MUST* BE FOLLOWED AND UPDATED AT ALL TIMES TO ENSURE THE PROGRESS IS ACTIVELY TRACKED AND WORK CAN BE RESUMED FROM THE SAME POINT WITHOUT CAUSING ANY CONFUSION AND REDUNDANCY, THE PROGRESS MUST BE UPDATED CONTINUOUSLY WITHOUT ANY EXCEPTION**

>**UPDATE THE CHECKLIST CONTINUOUSLY AT ALL TIMES WITHOUT ANY EXCEPTION**

⬜ ## PROJECT OVERVIEW

Implement the critical functional gaps and high-priority refinements identified in the Scribe v1.0.1 technical audit. The primary outcome is a fully functional, secure, and observable engine that aligns completely with its architectural blueprint and HMA specifications.

---

⬜ ## PHASE 1: Core Functional Integration & Logic Implementation
- Brief Description: This phase addresses the most critical gap: the lack of processing logic in the `Worker` thread. The goal is to connect all core components to create a fully operational event processing pipeline.

---

⬜ **🏁 PHASE 1 EXIT CONDITIONS**: (C=1)
⬜ **CONDITION 1**: The Scribe engine can successfully process a file system event from detection through rule matching, action dispatching, and final file modification using the `atomic_write` utility.
- [IF CONDITIONS = TRUE: GOTO CONDITION 2; ELSE: GOTO ONE LEVEL UP]
⬜ **CONDITION 2**: A new end-to-end integration test successfully validates the entire processing pipeline.
- [IF CONDITIONS = TRUE: GOTO PHASE 2; ELSE: GOTO ONE LEVEL UP]

---

⬜ ### STEP 1.1: Integrate Core Components into Worker Thread
- Brief Description: Refactor the `Worker` class to instantiate and orchestrate all necessary core services, transforming it from a placeholder into the engine's central processing hub.

---

⬜ **🏁 STEP 1.1 EXIT CONDITIONS**: (C=1)
⬜ **CONDITION 1**: The `Worker` class correctly initializes `ConfigManager`, `PluginLoader`, `SecurityManager`, `RuleProcessor`, and `ActionDispatcher`.
- [IF CONDITIONS = TRUE: GOTO CONDITION 2; ELSE: GOTO ONE LEVEL UP]
⬜ **CONDITION 2**: The `_process_event` method implements the full logic chain from reading a file to dispatching actions.
- [IF CONDITIONS = TRUE: GOTO STEP 1.2; ELSE: GOTO ONE LEVEL UP]

---

⬜ #### TASK 1.1.1: Instantiate Core Services in Worker
- Brief Description: Modify the `Worker`'s `__init__` method to create and hold instances of all core service components.

⬜ ##### SUBTASK 1.1.1.1: Modify `Worker.__init__`
- 🎬 Modify the `__init__` method in `scribe/worker.py` to accept no arguments and instead instantiate `ConfigManager`, `PluginLoader`, `SecurityManager`, `RuleProcessor`, and `ActionDispatcher`. Store these as instance attributes (e.g., `self.config_manager`, `self.plugin_loader`, etc.).

---

⬜ #### TASK 1.1.2: Implement Event Processing Logic in `_process_event`
- Brief Description: Replace the placeholder logic in the `_process_event` method with the complete, orchestrated workflow for handling a file event.

⬜ ##### SUBTASK 1.1.2.1: Read File Content
- 🎬 In `scribe/worker.py`, within `_process_event`, add logic to safely open and read the full content of the file specified by `event['file_path']`. Wrap this in a `try...except` block to handle potential `IOError`.

⬜ ##### SUBTASK 1.1.2.2: Find Rule Matches
- 🎬 Using the `self.rule_processor` instance, call `process_file()` with the file path and content to get a list of `RuleMatch` objects.

⬜ ##### SUBTASK 1.1.2.3: Dispatch Actions for Each Match
- 🎬 Loop through the list of `RuleMatch` objects. For each match, call `self.action_dispatcher.dispatch_actions()`. Keep track of the final, potentially modified, file content.

⬜ ##### SUBTASK 1.1.2.4: Atomically Write Modified Content
- 🎬 After the loop, check if the final file content has changed from the original. If it has, use the `atomic_write` function from `scribe/core/atomic_write.py` to save the new content back to the original file path.

---

⬜ ### STEP 1.2: Create Verification Test for End-to-End Flow
- Brief Description: Develop a new integration test that verifies the successful implementation of the entire Phase 1 workflow.

---

⬜ **🏁 STEP 1.2 EXIT CONDITIONS**: (C=1)
⬜ **CONDITION 1**: A new test file exists in `test-environment/scribe-tests/` that simulates a file change, triggering a pre-configured rule.
- [IF CONDITIONS = TRUE: GOTO CONDITION 2; ELSE: GOTO ONE LEVEL UP]
⬜ **CONDITION 2**: The test asserts that the action was executed and the target file's content was correctly modified.
- [IF CONDITIONS = TRUE: GOTO PHASE 1 EXIT CONDITIONS; ELSE: GOTO ONE LEVEL UP]

---

⬜ #### TASK 1.2.1: Develop New Integration Test
- 🎬 Create a new test file `test-environment/scribe-tests/test_full_pipeline.py`. This test will programmatically create a test file, start the Scribe engine, modify the test file to trigger a rule, wait for processing, and then assert that the file was correctly updated by the corresponding action.

---

⬜ ## PHASE 2: Security, API, and Observability Refinements
- Brief Description: This phase addresses the high and medium-priority recommendations from the audit, focusing on enhancing security features, improving API contracts, and enriching observability data.

---

⬜ **🏁 PHASE 2 EXIT CONDITIONS**: (C=1)
⬜ **CONDITION 1**: The `run_command` action correctly uses the `allowed_env_vars` parameter, and this is verified by a test.
- [IF CONDITIONS = TRUE: GOTO CONDITION 2; ELSE: GOTO ONE LEVEL UP]
⬜ **CONDITION 2**: The `/health` endpoint exposes detailed statistics from the `ActionDispatcher` and `CircuitBreakerManager`.
- [IF CONDITIONS = TRUE: GOTO PROJECT EXIT CONDITIONS; ELSE: GOTO ONE LEVEL UP]

---

⬜ ### STEP 2.1: Implement `allowed_env_vars` Security Feature
- Brief Description: Align the `SecurityManager` and `RunCommandAction` with the blueprint specification for securely passing environment variables.

---

⬜ **🏁 STEP 2.1 EXIT CONDITIONS**: (C=1)
⬜ **CONDITION 1**: `SecurityManager.execute_command_safely` is updated to correctly handle the `allowed_env_vars` parameter.
- [IF CONDITIONS = TRUE: GOTO CONDITION 2; ELSE: GOTO ONE LEVEL UP]
⬜ **CONDITION 2**: `RunCommandAction` correctly passes this parameter from its configuration.
- [IF CONDITIONS = TRUE: GOTO STEP 2.2; ELSE: GOTO ONE LEVEL UP]

---

⬜ #### TASK 2.1.1: Update `SecurityManager`
- Brief Description: Modify the `SecurityManager` to support selective environment variable pass-through.

⬜ ##### SUBTASK 2.1.1.1: Modify `execute_command_safely`
- 🎬 In `scribe/core/security_manager.py`, modify the signature of `execute_command_safely` to accept an optional `allowed_env_vars: List[str] = None` parameter.

⬜ ##### SUBTASK 2.1.1.2: Update `scrub_environment`
- 🎬 In `scribe/core/security_manager.py`, modify `scrub_environment` to accept the `allowed_env_vars` list. If the list is provided, the function should iterate through it and copy the specified variables from `os.environ` into the new "safe" environment dictionary.

---

⬜ #### TASK 2.1.2: Update `RunCommandAction` Plugin
- Brief Description: Connect the action's configuration to the new `SecurityManager` functionality.

⬜ ##### SUBTASK 2.1.2.1: Pass `allowed_env_vars` Parameter
- 🎬 In `scribe/actions/run_command_action.py`, within the `execute` method, retrieve the `allowed_env_vars` list from the `params` dictionary and pass it to the `self.security_manager.execute_command_safely` call.

---

⬜ ### STEP 2.2: Enhance Health Endpoint
- Brief Description: Expose the detailed statistics collected by core components through the `/health` monitoring endpoint.

---

⬜ **🏁 STEP 2.2 EXIT CONDITIONS**: (C=1)
⬜ **CONDITION 1**: The JSON response from the `/health` endpoint contains new top-level keys for `action_dispatcher_stats` and `circuit_breaker_stats`.
- [IF CONDITIONS = TRUE: GOTO PHASE 2 EXIT CONDITIONS; ELSE: GOTO ONE LEVEL UP]

---

⬜ #### TASK 2.2.1: Expose New Metrics in `ScribeEngine`
- Brief Description: Modify the engine's main status provider function to aggregate and include the new statistical data.

⬜ ##### SUBTASK 2.2.1.1: Update `get_status` Method
- 🎬 In `scribe/engine.py`, modify the `get_status` method. After the `Worker` is initialized, it will have instances of the `ActionDispatcher` and `CircuitBreakerManager`. Call the `get_execution_stats()` and `get_circuit_breaker_stats()` methods on these instances and add their output to the main `status` dictionary.

---

⬜ **🏁 PROJECT EXIT CONDITIONS**: (C=1)
⬜ **CONDITION 1**: All tasks in Phase 1 and Phase 2 are complete and their exit conditions are met.
- [IF CONDITIONS = TRUE: GOTO CONDITION 2; ELSE: GOTO TOP]
⬜ **CONDITION 2**: The Scribe engine is fully functional, secure according to its blueprint, and observable. All new functionality is covered by tests.
- [IF CONDITIONS = TRUE: GOTO CONDITION 3; ELSE: GOTO TOP]
⬜ **CONDITION 3**: The project's `README.md` is updated to reflect the new features and capabilities.
- [IF CONDITIONS = TRUE: GOTO TOP; ELSE: GOTO TOP]

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

