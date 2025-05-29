---
title: "Standard: Markdown Syntax for Definition Lists"
standard_id: "SF-SYNTAX-DEFINITION-LISTS"
aliases: ["Definition List Syntax", "Markdown DL Syntax"]
tags:
  - status/draft
  - criticality/P3-Low # Definition lists are less common than other elements
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Markdown Definition List Syntax" # As per prompt
related-standards: ["SF-FORMATTING-FILE-HYGIENE"] # For blank line rules
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "SF" # Syntax & Formatting
sub_domain: "SYNTAX" # As per prompt
scope_application: "Defines the syntax for creating definition lists in Markdown documents, intended for term-definition pairs such as glossaries or descriptive itemizations."
criticality: "P3-Low"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Structured content (glossaries, etc.)", "Readability", "Authoring consistency", "Semantic representation of definitions"]
change_log_url: "./SF-SYNTAX-DEFINITION-LISTS-changelog.md" # Placeholder
---

# Standard: Markdown Syntax for Definition Lists (SF-SYNTAX-DEFINITION-LISTS)

## 1. Standard Statement

This standard defines the recommended syntax for creating definition lists within Markdown documents. Definition lists are used to present a series of terms, each followed by one or more definitions or descriptions. While not part of the core CommonMark specification, definition list syntax is a common extension supported by many Markdown processors.

Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around block elements is also important for definition lists.

## 2. Core Definition List Syntax (Common Extension)

The most common syntax for definition lists, often associated with PHP Markdown Extra or Pandoc, is as follows:

### Rule 2.1: Term
The term to be defined is placed on a line by itself.
*   **Syntax:** `Term to be defined`

### Rule 2.2: Definition(s)
Each definition for the term MUST start on a new line, be preceded by a colon (`:`), and be indented (typically by one to four spaces, with **four spaces recommended for clarity and compatibility**).
*   **Syntax (Single Definition):**
    ```markdown
    Term
    :    Definition of the term.
    ```
*   **Syntax (Multiple Definitions or Paragraphs per Term):**
    Multiple definition lines for the same term MUST each start with an indented colon. Blank lines between definition paragraphs for the same term must also start with an indented colon (or be sufficiently indented to be part of the definition block).
    ```markdown
    Term
    :    First definition or first paragraph of a definition.
    :    Second definition or second paragraph of the same definition.
    ```
*   **Indentation:** Consistent indentation for the definition lines is crucial. Four spaces after the colon (before the definition text) is a common and robust convention.
    `Term`
    `:    Definition text`

### Rule 2.3: Blank Lines
*   A blank line SHOULD precede the first term of a definition list.
*   A blank line SHOULD separate a term from its definition(s) if the term itself contains internal formatting or if it improves readability, though many parsers do not strictly require this.
*   A blank line MUST be used to separate one term-definition group from the next term in the list if there's ambiguity or if the definition itself spans multiple paragraphs without explicit colons on each line. However, the most robust method is to ensure each definition line starts with an indented colon.
*   A blank line MUST follow the entire definition list block.

## 3. Illustrative Examples

### Example 3.1: Basic Definition List
```markdown
Apple
:    A round fruit, typically red, green, or yellow.
:    Keeps the doctor away if consumed daily.

Banana
:    An elongated, curved fruit with yellow skin when ripe.
```
**Conceptual Rendered Output:**
<dl>
  <dt>Apple</dt>
  <dd>A round fruit, typically red, green, or yellow.</dd>
  <dd>Keeps the doctor away if consumed daily.</dd>
  <dt>Banana</dt>
  <dd>An elongated, curved fruit with yellow skin when ripe.</dd>
</dl>

### Example 3.2: Definition List with More Spacing for Readability
```markdown
Markdown
:    A lightweight markup language with plain-text-formatting syntax. Its design allows it to be converted to many output formats, but the original tool by the same name only supported HTML.

Parser
:    A program that processes input text to determine its grammatical structure with respect to a given formal grammar.
:    Markdown parsers interpret Markdown text and convert it into another format, typically HTML.
```

## 4. Parser Compatibility and Extensions

*   **Not Core CommonMark:** Definition list syntax as described is an extension to Markdown and is not part of the core CommonMark specification.
*   **Supported Environments:** This syntax is supported by many popular Markdown processors, including:
    *   Pandoc
    *   PHP Markdown Extra and derivatives (e.g., Parsedown with extensions)
    *   Some static site generators (Jekyll, Hugo, etc., often via configuration or plugins)
    *   Some note-taking applications.
*   **Consideration:** Authors should be aware that rendering of definition lists may vary or not be supported in all Markdown environments or viewers. If broad compatibility with basic Markdown renderers is a primary concern, alternative formatting (e.g., using headings and paragraphs, or bolded terms followed by descriptions) might be considered.
*   **Recommendation:** When definition lists are used, the chosen authoring and publishing toolchain MUST support the specified syntax.

## 5. Importance of Consistent Definition List Syntax

*   **Semantic Representation:** Clearly and semantically represents term-definition pairs.
*   **Readability:** Improves the readability of glossaries, data dictionaries, and other definitional content.
*   **Authoring Consistency:** Ensures all authors use the same method for creating definition lists when the feature is employed.
*   **Potential for Styling:** Allows specific CSS styling to be applied to definition lists in rendered HTML output.

## 6. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where definition lists are used to present terms and their corresponding definitions or descriptions.

## 7. Cross-References
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines around block elements.

---
*This standard (SF-SYNTAX-DEFINITION-LISTS) is based on common Markdown extension syntax for definition lists.*
```
