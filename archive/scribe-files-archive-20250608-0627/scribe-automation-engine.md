---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:15Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: archive
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# Design Report: The "Scribe" Automation Engine

## 1. Executive Summary

"Scribe" is a lightweight, event-driven automation engine designed to maintain and enhance a plain-text knowledge base. It operates as a silent background service, observing file changes and executing pre-defined actions based on configurable rules.

Its primary purpose is to eliminate manual, repetitive tasks like timestamping, task ID generation, and file cleanup, ensuring the knowledge base remains consistent, accurate, and self-maintaining. The engine is built on principles of **modularity, resilience, and efficiency**, allowing it to coexist seamlessly with other user-driven and automated workflows in a large repository.

## 2. Core Architecture: The Timestamp Engine

At its heart, Scribe is a sophisticated timestamping utility. Its architecture is designed around a simple, powerful loop: **Observe → Trigger → Act**.

### 2.1. System Components

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| **The Observer** | Python `watchdog` | Efficiently monitors the file system for `create`, `modify`, and `delete` events using native OS APIs. |
| **The Brain** | `config.json` | A declarative JSON file that defines all rules, patterns (triggers), and corresponding actions. |
| **The Hands** | `engine.py` | The Python script that parses the config, runs the observer, and executes actions. |

### 2.2. The Fundamental Workflow

The engine's primary job is to manage timestamps on task lines within Markdown files.

1.  **A User Action:** A user or an LLM edits a line in a `.md` file to change a task's status.
    *   **Before:** `> [!TASK] Design the API | id: a4b3c | state: todo | ...`
    *   **After:** `> [!TASK] Design the API | id: a4b3c | state: done | ...`

2.  **The Engine's Response:**
    *   The **Observer** detects the file save.
    *   The **Engine** reads the changed file.
    *   It matches a **Trigger** in `config.json` (e.g., `state` field changed).
    *   It executes the specified **Action** (e.g., `update_timestamp` on the `updated` field).

3.  **The Result (Automatic & Instant):**
    *   **Final State:** `> [!TASK] ... | state: done | ... | updated: 2024-10-27T17:00:00Z`

This simple, automated loop ensures all timestamps are accurate to the second without any manual intervention.

## 3. Design Decisions & Safeguards

To ensure stability and performance in a large, active repository, the following design principles are critical.

| Principle | Implementation | Purpose |
| :--- | :--- | :--- |
| **Efficiency** | **Event-Driven Model:** Uses native OS events. No constant file scanning. CPU and disk I/O are near-zero when idle. | Prevents resource drain on large repositories. |
| **Resilience** | **Event Queue & Single Worker:** File events are placed in a queue and processed sequentially by a single worker thread. | Prevents system overload during bulk file modifications (e.g., 5,000+ file changes). The engine processes the backlog calmly instead of crashing. |
| **Control** | **Manual Pause/Resume:** A `.engine-pause` "lock file" allows any external script to pause the engine's activity before a bulk operation and resume it after. | Gives the user and other automations full control, eliminating the need to ever stop the engine process. |
| **Safety** | **Infinite Loop Prevention:** A temporary "ignore window" prevents the engine from reacting to its own file-write events. | Ensures stability and prevents runaway feedback loops between automations. |
| **Precision** | **`.gitignore` & Exclude Paths:** The engine respects `.gitignore` and a custom `exclude_paths` list to avoid watching irrelevant directories like `node_modules/`. | Dramatically reduces file system noise and focuses the engine's attention only where needed. |
| **Usability** | **Dry Run Mode:** A `--dry-run` flag allows the engine to log what it *would* do without modifying any files. | Enables safe testing and configuration validation. |

## 4. The Potential: Beyond Timestamps

The engine's true power lies in its generic, configurable design. The "action" is not limited to timestamping. By extending the `config.json`, the engine evolves into a general-purpose automation platform for your knowledge base.

### 4.1. Actionable Triggers

The engine can be configured to react to a wide variety of triggers:

*   **Text Patterns:** A specific emoji (`⛔`), a keyword (`FIXME`), or a change in a structured data field (`state: done`).
*   **File Events:** A new file created in a specific folder (`/meetings/`).
*   **Metadata:** A change in a file's YAML frontmatter (`status: published`).

### 4.2. Expanded Capabilities

This unlocks advanced, self-maintaining workflows:

*   **Project Management:**
    *   **Auto-Archiving:** Move completed tasks to an archive file.
    *   **Dependency Chaining:** Unlock blocked tasks when their dependencies are completed.
*   **Knowledge Base Hygiene:**
    *   **Template Injection:** Populate new notes from a template file.
    *   **Automatic Tagging:** Add frontmatter tags based on a file's location.
*   **Codebase Management:**
    *   **TODO Aggregation:** Sync `# TODO` comments from `.py` files into a central Markdown report.
    *   **Custom Linting:** Enforce documentation or code style rules.
*   **External Integrations:**
    *   **Notifications:** Send a push notification when a critical task is created.
    *   **Git Automation:** Automatically commit archival or report files.

By separating the **engine's logic** from the **workflow rules**, Scribe becomes a powerful, adaptable, and future-proof foundation for automating a plain-text-centric workflow.

---

Here is the technical deep-dive. This section translates the conceptual design into a concrete technical specification, using precise terminology to describe the implementation.

---

# Technical Specification: The "Scribe" Automation Engine

## 1. Core Architecture: A Decoupled Producer-Consumer Model

The engine is architected as a multi-threaded application employing a **Producer-Consumer pattern** to ensure resilience and non-blocking I/O. This decouples event detection from event processing.

| Component | Implementation Detail | Key Libraries/Modules |
| :--- | :--- | :--- |
| **Producer Thread** | `watchdog.observers.Observer` | `watchdog` |
| **Event Queue** | `queue.Queue` (thread-safe) | `queue` |
| **Consumer Thread** | A dedicated `threading.Thread` worker | `threading` |
| **Configuration** | A singleton `Config` class loading `config.json` | `json`, `pathlib` |

### 1.1. Event Flow

1.  **Initialization:** The main process instantiates and starts the `Observer` (Producer) and `Worker` (Consumer) threads.
2.  **Event Detection (Producer):** The `Observer` thread listens for file system events via OS-native APIs (`inotify`, `FSEvents`, `ReadDirectoryChangesW`). Upon detection, it creates an `Event` object (e.g., `{'type': 'modified', 'path': '/path/to/file.md'}`) and places it onto the shared `queue.Queue`. This is a low-latency, non-blocking operation.
3.  **Event Consumption (Consumer):** The `Worker` thread runs an infinite loop, calling `queue.get()`. This is a **blocking call**, ensuring the thread sleeps with 0% CPU usage until an event is available.
4.  **Processing:** Upon receiving an `Event`, the `Worker` invokes a `RuleProcessor` to handle the logic.

## 2. The Rule Processor: A State-Driven Regex Engine

The `RuleProcessor` is the core logic unit. It iterates through rules defined in `config.json` and applies them to the content of the modified file.

### 2.1. Rule Matching and Execution

For each file change, the processor executes the following algorithm:

1.  **File Read:** The file content is read into memory. For large files, a line-by-line streaming approach is used via a generator to minimize memory footprint.
2.  **Rule Iteration:** For each rule in the configuration:
    *   **Glob Matching:** The file path is matched against the rule's `file_glob` pattern using `pathlib.Path.glob()`.
    *   **Regex Search:** If the glob matches, `re.finditer()` is used to find all occurrences of the rule's `trigger_pattern` within the file content. This is more efficient than `re.search` for multiple matches.
3.  **Action Dispatch:** For each successful regex match, an `ActionFactory` instantiates and executes the corresponding action class (e.g., `UpdateTimestampAction`, `RunCommandAction`).

### 2.2. State-Aware Processing for Timestamps

To differentiate between new task creation and updates, the engine maintains a lightweight in-memory state.

*   **Trigger Logic:** A rule for "new tasks" uses a **negative lookahead** in its regex (`(?!.*id:)`) to match only lines *lacking* an ID. A rule for "updates" matches lines that *have* an ID.
*   **Idempotency:** Actions are designed to be idempotent. For example, the `AddFieldAction` for `id` generation first checks if the field already exists before acting, preventing duplicate fields.

## 3. Performance and Resilience Mechanisms

### 3.1. Concurrency and Resource Management

*   **Event Debouncing:** To handle rapid-fire saves (e.g., from an IDE), a **debouncing** mechanism is implemented. A `threading.Timer` is used. When an event arrives, a timer is started. If a subsequent event for the same file arrives before the timer expires, the timer is reset. The event is only added to the queue after the file has "settled."
*   **Queue-Based Throttling:** The `queue.Queue` naturally throttles processing. A burst of 5,000 events results in a queue of size 5,000, not 5,000 concurrent operations. This smooths CPU and disk I/O into a predictable, sequential workload.

### 3.2. System Interoperability and Safety

*   **External Pause/Resume (Safety Valve):** The `Worker` thread implements a **polling check** for a lock file (e.g., `.engine-pause`) at the start of its `queue.get()` loop. The existence of this file causes the thread to enter a `time.sleep()` cycle, effectively pausing consumption without terminating the process. This provides a simple, file-based IPC mechanism for other scripts.
*   **Feedback Loop Prevention:** A `collections.deque` with a `maxlen` acts as a short-term cache of recently modified file paths. Before processing an event, the engine checks this cache. If the path is present, the event is discarded. This prevents the engine from reacting to its own write operations.
*   **Graceful Shutdown:** The engine listens for `SIGINT` and `SIGTERM` signals. The signal handler sets a `threading.Event` flag, which gracefully terminates the `Observer` and `Worker` threads, ensuring a clean exit.

## 4. Advanced Feature Implementation

### 4.1. Frontmatter Processing

*   **YAML-Aware Actions:** Actions targeting frontmatter will use the `PyYAML` or `ruamel.yaml` library. The regex `(?s)^---\\n(.*?)\\n---` will capture the frontmatter block as a string. This string is then parsed into a Python dictionary, modified, and then dumped back into a string using `yaml.dump()`, preserving structure and comments (if using `ruamel.yaml`).

### 4.2. Template Population

*   **Event Hook:** This requires binding to the `watchdog.events.FileCreatedEvent`.
*   **Templating Engine:** The `populate_from_template` action will use a lightweight templating engine like `jinja2` to substitute variables (`{{title}}`, `{{date}}`) into the template file's content before writing it to the newly created file.

### 4.3. External Command Execution

*   **Subprocess Management:** The `RunCommandAction` will use the `subprocess.run()` module.
*   **Security:** Commands will be executed with `shell=False` where possible, passing arguments as a list to prevent shell injection vulnerabilities. Standard output and error streams will be captured for logging. A configurable timeout will be used to prevent hung processes.

---

This final section provides the deepest level of technical detail, including code patterns and specific configuration examples, to serve as a direct blueprint for implementation.

---

# Implementation Blueprint: The "Scribe" Automation Engine

## 1. Core Architecture: Multi-threaded Producer-Consumer

The engine's stability under load is guaranteed by a classic producer-consumer architecture using Python's standard libraries.

### 1.1. Main Orchestrator (`engine.py`)

The main script initializes and manages the lifecycle of the system's threads.

```python
# engine.py (simplified)
import time
from queue import Queue
from threading import Thread
from watchdog.observers import Observer

def main():
    event_queue = Queue()
    shutdown_event = threading.Event()

    # 1. Producer: The Watcher Thread
    event_handler = FileSystemEventHandler(event_queue)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    # 2. Consumer: The Worker Thread
    worker = Worker(event_queue, shutdown_event)
    worker_thread = Thread(target=worker.run, daemon=True)
    worker_thread.start()

    try:
        while not shutdown_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutdown signal received...")
    finally:
        shutdown_event.set()
        observer.stop()
        observer.join()
        worker_thread.join()
```

### 1.2. The Event Queue (`queue.Queue`)

This thread-safe queue is the critical buffer between detection and processing. A burst of 5,000 file events simply populates the queue rapidly. The worker consumes these events sequentially, preventing resource exhaustion.

## 2. The Worker and Rule Processor

The worker pulls from the queue and delegates to the `RuleProcessor`, which contains the core application logic.

### 2.1. Worker Thread Logic

The worker's design incorporates the **Pause/Resume safety valve**.

```python
# worker.py (simplified)
import os
from pathlib import Path

class Worker:
    def __init__(self, queue, shutdown_event):
        self.queue = queue
        self.shutdown_event = shutdown_event
        self.pause_file = Path('.engine-pause')
        self.rule_processor = RuleProcessor('config.json')

    def run(self):
        while not self.shutdown_event.is_set():
            # Safety Valve: Check for pause file before getting a new task
            if self.pause_file.exists():
                time.sleep(2) # Poll every 2 seconds
                continue

            try:
                event = self.queue.get(timeout=1) # Timeout allows checking shutdown_event
                self.rule_processor.process(event)
                self.queue.task_done()
            except queue.Empty:
                continue
```

### 2.2. Rule Configuration (`config.json`)

The `config.json` is the declarative brain. Its structure directly maps to the processor's logic.

**Example: A rule to manage task timestamps and auto-archive.**

```json
{
  "rules": [
    {
      "name": "Update Task Timestamp on State Change",
      "file_glob": "**/projects/**/*.md",
      "trigger_pattern": "^(> \\[!TASK\\].*?\\| state: (\\w+).*)$",
      "actions": [
        {
          "type": "update_structured_field",
          "field": "updated",
          "value_template": "{timestamp_utc_iso}"
        }
      ]
    },
    {
      "name": "Archive Completed Tasks",
      "file_glob": "**/projects/**/*.md",
      "trigger_pattern": "^(> \\[!TASK\\].*?\\| state: done.*)$",
      "actions": [
        {
          "type": "move_line_to_file",
          "target_file": "archive/completed_tasks.md",
          "content_template": "{matched_line} | archived: {timestamp_utc_iso}"
        }
      ]
    }
  ]
}
```

### 2.3. Rule Processing Algorithm

The `RuleProcessor` uses compiled regex for efficiency.

```python
# rule_processor.py (simplified)
import re

class RuleProcessor:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        # Pre-compile regex for performance
        for rule in self.config['rules']:
            rule['compiled_pattern'] = re.compile(rule['trigger_pattern'])

    def process(self, event):
        # ... logic to read file content ...
        new_lines = []
        lines_to_remove = set()

        for i, line in enumerate(original_lines):
            for rule in self.config['rules']:
                if rule['compiled_pattern'].match(line):
                    # ActionFactory creates and executes action objects
                    modified_line, status = ActionFactory.execute(rule['actions'], line)
                    if status == 'line_moved':
                        lines_to_remove.add(i)
                    line = modified_line # Chain modifications
            
            if i not in lines_to_remove:
                new_lines.append(line)
        
        # ... logic to write new_lines back to file ...
```

## 3. Advanced Feature Implementation Details

### 3.1. Frontmatter Handling with `ruamel.yaml`

To safely edit YAML frontmatter without destroying comments or formatting, `ruamel.yaml` is superior to `PyYAML`.

```python
# actions/frontmatter_action.py
from ruamel.yaml import YAML
import io

def update_frontmatter(content, field, value):
    yaml = YAML()
    # Regex to extract frontmatter block
    match = re.match(r'(?s)^---\n(.*?)\n---', content)
    if not match:
        return content # No frontmatter found

    frontmatter_str = match.group(1)
    data = yaml.load(frontmatter_str)
    data[field] = value

    string_stream = io.StringIO()
    yaml.dump(data, string_stream)
    updated_frontmatter = string_stream.getvalue()

    # Reconstruct the file content
    return f"---\n{updated_frontmatter}---\n{content[match.end():]}"
```

### 3.2. Feedback Loop Prevention

A fixed-size queue (`deque`) provides an efficient O(1) cache for recently modified files.

```python
# worker.py (within Worker class)
from collections import deque

class Worker:
    def __init__(self, ...):
        # ...
        self.recently_processed = deque(maxlen=50) # Cache last 50 files

    def process_event(self, event):
        # Check if we just wrote to this file
        if event.src_path in self.recently_processed:
            return # Ignore event to prevent feedback loop

        # ... process the file ...

        # If we wrote to the file, add it to the cache
        if file_was_modified:
            self.recently_processed.append(event.src_path)
```

### 3.3. External Command Execution with `subprocess`

This action demonstrates secure execution with timeouts.

```json
// config.json rule
{
  "name": "Critical Alert Notification",
  "trigger_pattern": ".*priority: critical.*",
  "actions": [
    {
      "type": "run_command",
      "command": [
        "curl",
        "-d", "Critical task detected: {matched_line}",
        "ntfy.sh/my-alerts-channel"
      ],
      "timeout": 5
    }
  ]
}
```

```python
# actions/command_action.py
import subprocess

def run_command(command_list, timeout):
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True, # Raises CalledProcessError on non-zero exit codes
            timeout=timeout
        )
        print(f"Command success: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.stderr}")
    except subprocess.TimeoutExpired:
        print("Command timed out.")
```
