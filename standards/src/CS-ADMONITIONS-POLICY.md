---

title: 'Policy: Usage of Admonitions and Callouts'
standard_id: CS-ADMONITIONS-POLICY
aliases:
- Callout Usage Policy
- Admonition Policy
tags:
- content-type/policy-document
- criticality/p2-medium
- kb-id/standards
- status/draft
- topic/cs
- topic/policy
kb-id: standards
info-type: policy-document
primary-topic: Admonition and Callout Usage Policy
related-standards:
- SF-CALLOUTS-SYNTAX
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: CS
sub_domain: POLICY
scope_application: Governs the appropriate and semantic use of admonition/callout
  blocks (as defined in SF-CALLOUTS-SYNTAX) across all knowledge base documents.
criticality: P2-Medium
lifecycle_gatekeeper: Editorial-Board-Approval
impact_areas:
- Content readability
- User experience
- Consistent highlighting of information
- Authoring practices
---
# Policy: Usage of Admonitions and Callouts (CS-ADMONITIONS-POLICY)

## 1. Policy Statement

This policy governs the appropriate and semantic use of admonition/callout blocks, whose syntax is defined in [[SF-CALLOUTS-SYNTAX]]. Admonitions are designed to draw the reader's attention to specific pieces of information that are ancillary or supplementary to the main text, or that require special emphasis (e.g., warnings, tips). Proper and consistent use of admonitions enhances readability and user experience.

## 2. Core Usage Policies for Admonitions/Callouts

### Rule 2.1: Semantic Use of `TYPE`
Admonition blocks MUST be used semantically, meaning the chosen `[!TYPE]` keyword (as defined in [[SF-CALLOUTS-SYNTAX]]) MUST accurately reflect the nature and purpose of the information being highlighted.
*   **Rationale:** Semantic usage ensures that the visual cues (colors, icons, etc.) provided by the rendered callout align with the content's intent, creating a consistent and predictable experience for the user.

### Rule 2.2: Guidance on Common `TYPE` Keywords
The following provides guidance on when to use the common `TYPE` keywords defined in [[SF-CALLOUTS-SYNTAX]]:

*   **`[!NOTE]`**: For general supplementary information that is relevant but tangential to the main text. Useful for elaborations, side comments, or additional context.
*   **`[!IMPORTANT]`**: For information that users must not overlook due to its significance for understanding or correct application of the main content.
*   **`[!WARNING]`**: For potential dangers, pitfalls, critical cautionary advice, or actions that could lead to negative consequences (e.g., data loss, security risks).
*   **`[!TIP]`**: For helpful hints, suggestions, best practices, or optional advice that can improve user experience or outcomes.
*   **`[!QUESTION]` / `[!FAQ]`**: For posing questions related to the content, or for structuring Frequently Asked Questions sections.
*   **`[!ERROR]`**: For highlighting error messages, incorrect outcomes, or troubleshooting advice related to errors.
*   **`[!SUCCESS]` / `[!INFO]` / `[!HELP]`**:
    *   `[!SUCCESS]`: For indicating successful outcomes, positive confirmations, or successful completion of steps.
    *   `[!INFO]`: For general informational messages that don't fit other categories but need to stand out.
    *   `[!HELP]`: For guidance on where to find help or more detailed support.
*   **`[!EXAMPLE]` / `[!DEMO]`**: For clearly demarcating examples or demonstrations within the text.
*   **`[!QUOTE]`**: For text quoted from external sources or other documents, especially if a distinct visual presentation from a standard Markdown blockquote is desired for emphasis.
*   **`[!ABSTRACT]` / `[!SUMMARY]` / `[!TLDR]`**: For summaries or abstracts at the beginning or end of a document or long section, providing a quick overview of key points.
*   **`[!TODO]`**: Primarily for editorial or authoring purposes to highlight pending tasks, items needing updates, or unresolved issues within a document. These may be stripped or hidden in final published outputs depending on tooling.
*   **`[!IF]`**: For indicating blocks of content that are conditional, assuming the processing toolchain supports conditional logic based on this type. The specific conditions are outside the scope of this syntax.

### Rule 2.3: Optional Title Usage
If an optional title is used after the `[!TYPE]` specifier, it SHOULD be concise and accurately summarize or label the content of the callout.
*   **Example:** `> [!WARNING] Data Integrity Risk`
*   **Rationale:** A good title provides immediate context for the callout's content.

### Rule 2.4: Content Indentation
All content within a callout block, including multiple paragraphs, lists, or other Markdown elements, MUST be correctly indented to align under the callout's initial `>` marker, as specified in [[SF-CALLOUTS-SYNTAX]] and [[SF-SYNTAX-BLOCKQUOTES]].
*   **Rationale:** Ensures correct rendering of the callout as a single, cohesive block.

### Rule 2.5: Avoid Overuse
Admonition blocks SHOULD be used judiciously and only when information genuinely needs to stand out or requires special emphasis.
*   **Guidance:** Overuse of callouts can lead to visual clutter, diminish their impact ("callout fatigue"), and make the document harder to read. The main narrative flow should carry the primary information.
*   **Alternative:** Consider if the information can be effectively integrated into the main text, or if a simple bolding or italicizing of a key phrase would suffice, before resorting to a callout.
*   **Rationale:** Ensures that callouts remain effective tools for drawing attention when truly necessary.

## 3. Rationale for Admonition Policy

*   **Improved Readability and Scannability:** Well-placed and semantically correct admonitions help users quickly identify and understand critical pieces of information or supplementary notes.
*   **Consistent User Experience:** Standardizing the use of admonition types provides users with a consistent visual language for different kinds of information across the knowledge base.
*   **Drawing Attention to Critical Information:** Effectively highlights warnings, important notes, or tips that might otherwise be missed in the main text.
*   **Enhanced Information Architecture:** Allows for a richer structuring of information by clearly delineating ancillary or emphatic content from the primary narrative.

## 4. Scope of Application

This policy applies to all authors and editors creating or modifying content within the knowledge base. It guides the decision-making process for when and how to use admonition/callout blocks.

## 5. Cross-References
- [[SF-CALLOUTS-SYNTAX]] - Defines the Markdown syntax for creating callout/admonition blocks.
- [[SF-SYNTAX-BLOCKQUOTES]] - Defines the base blockquote syntax.

---
*This policy (CS-ADMONITIONS-POLICY) provides guidance on the semantic and appropriate use of the callout/admonition syntax defined in [[SF-CALLOUTS-SYNTAX]], generalizing concepts from previous tool-specific standards like O-USAGE-CALLOUTS-001.*
