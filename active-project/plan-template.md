# Project Execution Plan

⬜ ## PROJECT OVERVIEW

[Brief Description: Purpose, Scope, and Outcome]

---

⬜ ## PHASE P: [Title Message] (P=0)
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P.S]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO ONE LEVEL UP]

⬜ ### STEP P.S: [Title Message] (S=1)
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P.S.T]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO ONE LEVEL UP]

⬜ #### TASK P.S.T: [Title Message] (T=1)
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P.S.T.U]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO ONE LEVEL UP]

⬜ ##### SUBTASK P.S.T.U: [Title Message] (U=1)
- [IF SUBLEVEL = TRUE: Brief Description: Purpose, Scope, and Outcome & GOTO P.S.T.U.A]
- [IF SUBLEVEL = FALSE: 🎬 Actionable Instruction THEN GOTO ONE LEVEL UP]

⬜ ###### ACTION P.S.T.U.A: [Title Message] (A=1)
- 🎬 [ATOMIC ACTIONABLE INSTRUCTION THEN GOTO ONE LEVEL UP]

⬜ **🏁 STEP P.S EXIT CONDITIONS**: [Overall Completion Criteria] (C=1)
⬜ **CONDITION C**: [Specific Completion Criteria]
- [IF CONDITIONS = TRUE: GOTO CONDITION C+1; ELSE: GOTO ONE LEVEL UP]

⬜ **🏁 PHASE P EXIT CONDITIONS**: [Overall Completion Criteria] (C=1)
⬜ **CONDITION C**: [Specific Completion Criteria]
- [IF CONDITIONS = TRUE: GOTO CONDITION C+1; ELSE: GOTO ONE LEVEL UP]

---

⬜ **🏁 PROJECT EXIT CONDITIONS**: [Final Completion Criteria for Entire Project] (C=1)
⬜ **CONDITION C**: [Specific Completion Criteria]
- [IF CONDITIONS = TRUE: GOTO CONDITION C+1; ELSE: GOTO TOP]

---

## 📋 STATUS LEGEND
⬜ **NOT STARTED**
🔄 **IN PROGRESS**
✅ **COMPLETED**

---

# 📚 TEMPLATE USAGE GUIDE

## 🔢 Formula Variables System

**Variables (each resets when parent changes):**
- **P** = Phase counter (0,1,2,3,4... resets only for new projects)
- **S** = Step counter (1,2,3,4... resets for each new phase P)
- **T** = Task counter (1,2,3,4... resets for each new step P.S)
- **U** = Subtask counter (1,2,3,4... resets for each new task P.S.T)
- **A** = Action counter (1,2,3,4... resets for each new subtask P.S.T.U)
- **C** = Condition counter (1,2,3,4... resets for each new exit condition block)

## 🔄 Loop Control Logic

**COUNTER**: Each variable increments (+1) when creating new items at same level
**RESET**: Child variables reset to 1 when parent level changes
**GOTO TOP**: After project completion, return to start for new projects
**GOTO ONE LEVEL UP**: After item completion, return to parent level
**GOTO NEXT**: Move to next item at same level (counter +1)

## 📋 Formula Logic Example

```
Starting: P=0, S=1, T=1, U=1, A=1, C=1

PHASE 1 (P=0+1=1): Project Setup
├── STEP 1.1 (S=1): Research Phase
│   ├── TASK 1.1.1 (T=1): Market Analysis
│   │   ├── SUBTASK 1.1.1.1 (U=1): Competitor Research
│   │   │   ├── ACTION 1.1.1.1.1 (A=1): Google search → GOTO ONE LEVEL UP
│   │   │   └── ACTION 1.1.1.1.2 (A=1+1=2): Document findings → GOTO ONE LEVEL UP
│   │   └── SUBTASK 1.1.1.2 (U=1+1=2, A resets to 1): Price Analysis
│   └── TASK 1.1.2 (T=1+1=2, U resets to 1): User Surveys
├── STEP 1.2 (S=1+1=2, T resets to 1): Planning Phase

PHASE 2 (P=1+1=2, S resets to 1): Development
├── STEP 2.1 (S=1): Design
│   ├── TASK 2.1.1 (T=1): Wireframes
│   └── TASK 2.1.2 (T=1+1=2): Prototypes
```

## 🧠 IF-ELSE Logic Explanation

**SUBLEVEL = TRUE**: Item has children beneath it
- Add brief description
- GOTO next level down (P.S, P.S.T, etc.)

**SUBLEVEL = FALSE**: Item is terminal (no children)  
- Use 🎬 actionable instruction
- THEN GOTO ONE LEVEL UP

**CONDITIONS = TRUE**: More conditions to check
- GOTO CONDITION C+1

**CONDITIONS = FALSE**: All conditions satisfied
- GOTO ONE LEVEL UP (or GOTO TOP if project complete)

## 🏗️ Template Expansion Rules

1. **Copy Template Block**: Copy the formula pattern
2. **Increment Variables**: P+1, S+1, T+1, U+1, A+1, C+1
3. **Reset Dependent Variables**: When P changes, S→1; when S changes, T→1; etc.
4. **Apply IF-ELSE Logic**: Determine if SUBLEVEL=TRUE or FALSE
5. **Set Exit Conditions**: Only at STEP and PHASE levels
6. **Follow GOTO Logic**: Navigate between levels using loop control

## 🎯 Precision Control

- **High Precision**: Break down to ACTION level (A variables)
- **Medium Precision**: Stop at TASK or SUBTASK level (T or U variables)
- **Low Precision**: Stop at STEP level (S variables)

---

**🚨 CRITICAL**: This formula-driven template expands mathematically using P.S.T.U.A.C variables with IF-ELSE conditional logic, COUNTER/RESET mechanisms, and GOTO flow control for infinite scalability and precision control.
