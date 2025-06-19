---
title: 'Standard: Draft Review and Promotion Process'
standard_id: SA-PROCESS-DRAFT-REVIEW
aliases:
- Draft Review Process
- Standards Promotion Process
- Quality Gate Process
tags:
- content-type/standard-definition
- content-type/process-standard
- criticality/p1-high
- kb-id/standards
- status/active
- topic/governance
- topic/quality-assurance
kb-id: standards
info-type: standard-definition
primary-topic: Formal process for reviewing and promoting draft standards to active status
related-standards:
- OM-POLICY-STANDARDS-GOVERNANCE
- OM-VERSIONING-CHANGELOGS
- MT-SCHEMA-FRONTMATTER
version: 1.0.0
date-created: '2025-06-19T21:00:00Z'
date-modified: '2025-06-19T21:00:00Z'
primary_domain: SA
sub_domain: PROCESS
scope_application: All standards documents requiring promotion from draft to active status
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Standards quality
- Governance compliance
- Knowledge base integrity
- Process standardization
---
# Standard: Draft Review and Promotion Process (SA-PROCESS-DRAFT-REVIEW)

## 1. Standard Statement

This standard defines the mandatory process for reviewing and promoting standards from `status/draft` to `status/active`. It establishes quality gates, review criteria, and approval workflows to ensure that only complete, accurate, and compliant standards achieve active status.

## 2. Review Prerequisites

### Rule 2.1: Lifecycle Status Verification
Standards MUST be in `status/draft` to be eligible for promotion review. Standards in other statuses (e.g., `planned`, `deprecated`) are not eligible for this process.

### Rule 2.2: Version Requirements  
Draft standards MUST have a valid semantic version (following [[OM-VERSIONING-CHANGELOGS]]) before review initiation. Initial promotion typically targets version `1.0.0`.

### Rule 2.3: Frontmatter Completeness
All mandatory frontmatter fields as defined in [[MT-SCHEMA-FRONTMATTER]] MUST be populated with valid, non-placeholder values before review.

## 3. Expert Review Checklist

### Rule 3.1: Content Completeness Review
The reviewer MUST verify that the standard contains:
- **✓ Clear Standard Statement**: Unambiguous description of what the standard mandates
- **✓ Complete Rule Set**: All necessary rules are defined with appropriate numbering
- **✓ Scope Definition**: Clear statement of what the standard applies to
- **✓ Examples**: Sufficient examples demonstrating rule application
- **✓ Rationale**: Justification for why the standard exists and its benefits

### Rule 3.2: Link Integrity Verification  
The reviewer MUST verify that:
- **✓ Internal Links**: All `[[STANDARD_ID]]` references point to existing standards
- **✓ Section Links**: All `[[STANDARD_ID#Section]]` references point to existing sections
- **✓ Cross-References**: Related standards listed in frontmatter actually exist
- **✓ External Links**: External URLs are accessible and relevant

### Rule 3.3: Reference Validity Check
The reviewer MUST verify that:
- **✓ Standard References**: All referenced standards exist and are not deprecated
- **✓ Circular Dependencies**: No circular reference chains exist
- **✓ Dependency Chain**: Referenced standards are logically consistent
- **✓ Citation Format**: All references follow established citation standards

### Rule 3.4: Linter Compliance Verification
The reviewer MUST verify that:
- **✓ Markdown Syntax**: Valid Markdown with no syntax errors
- **✓ YAML Frontmatter**: Valid YAML structure with no parsing errors  
- **✓ Naming Conventions**: File names follow established naming standards
- **✓ Formatting Standards**: Content follows formatting and style guidelines

### Rule 3.5: Logical Soundness Assessment
The reviewer MUST verify that:
- **✓ Rule Coherence**: Rules are internally consistent and non-contradictory
- **✓ Practical Applicability**: Rules can be realistically implemented
- **✓ Domain Alignment**: Standard fits appropriately within its assigned domain
- **✓ Scope Boundaries**: Standard scope is neither too broad nor too narrow

### Rule 3.6: Quality Standards Check
The reviewer MUST verify that:
- **✓ Language Quality**: Clear, professional, unambiguous writing
- **✓ Technical Accuracy**: Technical content is correct and current
- **✓ Completeness**: No obvious gaps or missing essential information
- **✓ Consistency**: Terminology and approach consistent with related standards

## 4. Review Documentation Requirements

### Rule 4.1: Review Record Creation
For each reviewed standard, the reviewer MUST create a review record containing:
- Standard ID and version reviewed
- Review date and reviewer identification  
- Checklist completion status (pass/fail for each item)
- Issues identified and resolution status
- Final recommendation (approve/reject/needs-revision)

### Rule 4.2: Issue Tracking
All identified issues MUST be:
- Documented with specific location references (line numbers, section names)
- Categorized by severity (blocking, major, minor)
- Tracked through to resolution or acceptance
- Verified as resolved before final approval

## 5. Promotion Process Workflow

### Rule 5.1: Review Initiation
Draft promotion review is initiated when:
- A draft standard is identified for promotion
- The review prerequisites (Section 2) are verified
- A qualified reviewer is assigned

### Rule 5.2: Review Execution
The reviewer MUST:
1. Complete all checklist items in Section 3
2. Document findings according to Section 4
3. Provide clear recommendation with justification
4. Submit review record for approval

### Rule 5.3: Status Promotion
Upon successful review completion:
- Standard frontmatter `status` field is updated from `draft` to `active`
- Standard version is updated to promotion target (typically `1.0.0`)
- Date-modified field is updated to promotion date
- Promotion is documented in project tracking

### Rule 5.4: Rejection Handling  
If review identifies blocking issues:
- Standard remains in `status/draft`
- Issues are documented and communicated to standard owner
- Re-review is scheduled after issue resolution
- Process iterates until approval or formal rejection

## 6. Reviewer Qualifications

### Rule 6.1: Technical Competency
Reviewers MUST demonstrate:
- Deep understanding of the knowledge base architecture
- Familiarity with all related standards and dependencies
- Experience with content quality assessment
- Knowledge of the specific domain being reviewed

### Rule 6.2: Authority and Independence
Reviewers MUST:
- Have architect-level authority for final approval decisions  
- Be independent from the standard's original development
- Have no conflicts of interest regarding the standard's approval

## 7. Quality Metrics and Success Criteria

### Rule 7.1: Review Completion Metrics
Success is measured by:
- **100% checklist completion** for all reviewed standards
- **Complete issue resolution** before promotion approval  
- **Zero post-promotion corrections** required within 30 days
- **Stakeholder acceptance** of promoted standards

### Rule 7.2: Process Efficiency Metrics
Process efficiency is measured by:
- Average review cycle time from initiation to decision
- Percentage of standards passing review on first attempt
- Issue discovery rate by review phase
- Reviewer workload distribution and capacity

## 8. Scope of Application

This standard applies to:
- All standards documents requiring promotion from draft to active status
- All personnel involved in standards review and approval processes
- All documentation and tracking related to the promotion process

## 9. Cross-References
- [[OM-POLICY-STANDARDS-GOVERNANCE]] - Overall governance framework for standards
- [[OM-VERSIONING-CHANGELOGS]] - Version numbering and change documentation requirements
- [[MT-SCHEMA-FRONTMATTER]] - Mandatory frontmatter field definitions and formats

---

*This standard (SA-PROCESS-DRAFT-REVIEW) establishes the formal quality gate process for ensuring that only complete, accurate, and compliant standards achieve active status in the knowledge base repository.*