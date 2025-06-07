# Frontmatter Registry Generation Report
Generated on: 2025-06-04 20:39:19
Source: master-knowledge-base\standards\src\MT-SCHEMA-FRONTMATTER.md
Mode: DRY RUN

## Extraction Summary
- Info-types extracted: 27
- Field definitions extracted: 18
- Field order positions: 2

## Generated Files
- info_types.txt
- frontmatter_fields.yaml
- field_order.yaml

## Info-Types Extracted
- standard-definition
- policy-document
- guide-document
- glossary-document
- template-document
- registry-document
- schema-document
- chapter-document
- key-definition-set
- kb-definition-map
- how-to-guide
- tutorial-document
- troubleshooting-guide
- reference-document
- architecture-overview
- design-specification
- meeting-notes
- report-document
- process-definition
- role-definition
- service-definition
- api-specification
- data-model-definition
- security-standard
- compliance-guideline
- collection-document
- changelog

## Field Definitions Summary
- title: mandatory | String.
- standard_id: mandatory | String.
- aliases: optional | List of Strings.
- tags: mandatory | List of Strings.
- kb-id: mandatory | String. [CV]
- info-type: mandatory | String.
- primary-topic: mandatory | String.
- related-standards: optional | List of Strings.
- version: mandatory | String.
- date-created: mandatory | String.
- date-modified: mandatory | String.
- primary_domain: mandatory | String.
- sub_domain: mandatory | String.
- scope_application: mandatory | String.
- criticality: mandatory | String. [CV]
- lifecycle_gatekeeper: mandatory | String. [CV]
- impact_areas: mandatory | List of Strings.
- change_log_url: mandatory | String.

## Field Order
 1. title
 2. standard_id