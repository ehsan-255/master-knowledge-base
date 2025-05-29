---
title: "Standard: Markdown Syntax for Math Equations"
standard_id: "SF-SYNTAX-MATH-EQUATIONS"
aliases: ["Math Equation Syntax", "LaTeX in Markdown", "Markdown Math"]
tags:
  - status/draft
  - criticality/P3-Low # Specialized usage, but important if used
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Markdown Math Equation Syntax" # As per prompt
related-standards: ["SF-FORMATTING-FILE-HYGIENE"] # For blank line rules around blocks
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "SF" # Syntax & Formatting
sub_domain: "SYNTAX" # As per prompt
scope_application: "Defines the syntax for embedding mathematical equations (inline and block) using LaTeX within Markdown documents."
criticality: "P3-Low"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Technical documentation", "Scientific writing", "Educational content", "Accurate rendering of mathematical formulas"]
change_log_url: "./SF-SYNTAX-MATH-EQUATIONS-changelog.md" # Placeholder
---

# Standard: Markdown Syntax for Math Equations (SF-SYNTAX-MATH-EQUATIONS)

## 1. Standard Statement

This standard defines the recommended syntax for embedding mathematical equations (both inline and as display blocks) within Markdown documents. The internal content of these equations SHOULD generally be expressed using LaTeX syntax. Consistent application of this standard facilitates the clear and accurate representation of mathematical formulas.

Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around block-level math equations is also important.

## 2. Core Math Syntax Rules (Common Extensions)

Mathematical equation rendering in Markdown is typically handled by extensions that process LaTeX syntax. Common Markdown processors often support MathJax, KaTeX, or similar JavaScript libraries for this purpose.

### Rule 2.1: Inline Mathematical Equations
Inline mathematical equations (equations that appear within a line of text) SHOULD be enclosed by single dollar signs (`$`) or by backslash-parentheses (`\(` and `\)`).
*   **Syntax Option 1 (Single Dollar Signs - Recommended for Simplicity):** `$ LaTeX equation here $`
*   **Syntax Option 2 (Backslash-Parentheses):** `\( LaTeX equation here \)`
*   **Consistency:** For consistency across the knowledge base, **Syntax Option 1 (single dollar signs: `$equation$`) IS THE PREFERRED STYLE** for inline math.
*   **Example (Preferred):**
    ```markdown
    The equation for energy is $E = mc^2$. This is a fundamental concept.
    ```
    *Conceptual Rendered Output:* The equation for energy is $E = mc^2$. This is a fundamental concept.
*   **Example (Alternative):**
    ```markdown
    The equation for energy is \(E = mc^2\). This is a fundamental concept.
    ```
*   **Rationale:** Provides a standard way to embed simple mathematical expressions directly within text. Using a single consistent style enhances readability of raw Markdown.

### Rule 2.2: Block (Display) Mathematical Equations
Block or display mathematical equations (equations that are set apart from the main text, typically centered and on their own lines) SHOULD be enclosed by double dollar signs (`$$`) or by backslash-square brackets (`\[` and `\]`).
*   **Syntax Option 1 (Double Dollar Signs - Recommended for Simplicity):**
    ```markdown
    $$
    LaTeX equation here
    $$
    ```
*   **Syntax Option 2 (Backslash-Square Brackets):**
    ```markdown
    \[
    LaTeX equation here
    \]
    ```
*   **Consistency:** For consistency across the knowledge base, **Syntax Option 1 (double dollar signs: `$$equation$$`) IS THE PREFERRED STYLE** for block math.
*   **Spacing:** A blank line MUST precede and follow the opening and closing delimiters of a block math equation to ensure correct parsing and rendering as a distinct block.
*   **Example (Preferred):**
    ```markdown
    The quadratic formula is given by:

    $$
    x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
    $$

    This formula is used to solve quadratic equations.
    ```
    *Conceptual Rendered Output:*
    The quadratic formula is given by:
    $$
    x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
    $$
    This formula is used to solve quadratic equations.
*   **Rationale:** Allows more complex mathematical expressions to be displayed clearly, separated from the main text flow. Using a single consistent style improves raw Markdown readability.

### Rule 2.3: Equation Content (LaTeX)
The content within the math delimiters (e.g., between `$`...`$`, or `$$`...`$$`) SHOULD be valid LaTeX mathematical syntax.
*   **Guidance:** Authors should be familiar with basic LaTeX math commands for symbols, fractions, roots, sums, integrals, matrices, etc.
*   **Example (LaTeX content):** `\sum_{i=1}^{n} i = \frac{n(n+1)}{2}`
*   **Rationale:** LaTeX is the de facto standard for typesetting mathematical and scientific notation, offering a comprehensive set of features for representing complex formulas.

## 3. Parser and Renderer Dependencies

*   **Not Core CommonMark:** Math equation syntax as described is an extension to Markdown. Native support is not available in all Markdown parsers.
*   **Rendering Engines:** Proper rendering of LaTeX math in Markdown typically requires a JavaScript library like MathJax or KaTeX to be active in the Markdown previewer, publishing system, or browser.
*   **Configuration:** The specific Markdown processor or platform being used might require configuration to enable math rendering and to choose the specific rendering engine (MathJax, KaTeX, etc.).
*   **Recommendation:** The chosen authoring and publishing toolchain for the knowledge base MUST support one of the specified syntaxes and a LaTeX-based rendering engine.

## 4. Importance of Consistent Math Syntax

*   **Accuracy:** Ensures mathematical formulas are represented correctly and unambiguously.
*   **Readability:** Well-rendered math significantly improves the readability and comprehension of technical and scientific content.
*   **Authoring Consistency:** Provides a uniform method for authors to include mathematical notation.
*   **Professional Presentation:** Correctly typeset math contributes to a professional and credible appearance of documents.

## 5. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where mathematical equations are included.

## 6. Cross-References
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines around block elements, which applies to display math blocks.

---
*This standard (SF-SYNTAX-MATH-EQUATIONS) is based on common Markdown extension syntaxes for embedding LaTeX mathematical equations.*
```
