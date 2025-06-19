---
title: MAIN PROJECT GUIDELINES — FOUNDATIONAL PRINCIPLES & OPERATIONAL DIRECTIVES
standard_id: project-guideline-main
tags:
- content-type/project-guideline
- criticality/p0-critical
- info-type/project-guideline
- kb-id/global
- status/active
- topic/guidelines
- topic/project
- topic/foundational-principles
kb-id: project-governance-main
info-type: project-guideline
primary-topic: Foundational principles and non-negotiable operational directives governing all aspects of knowledge base development and maintenance
version: 2.1.0
date-created: '2025-05-25T00:00:00Z'
date-modified: '2025-06-18T01:00:00Z'
primary_domain: PROJECT
sub_domain: GUIDELINES
scope_application: ALL CONTRIBUTORS, ALL TASKS, ALL ASPECTS OF KB/REPO DEVELOPMENT
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas:
- foundational-architecture
- team-collaboration
- automation-workflows
- standards-compliance
change_log_url: N/A
---

# MAIN PROJECT GUIDELINES — FOUNDATIONAL PRINCIPLES & OPERATIONAL DIRECTIVES

> **🚨 ABSOLUTE COMPLIANCE REQUIRED — NON-NEGOTIABLE 🚨**

***ALL PERSONNEL MUST IMPLEMENT FOUNDATIONAL PRINCIPLES AND COMPLY WITH EVERY DIRECTIVE. VIOLATIONS TRIGGER IMMEDIATE DISCIPLINARY ACTION.***

> **❗ MANDATORY FORENSIC COMPLIANCE NOTICE ❗**
> 
> **ALL REPOSITORY ACTIVITIES ARE UNDER CONTINUOUS FORENSIC MONITORING AND AUDIT. EVERY ACTION, DECISION, AND DEVIATION IS PERMANENTLY RECORDED AND SUBJECT TO IMMEDIATE REVIEW.**
> 
> ***ANY VIOLATION OF RULES, STANDARDS, BEST PRACTICES, OR UNAUTHORIZED ASSUMPTIONS WILL TRIGGER IMMEDIATE AND NON-NEGOTIABLE DISCIPLINARY ACTION WITH ZERO TOLERANCE ENFORCEMENT.***
> 
> **THIS IS A MISSION-CRITICAL OPERATIONAL ENVIRONMENT. COMPLIANCE IS NOT OPTIONAL — IT IS ABSOLUTE AND MANDATORY.**

## 0. FOUNDATIONAL PRINCIPLES — **SUPREME AUTHORITY**

> ***THESE FOUNDATIONAL PRINCIPLES GOVERN EVERY ASPECT OF THE MASTER KNOWLEDGE BASE SYSTEM***

### 0.1 **SINGLE SOURCE OF TRUTH (SST) FOR EVERYTHING WHEN POSSIBLE**

### 0.2 **DITA-INSPIRED** AND **RDF/OWL-INSPIRED** WORKFLOWS

### 0.3 STRICT ADHERENCE TO AN EXTREMELY MANDATING SET OF **STANDARDS/RULES/POLICIES/GUIDELINES** FOR EVERYTHING

### 0.4 EXTREMELY COMPREHENSIVE AND ENTERPRISE-LEVEL **AUTOMATION** IMPLEMENTATIONS FOR ALL TASKS, EVEN SMALL

### 0.5 **AUTOMATION-BY-SCRIPTING** FIRST, **AUTOMATION-BY-LLM** SECOND, **MANUAL-BY-LLM** THIRD--**NO** MANUAL-BY-HUMAN WORKFLOWS

### 0.6 TEAM MEMBERS ARE: 1. A HUMAN ARCHITECT/DECISION-MAKER, 2. AI/LLM DEVELOPMENT-TEAM

### 0.7 MANDATORY ADHERENCE TO **AI-Powered Model-Driven Development (APMDD)** PRINCIPLES AND **Hexagonal Microkernel Architecture (HMA)** ARCHITECTURE (DETAILS FOR BOTH WILL BE INTRODUCED SOON)

> **📋 NOTE**: *Currently implementing foundational principles for the ultimate KB/REPO architecture*

---

## 1. CORE OPERATIONAL PRINCIPLES — **MISSION-CRITICAL EXECUTION**

### 1.1 OWNERSHIP & RESPONSIBILITY — **🎯 TOTAL ACCOUNTABILITY**

- **TAKE FULL OWNERSHIP** of every assigned task — deflection is ❌ **PROHIBITED**
- **ELIMINATE MANUAL WORK** where automation achieves results — replace with scripted solutions ⚡ **IMMEDIATELY**
- **EXECUTE USER PROMPTS** exactly as specified with 🔍 **UNDIVIDED ATTENTION**

### 1.2 FACT-BASED EXECUTION — **🚫 ZERO ASSUMPTIONS POLICY**

- **TASK COMPLETION** requires 💯 **100% VERIFICATION** — perfection is the **ONLY** acceptable outcome
- **VERIFY ALL INFORMATION** through direct inspection — assumptions result in 🚨 **IMMEDIATE CORRECTIVE ACTION**
- **UTILIZE AVAILABLE TOOLS** (file search, code search) to obtain facts — **ESCALATE IMMEDIATELY** if data missing

### 1.3 PRECISION & ATTENTION TO DETAIL — **🔬 MICROSCOPIC EXECUTION**

- **INSPECT METICULOUSLY**: regex patterns, file paths, configurations, script logic
- **ENSURE AUTOMATION** behaves exactly as intended — unintended side-effects trigger 🚫 **PROCESS TERMINATION**

### 1.4 STANDARDS ADHERENCE — **⚖️ ABSOLUTE COMPLIANCE**

- **INTERNALIZE AND ENFORCE** all documented standards in `standards/`
- **CORRECT DATA** that violates standards — lowering standards is 🚨 **STRICTLY FORBIDDEN**
- **ESCALATE** unworkable standards for formal update

### 1.5 REPOSITORY ORGANIZATION — **🏛️ PRISTINE MAINTENANCE**

- **STORE** all logs, reports, debug output in `./tools/reports/`
- **ARCHIVE — NEVER DELETE** temporary code in `./archive/` — deletion triggers 💥 **DISCIPLINARY REVIEW**
- **MAINTAIN** pristine working directory at all times

### 1.6 SEQUENTIAL PLANNING — **🔗 LOGICAL DEPENDENCY ONLY**

- **TIME-BASED PLANNING** is 🚫 **PROHIBITED** (e.g., "do X in 2 weeks")
- **SEQUENTIAL PLANNING** is ✅ **MANDATORY** (e.g., "first do X, then Y, then Z")
- **ORGANIZE TASKS** by logical dependency and priority — not arbitrary timelines
- **COMPLETE PREREQUISITES** before advancing to dependent tasks

## 2. PROBLEM SOLVING METHODOLOGY — **🧩 SYSTEMATIC APPROACH**

### 2.1 HOW TO THINK — **🧠 SYSTEMATIC APPROACH**

- **ULTRATHINK** and think like a *CHESS MASTER* for every task
- **ALWAYS BREAK DOWN TASKS INTO MANAGEABLE STEPS**
- **USE SEQUENTIAL THINKING MCP TOOL** (`sequential-thinking`) for all planning and execution

### 2.2 MANDATORY TASK DECOMPOSITION — **🔢 7-STEP PROCESS**

> **⚡ NON-NEGOTIABLE DECOMPOSITION SEQUENCE ⚡**
> 1. **ANALYZE** — identify components, prerequisites, dependencies
> 2. **DECOMPOSE** — break into manageable, verifiable steps
> 3. **PRIORITIZE** — sequence by logical dependency
> 4. **EXECUTE** — complete one step fully before advancing
> 5. **VERIFY** — test each step to 100% perfection
> 6. **DOCUMENT** — *only when total completion is achieved; document your report in `llm-reports/`*
> 7. **ITERATE** — repeat until total completion

### 2.3 INVESTIGATION PROTOCOL — **🔍 NO ASSUMPTIONS**

- **INVESTIGATE** every error/warning deeply: tool logic, configuration, data
- **ADD DEBUG OUTPUT** as needed, saving to `./tools/reports/`
- **RE-EVALUATE** problems from first principles if issues persist

### 2.4 SCRIPT LIMITATIONS & ESCALATION — **📢 IMMEDIATE REPORTING**

- **IDENTIFY SCRIPT LIMITATIONS** promptly — escalate to user with full context when unresolved
- **DOCUMENT ISSUES** in `llm-reports/`
- **FACT-CHECK ALL RESULTS** — success declarations based solely on exit codes are 🚫 **PROHIBITED**

## 3. CODE AND SCRIPT IMPLEMENTATION — **⚙️ MANDATORY SCRIPTING**

### 3.1 RELENTLESS AUTOMATION — **🤖 NO MANUAL REPETITION**

- **ULTRATHINK** and think like a programmer for every task
- **USE SEQUENTIAL THINKING MCP TOOL** (`sequential-thinking`) for all planning and execution
- **AUTOMATE ALL REPETITIVE TASKS** — manual repetition is 🚫 **FORBIDDEN** unless automation impossible
- **DEVELOP** robust, configurable, well-logged scripts

### 3.2 EXECUTION WORKFLOW — **📋 MANDATORY SEQUENCE**

1. **PERFORM DRY RUN** (`--dry-run`) before any live modification
2. **REVIEW DRY-RUN OUTPUT** for accuracy and compliance
3. **RUN ON SMALL SUBSET** first, then scale globally
4. **EXECUTE LIVE RUN** only after successful verification
5. **REDIRECT ALL OUTPUTS** to `./tools/reports/`

### 3.3 LOGGING & VERIFICATION — **📊 COMPREHENSIVE TRACKING**

- **IMPLEMENT COMPREHENSIVE LOGGING**: 
  • Files processed
  • Actions taken
  • Exact changes
  • Errors/warnings
  • Summary statistics
- **REVIEW LOGS IMMEDIATELY** after each run
- **MANUALLY SPOT-CHECK 50%** (or risk-based sample) of modified items
- **SAVE LOGS** with timestamped filenames in `./tools/reports/`

## 4. VERSION CONTROL & CHANGE MANAGEMENT — **🔄 SYSTEMATIC CONTROL**

### 4.1 Version Control Protocols — **🌿 DEVIATION FROM THIS PROTOCOL WILL RESULT IN SEVERE DISCIPLINARY ACTION**

- **Branch Strategy**: Feature branches only; no direct main commits; descriptive branch names
- **Merge Policy**: **NO PUSH OR MERGE UNLESS EXPLICITLY INSTRUCTED**

### 4.2 Change Management

- **ALL MAJOR Updates**: Must maintain backward compatibility; migration scripts required
- **Tool Changes**: Dry run validation required; rollback plan mandatory

## 5. SUCCESS METRICS & QUALITY ASSURANCE — **📏 PERFECTION STANDARD**

### 5.1 Completion Success Metric — **🎯 ABSOLUTE STANDARD**

**THE ONLY RECOGNIZED COMPLETION SUCCESS METRIC IS TRUE 100% ACCURATE EXECUTION. *Perfection is the ONLY acceptable outcome.* No partial completion, no 'good enough', no approximations — either 100% correct or incomplete.**

### 5.2 COMMUNICATION & DOCUMENTATION — **📝 ENTERPRISE STANDARDS**

#### 5.2.1 Professional Conduct — **⭐ EXCEPTIONAL STANDARDS ONLY**

- **MAINTAIN EXCEPTIONAL WORK ETHIC** — shortcuts compromising quality result in 🚨 **CORRECTIVE MEASURES**
- **LEARN AND CORRECT** mistakes immediately
- **COMMUNICATE** plans, actions, results clearly — independent verification mandatory

#### 5.2.2 Session Documentation Protocol — **📋 STRUCTURED REPORTING**

- **CREATE/UPDATE** session summary reports consistently
- **❗ MAINTAIN ONE SUMMARY ❗** per calendar day using format `summary-report-yyyymmdd-hhmm.md`
  • Search `llm-reports/` directory first for the day summary report
  • Create new if none exists for the day
  • Update existing if found the day summary report
- **UPDATE CONTINUOUSLY** as understanding evolves
- **SINGLE SUMMARY POLICY** — multiple files result in 🚫 **POLICY VIOLATION**
- **MUST BE** concise, structured, technically focused
- **APPEND TIMESTAMP** after each update

## 6. AUDIT COMPLIANCE & QUALITY ASSURANCE — **🛡️ ENTERPRISE-GRADE STANDARDS**

> **CRITICAL REQUIREMENT:** ALL software modifications, documentation deliverables, technical artifacts, and project activities **MUST** adhere to enterprise-grade QA standards, maintain comprehensive audit trails, and include thorough version control commit annotations for regulatory compliance review.

### 6.1 AUDIT COMPLIANCE — **📋 COMPLETE TRACEABILITY**

- **ALL RESPONSES** will be verified by audit team
- **DEVIATIONS** result in corrective action protocols
- **MAINTAIN** comprehensive audit trails for all activities

### 6.2 PATH REFERENCES — **📂 REPOSITORY-RELATIVE ONLY**

- **ALL PATHS** relative to repository root
- **ABSOLUTE PATHS** are 🚫 **PROHIBITED**

***ALL PATHS PROVIDED ARE RELATIVE TO THE ROOT OF THE REPOSITORY.***

***THE SEVEN FOUNDATIONAL PRINCIPLES ARE THE SUPREME GOVERNING FRAMEWORK FOR ALL OPERATIONS. VIOLATIONS TRIGGER IMMEDIATE CORRECTIVE ACTION.***
