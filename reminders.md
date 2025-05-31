**Reminders:**

1.  **`CONTRIBUTOR_GUIDE.md`:** Please review/define its purpose, structure, guidelines, and final location. Update the commented-out/corrected links in `GM-GUIDE-STANDARDS-BY-TASK.md` and any other relevant documents.
2.  **`TODO-MASTER-LIST.md`:** Please review/define its purpose, structure, and guidelines for tracking major project TODOs.
3.  **`master_todo_populate.py`:** Please define its purpose (likely to scan for `[!TODO]` callouts in documents and populate `TODO-MASTER-LIST.md`), its responsibilities (how it parses, what it extracts), and usage guidelines. Consider its interaction with the linter (which could also flag TODOs).
4.  **Scripting Standards/Guidelines:** Please initiate, define, and document a new category of standards/guidelines specifically for scripting within this project. This should cover aspects like:
    *   Script naming conventions.
    *   Required error handling and exit codes.
    *   Comprehensive logging practices.
    *   Argument parsing conventions.
    *   Dependency management (e.g., use of `requirements.txt`, conda environments).
    *   Code style and commenting.
5.  **Logging & Review Mandate for Scripts:** Please add to the new scripting guidelines (and any relevant process documentation) that every team member MUST:
    *   Implement comprehensive logging in every script created or modified.
    *   Ensure logs capture key decisions, actions taken, files processed, and any errors or warnings encountered.
    *   Fully review logs immediately after each script run to verify expected behavior.
    *   Manually review a significant percentage of affected files (e.g., 50% or a sample based on risk/impact) to ensure the accuracy of the script and the correctness of the changes reflected in the logs.