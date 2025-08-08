---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:12Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: archive
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# PROJECT EXECUTION ROADMAP TEMPLATE

>**THE TEMPLATE AND THE TEMPLATE-POPULATION GUIDELINES ARE TO BE USED TO GENERATE THE ACTUAL PROJECT EXECUTION ROADMAP**

>**TO POPULATE THE *1. TEMPLATE*, FOLLOW THE *2. TEMPLATE-POPULATION GUIDELINES* BELOW**

>**REMEMBER TO ADD THE *📋 EXECUTION-SPECIFIC TEXT BLOCKS* TO THE BEGINNING AND END OF EVERY POPULATED ROADMAP**

---

## **1. TEMPLATE**

```
# PROJECT EXECUTION ROADMAP

⬜ ## PROJECT OVERVIEW

[Brief Description: Purpose, Scope, and Outcome]

---

⬜ ## PHASE P: [Title Message] (P=0)
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P.S]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO NEXT]

---

⬜ **🏁 PHASE P EXIT CONDITIONS**: [End of Phase P Completion Criteria] (C=1)
⬜ **CONDITION C**: [Specific Completion Criteria]
- [IF CONDITIONS = TRUE: GOTO CONDITION C+1; ELSE: GOTO ONE LEVEL UP]

---

⬜ ### STEP P.S: [Title Message] (S=1)
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P.S.T]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO NEXT]

---

⬜ **🏁 STEP P.S EXIT CONDITIONS**: [Overall Completion Criteria] (C=1)
⬜ **CONDITION C**: [Specific Completion Criteria]
- [IF CONDITIONS = TRUE: GOTO CONDITION C+1; ELSE: GOTO ONE LEVEL UP]

---

⬜ #### TASK P.S.T: [Title Message] (T=1)
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P.S.T.U]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO NEXT]

⬜ ##### SUBTASK P.S.T.U: [Title Message] (U=1)
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P.S.T.U.A]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO NEXT]

⬜ ###### ACTION P.S.T.U.A: [Title Message] (A=1)
- 🎬 [ATOMIC ACTIONABLE INSTRUCTION THEN GOTO NEXT]

---

⬜ **🏁 PROJECT EXIT CONDITIONS**: [Final Completion Criteria for Entire Project] (C=1)
⬜ **CONDITION C**: [Specific Completion Criteria]
- [IF CONDITIONS = TRUE: GOTO CONDITION C+1; ELSE: GOTO TOP]

---

```

---

## **2. TEMPLATE-POPULATION GUIDELINES**

>**BELOW ARE THE GUIDELINES TO POPULATE THE "1. TEMPLATE"**

### **📂 ROADMAP NAMING CONVENTION**

**FILE NAME FORMAT**: `[job-description]-roadmap.md`
- **Use 1-3 words** describing the job/project in kebab-case
- **Examples**: `database-migration-roadmap.md`, `api-redesign-roadmap.md`, `user-auth-roadmap.md`
- **Always end with** `-roadmap.md`

---

### **🎯 DECOMPOSITION STRATEGY**

>**IN ORDER TO GENERATE ANY SIMPLE STEP-BY-STEP PLAN OR A COMPLEX MULTI-LAYERED ROADMAP, THE WORK HAS TO BE DECOMPOSED OR BROKEN DOWN INTO SMALLER PARTS**

---

#### **💣 DECOMPOSITION LEVELS**

##### **A. Highest Precision & Predictability**
- Break down to **ACTION level** (🎬 emoji)
- Use when: Complex technical work, critical systems, regulatory compliance
- Benefits: Predictable outcomes, reduced errors, clear accountability
- **🚨 CRITICAL**: Exit conditions are mandatory for this level
- **📋 CHECKLIST**: Separate progress checklist is **MANDATORY** for this level

##### **B. Highest Flexibility & Creativity**
- **Don't** break down at all (or maybe break down to **STEP level**)
- Use when: Research, design, strategic planning, innovation, creative work, etc.
- Benefits: Flexibility, creative freedom, adaptive execution, etc.
- Most plans will not need exit conditions for this level
- **📋 CHECKLIST**: Separate progress checklist **MOST LIKELY NOT NEEDED** for this level

##### **C. Balanced Approach**
- Break down to **TASK or SUBTASK level (or even STEP level)**
- Use when: Most projects fall in this category, where precision and predictability are required, but in moderation
- Exit conditions are **HIGHLY RECOMMENDED** for this level
- **📋 CHECKLIST**: Separate progress checklist is **HIGHLY RECOMMENDED** for this level

>**USE CHECKLIST TEMPLATE: `roadmap-checklist-template.md` TO GENERATE THE CHECKLIST**

---

#### **🏁 EXIT CONDITIONS GUIDELINES**

>**FOR COMPLEX, LONG-RUNNING, AND MULTI-LAYERED ROADMAPS, IT IS HIGHLY RECOMMENDED TO IMPLEMENT EXIT CONDITIONS THROUGHOUT THE ROADMAP LEVELS TO DEFINE RELIABLE COMPLETION CHECKPOINTS**

##### **PROJECT LEVEL**
- Overall success criteria
- Deliverable acceptance criteria
- Stakeholder approval requirements

##### **PHASE LEVEL**
- Major milestone achievements
- Quality gates passed
- Dependencies satisfied for next phase

##### **STEP LEVEL**
- Specific output produced
- Validation criteria met
- Handoff requirements satisfied

---

### **👍🏼 BEST PRACTICES**

- Start with high-level phases, decompose as needed
- Use consistent terminology (Phase/Step/Task/Subtask/Action)
- Balance predictability of outcome with flexibility and creativity in planning and execution based on the project type:
   - For More Predictability: Break down more (all the way to ACTION level)
   - For More Flexibility: Break down less (to TASK or SUBTASK level)
   - For a Basic Step-By-Step Plan: Don't break down at all (or break down to STEP level)
- Regular checkpoint reviews at exit conditions
   - Exit conditions are not mandatory, but highly recommended

---

### **🔄 PROGRESS TRACKER AND CHECKLIST TEMPLATES**

>**USE PROGRESS TRACKER TEMPLATE: `roadmap-progress-tracker-template.md` TO GENERATE THE PROGRESS TRACKER**
>**USE CHECKLIST TEMPLATE: `roadmap-checklist-template.md` TO GENERATE THE CHECKLIST.** *APPLIED TO (OPTION A) & (OPTION C) IN **💣 DECOMPOSITION LEVELS***

---

### **🚦 COORDINATION**
- **This roadmap** remains the authoritative source for execution instructions
- **Checklist** is for quick status updates and brief notes. *applicable to (OPTION A) & (OPTION C) in **💣 DECOMPOSITION LEVELS***
- **Progress tracker** is for detailed completion documentation

>**NO OTHER REPORTING, TRACKING, OR DOCUMENTATION IS REQUIRED FOR A ROADMAP**

---

### **📋 EXECUTION-SPECIFIC TEXT BLOCKS**

>**BELOW ARE THE TEXT BLOCKS REQUIRED FOR EACH ROADMAP LEVEL DURING THE EXECUTION STAGE. THEY ARE INSTRUCTIONS WHICH ARE NEEDED TO BE FOLLOWED DURING THE EXECUTION STAGE. ADD THEM TO THE BEGINNING AND END OF EVERY POPULATED ROADMAP**

>**APPLY MINOR ADJUSTMENTS TO THE TEXT BLOCKS ONLY IF THEY IMPROVE THE EXECUTION PROCESS, *e.g. IF THE CHECKLIST IS NOT APPLICABLE, REMOVE THE CHECKLIST TEXT BLOCK***


**ADD THIS SECTION (which is delimited by '```') TO THE BEGINNING OF EVERY POPULATED ROADMAP (without '```')**
```
>**THE "*🚨 MANDATORY* ROADMAP PROGRESS MANAGEMENT PROTOCOL" *MUST* BE FOLLOWED AND UPDATED AT ALL TIMES TO ENSURE THE PROGRESS IS ACTIVELY TRACKED AND WORK CAN BE RESUMED FROM THE SAME POINT WITHOUT CAUSING ANY CONFUSION AND REDUNDANCY, THE PROGRESS MUST BE UPDATED CONTINUOUSLY WITHOUT ANY EXCEPTION**

>**UPDATE THE CHECKLIST CONTINUOUSLY AT ALL TIMES WITHOUT ANY EXCEPTION**

```

---

**ADD THIS SECTION (which is delimited by '```') TO THE END OF EVERY POPULATED ROADMAP (without '```')**

```

---

## STATUS LEGEND

⬜ **NOT STARTED**
🔄 **IN PROGRESS**
✅ **COMPLETED**
❌ **BLOCKED**

**NOTE:** ***🔄 IN PROGRESS and ❌ BLOCKED statuses must be applied to all the affected parent branches all the way up to the project level***

---

## EXECUTION PROTOCOL

### **SEQUENTIAL PROGRESSION**

- **PHASES**: Must complete 1 → 2 → 3...
- **STEPS**: Must complete 1.1 → 1.2 → 1.3...
- **TASKS**: Must complete 1.1.1 → 1.1.2 → 1.1.3...
- **NO PARALLEL EXECUTION** unless explicitly planned

### **COMPLETION STANDARDS**

- **100% COMPLETION REQUIRED** before advancing
- **ZERO TOLERANCE** for partial completion
- **EXIT CONDITIONS** must be verified and checked off

### **BLOCKED PROGRESS PROTOCOL**
If progress is blocked,

1. **TAKE A STEP BACK**, review and analyze the plan from a different perspective, then craft an alternative strategy and try again. IF resolved, continue, ELSE, GOTO 2
2. **GO BACKWARDS STEP BY STEP**, review and analyze the plan meticulously at each step, and try to identify the flaw in the plan or where the problem was introduced (go back until the previous 100% checkpoint)
2.1 **IF A SOLUTION IS FOUND**, apply and continue
2.2 **ELSE IF NO SOLUTION IS FOUND**, mark the plan as **❌ BLOCKED** and execute the **FAILURE PROTOCOL**

### **FAILURE PROTOCOL**
If progress is blocked,

1. **IMMEDIATELY STOP** all progression
2. **DOCUMENT** blocking issue with specific details
2.1 **ADD** a one-liner note to the plan
2.2 **UPDATE** the progress report with specific details
2.3 **ENSURE** the specific item and all the affected parent branches are marked as **❌ BLOCKED**

## **🚨 MANDATORY** ROADMAP PROGRESS MANAGEMENT PROTOCOL

>**THIS PROTOCOL IS *MANDATORY* AND *MUST* BE FOLLOWED AT ALL TIMES**

### **PROGRESS TRACKING OPTIONS**

#### **OPTION A: DIRECT ROADMAP UPDATES** (for shorter roadmaps)
- **UPDATE** status checkboxes continuously in the roadmap
- **ADD** one-liner notes directly to roadmap items for important points
- **MAINTAIN** separate detailed progress tracker document

#### **OPTION B: SEPARATE PROGRESS CHECKLIST** (for longer roadmaps)
- **GENERATE** separate progress checklist file with tree-structure matching roadmap ToC
- **UPDATE** status checkboxes in the separate checklist
- **ADD** one-liner notes to the checklist items (NOT the roadmap)
- **MAINTAIN** separate detailed progress tracker document

### **MANDATORY UPDATES**

1. **STATUS TRACKING**: Update checkboxes continuously (refer to status legend)
2. **ONE-LINER NOTES**: Add important execution points (roadmap OR checklist based on option chosen)
3. **DETAILED PROGRESS**: Update progress tracker document after each completion

---

```
