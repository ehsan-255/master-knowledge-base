---
title: PROJECT EXECUTION ROADMAP TEMPLATE
description: MANDATORY template for creating project execution roadmaps with standardized
  structure and terminology
version: '2.0'
created: '2025-06-12'
last_modified: '2025-06-12'
template_type: roadmap
status: active
compliance_level: mandatory
author: Master Knowledge Base System
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
- mandatory
- project-execution
- roadmap
- template
info-type: general
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:12Z'
kb-id: active-project
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# PROJECT EXECUTION ROADMAP TEMPLATE

>**THE TEMPLATE AND THE TEMPLATE-POPULATION GUIDELINES **MUST** BE USED TO GENERATE THE ACTUAL PROJECT EXECUTION ROADMAP**

>**TO POPULATE THE *1. TEMPLATE*, **FOLLOW** THE *2. TEMPLATE-POPULATION GUIDELINES* BELOW**

>****REMEMBER** TO ADD THE *📋 EXECUTION-SPECIFIC TEXT BLOCKS* TO THE BEGINNING AND END OF EVERY POPULATED ROADMAP**

---

## **1. TEMPLATE**

```
# PROJECT EXECUTION ROADMAP

## PROJECT OVERVIEW

[Brief Description: Purpose, Scope, and Outcome]

---

## PHASE P1: [Title Message]
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P1.S]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO NEXT]

---

**🏁 PHASE P1 EXIT CONDITIONS**: [End of Phase P1 Completion Criteria]
**CONDITION C1**: [Specific Completion Criteria]
- [IF CONDITIONS = TRUE: GOTO CONDITION C+1; ELSE: GOTO ONE LEVEL UP]

---

### P1.1: [Title Message]
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P1.1.1]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO NEXT]

---

**🏁 P1.1 EXIT CONDITIONS**: [Overall Completion Criteria]
**CONDITION C1**: [Specific Completion Criteria]
- [IF CONDITIONS = TRUE: GOTO CONDITION C+1; ELSE: GOTO ONE LEVEL UP]

---

#### P1.1.1: [Title Message]
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P1.1.1.1]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO NEXT]

##### P1.1.1.1: [Title Message]
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P1.1.1.1.1]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO NEXT]

###### P1.1.1.1.1: [Title Message]
- 🎬 [ATOMIC ACTIONABLE INSTRUCTION THEN GOTO NEXT]

---

**🏁 PROJECT EXIT CONDITIONS**: [Final Completion Criteria for Entire Project]
**CONDITION C1**: [Specific Completion Criteria]
- [IF CONDITIONS = TRUE: GOTO CONDITION C+1; ELSE: GOTO TOP]

---

```

---

## **2. TEMPLATE-POPULATION GUIDELINES**

>**BELOW ARE THE **MANDATORY** GUIDELINES TO POPULATE THE "1. TEMPLATE"**

### **📂 ROADMAP NAMING CONVENTION — STRICT COMPLIANCE**

**FILE NAME FORMAT**: `[job-description]-roadmap.md`
- **USE 1-3 WORDS** describing the job/project in kebab-case
- **EXAMPLES**: `database-migration-roadmap.md`, `api-redesign-roadmap.md`, `user-auth-roadmap.md`
- **ALWAYS END WITH** `-roadmap.md`

---

### **🎯 DECOMPOSITION STRATEGY — MANDATORY IMPLEMENTATION**

>**IN ORDER TO GENERATE ANY SIMPLE STEP-BY-STEP PLAN OR A COMPLEX MULTI-LAYERED ROADMAP, THE WORK **MUST** BE DECOMPOSED OR BROKEN DOWN INTO SMALLER PARTS**

---

#### **💣 DECOMPOSITION LEVELS**

##### **A. Highest Precision & Predictability — MAXIMUM CONTROL**
- **BREAK DOWN TO P1.1.1.1.1 LEVEL** (🎬 emoji)
- **USE WHEN**: Complex technical work, critical systems, regulatory compliance
- **BENEFITS**: Predictable outcomes, reduced errors, clear accountability
- **🚨 CRITICAL**: Exit conditions are **MANDATORY** for this level
- **📋 CHECKLIST**: Separate progress checklist is **ABSOLUTELY MANDATORY** for this level

##### **B. Highest Flexibility & Creativity — MAXIMUM ADAPTABILITY**
- **DO NOT BREAK DOWN AT ALL** (or maybe break down to **P1.1 level**)
- **USE WHEN**: Research, design, strategic planning, innovation, creative work, etc.
- **BENEFITS**: Flexibility, creative freedom, adaptive execution, etc.
- Most plans **WILL NOT NEED** exit conditions for this level
- **📋 CHECKLIST**: Separate progress checklist is **MANDATORY** for this level

##### **C. Balanced Approach — STANDARD IMPLEMENTATION**
- **BREAK DOWN TO P1.1.1 OR P1.1.1.1 LEVEL** (or even P1.1 level)
- **USE WHEN**: Most projects fall in this category, where precision and predictability are required, but in moderation
- Exit conditions are **HIGHLY RECOMMENDED** for this level
- **📋 CHECKLIST**: Separate progress checklist is **MANDATORY** for this level

>**USE CHECKLIST TEMPLATE: `roadmap-checklist-template.md` TO GENERATE THE CHECKLIST — THIS IS **MANDATORY** FOR ALL ROADMAPS**

---

#### **🏁 EXIT CONDITIONS GUIDELINES — MANDATORY IMPLEMENTATION**

>**FOR COMPLEX, LONG-RUNNING, AND MULTI-LAYERED ROADMAPS, IT IS **MANDATORY** TO IMPLEMENT EXIT CONDITIONS THROUGHOUT THE ROADMAP LEVELS TO DEFINE RELIABLE COMPLETION CHECKPOINTS**

##### **PROJECT LEVEL — ABSOLUTE REQUIREMENTS**
- Overall success criteria
- Deliverable acceptance criteria
- Stakeholder approval requirements

##### **PHASE LEVEL — CRITICAL CHECKPOINTS**
- Major milestone achievements
- Quality gates passed
- Dependencies satisfied for next phase

##### **P1.1 LEVEL — OPERATIONAL VALIDATION**
- Specific output produced
- Validation criteria met
- Handoff requirements satisfied

---

### **👍🏼 BEST PRACTICES — MANDATORY COMPLIANCE**

- **START** with high-level phases, decompose as needed
- **USE** consistent terminology (Phase for highest level, numerical designations for all sub-levels)
- **BALANCE** predictability of outcome with flexibility and creativity in planning and execution based on the project type:
   - **For More Predictability**: Break down more (all the way to P1.1.1.1.1 level)
   - **For More Flexibility**: Break down less (to P1.1.1 or P1.1.1.1 level)
   - **For a Basic Step-By-Step Plan**: Don't break down at all (or break down to P1.1 level)
- **IMPLEMENT** regular checkpoint reviews at exit conditions
   - Exit conditions are **HIGHLY RECOMMENDED** for optimal project control

---

### **🔄 PROGRESS TRACKER AND CHECKLIST TEMPLATES — MANDATORY USAGE**

>**USE PROGRESS TRACKER TEMPLATE: `roadmap-progress-tracker-template.md` TO GENERATE THE PROGRESS TRACKER**
>**USE CHECKLIST TEMPLATE: `roadmap-checklist-template.md` TO GENERATE THE CHECKLIST — **MANDATORY** FOR ALL ROADMAPS**

---

### **🚦 COORDINATION — STRICT PROTOCOL**
- **THIS ROADMAP** remains the authoritative source for execution instructions
- **CHECKLIST** is for quick status updates and brief notes — **MANDATORY** for all roadmaps
- **PROGRESS TRACKER** is for detailed completion documentation

>**NO OTHER REPORTING, TRACKING, OR DOCUMENTATION IS REQUIRED FOR A ROADMAP**

---

### **📋 EXECUTION-SPECIFIC TEXT BLOCKS — MANDATORY IMPLEMENTATION**

>**BELOW ARE THE TEXT BLOCKS **REQUIRED** FOR EACH ROADMAP LEVEL DURING THE EXECUTION STAGE. THEY ARE INSTRUCTIONS WHICH **MUST** BE FOLLOWED DURING THE EXECUTION STAGE. ADD THEM TO THE BEGINNING AND END OF EVERY POPULATED ROADMAP**

>**APPLY MINOR ADJUSTMENTS TO THE TEXT BLOCKS ONLY IF THEY IMPROVE THE EXECUTION PROCESS, *e.g. IF THE CHECKLIST IS NOT APPLICABLE, REMOVE THE CHECKLIST TEXT BLOCK***


**ADD THIS SECTION (which is delimited by '```') TO THE BEGINNING OF EVERY POPULATED ROADMAP (without '```')**
```
>**THE "*🚨 MANDATORY* ROADMAP PROGRESS MANAGEMENT PROTOCOL" **MUST** BE FOLLOWED AND UPDATED AT ALL TIMES TO ENSURE THE PROGRESS IS ACTIVELY TRACKED AND WORK CAN BE RESUMED FROM THE SAME POINT WITHOUT CAUSING ANY CONFUSION AND REDUNDANCY, THE PROGRESS **MUST** BE UPDATED CONTINUOUSLY WITHOUT ANY EXCEPTION**

>**UPDATE THE CHECKLIST CONTINUOUSLY AT ALL TIMES WITHOUT ANY EXCEPTION — CHECKLIST GENERATION IS **MANDATORY** FOR ALL ROADMAPS**

```

---

**ADD THIS SECTION (which is delimited by '```') TO THE END OF EVERY POPULATED ROADMAP (without '```')**

```

---

## EXECUTION PROTOCOL — MANDATORY COMPLIANCE

### **SEQUENTIAL PROGRESSION — STRICT ORDER**
- **EXECUTE** tasks in the exact sequence specified
- **COMPLETE** each phase before proceeding to the next
- **VALIDATE** exit conditions before progression
- **DOCUMENT** all deviations and justifications

### **PROGRESS MANAGEMENT — CONTINUOUS REQUIREMENT**
- **UPDATE** checklist status continuously
- **MAINTAIN** progress tracker with detailed entries
- **ESCALATE** blocked items immediately
- **COORDINATE** with all stakeholders on status changes

### **QUALITY ASSURANCE — NON-NEGOTIABLE**
- **VERIFY** completion criteria for each deliverable
- **CONDUCT** quality reviews at designated checkpoints
- **IMPLEMENT** corrective actions for any deficiencies
- **OBTAIN** formal approval before phase completion

---

```
