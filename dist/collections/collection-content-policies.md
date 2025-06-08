---
title: "Content Style & Policies"
description: "A collection of key policies and standards related to content authoring, tone, language, accessibility, and specific content behaviors from the CS (Content Standards) domain."
date_generated: "2025-06-04T22:19:33.657410+00:00"
source_collection_definition_id: "coll_cs_content_policies"
number_of_standards: 16
tags: ["content-type/collection-document", "status/published", "topic/derived-view"] 
info-type: "collection-document" 
# Consider adding a standard_id for the collection itself, e.g.:
# standard_id: "COLL-COLL-CS-CONTENT-POLICIES" 
---

## Table of Contents
- [Policy: Usage of Admonitions and Callouts (`CS-ADMONITIONS-POLICY`)](#policy-usage-of-admonitions-and-callouts-cs-admonitions-policy)
- [Policy: Content Profiling and Conditional Text (`CS-CONTENT-PROFILING-POLICY`)](#policy-content-profiling-and-conditional-text-cs-content-profiling-policy)
- [Policy: Internal Knowledge Base Linking Strategy (`CS-LINKING-INTERNAL-POLICY`)](#policy-internal-knowledge-base-linking-strategy-cs-linking-internal-policy)
- [Policy: Content Modularity and Use of Transclusion (`CS-MODULARITY-TRANSCLUSION-POLICY`)](#policy-content-modularity-and-use-of-transclusion-cs-modularity-transclusion-policy)
- [Policy: Content Accessibility (`CS-POLICY-ACCESSIBILITY`)](#policy-content-accessibility-cs-policy-accessibility)
- [Policy: Translating Non-Digital Concepts for Digital Workflows (`CS-POLICY-DIGITAL-ABSTRACTION`)](#policy-translating-non-digital-concepts-for-digital-workflows-cs-policy-digital-abstraction)
- [Policy: Content Organization and Heading Usage in Chapters (`CS-POLICY-DOC-CHAPTER-CONTENT`)](#policy-content-organization-and-heading-usage-in-chapters-cs-policy-doc-chapter-content)
- [Policy: Unique Knowledge Base Identification and Naming (`CS-POLICY-KB-IDENTIFICATION`)](#policy-unique-knowledge-base-identification-and-naming-cs-policy-kb-identification)
- [Policy: Content Organization within Knowledge Base Parts (`CS-POLICY-KB-PART-CONTENT`)](#policy-content-organization-within-knowledge-base-parts-cs-policy-kb-part-content)
- [Policy: Consistent Application of Knowledge Base Root Structure (`CS-POLICY-KB-ROOT`)](#policy-consistent-application-of-knowledge-base-root-structure-cs-policy-kb-root)
- [Policy: Layered Information Presentation and Progressive Disclosure (`CS-POLICY-LAYERED-INFORMATION`)](#policy-layered-information-presentation-and-progressive-disclosure-cs-policy-layered-information)
- [Policy: Knowledge Base Part Overviews (`CS-POLICY-PART-OVERVIEW`)](#policy-knowledge-base-part-overviews-cs-policy-part-overview)
- [Policy: Universal Principles for Content Exclusion (`CS-POLICY-SCOPE-EXCLUSION`)](#policy-universal-principles-for-content-exclusion-cs-policy-scope-exclusion)
- [Policy: Universal Principles for Content Inclusion (`CS-POLICY-SCOPE-INCLUSION`)](#policy-universal-principles-for-content-inclusion-cs-policy-scope-inclusion)
- [Policy: Clarity, Objectivity, and Consistency in Language (`CS-POLICY-TONE-LANGUAGE`)](#policy-clarity-objectivity-and-consistency-in-language-cs-policy-tone-language)
- [Policy: Table of Contents (ToC) Usage and Generation (`CS-TOC-POLICY`)](#policy-table-of-contents-toc-usage-and-generation-cs-toc-policy)


## Policy: Usage of Admonitions and Callouts (CS-ADMONITIONS-POLICY)

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

---

## Policy: Content Profiling and Conditional Text (CS-CONTENT-PROFILING-POLICY)

# Policy: Content Profiling and Conditional Text (CS-CONTENT-PROFILING-POLICY)

## 1. Policy Statement

This policy governs the strategy for content profiling and the implementation of conditional text within knowledge base documents. Content profiling allows for tailoring content to specific audiences, platforms, feature versions, or other defined contexts. This is achieved using conditional text blocks, which display content only when specified conditions are met.

## 2. Purpose of Content Profiling

Content profiling and conditional text serve several key purposes:
*   **Targeted Information:** Delivering information that is most relevant to a specific user group or situation (e.g., novice vs. expert users, different operating systems).
*   **Reduced Clutter:** Hiding information that is not relevant to a particular context, making documents less overwhelming and easier to navigate.
*   **Single-Sourcing (with Variation):** Managing variations of information within a single document, reducing duplication and simplifying updates for common content.
*   **Phased Rollout:** Allowing documentation for new or beta features to be present but hidden until the feature is generally available.

## 3. Implementation of Conditional Text

### Rule 3.1: Use of `[!IF condition]` Callouts (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rule 1.1)
Conditional text blocks MUST be implemented using the `[!IF condition]` callout syntax as defined in [[SF-CALLOUTS-SYNTAX]].
*   **Syntax Reminder:** `> [!IF condition]`
*   **Rationale:** Provides a standardized and visually distinct way to mark conditional content.

### Rule 3.2: Condition String Syntax
The `condition` string within the `[!IF condition]` callout MUST adhere to the syntax defined in [[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]].
*   **Syntax Reminder:** Conditions are `attribute=value` pairs, combinable with `AND` (case-insensitive). `OR` logic requires separate blocks. Attribute names and values must not contain spaces; values should use kebab-case for multiple words.
*   **Rationale:** Ensures conditions are parsable and consistently interpreted.

### Rule 3.3: Content Indentation and Structure (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rules 1.4 & 1.5)
All content that is conditional upon the `IF` statement MUST be correctly indented under the callout, following standard callout content rules as specified in [[SF-CALLOUTS-SYNTAX]].
*   **Guidance:** Conditional blocks can span multiple paragraphs, lists, or other Markdown elements, as long as each line of the conditional content starts with the callout marker (`> `) and appropriate indentation for nested elements within the callout.
*   **Rationale:** Ensures correct rendering and association of content with its condition.

### Rule 3.4: Blank Lines Around Conditional Blocks (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rule 1.6)
A blank line SHOULD precede and follow a conditional block for readability, unless it is immediately followed by another related conditional block (e.g., a series of mutually exclusive conditions). This aligns with [[SF-FORMATTING-FILE-HYGIENE]].
*   **Rationale:** Improves visual separation and parsing reliability.

## 4. Profiling Attributes and Values (Authoritative Source)

This policy document is the authoritative source for defining and managing the permissible profiling attributes and their corresponding values. This replaces any previous documents like `U-PROFILING-ATTRIBUTES-001.md`.

### Rule 4.1: Initial List of Approved Attributes and Values
The following attributes and example values are initially approved for use. Values SHOULD be in kebab-case if multi-word.

*   **`audience`**: Defines the target audience for the content.
    *   `novice`: Users new to the subject or product.
    *   `intermediate`: Users with some experience but not experts.
    *   `expert`: Users with deep knowledge and experience.
    *   `developer`: Users who are software developers.
    *   `admin`: System administrators or users with administrative privileges.
    *   `internal-only`: For content intended only for internal team members.
*   **`platform`**: Specifies the operating system or platform.
    *   `windows`
    *   `linux`
    *   `macos`
    *   `ios`
    *   `android`
    *   `web` (for web browser based platforms/features)
*   **`feature-version`**: Specifies a version of a feature (distinct from document version).
    *   `v1.0`
    *   `v2.x`
    *   `beta`
    *   `alpha`
*   **`deployment-model`**: Specifies the deployment environment.
    *   `cloud`
    *   `on-premises`
    *   `hybrid`
*   **`access-level`**: Specifies user access or permission levels.
    *   `user`
    *   `premium-user`
    *   `administrator`

### Rule 4.2: Process for Managing Attributes and Values
*   **Proposal:** New attributes or values, or changes to existing ones, MUST be proposed to the designated governance body (e.g., Editorial Board, Standards Committee).
*   **Review:** Proposals will be reviewed for clarity, necessity, potential overlap, and impact on the overall profiling strategy.
*   **Approval & Documentation:** Approved attributes and values will be formally added to this policy document (Rule 4.1). Changes to this section MUST follow the standard versioning and changelog process for this policy document itself, as defined in [[OM-VERSIONING-CHANGELOGS]].
*   **Rationale:** Ensures that the set of profiling attributes and values remains controlled, consistent, and aligned with the evolving needs of the knowledge base.

## 5. Illustrative Examples of Conditional Text Usage

### Example 5.1: Audience-Specific Content
```markdown
General introduction to the feature.

> [!IF audience=expert]
> For expert users, you can further optimize performance by adjusting the following parameters in the configuration file:
> - `max_cache_size`
> - `thread_pool_count`

> [!IF audience=novice]
> If you are new to this feature, we recommend starting with the default settings. You can learn more about configuration in the [[GUIDE-FEATURE-ADVANCED-SETTINGS]].

This concludes the feature description.
```

### Example 5.2: Platform-Specific Instructions
```markdown
To install the software:

> [!IF platform=windows]
> 1. Download the `setup.exe` installer.
> 2. Double-click the installer and follow the on-screen prompts.

> [!IF platform=linux]
> 1. Download the `.tar.gz` archive.
> 2. Extract the archive: `tar -xvzf package.tar.gz`
> 3. Run the installation script: `sudo ./install.sh`

> [!IF platform=macos]
> 1. Download the `.dmg` file.
> 2. Open the `.dmg` and drag the application icon to your Applications folder.
```

## 6. Importance of a Content Profiling Policy

*   **Targeted Communication:** Enables delivery of the right information to the right audience at the right time.
*   **Improved User Experience:** Reduces information overload and makes content more relevant to the user's context.
*   **Maintainability:** While adding complexity, it can help manage variations of content within a single source if used carefully.
*   **Consistency:** Ensures a consistent approach to conditional content across the knowledge base.

## 7. Scope of Application

This policy applies to all content within the knowledge base where conditional text is used for profiling or selective display. All authors and editors MUST adhere to this policy when implementing conditional content.

## 8. Cross-References
- [[SF-CALLOUTS-SYNTAX]] - Defines the general syntax for callout blocks, including the `[!IF ...]` type.
- [[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]] - Defines the specific syntax for the condition string within `[!IF ...]` callouts.
- [[OM-VERSIONING-CHANGELOGS]] - For versioning this policy document when attributes/values are updated.

---
*This policy (CS-CONTENT-PROFILING-POLICY) is based on rules 1.1, 1.4, 1.5, and 1.6 previously defined in M-CONDITIONAL-TEXT-SYNTAX-001. It also establishes itself as the new authoritative source for profiling attributes and values, superseding U-PROFILING-ATTRIBUTES-001.*

---

## Policy: Internal Knowledge Base Linking Strategy (CS-LINKING-INTERNAL-POLICY)

# Policy: Internal Knowledge Base Linking Strategy (CS-LINKING-INTERNAL-POLICY)

## 1. Policy Statement

This policy outlines the strategy and best practices for creating internal links within documents in the Knowledge Base (KB). Effective internal linking is crucial for knowledge discovery, enhancing navigability, creating content cohesion, and improving the overall user experience. All internal links MUST adhere to the syntax defined in [[SF-LINKS-INTERNAL-SYNTAX]].

## 2. Core Linking Policies

### Rule 2.1: Extensive Use of Internal Links (Derived from U-INTERLINK-001, Rule 1.1)
Internal links between documents, notes, and specific sections within the same Knowledge Base MUST be used extensively and purposefully to connect related concepts, methodologies, definitions, and supporting information.
*   **Rationale:** Promotes discoverability of related information, helps users build a more holistic understanding of topics, and transforms the KB into a truly interconnected web of knowledge rather than a collection of isolated documents.

### Rule 2.2: Descriptive Link Text (Derived from U-INTERLINK-001, Rule 1.3)
Link text MUST be descriptive and clearly indicate the nature of the target content.
*   **Guidance for `[[STANDARD_ID]]` or `[[filename]]` style links:** If the raw `STANDARD_ID` or filename (used as link text by default in some syntaxes) is not sufficiently descriptive for the context, an alias or display text MUST be used.
    *   **Example:** Instead of just `See [[SF-LINKS-INTERNAL-SYNTAX]].`, prefer `For detailed syntax rules, see the [[SF-LINKS-INTERNAL-SYNTAX|Internal Linking Syntax Standard]].`
*   **Rationale:** Descriptive link text improves scannability, accessibility (for screen reader users), and helps users decide whether to follow a link by providing clear context about the destination.

### Rule 2.3: "See Also" Sections for Grouped Links (Derived from U-INTERLINK-001, Rule 1.4)
"See Also" sections, as defined in [[AS-STRUCTURE-DOC-CHAPTER]], ARE a primary and mandatory mechanism for grouping links to related documents, standards, or external resources at the end of a document.
*   **Rationale:** Provides a dedicated and consistent location for users to find further relevant information, acting as a curated list of related readings or next steps.

### Rule 2.4: Contextual Relevance and Avoidance of Over-Linking (Derived from U-INTERLINK-001, Rule 1.5)
Links embedded within the main body of the text MUST be contextually relevant to the specific point being discussed. Over-linking (creating too many links in a way that distracts from the primary content) MUST be avoided.
*   **Guidance:**
    *   A link should add value and enhance understanding at the point where it is inserted.
    *   Avoid linking common terms or every possible keyword. Focus on links that provide significant additional context, definitions for specialized terms, or direct pathways to closely related procedures or concepts.
    *   Consider whether a concept is better explained briefly in situ or if a link to a more detailed explanation is truly necessary.
*   **Rationale:** Ensures that links are helpful rather than distracting, maintaining readability and focus on the current document's narrative.

## 3. Adherence to Link Syntax Standard

All internal links, regardless of the specific linking strategy employed, MUST strictly adhere to the syntactical rules defined in [[SF-LINKS-INTERNAL-SYNTAX]]. This ensures consistency, maintainability, and allows for potential automated processing or validation of links.

## 4. Rationale for Linking Policy

A coherent internal linking strategy provides significant benefits:

*   **Enhanced Knowledge Discovery:** Allows users to naturally explore related topics and discover information they might not have found otherwise.
*   **Improved Navigability:** Makes it easier for users to move between related pieces of information, creating intuitive pathways through the KB.
*   **Reduced Redundancy:** Encourages linking to a single authoritative source for a concept or definition rather than repeating information across multiple documents.
*   **Increased Content Cohesion:** Weaves individual documents into a more cohesive and integrated knowledge resource.
*   **Better User Experience:** A well-linked KB feels more like an integrated system and is generally easier and more satisfying to use.

## 5. Scope of Application

This policy applies to all content creators, editors, and curators working within any Knowledge Base in the repository. It governs the creation and maintenance of all internal links.

## 6. Cross-References
- [[SF-LINKS-INTERNAL-SYNTAX]] - Defines the mandatory syntax for internal links.
- [[AS-STRUCTURE-DOC-CHAPTER]] - Defines the requirement for "See Also" sections in documents.

---
*This policy (CS-LINKING-INTERNAL-POLICY) is based on rules 1.1, 1.3, 1.4, and 1.5 previously defined in U-INTERLINK-001 from COL-LINKING-UNIVERSAL.md. Rule 1.2 regarding syntax is now covered by [[SF-LINKS-INTERNAL-SYNTAX]].*

---

## Policy: Content Modularity and Use of Transclusion (CS-MODULARITY-TRANSCLUSION-POLICY)

# Policy: Content Modularity and Use of Transclusion (CS-MODULARITY-TRANSCLUSION-POLICY)

## 1. Policy Statement

This policy promotes the design of content for modularity and governs the appropriate use of transclusion (content embedding) as defined in [[SF-TRANSCLUSION-SYNTAX]]. The goal is to foster content reusability, improve maintainability, ensure consistency, and adhere to the "Don't Repeat Yourself" (DRY) principle.

## 2. Core Policies for Modularity and Transclusion

### Rule 2.1: Atomic and Self-Contained Content (Derived from U-MODULAR-001, Rule 1.1 & 1.3)
Content pertaining to distinct concepts, methodologies, processes, or key steps SHOULD be designed to be as atomic and self-contained as possible.
*   **Guidance:**
    *   Each document or major section should focus on a specific, well-defined topic.
    *   Minimize "context bleeding" from unrelated surrounding topics within the same content chunk. If context from other documents is needed, prefer linking using [[CS-LINKING-INTERNAL-POLICY]] rather than extensive repetition.
    *   This aligns with the principles behind specific content schemas like [[AS-SCHEMA-METHODOLOGY-DESCRIPTION]] and [[AS-SCHEMA-CONCEPT-DEFINITION]], which encourage focused content.
*   **Rationale:** Atomic content is easier to understand in isolation, reuse in different contexts (including via transclusion), and maintain independently.

### Rule 2.2: Use Transclusion to Avoid Duplication (Derived from U-MODULAR-001, Rule 1.2)
Transclusion, using the syntax defined in [[SF-TRANSCLUSION-SYNTAX]], MUST be used instead of duplicating substantial, identical blocks of common content across multiple documents.
*   **Examples of "substantial common content":**
    *   Sets of core principles applicable to multiple methodologies.
    *   Standard disclaimers, warnings, or introductory paragraphs.
    *   Reusable tables or complex list structures.
    *   Key definitions that need to appear in context in multiple places.
*   **Rationale:** Transclusion ensures that common information is sourced from a single place, making updates easier (edit once, updates reflect everywhere) and guaranteeing consistency.

## 3. Guidance on When to Transclude vs. Link

Choosing between transclusion and simple linking requires judgment. Here are some guidelines:

### Rule 3.1: Linking for Contextual Navigation
Use standard internal links (see [[CS-LINKING-INTERNAL-POLICY]]) when:
*   Referring to a related but distinct topic that the user might want to explore for more comprehensive understanding.
*   Pointing to prerequisite knowledge or subsequent steps in a larger workflow.
*   The referenced content is substantial enough to be its own document or major section, and embedding it would disrupt the flow of the current document.
*   **Example:** A document on "Advanced Data Analysis" might link to a document defining "Statistical Significance" rather than transcluding the entire definition.

### Rule 3.2: Transclusion for Seamless Integration of Reusable Content
Use transclusion (see [[SF-TRANSCLUSION-SYNTAX]]) when:
*   A specific, relatively small piece of content (e.g., a definition, a set of principles, a specific instruction set, a warning notice) needs to appear *as if it's part of the current document* for clarity or completeness.
*   The transcluded content is truly identical and intended to be reused verbatim in multiple locations.
*   The flow of the current document benefits from having that piece of information directly embedded, rather than requiring the user to navigate away.
*   **Example:** Transcluding a standard safety warning into multiple procedural documents. Transcluding a shared "Core Principles" section into several related methodology descriptions.

### Rule 3.3: Avoid Overuse of Transclusion
While transclusion is powerful for reuse, overuse can lead to documents that are difficult to read as standalone entities or that obscure the primary narrative of the host document.
*   **Guidance:** Ensure that the host document still has a clear primary purpose and narrative, and that transcluded content serves to support that narrative rather than replace it entirely or make it disjointed.
*   **Consideration:** If a document becomes merely a collection of transcluded blocks, re-evaluate if a different structuring approach (e.g., a well-linked collection document) might be more appropriate.

## 4. Benefits of Modularity and Transclusion

*   **Maintainability (DRY Principle):** Edit information in one place, and changes propagate to all documents where it is transcluded. This significantly reduces the effort and risk of errors associated with updating duplicated content.
*   **Consistency:** Ensures that common information (definitions, principles, warnings) is presented identically wherever it appears.
*   **Reusability:** Allows valuable content components to be reused across different contexts without copy-pasting.
*   **Authoring Efficiency:** Authors can assemble new documents more quickly by reusing existing modular content blocks.
*   **Reduced Redundancy:** Minimizes content duplication, making the knowledge base more concise and efficient.

## 5. Scope of Application

This policy applies to all content creators and editors within the knowledge base. It guides decisions on how to structure content for reusability and when to employ transclusion.

## 6. Cross-References
- [[SF-TRANSCLUSION-SYNTAX]] - Defines the syntax for embedding content.
- [[CS-LINKING-INTERNAL-POLICY]] - Policy for general internal linking.
- [[AS-SCHEMA-METHODOLOGY-DESCRIPTION]] - Example of a content type that can benefit from modular design.
- [[AS-SCHEMA-CONCEPT-DEFINITION]] - Another example of a content type that can be designed for modularity.

---
*This policy (CS-MODULARITY-TRANSCLUSION-POLICY) is based on rules 1.1, 1.2, and 1.3 previously defined in U-MODULAR-001 from COL-LINKING-UNIVERSAL.md, and provides guidance on applying the syntax defined in [[SF-TRANSCLUSION-SYNTAX]].*

---

## Policy: Content Accessibility (CS-POLICY-ACCESSIBILITY)

# Policy: Content Accessibility (CS-POLICY-ACCESSIBILITY)

## 1. Policy Statement

This policy affirms the commitment to making all content within the Knowledge Base (KB) accessible to the widest possible audience, including individuals with disabilities. Adherence to accessibility standards is crucial for inclusivity, user experience, and legal compliance. This policy provides overarching principles, while specific technical standards (like those for image alt text or heading usage) provide detailed implementation rules.

## 2. Core Accessibility Principles and Requirements

### Rule 2.1: Commitment to Accessibility
All content creators, editors, and curators MUST strive to ensure that content meets recognized accessibility standards, such as the Web Content Accessibility Guidelines (WCAG), to an appropriate level (e.g., WCAG 2.1 Level AA as a target).
*   **Rationale:** Ensures a consistent and high-quality experience for all users, regardless of ability.

### Rule 2.2: Image Accessibility (Reference to Specific Standard)
All images that convey information MUST be made accessible through the provision of descriptive alternative text (alt text), as mandated by [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]].
*   **Summary of [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]:**
    *   Informational images require descriptive alt text.
    *   Alt text must be concise yet convey the image's purpose and meaning.
    *   Purely decorative images should use empty alt text (`alt=""`) to be ignored by assistive technologies.
*   **Rationale:** Ensures that visually impaired users can understand the content and purpose of images.

### Rule 2.3: Semantic Use of Headings (Derived from U-ACCESSIBILITY-001, Rule 1.3)
Headings (H1-H6) MUST be used semantically to structure content logically and serve as navigational landmarks. They MUST be succinct and accurately reflect the content of the section they introduce.
*   **Guidance:**
    *   The H1 is reserved for the main document title.
    *   Subsequent headings (H2-H6) must follow a correct hierarchical order (e.g., an H2 followed by H3, not H4). Do not skip heading levels for styling purposes.
    *   Use headings to break up long blocks of text and clearly delineate topics and subtopics.
*   **Reference:** The specific Markdown syntax for headings is defined in [[SF-SYNTAX-HEADINGS]].
*   **Rationale:** Proper heading structure is critical for screen reader users, allowing them to navigate documents efficiently and understand their organization. It also benefits all users by making content more scannable and readable.

## 3. Future Expansion

This policy will be expanded over time to incorporate additional accessibility guidelines, which may include but are not limited to:

*   **Link Text Clarity:** Ensuring link text is descriptive and makes sense out of context.
*   **Color Contrast:** Guidelines for ensuring sufficient color contrast between text and background (if applicable to the platform or custom styling).
*   **Keyboard Navigation:** Ensuring all interactive elements can be navigated using a keyboard.
*   **Accessible Tables:** Standards for structuring data tables for accessibility.
*   **Multimedia Accessibility:** Requirements for captions, transcripts, and audio descriptions for video and audio content.

## 4. Importance of Accessibility

*   **Inclusivity:** Provides equal access and opportunity to people with diverse abilities.
*   **User Experience:** Accessible design often results in a better user experience for everyone.
*   **Legal and Ethical Compliance:** Adherence to accessibility standards is often a legal requirement and an ethical imperative.
*   **Wider Audience Reach:** Makes content available to more people, including those with disabilities and those using a variety of devices or in different environments.

## 5. Scope of Application

This policy applies to all content within the Knowledge Base and to all individuals involved in its creation, editing, and maintenance.

## 6. Cross-References
- [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]] - Specific standard for image alt text.
- [[SF-SYNTAX-HEADINGS]] - Standard defining the syntax and semantic use of headings.

---
*This policy (CS-POLICY-ACCESSIBILITY) incorporates Rule 1.3 from U-ACCESSIBILITY-001 (regarding headings) and sets a general framework for content accessibility, referencing the specific standard created for image alt text.*

---

## Policy: Translating Non-Digital Concepts for Digital Workflows (CS-POLICY-DIGITAL-ABSTRACTION)

# Policy: Translating Non-Digital Concepts for Digital Workflows (CS-POLICY-DIGITAL-ABSTRACTION)

## 1. Policy Statement

This policy provides guidelines for translating methodologies, techniques, or concepts that traditionally involve non-digital (physical, interpersonal, or ethically complex out-of-scope) components into a format suitable for a digitally-focused Knowledge Base (KB). The aim is to accurately represent the information-based aspects of such concepts while clearly delineating what is out of scope for the digital representation.

## 2. Core Principles for Digital Abstraction

### Rule 2.1: Explicit Exclusion or Abstraction of Non-Digital Aspects (Derived from U-ABSTR-DIGITAL-001, Rule 1.1)
When a methodology or concept traditionally involves physical real-world actions, direct interpersonal interactions, or ethically sensitive areas that are OUT OF SCOPE for the KB's digital and informational focus (as per [Policy: Universal Principles for Content Inclusion](#policy-universal-principles-for-content-inclusion-cs-policy-scope-inclusion) and [Policy: Universal Principles for Content Exclusion](#policy-universal-principles-for-content-exclusion-cs-policy-scope-exclusion)), those aspects MUST be explicitly excluded or clearly abstracted.
*   **Example:** For a medical diagnostic procedure, a KB focused on data analysis would abstract the physical examination steps, focusing instead on the data inputs (symptoms, test results) and analytical processes. The physical examination itself would be noted as out of scope or handled abstractly (e.g., "patient data collected via standard examination protocols (out of scope for this document)").
*   **Rationale:** Maintains the KB's focus on digitally manageable information and processes, preventing scope creep into areas it's not designed to cover.

### Rule 2.2: Focus on Information-Based Processes (Derived from U-ABSTR-DIGITAL-001, Rule 1.2)
Abstracted methodologies or concepts MUST focus on the information-based processes, decision points, inputs, and outputs that *can* be executed, managed, or represented digitally.
*   **Example:** When abstracting a traditional face-to-face interview technique for a KB on qualitative data analysis:
    *   **Focus on:** Designing interview questions, structuring an interview protocol (as a digital document), methods for analyzing transcript data, coding qualitative data.
    *   **Abstract/Exclude:** The nuances of in-person rapport-building, non-verbal cues (unless a method for their digital capture and analysis is within scope).
*   **Guidance:** The goal is to capture the intellectual and procedural core of the concept that is relevant to the KB's purpose. This is particularly relevant for schemas like [[AS-SCHEMA-METHODOLOGY-DESCRIPTION]], where inputs and outputs of steps are defined.
*   **Rationale:** Ensures that the KB provides practical, actionable knowledge within its intended digital domain, even when dealing with concepts that have non-digital origins.

### Rule 2.3: Acknowledge Omission of Critical Out-of-Scope Steps (Derived from U-ABSTR-DIGITAL-001, Rule 1.3)
If a traditional step or component of a methodology is entirely out of scope for the digital abstraction, and its omission might lead to a misunderstanding of the abstracted version's context or limitations, its absence and the rationale for exclusion MUST be briefly noted.
*   **Example:** For a manufacturing quality control process, if physical inspection steps are excluded: "Note: This document focuses on the statistical analysis of quality data. Physical inspection and material handling procedures are out of scope and covered in separate operational manuals."
*   **Rationale:** Provides necessary context, manages user expectations, and prevents misapplication of the abstracted information by clarifying its boundaries.

## 3. Rationale and Importance

Adhering to this policy is important for several reasons:

*   **Maintaining KB Focus and Scope:** Prevents the KB from becoming overly broad or attempting to cover aspects beyond its intended digital and informational purpose.
*   **Ensuring Relevance:** Keeps content relevant to users seeking information that can be applied in a digital context or understood through information-based processes.
*   **Clarity and Accuracy:** Explicitly addressing abstractions and exclusions prevents misinterpretation and ensures the abstracted representation is understood in its proper context.
*   **Managing User Expectations:** Helps users understand what they can and cannot expect to find regarding methodologies that have significant non-digital components.
*   **Ethical Considerations:** Provides a framework for responsibly handling concepts where certain aspects (e.g., sensitive interpersonal interactions, direct ethical interventions) are not suitable for full representation in the KB.

## 4. Scope of Application

This policy applies to all content creators and subject matter experts when documenting methodologies, techniques, processes, or concepts that originate from or include significant non-digital elements, and which are being adapted for inclusion in a Knowledge Base.

## 5. Cross-References
- [Policy: Universal Principles for Content Inclusion](#policy-universal-principles-for-content-inclusion-cs-policy-scope-inclusion) - Policy on what content should be included in KBs.
- [Policy: Universal Principles for Content Exclusion](#policy-universal-principles-for-content-exclusion-cs-policy-scope-exclusion) - Policy on what content should be excluded from KBs.
- [[AS-SCHEMA-METHODOLOGY-DESCRIPTION]] - Standard schema for methodology descriptions, which will often require digital abstraction.

---
*This policy (CS-POLICY-DIGITAL-ABSTRACTION) is based on rules 1.1 through 1.3 previously defined in U-ABSTR-DIGITAL-001 from COL-CONTENT-UNIVERSAL.md.*

---

## Policy: Content Organization and Heading Usage in Chapters (CS-POLICY-DOC-CHAPTER-CONTENT)

# Policy: Content Organization and Heading Usage in Chapters (CS-POLICY-DOC-CHAPTER-CONTENT)

## 1. Policy Statement

This policy mandates the correct hierarchical use of Markdown headings (H2-H6) for structuring content within "Chapter" documents and requires that each H2 section represents a major sub-topic. This ensures content is organized logically, semantically structured, accessible, and easily processable by automated tools.

## 2. Core Requirements

### Rule 2.1: Hierarchical Markdown Headings (Derived from U-STRUC-002, Rule 2.4)
Content within a "Chapter" document MUST be organized using hierarchical Markdown headings (H2 through H6). Heading levels MUST NOT be skipped.
*   **Example:** An H2 heading may be followed by an H3, but not directly by an H4.
    ```markdown
    ## Section 1 (H2)
    ### Subsection 1.1 (H3)
    #### Detail A (H4)
    ### Subsection 1.2 (H3)
    ## Section 2 (H2)
    ```
*   **Notes:**
    *   The H1 heading is reserved for the document title as per [[AS-STRUCTURE-DOC-CHAPTER]].
    *   Adherence to the specific Markdown syntax for headings defined in [[SF-SYNTAX-HEADINGS]] is mandatory.

### Rule 2.2: H2 Sections as Major Sub-Topics (Derived from U-STRUC-002, Rule 2.5)
Each H2 section within a "Chapter" document MUST represent a major sub-topic of that chapter.
*   **Guidance:**
    *   H2 sections break down the chapter's primary subject (defined by the H1/title) into its core components or logical divisions.
    *   If an H2 section becomes too long or covers too many distinct ideas, it should be further subdivided using H3 headings, or potentially split into a separate chapter if the sub-topic is substantial enough.

## 3. Rationale and Importance

Adherence to this policy is crucial for:

*   **Readability and Scannability:** A clear and consistent heading hierarchy allows readers to easily scan the document, understand its structure, and locate specific information.
*   **Accessibility:** Screen readers and other assistive technologies rely on proper heading structures to provide navigation and context to users with disabilities. Skipping heading levels or using them non-semantically can create significant accessibility barriers.
*   **Semantic Structure and Machine Processing:** Correct heading hierarchy provides a clear semantic structure that can be understood by machines. This is vital for:
    *   Automated generation of accurate Tables of Contents.
    *   Content indexing and search engine optimization.
    *   AI-driven content summarization, analysis, or repurposing.
    *   Automated quality checks and validation.
*   **Authoring Consistency:** Clear rules on heading usage simplify the authoring process and ensure a uniform look and feel across all documents.
*   **Maintainability:** Well-structured documents are easier to understand, update, and maintain over time.

## 4. Scope of Application

This policy applies to all "Chapter" documents (as defined in [[AS-STRUCTURE-DOC-CHAPTER]]) across all Knowledge Bases.

## 5. Cross-References
- [[AS-STRUCTURE-DOC-CHAPTER]] - Defines the overall internal structure for Chapter documents.
- [[SF-SYNTAX-HEADINGS]] - Standard for Markdown Heading Syntax.

---
*This policy (CS-POLICY-DOC-CHAPTER-CONTENT) is based on rules 2.4 and 2.5 previously defined in U-STRUC-002 from COL-ARCH-UNIVERSAL.md.*

---

## Policy: Unique Knowledge Base Identification and Naming (CS-POLICY-KB-IDENTIFICATION)

# Policy: Unique Knowledge Base Identification and Naming (CS-POLICY-KB-IDENTIFICATION)

## 1. Policy Statement

This policy mandates unique identification for each Knowledge Base (KB) through its primary folder name and requires clear articulation of the KB's identity within its root file. These measures are essential for maintaining an organized, navigable, and unambiguous knowledge ecosystem.

## 2. Core Requirements

### Rule 2.1: Globally Unique KB Primary Folder Name (Derived from U-ARCH-002, Rule 2.2)
Each Knowledge Base (KB) primary folder name MUST be globally unique within the master KB directory.
*   **Example:** `research-methodology-kb`, `prompt-engineering-kb`
*   **Notes:**
    *   This primary folder name acts as the de facto unique identifier for the KB at the file system level.
    *   Folder naming conventions (e.g., case, separators) MUST adhere to the global file and folder naming standard: [[GM-CONVENTIONS-NAMING]].
    *   Uniqueness prevents naming conflicts and ambiguity, ensuring that each KB can be distinctly referenced.

### Rule 2.2: Consistent KB Identity in `root.md` (Derived from U-ARCH-002, Rule 2.5)
The `root.md` file of each Knowledge Base MUST clearly state the full name and primary scope of that KB in its introductory content (typically the first paragraph or section after the H1 title). This stated identity MUST align with the KB's entry in the `kb-directory.md` file (as defined in [[AS-STRUCTURE-MASTER-KB-INDEX]]).
*   **Example (Text in `prompt-engineering-kb/root.md`):** "Welcome to the Prompt Engineering Knowledge Base. This KB covers principles, techniques, and frameworks for designing effective prompts for Large Language Models..."
*   **Notes:**
    *   This ensures that users entering a KB via its `root.md` immediately understand its identity and scope.
    *   Consistency with the `kb-directory.md` entry reinforces a single source of truth for KB descriptions.

## 3. Rationale and Importance

Adherence to this policy is critical for:

*   **Preventing Conflicts:** Unique KB folder names prevent technical issues and ambiguity in file paths and automated processes.
*   **Ensuring Clarity:** Consistent and clearly stated KB identity within `root.md` helps users confirm they are in the correct knowledge base and understand its purpose.
*   **Discoverability:** Unique and descriptive names, reflected in both the folder structure and `kb-directory.md`, improve the ability to locate specific KBs.
*   **Link Integrity:** While not directly governing link syntax, unique KB identifiers are foundational for reliable inter-KB linking strategies that might emerge.
*   **Maintainability and Governance:** A clear and unique identification scheme simplifies the management and governance of multiple KBs.

## 4. Scope of Application

This policy applies to all Knowledge Bases developed and maintained within the organization's master KB directory.

## 5. Cross-References
- [[AS-STRUCTURE-MASTER-KB-INDEX]] - Defines the structure of the master KB directory and the `kb-directory.md` index file.
- [[GM-CONVENTIONS-NAMING]] - File and Folder Naming Conventions (to be updated with actual ID).

---
*This policy (CS-POLICY-KB-IDENTIFICATION) is based on rules 2.2 and 2.5 previously defined in U-ARCH-002 from COL-ARCH-UNIVERSAL.md.*

---

## Policy: Content Organization within Knowledge Base Parts (CS-POLICY-KB-PART-CONTENT)

# Policy: Content Organization within Knowledge Base Parts (CS-POLICY-KB-PART-CONTENT)

## 1. Policy Statement

This policy mandates that "Chapters" (individual documents or major H2 sections representing distinct topics) within a "Part" of a Knowledge Base (KB) are organized in a logical sequence and that each Chapter addresses a distinct, coherent topic. This ensures clarity, facilitates learning, and supports effective navigation.

## 2. Core Requirements

### Rule 2.1: Logical Sequencing of "Chapters" (Derived from U-STRUC-001, Rule 1.5)
"Chapters" within a "Part" of a Knowledge Base MUST be arranged in a logical sequence.
*   **Guidance:**
    *   The sequence should support a progressive understanding of the Part's subject matter. This might involve, for example, moving from foundational concepts to more advanced topics, or following a chronological or procedural order where appropriate.
    *   Sequencing is typically managed by numerical prefixes in filenames (e.g., `01-introduction.md`, `02-core-concepts.md`) as defined in [[GM-CONVENTIONS-NAMING]], or by the order of H2 headings if Chapters are sections within a single document (e.g., within `_overview.md` for a very small Part).
    *   The Table of Contents within the Part's overview (defined in [[AS-STRUCTURE-KB-PART]]) MUST reflect this logical sequence.

### Rule 2.2: Distinct and Coherent Topic per "Chapter" (Derived from U-STRUC-001, Rule 1.6)
Each "Chapter" file or document (or H2 section if Chapters are not separate files) MUST address a distinct, coherent topic that aligns with the overall theme of the Part.
*   **Guidance:**
    *   A Chapter should have a clear focus and not attempt to cover too many disparate subjects.
    *   If a topic becomes too large or complex for a single Chapter, it should be broken down into multiple, more focused Chapters.
    *   The scope of each Chapter should be clearly articulated, often in its introductory section, as per [[AS-STRUCTURE-DOC-CHAPTER]].

## 3. Rationale and Importance

Adherence to this policy is vital for creating an effective and user-friendly knowledge base:

*   **Clarity and Understanding:** A logical flow of information helps users build knowledge progressively, making complex subjects easier to understand.
*   **Navigability:** Predictable sequencing allows users to easily find information and understand their current position within the broader context of a Part.
*   **Learning Pathways:** Well-structured Parts with logically sequenced Chapters create natural learning pathways for users wishing to master a subject.
*   **Information Architecture:** This policy supports a sound information architecture by ensuring that content is appropriately chunked and ordered.
*   **Maintainability:** Coherent, focused Chapters are easier to maintain, update, and refactor than overly broad or poorly organized content.
*   **Reduced Cognitive Load:** Presenting information in a structured, logical sequence reduces the cognitive load on users, allowing them to focus on understanding the content itself.

## 4. Scope of Application

This policy applies to the organization of "Chapters" within all "Parts" of all Knowledge Bases within the repository.

## 5. Cross-References
- [[AS-STRUCTURE-KB-PART]] - Defines the overall structure of KB Parts and their overviews.
- [[AS-STRUCTURE-DOC-CHAPTER]] - Standard for Content Document ("Chapter") Internal Structure (to be updated with actual ID).
- [[GM-CONVENTIONS-NAMING]] - File and Folder Naming Conventions (relevant for Chapter sequencing).

---
*This policy (CS-POLICY-KB-PART-CONTENT) is based on rules 1.5 and 1.6 previously defined in U-STRUC-001 from COL-ARCH-UNIVERSAL.md.*

---

## Policy: Consistent Application of Knowledge Base Root Structure (CS-POLICY-KB-ROOT)

# Policy: Consistent Application of Knowledge Base Root Structure (CS-POLICY-KB-ROOT)

## 1. Policy Statement

This policy mandates the consistent application of structural choices for Knowledge Base (KB) root organization, as defined in standard [[AS-STRUCTURE-KB-ROOT]]. Specifically, it pertains to the organization of top-level "Parts" (primary sections) within a KB.

## 2. Core Requirement

### Rule 2.1: Consistent Structure for "Parts" (Derived from U-ARCH-001, Rule 1.6)
The chosen method for organizing top-level "Parts" — either as distinct sub-folders (for larger KBs) or as major H1 sections within the `root.md` file (for smaller KBs) — MUST be consistently applied throughout a single Knowledge Base.
*   **Reference:** See [[AS-STRUCTURE-KB-ROOT#Rule 1.4: Top-Level "Parts" in Larger KBs (Sub-folders)]] and [[AS-STRUCTURE-KB-ROOT#Rule 1.5: Top-Level "Parts" in Smaller KBs (`root.md` Sections)]].
*   **Guidance:** A KB should not mix these two approaches. For instance, one Part should not be a sub-folder while another Part in the same KB is an H1 section in `root.md`.

## 3. Rationale and Importance

Adherence to this policy is crucial for several reasons:

*   **User Experience & Navigability:** A consistent structure makes it easier for users to understand, navigate, and predict how content is organized within any given KB. Inconsistent structures can lead to confusion and difficulty in locating information.
*   **Authoring Consistency:** Clear rules on KB structure simplify the authoring process, as contributors do not have to guess how to organize new top-level sections.
*   **Maintainability:** Uniformity in structure reduces complexity when performing maintenance tasks, refactoring content, or applying batch updates.
*   **Automation & Tooling:** Automated tools for validation, indexing, or building KB views rely on predictable structures. Inconsistencies can break these tools or lead to incorrect outputs.
*   **Scalability:** While [[AS-STRUCTURE-KB-ROOT]] provides options for different KB sizes, this policy ensures that the chosen option is applied uniformly, supporting clearer growth paths for KBs. If a "smaller" KB grows, a decision to refactor its Part structure to sub-folders should be applied to all Parts.

## 4. Scope of Application

This policy applies to all Knowledge Bases developed and maintained within the organization.

## 5. Decision Criteria for "Larger" vs. "Smaller" KBs

While [[AS-STRUCTURE-KB-ROOT]] outlines the two structural options for Parts based on KB size, the decision to classify a KB as "larger" (requiring sub-folders for Parts) versus "smaller" (allowing H1 sections in `root.md` for Parts) should be guided by the following considerations:

*   **Number of Top-Level Parts:** If a KB is anticipated to have more than 5-7 top-level Parts, using sub-folders is generally recommended.
*   **Depth of Content within Parts:** If individual Parts are expected to contain a large number of "Chapters" or deep sub-sections, sub-folders provide better organization from the outset.
*   **Complexity of `root.md`:** If the `root.md` file becomes excessively long or difficult to manage due to numerous H1 sections and their inline ToCs, transitioning to sub-folders for Parts is advisable.
*   **Team Size and Collaboration:** Larger teams or more complex collaborative environments may benefit from the clearer separation provided by sub-folders.

The final decision rests with the KB owners or architects, but it should be made with long-term scalability and user experience in mind, and once made, applied consistently as per Rule 2.1.

## 6. Cross-References
- [[AS-STRUCTURE-KB-ROOT]] - Defines the technical structure for KB root organization.

---
*This policy (CS-POLICY-KB-ROOT) supports rule 1.6 previously defined in U-ARCH-001 from COL-ARCH-UNIVERSAL.md.*

---

## Policy: Layered Information Presentation and Progressive Disclosure (CS-POLICY-LAYERED-INFORMATION)

# Policy: Layered Information Presentation and Progressive Disclosure (CS-POLICY-LAYERED-INFORMATION)

## 1. Policy Statement

This policy mandates that all content within the knowledge base be structured using principles of layered information presentation and progressive disclosure. This approach ensures that users can access information at the level of detail appropriate to their needs and understanding, from high-level overviews down to specific details.

## 2. Core Principles and Requirements

The core principle is to present information in an "information funnel," where users start with a general understanding and can progressively drill down into more detailed content as needed.

### Rule 2.1: General to Specific Structure (Derived from U-DETAIL-LEVEL-001, Rule 1.1)
Content MUST be structured to allow users to gain an understanding from a high-level overview progressively down to specific details.
*   **Guidance:** This is an overarching principle that applies to the structure of the entire KB (see [[AS-STRUCTURE-KB-ROOT]]), individual "Parts" (see [[AS-STRUCTURE-KB-PART]]), and "Chapters" (see [[AS-STRUCTURE-DOC-CHAPTER]]).

### Rule 2.2: Mandatory Summaries/Abstracts (Derived from U-DETAIL-LEVEL-001, Rule 1.2)
Every major concept, method, "Part," or "Chapter" MUST begin with a concise summary or abstract.
*   **Guidance:**
    *   For "Chapters," this is mandated by [[AS-STRUCTURE-DOC-CHAPTER]] (Rule 1.2: Topic Abstract).
    *   For specific content types like "Methodology/Technique Descriptions" or "Concept Definitions," this is reinforced by their respective schemas (e.g., [[AS-SCHEMA-METHODOLOGY-DESCRIPTION]], [[AS-SCHEMA-CONCEPT-DEFINITION]]).
    *   This initial summary allows users to quickly grasp the essence of the content and decide if it's relevant to their needs.

### Rule 2.3: Core Ideas Before Details (Derived from U-DETAIL-LEVEL-001, Rule 1.3)
Following a summary or abstract, core principles, main ideas, or key takeaways MUST be presented before detailed elaborations or procedural steps.
*   **Example:** In a document explaining a complex algorithm, outline the algorithm's purpose and main phases before detailing each mathematical step.
*   **Guidance:** This helps users build a foundational understanding before encountering more complex information.

### Rule 2.4: Detailed Information in Deeper Levels (Derived from U-DETAIL-LEVEL-001, Rule 1.4)
Detailed elaborations, such as step-by-step instructions, complex arguments, code snippets, or extensive data, MUST be placed within deeper hierarchical levels of the document (e.g., H3, H4 sections) or, if very extensive, in separate, linked sub-documents or appendices.
*   **Guidance:** Avoid overwhelming users with excessive detail at the higher levels of a document. Use clear headings and subheadings to structure detailed information logically.

### Rule 2.5: Inclusion of Practical Examples (Derived from U-DETAIL-LEVEL-001, Rule 1.5)
Practical examples, application notes, or case studies MUST be included where appropriate to concretize abstract information or illustrate procedures. These should typically follow the theoretical explanations or procedural outlines.
*   **Example:** After explaining a configuration setting, provide an example of its usage.
*   **Guidance:** Examples make information more tangible and easier to understand and apply.

## 3. Benefits of Layered Information Presentation

Adopting this policy provides numerous benefits:

*   **Improved Readability and Scannability:** Users can quickly scan summaries and high-level points to find what they need without being forced to read through exhaustive details.
*   **Enhanced User Comprehension:** Presenting information progressively allows users to build understanding layer by layer, improving comprehension and retention.
*   **Catering to Diverse Expertise Levels:** Novices can focus on overviews and core principles, while experts can quickly navigate to detailed sections.
*   **Reduced Cognitive Load:** Users are not overwhelmed with information they may not need, making the content feel more approachable and easier to digest.
*   **Efficient Information Retrieval:** Finding specific details is faster when the overall structure guides the user effectively from general to specific.
*   **Better User Engagement:** Content that is easy to navigate and understand at the desired level of detail is more likely to keep users engaged.

## 4. Scope of Application

This policy applies to all content creation, structuring, and presentation within all Knowledge Bases in the repository. It is a fundamental principle guiding how authors should think about and organize information.

## 5. Cross-References
*   [[AS-STRUCTURE-KB-ROOT]] - Standard for KB Root Structure.
*   [[AS-STRUCTURE-KB-PART]] - Standard for KB Part Structure.
*   [[AS-STRUCTURE-DOC-CHAPTER]] - Standard for Chapter Internal Structure (especially regarding abstracts and heading hierarchy).
*   [[AS-SCHEMA-METHODOLOGY-DESCRIPTION]] - Content Schema for "Methodology/Technique Descriptions" (example of a content type that embodies layered information).
*   [[AS-SCHEMA-CONCEPT-DEFINITION]] - Content Schema for "Concept Definitions" (another example).

---
*This policy (CS-POLICY-LAYERED-INFORMATION) is based on rules 1.1 through 1.5 previously defined in U-DETAIL-LEVEL-001 from COL-ARCH-UNIVERSAL.md.*

---

## Policy: Knowledge Base Part Overviews (CS-POLICY-PART-OVERVIEW)

# Policy: Knowledge Base Part Overviews (CS-POLICY-PART-OVERVIEW)

## 1. Policy Statement

This policy mandates that each "Part" (top-level primary section) of a Knowledge Base (KB), as defined in [[AS-STRUCTURE-KB-ROOT]], MUST be introduced by a dedicated overview. The specific structural and content requirements for this overview (e.g., its filename `_overview.md` when Parts are folders, or its placement within `root.md` for smaller KBs, and its content including scope, purpose, and Table of Contents) are defined in [[AS-STRUCTURE-KB-PART]].

## 2. Core Requirement

### Rule 2.1: Mandatory Overview for Each KB Part
Every "Part" within a Knowledge Base, whether implemented as a sub-folder or as a major section within the `root.md` file (see [[AS-STRUCTURE-KB-ROOT]]), MUST have an associated overview document or section.
*   **Content and Structure:** The content, naming (e.g., `_overview.md`), and placement of this overview are governed by [[AS-STRUCTURE-KB-PART]]. This includes:
    *   A brief explanation of the Part's scope and purpose.
    *   A linked Table of Contents (ToC) to its main sub-sections ("Chapters").
*   **Rationale:** Part overviews serve as clear entry points to major sections of a KB. They aid navigation by providing context and a roadmap to the content within that Part, helping users understand its structure and quickly locate relevant "Chapters."

## 3. Tool-Agnostic Nature of this Policy

This policy mandates the *existence* and *purpose* of the Part overview content as defined by [[AS-STRUCTURE-KB-PART]].
*   **Display and Interaction:** How a Part overview (e.g., an `_overview.md` file acting as a "folder note") is displayed or interacted with (for instance, a feature where clicking a folder in a file tree opens its associated `_overview.md` note) is considered a tool-specific enhancement or feature of the authoring/publishing platform.
*   **Focus of this Policy:** This policy is concerned with the information architecture requirement that such an overview exists and fulfills its navigational and contextual purpose, regardless of specific tool features that might enhance its presentation. The structural standard [[AS-STRUCTURE-KB-PART]] ensures the overview is discoverable and consistently named/placed.

## 4. Importance of Part Overviews

*   **Enhanced Navigability:** Provides users with a clear understanding of what each major section of the KB contains before they delve into individual "Chapters."
*   **Improved User Experience:** Reduces confusion and helps users orient themselves within the potentially large and complex structure of a KB.
*   **Content Discoverability:** The Table of Contents within each Part overview acts as a local guide, making it easier to discover all related content within that Part.
*   **Structural Clarity:** Reinforces the logical structure of the KB by providing a summary and entry point for each main thematic grouping of content.
*   **Authoring Consistency:** Ensures that all major sections of a KB are introduced in a uniform and helpful way.

## 5. Scope of Application

This policy applies to all Knowledge Bases and their constituent "Parts." All individuals involved in KB architecture, content creation, and curation are responsible for ensuring that Part overviews are created and maintained according to this policy and the referenced structural standards.

## 6. Cross-References
- [[AS-STRUCTURE-KB-PART]] - Defines the specific structural and content requirements for Part overviews (e.g., `_overview.md` content).
- [[AS-STRUCTURE-KB-ROOT]] - Defines how "Parts" are organized within a KB (as folders or sections in `root.md`).

---
*This policy (CS-POLICY-PART-OVERVIEW) mandates the use of Part Overviews, generalizing concepts previously associated with tool-specific features like Obsidian's folder notes (formerly U-USAGE-FOLDERS-NOTES-001) into a tool-agnostic architectural requirement.*

---

## Policy: Universal Principles for Content Exclusion (CS-POLICY-SCOPE-EXCLUSION)

# Policy: Universal Principles for Content Exclusion (CS-POLICY-SCOPE-EXCLUSION)

## 1. Policy Statement

This policy outlines the universal principles governing the exclusion of certain types of content from any Knowledge Base (KB). Adherence to these principles is mandatory to ensure legal compliance, uphold ethical standards, maintain data security, protect intellectual property, and preserve the quality, focus, and trustworthiness of the knowledge base.

## 2. Core Principles for Content Exclusion

### Rule 2.1: Prohibition of Illegal, Unethical, or Harmful Content (Derived from U-SCOPE-EXCLUDE-001, Rule 1.1)
Content that is illegal, unethical (by broad societal or organizational consensus), or promotes harm, discrimination, or violence MUST NOT be included in any Knowledge Base.
*   **Guidance:** This includes, but is not limited to, hate speech, incitement to violence, defamation, and content that violates applicable laws or regulations.
*   **Rationale:** Essential for legal compliance, ethical conduct, and maintaining a safe and respectful environment.

### Rule 2.2: Strict Control of Sensitive Personally Identifiable Information (PII) (Derived from U-SCOPE-EXCLUDE-001, Rule 1.2)
Sensitive Personally Identifiable Information (PII) MUST NOT be included in publicly accessible or broadly available Knowledge Bases.
*   **Exception:** PII may only be included if explicitly mandated by the KB's secure design for specific, legitimate internal operational use, AND such inclusion is governed by strict access controls, data privacy policies, and relevant legal/regulatory compliance measures.
*   **Examples of PII to generally exclude:** Social Security numbers, private financial details, personal health information (unless in a specifically secured and compliant system), unmasked personal contact details of non-public figures.
*   **Rationale:** Protects individual privacy, ensures compliance with data protection regulations (e.g., GDPR, CCPA), and prevents misuse of sensitive personal data.

### Rule 2.3: Respect for Intellectual Property (Derived from U-SCOPE-EXCLUDE-001, Rule 1.3)
Proprietary information, copyrighted material, or other intellectual property from third parties to which the organization does not hold explicit rights or a valid license for use and distribution within the KB MUST NOT be included.
*   **Guidance:** This includes verbatim copying of large text sections from copyrighted books, articles, or websites; use of unlicensed images, software code, or trade secrets.
*   **Alternative:** Instead of copying, summarize and cite the original source according to [[SF-FORMATTING-CITATIONS]].
*   **Rationale:** Ensures legal compliance with copyright laws and respects the intellectual property rights of others.

### Rule 2.4: Avoidance of Unnecessary Redundancy (Derived from U-SCOPE-EXCLUDE-001, Rule 1.4)
Redundant information that is already well-covered and adequately explained elsewhere within the *same Knowledge Base section or its direct conceptual hierarchy* MUST NOT be included if it does not add significant new value, perspective, or context.
*   **Guidance:**
    *   Prefer linking to the authoritative source of the information within the KB using [[SF-LINKS-INTERNAL-SYNTAX]].
    *   This rule does not prohibit summaries or syntheses that draw upon multiple sources to create new insights, but rather discourages simple repetition of existing content.
*   **Rationale:** Improves maintainability (updates only need to happen in one place), reduces KB clutter, and ensures users are directed to the most current and authoritative information on a topic.

## 3. Importance of These Exclusions

Strict adherence to these content exclusion principles is critical for:

*   **Legal and Regulatory Compliance:** Avoiding illegal content, PII breaches, and copyright infringement is fundamental to legal operation.
*   **Ethical Responsibility:** Upholding ethical standards in content ensures the KB is a responsible and trustworthy resource.
*   **Data Security and Privacy:** Protecting sensitive information is paramount.
*   **Maintaining Knowledge Base Quality and Focus:** Excluding irrelevant, harmful, or redundant information keeps the KB focused, reliable, and valuable.
*   **Building and Retaining User Trust:** Users must be confident that the KB content is legal, ethical, and respects privacy and intellectual property.
*   **Mitigating Risk:** Proactive exclusion of problematic content mitigates various organizational risks.

## 4. Scope of Application

This policy applies to all individuals involved in planning, creating, contributing, curating, or reviewing content for any Knowledge Base within the repository.

## 5. Cross-References
- [Policy: Universal Principles for Content Inclusion](#policy-universal-principles-for-content-inclusion-cs-policy-scope-inclusion) - Policy detailing what content SHOULD be included.
- [[SF-FORMATTING-CITATIONS]] - Standard for Citing External Sources (relevant for avoiding IP issues).
- [[SF-LINKS-INTERNAL-SYNTAX]] - Standard for Internal Linking Syntax (relevant for avoiding redundancy).

---
*This policy (CS-POLICY-SCOPE-EXCLUSION) is based on rules 1.1 through 1.4 previously defined in U-SCOPE-EXCLUDE-001 from COL-CONTENT-UNIVERSAL.md.*

---

## Policy: Universal Principles for Content Inclusion (CS-POLICY-SCOPE-INCLUSION)

# Policy: Universal Principles for Content Inclusion (CS-POLICY-SCOPE-INCLUSION)

## 1. Policy Statement

This policy outlines the universal principles governing the inclusion of content within any Knowledge Base (KB). Adherence to these principles is essential for maintaining the focus, quality, relevance, and overall utility of the knowledge base, ensuring it remains a valuable and trusted resource.

## 2. Core Principles for Content Inclusion

### Rule 2.1: Relevance to KB Scope (Derived from U-SCOPE-INCLUDE-001, Rule 1.1)
All content included in any Knowledge Base (KB) MUST be directly relevant to the stated scope and purpose of that specific KB.
*   **Guidance:** The scope and purpose of each KB are typically defined in its `root.md` file and its entry in the `kb-directory.md` (see [[AS-STRUCTURE-MASTER-KB-INDEX]]). Content that falls outside this defined scope should not be included in that particular KB, though it may be relevant for a different KB.
*   **Rationale:** This ensures that KBs remain focused and do not become diluted with irrelevant information, making it easier for users to find what they need.

### Rule 2.2: Verifiability and Citability (Derived from U-SCOPE-INCLUDE-001, Rule 1.2)
Content MUST be verifiable or derived from citable sources for KBs that deal with factual information. For KBs focusing on conceptual or philosophical topics, content should be based on logical reasoning and established schools of thought.
*   **Guidance:**
    *   Factual claims, data, and significant assertions should be supported by evidence.
    *   Citations for external sources MUST adhere to [[SF-FORMATTING-CITATIONS]].
*   **Rationale:** Requiring verifiability and proper citation builds trust in the KB's content and allows users to explore source material for deeper understanding or validation.

### Rule 2.3: Focus on Actionable and Evergreen Knowledge (Derived from U-SCOPE-INCLUDE-001, Rule 1.3)
Content MUST primarily focus on providing information and actionable knowledge (e.g., "how-to" guides, explanations of "why" or "what," best practices, standard procedures, definitions).
*   **Exclusions:** Content should generally avoid:
    *   Ephemeral news or time-sensitive announcements (unless the KB is specifically an archive for such items and this is clearly stated in its scope).
    *   Personal opinions that are not protected by a specific, defined "Expert Opinion" or similar template/schema.
    *   Transient discussions or uncurated commentary.
*   **Rationale:** Prioritizing durable, actionable knowledge ensures the long-term value and utility of the KB. This focus helps differentiate the KB from more informal communication channels.

## 3. Importance of These Principles

Upholding these content inclusion principles is vital for:

*   **Maintaining Focus:** Ensures each KB stays true to its defined purpose, preventing scope creep and information overload.
*   **Ensuring Quality and Reliability:** By requiring verifiability and a focus on actionable knowledge, the overall quality and reliability of the KB are enhanced.
*   **Maximizing Utility:** Relevant, focused, and high-quality content makes the KB a more useful and valuable resource for its target audience.
*   **Building User Trust:** Users are more likely to trust and rely on a KB that contains accurate, well-sourced, and relevant information.
*   **Improving Discoverability:** When content is relevant and focused, search and navigation within the KB become more effective.
*   **Streamlining Maintenance:** Clear inclusion criteria simplify content lifecycle management, including reviews, updates, and archiving decisions.

## 4. Scope of Application

This policy applies to all individuals involved in planning, creating, contributing, or curating content for any Knowledge Base within the repository.

## 5. Cross-References
- [Policy: Universal Principles for Content Exclusion](#policy-universal-principles-for-content-exclusion-cs-policy-scope-exclusion) - Policy detailing what content MUST NOT be included.
- [[SF-FORMATTING-CITATIONS]] - Standard for Citing External Sources.
- [[AS-STRUCTURE-MASTER-KB-INDEX]] - For understanding how KB scope is documented.

---
*This policy (CS-POLICY-SCOPE-INCLUSION) is based on rules 1.1 through 1.3 previously defined in U-SCOPE-INCLUDE-001 from COL-CONTENT-UNIVERSAL.md.*

---

## Policy: Clarity, Objectivity, and Consistency in Language (CS-POLICY-TONE-LANGUAGE)

# Policy: Clarity, Objectivity, and Consistency in Language (CS-POLICY-TONE-LANGUAGE)

## 1. Policy Statement

This policy establishes the standards for language, tone, and style to be used in all written content within the knowledge base. Adherence to these standards is essential for ensuring clarity, promoting user understanding, maintaining objectivity, and achieving consistency across all documents.

## 2. Core Language and Tone Requirements

### Rule 2.1: Clarity, Conciseness, and Precision (Derived from U-TONE-LANG-001, Rule 1.1)
All language used MUST be clear, concise, precise, and unambiguous. Overly complex sentence structures, jargon where simpler terms suffice, and verbose phrasing MUST be avoided.
*   **Example:** Prefer "The method involves..." over "It is the case that the method, in its fundamental aspects, necessitates..."
*   **Rationale:** Clear and direct language reduces ambiguity, improves reader comprehension, and makes information more accessible to a wider audience, including those for whom the language may be a second language or who are new to the subject matter.

### Rule 2.2: Objective and Informative Tone (Derived from U-TONE-LANG-001, Rule 1.2)
The tone of content MUST be objective, academic (where appropriate to the subject), and informative. Overly informal language, expressions of personal opinion (unless explicitly framed as such and necessary for context, e.g., an "Expert Opinion" section), or persuasive language MUST NOT be used as the default style.
*   **Guidance:** The primary goal is to inform and explain, not to entertain or persuade, unless the specific purpose of a document (e.g., a vision statement) explicitly calls for a different tone.
*   **Rationale:** An objective tone builds trust and credibility. It ensures that the information is presented factually, allowing users to form their own conclusions.

### Rule 2.3: Consistent Use of Terminology (Derived from U-TONE-LANG-001, Rule 1.3)
Terminology specific to a domain or subject MUST be used consistently throughout all related documents. If a term has multiple meanings, the intended meaning MUST be clarified upon its first use within a document, or the term should be linked to its definition in a relevant glossary (e.g., [[GM-GLOSSARY-STANDARDS-TERMS]]).
*   **Example:** If "Systematic Review" is chosen as the standard term, it should be used consistently instead of interchanging it with "structured review" or "comprehensive literature survey" without clarification.
*   **Rationale:** Consistent terminology prevents confusion and ensures that all readers share a common understanding of key terms. This is vital for precise communication, especially in technical or specialized fields.

### Rule 2.4: Definition of Acronyms and Abbreviations (Derived from U-TONE-LANG-001, Rule 1.4)
Acronyms and abbreviations MUST be defined upon their first use in any given document. The full term should be written out, followed by the acronym or abbreviation in parentheses. Subsequently, the acronym or abbreviation can be used.
*   **Example:** "This document adheres to the Knowledge Base (KB) standards. The KB provides..."
*   **Exception:** Widely understood universal acronyms (e.g., HTML, API in a technical KB) may not require definition in every document, but when in doubt, define.
*   **Rationale:** Defining acronyms ensures that all readers, regardless of their familiarity with the subject, can understand the terminology used. It avoids ambiguity and improves readability.

### Rule 2.5: Preference for Active Voice (Derived from U-TONE-LANG-001, Rule 1.5)
Active voice MUST be used more frequently than passive voice where appropriate, especially for clarity and directness in instructional or procedural content.
*   **Example:** Prefer "The linter checks the frontmatter." over "The frontmatter is checked by the linter."
*   **Guidance:** While passive voice has its uses (e.g., when the agent performing an action is unknown or unimportant), active voice generally makes sentences more direct, easier to understand, and more engaging.
*   **Rationale:** Active voice clearly identifies the actor performing an action, which can be crucial for understanding processes or responsibilities. It often results in shorter, more impactful sentences.

## 3. Scope of Application

This policy applies to all textual content within all Knowledge Bases, including but not limited to:
*   Standard and policy documents
*   Guides and instructional materials
*   Descriptive texts within schemas and templates
*   Content of `primary-topic`, `scope_application`, and similar metadata fields

## 4. Cross-References
- [[GM-GLOSSARY-STANDARDS-TERMS]] - For definitions of standard terms used across the knowledge base (if such a glossary exists).

---
*This policy (CS-POLICY-TONE-LANGUAGE) is based on rules 1.1 through 1.5 previously defined in U-TONE-LANG-001 from COL-CONTENT-UNIVERSAL.md.*

---

## Policy: Table of Contents (ToC) Usage and Generation (CS-TOC-POLICY)

# Policy: Table of Contents (ToC) Usage and Generation (CS-TOC-POLICY)

## 1. Policy Statement

This policy defines requirements and recommendations for the inclusion, content, and generation of Tables of Contents (ToCs) within knowledge base documents. Effective ToCs are crucial for document navigation, providing users with an overview of the document's structure and direct access to its sections.

## 2. Core ToC Requirements and Recommendations

### Rule 2.1: ToC Mandate for "Chapter" Documents
As mandated by [[AS-STRUCTURE-DOC-CHAPTER]] (Rule 1.3), all "Chapter" documents (primary content documents) MUST include a Table of Contents.
*   **Placement:** The ToC typically follows the introductory abstract, as specified in [[AS-STRUCTURE-DOC-CHAPTER]].
*   **Rationale:** Essential for navigating longer content documents and understanding their structure at a glance.

### Rule 2.2: Content of ToC - Heading Levels
The Table of Contents SHOULD typically list all H2 and H3 headings within the document.
*   **Deeper Levels (H4-H6):** Inclusion of H4 and deeper heading levels in the ToC is OPTIONAL and should be determined by the document's length and complexity. If including deeper levels significantly clutters the ToC without adding substantial navigational value, they may be omitted.
*   **Rationale:** Provides a useful balance between detail and conciseness in the ToC. H2s and H3s usually represent the main sections and sub-sections that users will want to navigate to directly.

### Rule 2.3: No ToC Mandate for Atomic Standard Documents
Individual atomic standard documents (e.g., those located in `/standards/src/` such as `SF-*.md`, `CS-*.md`, `AS-*.md`, `OM-*.md`, `GM-*.md`, `MT-*.md`) are NOT required to have an internal Table of Contents.
*   **Rationale:**
    *   Atomic standard documents are typically shorter and more focused on a specific set of rules or a single concept. Their structure is usually evident from the main headings, and an internal ToC often provides limited additional navigational value for their typical length.
    *   The primary navigation for standards is intended to be through the Standards KB `root.md`, collection documents (which may be deprecated but linked from new navigational aids), and the relationships defined in their `related-standards` frontmatter.
*   **Exception:** Very long or complex standard documents MAY include a ToC if the author deems it beneficial for readability, but it is not a mandatory requirement for this `info-type`.

### Rule 2.4: Tooling for ToC Generation (Recommended)
While manual ToCs MUST follow the syntax defined in [[SF-TOC-SYNTAX]], the use of **automated tools or plugins to generate and maintain Tables of Contents is STRONGLY RECOMMENDED** for "Chapter" documents and other longer content forms.
*   **Benefits of Automation:**
    *   **Accuracy:** Ensures ToC entries and links are always up-to-date with the document's headings, reducing the risk of broken links or outdated titles.
    *   **Efficiency:** Saves significant authoring and maintenance effort compared to manual ToC creation.
*   **Output Conformance:** The output generated by any automated ToC tool MUST conform to the syntax specified in [[SF-TOC-SYNTAX]] (i.e., standard Markdown unordered lists with internal anchor links). This ensures that the ToC is portable and correctly rendered even if the specific tool is not available in all environments.
*   **Tool-Agnostic Principle:** The choice of a specific ToC generation tool is secondary to the requirement that the generated ToC adheres to the defined Markdown syntax standard. Authors should select tools that produce compliant output.

## 3. Importance of ToC Policy

*   **Enhanced Document Navigation:** Allows users to quickly understand the structure of a document and jump to relevant sections.
*   **Improved User Experience:** Makes longer documents more accessible and less daunting to read.
*   **Authoring Efficiency (with Automation):** Reduces the manual effort required to create and maintain accurate ToCs.
*   **Consistency:** Ensures a consistent approach to ToC provision and formatting across the knowledge base.

## 4. Scope of Application

This policy applies to all documents within the knowledge base, particularly "Chapter" documents. It guides decisions on when a ToC is required, what it should contain, and how it should be generated.

## 5. Cross-References
- [[SF-TOC-SYNTAX]] - Defines the mandatory Markdown syntax for manually created ToCs (and the target output for automated tools).
- [[AS-STRUCTURE-DOC-CHAPTER]] - Mandates the inclusion of a ToC in "Chapter" documents and specifies its typical placement.

---
*This policy (CS-TOC-POLICY) generalizes previous mandates (like O-USAGE-TOC-MANDATE-001) and tool-specific recommendations (like O-USAGE-TOC-PLUGIN-001) into a tool-agnostic policy framework, emphasizing standard Markdown output for ToCs while recommending automation.*
