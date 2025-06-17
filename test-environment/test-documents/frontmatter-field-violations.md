---
title: Frontmatter Field Violations Test
standard_id: TEST-FRONTMATTER-VIOLATIONS
date-created: 2025-01-11
primary_domain: TEST
sub_domain: VIOLATIONS
custom_field: value
kebab_case_field: value
camel_case_field: value
info-type: general
version: 0.0.1
date-modified: '2025-06-17T02:29:16Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
- topic/test
- topic/violations
kb-id: test-environment
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# Frontmatter Field Violations

This file contains frontmatter fields that violate snake_case convention:
- standard-id (should be standard_id)
- primaryDomain (should be primary_domain)  
- subDomain (should be sub_domain)
- kebab-case-field (should be kebab_case_field)
- camelCaseField (should be camel_case_field)
