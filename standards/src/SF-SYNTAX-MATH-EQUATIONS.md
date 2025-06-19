---
title: 'Standard: Mathematical Equation Syntax'
standard_id: SF-SYNTAX-MATH-EQUATIONS
aliases:
- Math Equations
- LaTeX Math
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p3-low
- kb-id/standards
- status/draft
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Mathematical Equation Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for mathematical equations in knowledge base
  documents.
criticality: P3-Low
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Mathematical notation
- Content presentation
- Technical documentation
---
# Standard: Markdown Syntax for Math Equations (SF-SYNTAX-MATH-EQUATIONS)

## 1. Standard Statement

This standard **MANDATES** the exclusive syntax for embedding mathematical equations (both inline and as display blocks) within Markdown documents. The internal content of these equations **MUST** be expressed using LaTeX syntax. Consistent application of this standard is **CRITICAL** for the clear and accurate representation of mathematical formulas.

Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around block-level math equations is also **MANDATORY**.

## 2. Core Math Syntax Rules

### Rule 2.1: Inline Mathematical Equations
Inline mathematical equations **MUST** be enclosed by single dollar signs (`$`). The use of backslash-parentheses (`\(` and `\)`) is **PROHIBITED**.
*   **Mandatory Syntax:** `$ LaTeX equation here $`
*   **Example:**
    ```markdown
    The equation for energy is $E = mc^2$. This is a fundamental concept.
    ```
*   **Rationale:** Provides a single, clear method to embed simple mathematical expressions directly within text, enhancing readability and consistency.

### Rule 2.2: Block (Display) Mathematical Equations
Block or display mathematical equations **MUST** be enclosed by double dollar signs (`$$`). The use of backslash-square brackets (`\[` and `\]`) is **PROHIBITED**.
*   **Mandatory Syntax:**
    ```markdown
    $$
    LaTeX equation here
    $$
    ```
*   **Spacing:** A blank line **MUST** precede and follow the opening and closing delimiters of a block math equation.
*   **Example:**
    ```markdown
    The quadratic formula is given by:

    $$
    x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
    $$

    This formula is used to solve quadratic equations.
    ```
*   **Rationale:** Allows complex mathematical expressions to be displayed clearly, separated from main text. Ensures consistency and correct parsing.

### Rule 2.3: Equation Content (LaTeX)
The content within the math delimiters (**MUST** be valid LaTeX mathematical syntax).
*   **Example (LaTeX content):** `\sum_{i=1}^{n} i = \frac{n(n+1)}{2}`
*   **Rationale:** LaTeX is the de facto standard for typesetting mathematical and scientific notation, offering comprehensive features for complex formulas.

## 3. Parser and Renderer Dependencies

Math equation syntax is a Markdown extension; native support is not universal. Proper rendering requires a JavaScript library (e.g., MathJax, KaTeX) in the toolchain.

The chosen authoring and publishing toolchain for the Knowledge Base **MUST** support the specified syntax and a LaTeX-based rendering engine.

## 4. Importance of Strict Math Syntax

*   **Accuracy:** Ensures mathematical formulas are represented correctly and unambiguously.
*   **Readability:** Well-rendered math significantly improves comprehension of technical content.
*   **Authoring Consistency:** Provides a uniform method for authors to include mathematical notation.
*   **Professional Presentation:** Correctly typeset math contributes to a professional and credible appearance.

## 5. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where mathematical equations are included. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 6. Cross-References
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-SYNTAX-MATH-EQUATIONS) has been revised to mandate a strict, singular syntax for embedding LaTeX mathematical equations, replacing previous recommendations with clear requirements.*
