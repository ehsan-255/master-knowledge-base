# PROJECT EXECUTION ROADMAP PROGRESS TRACKER TEMPLATE

>**THIS TEMPLATE IS FOR CONTINUOUS PROGRESS TRACKING THROUGHOUT PROJECT EXECUTION**

>**CHOOSE ONE OF THE *3 COMPLEXITY LEVELS* BASED ON YOUR ROADMAP DECOMPOSITION LEVEL**

>**TO POPULATE THE CHOSEN TEMPLATE, FOLLOW THE *TEMPLATE-POPULATION GUIDELINES* BELOW**

---

## **🔍 COMPLEXITY LEVEL SELECTION**

### **BASIC TRACKER** (for Highest Flexibility & Creativity roadmaps)
- Use when: Research, design, strategic planning, innovation
- Roadmap breakdown: STEP level or no breakdown
- Features: Simple completion log with timestamps

### **STANDARD TRACKER** (for Balanced Approach roadmaps)  
- Use when: Most standard projects with moderate complexity
- Roadmap breakdown: TASK or SUBTASK level
- Features: Completion log + execution timeline + progress metrics

### **COMPREHENSIVE TRACKER** (for Highest Precision & Predictability roadmaps)
- Use when: Complex technical work, critical systems, regulatory compliance
- Roadmap breakdown: ACTION level
- Features: Detailed progress entries + execution timeline + comprehensive metrics

---

## **1. BASIC TRACKER TEMPLATE**

```
# PROJECT EXECUTION PROGRESS TRACKER - BASIC

**Project**: [Project Name]
**Started**: [YYYYMMDD-HHMM]
**Status**: [NOT STARTED/IN PROGRESS/COMPLETED/BLOCKED]
**Last Updated**: [YYYYMMDD-HHMM]

---

## **📝 COMPLETION LOG**

### **[YYYYMMDD-HHMM]** | **[Item ID]**: [Item Title]
**Status**: [COMPLETED/BLOCKED]
**Duration**: [X minutes/hours]
**Outcome**: [Brief description of what was accomplished]

---

## **🚨 ISSUE TRACKING** (Only used when BLOCKED status occurs)

### **Issue [#]**: [Issue Title] 
**Identified**: [YYYYMMDD-HHMM]
**Status**: [OPEN/RESOLVED]
**Description**: [What is blocking progress]
**Resolution**: [How it was resolved]
**Resolved**: [YYYYMMDD-HHMM]

---

```

---

## **2. STANDARD TRACKER TEMPLATE**

```
# PROJECT EXECUTION PROGRESS TRACKER - STANDARD

**Project**: [Project Name]
**Started**: [YYYYMMDD-HHMM]
**Status**: [NOT STARTED/IN PROGRESS/COMPLETED/BLOCKED]
**Last Updated**: [YYYYMMDD-HHMM]

---

## **⏱️ EXECUTION TIMELINE**

| **Item ID** | **Item Title** | **Start** | **Complete** | **Duration** | **Status** |
|-------------|----------------|-----------|--------------|--------------|------------|
| [ID]        | [Title]        | [YYYYMMDD-HHMM] | [YYYYMMDD-HHMM] | [X min/hr] | [Status] |

---

## **📝 COMPLETION LOG**

### **[YYYYMMDD-HHMM]** | **[Item ID]**: [Item Title]
**Status**: [COMPLETED/BLOCKED]
**Duration**: [X minutes/hours]
**Outcome**: [Brief description of what was accomplished]
**Notes**: [Any important execution points or decisions made]

---

## **📊 PROGRESS METRICS**

**Total Items**: [Number]
**Completed**: [Number] ([Percentage]%)
**In Progress**: [Number]
**Blocked**: [Number]
**Average Duration**: [X minutes/hours per item]

---

## **🚨 ISSUE TRACKING** (Only used when BLOCKED status occurs)

### **Issue [#]**: [Issue Title]
**Identified**: [YYYYMMDD-HHMM]
**Status**: [OPEN/RESOLVED]
**Description**: [What is blocking progress]
**Impact**: [How this affects project execution]
**Resolution**: [How it was resolved]
**Resolved**: [YYYYMMDD-HHMM]

---

```

---

## **3. COMPREHENSIVE TRACKER TEMPLATE**

```
# PROJECT EXECUTION PROGRESS TRACKER - COMPREHENSIVE

**Project**: [Project Name]
**Started**: [YYYYMMDD-HHMM]
**Status**: [NOT STARTED/IN PROGRESS/COMPLETED/BLOCKED]
**Last Updated**: [YYYYMMDD-HHMM]

---

## **⏱️ EXECUTION TIMELINE**

| **Item ID** | **Item Title** | **Start** | **Complete** | **Duration** | **Status** |
|-------------|----------------|-----------|--------------|--------------|------------|
| [ID]        | [Title]        | [YYYYMMDD-HHMM] | [YYYYMMDD-HHMM] | [X min/hr] | [Status] |

---

## **📝 DETAILED PROGRESS ENTRIES**

### **Entry [#]**: **[YYYYMMDD-HHMM]** | **[Item ID]**: [Item Title]
**Status**: [COMPLETED/BLOCKED]
**Duration**: [X minutes/hours]

#### **🎯 What Was Done**
[Specific actions taken and work performed]

#### **📊 Outcome**
[Results achieved, deliverables produced]

#### **💡 Notes**
[Important decisions, lessons learned, key insights]

---

## **📊 COMPREHENSIVE METRICS**

**Total Items**: [Number]
**Completed**: [Number] ([Percentage]%)
**In Progress**: [Number]
**Blocked**: [Number]
**Average Duration**: [X minutes/hours per item]
**Total Execution Time**: [X hours/days]
**Efficiency**: [Items completed per hour/day]

---

## **🚨 ISSUE TRACKING** (Only used when BLOCKED status occurs)

### **Issue [#]**: [Issue Title]
**Identified**: [YYYYMMDD-HHMM]
**Severity**: [LOW/MEDIUM/HIGH/CRITICAL]
**Status**: [OPEN/IN PROGRESS/RESOLVED]
**Affected Items**: [List of blocked roadmap items]

#### **🔍 Description**
[Detailed description of the blocking issue]

#### **📈 Impact**
[How this affects project timeline and execution]

#### **🛠️ Resolution**
[Actions taken to resolve the issue]
**Resolved**: [YYYYMMDD-HHMM]

---

```

---

## **📋 TEMPLATE-POPULATION GUIDELINES**

### **📂 PROGRESS TRACKER NAMING CONVENTION**

**FILE NAME FORMAT**: `[job-description]-progress-tracker.md`
- **Use same 1-2 words** from the corresponding roadmap filename
- **Examples**: `database-migration-progress-tracker.md`, `api-redesign-progress-tracker.md`, `user-auth-progress-tracker.md`
- **Always end with** `-progress-tracker.md`

---

### **🚨 MANDATORY TIMESTAMP REQUIREMENTS**

#### **TIMESTAMP FORMAT**: **YYYYMMDD-HHMM** (NO DEVIATIONS ALLOWED)
- **Example**: 20241205-1430 (December 5, 2024 at 2:30 PM)
- **System Extraction**: ALWAYS extract current timestamp from system using terminal commands
- **Terminal Command**: `date +"%Y%m%d-%H%M"` (use this exact format)
- **NO MANUAL TIMESTAMPS**: Never manually type timestamps - always extract from system

#### **DURATION CALCULATIONS**
- **Primary Unit**: Minutes (for tasks under 60 minutes)
- **Secondary Unit**: Hours (for tasks 1+ hours, format: "2.5 hours")  
- **Tertiary Unit**: Days (rarely used, format: "1.2 days")
- **NO TARGET DATES**: Focus on actual execution times only

---

### **🎯 CONTINUOUS USAGE PROTOCOL**

#### **AFTER EACH ITEM COMPLETION**
1. **Extract system timestamp** using terminal command
2. **Add completion entry** to appropriate log section
3. **Update timeline table** (Standard/Comprehensive only)
4. **Update metrics** (Standard/Comprehensive only)
5. **Keep entries brief** - focus on essential information only

#### **ONLY WHEN BLOCKED**
1. **Log issue** in Issue Tracking section
2. **Update item status** to BLOCKED in timeline
3. **Document resolution** when issue is resolved
4. **Extract resolution timestamp** from system

#### **SELECTION CRITERIA**
- **BASIC**: Choose for simple, creative, or research-based roadmaps
- **STANDARD**: Choose for most balanced project roadmaps
- **COMPREHENSIVE**: Choose for complex, critical, or highly detailed roadmaps

---

### **👍🏼 BEST PRACTICES**

- **Immediate updates** - log completion within minutes of finishing
- **System timestamps** - never estimate or manually type timestamps
- **Brief entries** - focus on outcomes and key points only
- **Issue focus** - only track significant blocking issues
- **Consistent format** - maintain template structure throughout execution

--- 