## Remediation Plan for HMA v2.2 Compliance

### Introduction

This remediation plan synthesizes the findings from a collaborative compliance analysis of the Scribe v2.2 codebase. The analysis confirms a strong architectural foundation aligned with HMA principles. However, it also reveals critical gaps between the documented architecture and the current implementation.

The primary issues preventing full compliance are:
1.  **Incomplete Architectural Refactoring:** A significant number of plugins still use legacy patterns, bypassing the mandatory Ports & Adapters interaction model.
2.  **Superficial Tier 3 Compliance:** The required Compliance Adapter for the SHACL validator is a non-functional mock.
3.  **Inconsistent Tier 1 Standard Enforcement:** Mandatory boundary validation and telemetry are not applied to all system entry and exit points.

This plan provides precise, actionable instructions to close these gaps and bring the codebase into 100% compliance with the HMA v2.2 standard.

### Priority 1 (Critical): Enforce Strict Ports & Adapters Interaction Model Across All Plugins

This is the most severe architectural violation. It breaks the core principle of decoupling business logic from infrastructure and bypasses security and observability controls.

-   **Problem:** Multiple plugins in `scribe/actions/` do not use the HMA-compliant `PluginContextPort` for dependency injection. They instantiate dependencies directly or use outdated constructors, creating tight coupling.
-   **Risk:** Violates core HMA principles, prevents technology swapping, makes testing difficult, and bypasses security/telemetry controls enforced at port boundaries.
-   **Implementation Guide:**
    1.  **Identify Non-Compliant Plugins:** The following plugins require immediate refactoring:
        -   `enhanced_frontmatter_action.py`
        -   `graph_validation_action.py`
        -   `naming_enforcement_action.py`
        -   `reconciliation_action.py`
        -   `roadmap_populator_action.py`
        -   `view_generation_action.py`
    2.  **Refactor Constructors:** For each plugin identified above, modify its `__init__` method to match the HMA v2.2 signature defined in `actions/base.py`:
        ```python
        # BEFORE (Example from graph_validation_action.py)
        def __init__(self, action_type: str, params: Dict[str, Any], plugin_context):
            super().__init__(action_type, params, plugin_context)
            # ... direct access to self.context.get_port("configuration") ...
            # This part is compliant, but other plugins are not.
            # The issue is in plugins like enhanced_frontmatter_action.py:
            # def __init__(self):
            #     super().__init__()
            #     self.llm_integration = LLMSchemaIntegration(...) # VIOLATION

        # AFTER (Required for all plugins)
        def __init__(self, action_type: str, params: Dict[str, Any], plugin_context: 'PluginContextPort'):
            super().__init__(action_type, params, plugin_context)
            # Dependencies are now accessed via ports, not instantiated here.
        ```
    3.  **Eliminate Direct Instantiation:** Remove all lines within plugin constructors that directly instantiate classes (e.g., `LLMSchemaIntegration()`, `GraphValidator()`, `NamingEnforcerV2()`). These functionalities must be wrapped in Adapters and accessed via Ports.
    4.  **Adopt Port-Based Access:** Replace all direct method calls to core components or external libraries with asynchronous calls to ports obtained from the `plugin_context`.
        ```python
        # BEFORE
        validation_errors = self.validator_instance.validate_all_documents()

        # AFTER
        validation_port = self.context.get_port("validation") # Assuming a ValidationPort exists
        validation_result = await validation_port.validate_graph(file_path)
        ```
    5.  **Standardize `execute` Method:** Ensure the primary execution method in every plugin is asynchronous and matches the signature in `BaseAction`, returning the modified file content string.
        ```python
        async def execute(self, file_content: str, match: re.Match, file_path: str, params: Dict[str, Any]) -> str:
            # ... implementation ...
            return modified_content
        ```

### Priority 2 (Critical): Implement Production-Ready Tier 3 Compliance Adapter for SHACL

-   **Problem:** The `shacl_adapter.py` is a mock implementation. It returns simulated results instead of performing actual SHACL validation.
-   **Risk:** A core feature of the `enhanced_frontmatter_action` is non-functional. The system provides a false sense of data integrity, as semantic validation is not actually occurring.
-   **Implementation Guide:**
    1.  **Update Dependencies:** Add `pyshacl` and `rdflib` with appropriate versions to the `[project.dependencies]` section of `scribe/pyproject.toml`.
    2.  **Implement Real Validation:** In `scribe/adapters/shacl_adapter.py`, remove the `_simulate_shacl_validation` method. Modify `validate_with_compliance_bridge` to call the actual `pyshacl.validate()` function.
    3.  **Implement Violation Parsing:** In `_extract_shacl_violations`, replace the simulation logic with code that parses the RDF results graph returned by `pyshacl`. This will likely involve using `rdflib` to execute SPARQL queries against the results graph to extract violation details.
    4.  **Ensure Correct Transformation:** Verify that the real violation data is correctly transformed into the HMA-compliant `ComplianceReport` and `ValidationResult` data classes defined in the adapter.

### Priority 3 (High): Enforce Tier 1 Standards at All System Boundaries

-   **Problem:** While utilities for validation and telemetry exist, they are not consistently applied at all L1/L4 adapter boundaries, particularly in the file watcher.
-   **Risk:** Incomplete observability hinders debugging and monitoring. Unvalidated data entering the system from the file system poses a security risk and violates a mandatory HMA principle.
-   **Implementation Guide:**
    1.  **Validate Incoming File Events:**
        -   In `scribe/watcher.py`, the `ScribeEventHandler` must be provided with an instance of the `BoundaryValidator`.
        -   Before calling `self.event_bus_port.publish_event`, the handler must construct the event payload and validate it against the `l1_file_system_input` schema.
        -   If validation fails, the event must be rejected, and an error-level log and an OpenTelemetry error span must be emitted.
    2.  **Instrument All Boundaries with OpenTelemetry:**
        -   Review all public methods in L1 and L4 adapters (`watcher.py`, `core/port_adapters.py`, `adapters/shacl_adapter.py`).
        -   Wrap each public method with a `HMATelemetry` span. The span must include HMA-specific attributes (`hma.boundary.type`, `hma.operation`, `hma.source.component`, `hma.target.component`).
        -   **Example for `watcher.py`:**
            ```python
            # In ScribeEventHandler.on_modified
            with telemetry.trace_boundary_operation("on_modified", "l1_driving_adapter", "file_system", "scribe_core") as span:
                # ... existing logic ...
            ```

### Priority 4 (High): Establish Production-Ready Dependencies and Testing

-   **Problem:** The `pyproject.toml` file is missing critical production dependencies, and the testing framework outlined in `TODO.md` has not been created.
-   **Risk:** The application cannot be reliably built, deployed, or maintained without a complete dependency list and an automated test suite. This introduces a high risk of regressions.
-   **Implementation Guide:**
    1.  **Finalize Dependencies:** Audit the entire codebase, including the newly implemented SHACL adapter, and add all missing production dependencies (`nats-py`, `pyshacl`, `rdflib`, `opentelemetry-*`, etc.) to `scribe/pyproject.toml`. Pin versions for build reproducibility.
    2.  **Create Testing Framework:**
        -   Create the `tests/` directory at the project root.
        -   Configure `pytest` as specified in `pyproject.toml`.
    3.  **Implement Foundational Tests:**
        -   Create unit tests for all Port Adapters in `core/port_adapters.py`. Mock external dependencies (e.g., `nats-py`, `pyshacl`) to test the adapter logic in isolation.
        -   Create an integration test for the `file_processing_orchestrator` plugin to verify that it can correctly load and execute a chain of (mocked) L3 capability plugins.
        -   Establish a CI pipeline (e.g., GitHub Actions) that runs these tests and reports on code coverage, with an initial target of >70%.

---

**Key Constraints & Requirements:**

1.  **Test-Driven Development (with a specific location):**
    *   *All testing (writing and execution) must occur within the *test-environment* folder located in the project's root directory.*  
		- The folder **test-environment\scribe-tests** has already been created and must be used for this purpose.  
		- All old tests have been archived.  
		- A **new test suite** is required.  

    	**Note:** This is a strict location requirement.

2.  **GitHub Actions (Incremental Addition):**
    *   The project already has some GitHub Actions defined, but they're disabled.
    *   *Add* new GitHub Actions for your upgrade process (e.g., automated testing, deployment), but *do not* enable the pre-existing, disabled ones. Keep them as they are.

3.  **Centralized Logging:**
    *   *All* logs generated during the upgrade process must be saved *only* within the `tools\reports` folder.  No logging anywhere else is allowed.

4.  **Scribe Code Isolation:**
    *   All code related to the Scribe system (the current version is already backed up, so you can make changes to existing files without any limitations) must reside within the `tools\scribe` folder. This includes all source code, configuration files, etc.

5.  **Conda Environment:**
    *   The project uses a Conda virtual environment named `conda-kb`.
    *   You *must* activate this environment (`conda activate conda-kb`) before starting any work.
    *   All new packages and dependencies needed for the upgrade *must* be installed within this `conda-kb` environment.

**In essence:** You need to address all Scribe issues, but within a tightly controlled environment and with specific restrictions on where code lives, where tests are run, where logs are stored, and which virtual environment to use.  You also need to leverage GitHub Actions for automation, but without touching the existing (disabled) ones.