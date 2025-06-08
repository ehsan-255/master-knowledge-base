# Complete Timestamp Monitor Setup Instructions for LLM Implementation

## Repository Information
- **OS**: Windows
- **Terminal**: PowerShell
- **Node.js Version**: v22.14.0 (confirmed working)
- **NPM Version**: 10.9.2
- **Repo Location**: `C:\Users\E L I A N A\Downloads\_apmdd_vault`

## File Structure Overview
```
C:\Users\E L I A N A\Downloads\_apmdd_vault\
├── master-knowledge-base/
│   └── tools/
│       └── utilities/
│           └── timestamp-monitor/           # ← CREATE THIS
│               ├── monitor.js               # ← CREATE THIS
│               ├── start-monitor.ps1        # ← CREATE THIS
│               ├── config.json              # ← CREATE THIS
│               └── README.md                # ← CREATE THIS
├── active-project/
│   ├── (existing files...)
│   └── roadmap-progress-tracker-template.md  # ← UPDATE THIS
└── (other existing files...)
```

---

## Step 1: Create Directory Structure

**PowerShell Commands:**
```powershell
# Navigate to repo root
cd "C:\Users\E L I A N A\Downloads\_apmdd_vault"

# Create timestamp monitor directory
New-Item -ItemType Directory -Path "master-knowledge-base\tools\utilities\timestamp-monitor" -Force

# Navigate to the new directory
cd "master-knowledge-base\tools\utilities\timestamp-monitor"

# Verify location
Get-Location
```

---

## Step 2: Create monitor.js (Main Engine)

**File**: `master-knowledge-base\tools\utilities\timestamp-monitor\monitor.js`

```javascript
const fs = require('fs');
const path = require('path');

class TimestampMonitor {
    constructor() {
        this.watchers = new Map();
        this.baseDir = process.cwd();
    }

    formatTimestamp() {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        return `${year}${month}${day}-${hours}${minutes}`;
    }

    updateTimestamps(filePath) {
        if (!fs.existsSync(filePath)) {
            console.log(`File ${filePath} no longer exists, removing watcher`);
            this.stopWatching(filePath);
            return;
        }

        let content = fs.readFileSync(filePath, 'utf8');
        let modified = false;
        const timestamp = this.formatTimestamp();
        
        // Pattern 1: ✅ Task Name {{TSx}} -> ✅ Task Name 20241201-1430
        const completedPattern = /✅(.+?){{(TS\d+)}}/g;
        content = content.replace(completedPattern, (match, taskText, placeholder) => {
            modified = true;
            console.log(`✅ COMPLETED: ${taskText.trim()} [${placeholder}] -> ${timestamp}`);
            return `✅${taskText}${timestamp}`;
        });
        
        // Pattern 2: 🔄 Task Name {{TSx}} -> 🔄 Task Name 20241201-1430
        const inProgressPattern = /🔄(.+?){{(TS\d+)}}/g;
        content = content.replace(inProgressPattern, (match, taskText, placeholder) => {
            modified = true;
            console.log(`🔄 IN PROGRESS: ${taskText.trim()} [${placeholder}] -> ${timestamp}`);
            return `🔄${taskText}${timestamp}`;
        });
        
        // Pattern 3: ❌ Task Name {{TSx}} -> ❌ Task Name 20241201-1430
        const blockedPattern = /❌(.+?){{(TS\d+)}}/g;
        content = content.replace(blockedPattern, (match, taskText, placeholder) => {
            modified = true;
            console.log(`❌ BLOCKED: ${taskText.trim()} [${placeholder}] -> ${timestamp}`);
            return `❌${taskText}${timestamp}`;
        });
        
        if (modified) {
            fs.writeFileSync(filePath, content);
            console.log(`📝 Updated: ${path.relative(this.baseDir, filePath)}\n`);
        }
    }

    startWatching(filePath) {
        const absolutePath = path.resolve(filePath);
        
        if (!fs.existsSync(absolutePath)) {
            console.error(`❌ File not found: ${filePath}`);
            return false;
        }

        if (this.watchers.has(absolutePath)) {
            console.log(`👁️  Already watching: ${path.relative(this.baseDir, absolutePath)}`);
            return true;
        }

        try {
            const watcher = fs.watchFile(absolutePath, { interval: 500 }, (curr, prev) => {
                if (curr.mtime > prev.mtime) {
                    console.log(`📄 File changed: ${path.relative(this.baseDir, absolutePath)}`);
                    setTimeout(() => this.updateTimestamps(absolutePath), 300);
                }
            });

            this.watchers.set(absolutePath, watcher);
            console.log(`👁️  Watching: ${path.relative(this.baseDir, absolutePath)}`);
            
            // Initial check for existing status changes
            this.updateTimestamps(absolutePath);
            return true;
        } catch (error) {
            console.error(`❌ Error watching ${filePath}:`, error.message);
            return false;
        }
    }

    stopWatching(filePath) {
        const absolutePath = path.resolve(filePath);
        
        if (this.watchers.has(absolutePath)) {
            fs.unwatchFile(absolutePath);
            this.watchers.delete(absolutePath);
            console.log(`🔍 Stopped watching: ${path.relative(this.baseDir, absolutePath)}`);
            return true;
        }
        return false;
    }

    listWatched() {
        console.log(`\n👁️  Currently watching ${this.watchers.size} files:`);
        for (const filePath of this.watchers.keys()) {
            console.log(`   - ${path.relative(this.baseDir, filePath)}`);
        }
        console.log();
    }

    stopAll() {
        console.log('🛑 Stopping all watchers...');
        for (const filePath of this.watchers.keys()) {
            this.stopWatching(filePath);
        }
    }

    // Auto-discover roadmap files
    autoDiscover(searchPaths = ['./', './active-project']) {
        const patterns = [
            '*roadmap*.md',
            '*progress*.md',
            '*checklist*.md',
            '*tracker*.md'
        ];

        let foundFiles = [];

        searchPaths.forEach(searchPath => {
            if (fs.existsSync(searchPath)) {
                this.scanDirectory(searchPath, patterns, foundFiles);
            }
        });

        console.log(`🔍 Auto-discovered ${foundFiles.length} files:`);
        foundFiles.forEach(file => {
            console.log(`   - ${path.relative(this.baseDir, file)}`);
            this.startWatching(file);
        });

        return foundFiles;
    }

    scanDirectory(dir, patterns, foundFiles) {
        const items = fs.readdirSync(dir);
        
        items.forEach(item => {
            const fullPath = path.join(dir, item);
            const stat = fs.statSync(fullPath);
            
            if (stat.isDirectory()) {
                this.scanDirectory(fullPath, patterns, foundFiles);
            } else if (item.endsWith('.md')) {
                const shouldInclude = patterns.some(pattern => {
                    const regex = new RegExp(pattern.replace('*', '.*'), 'i');
                    return regex.test(item);
                });
                
                if (shouldInclude) {
                    foundFiles.push(fullPath);
                }
            }
        });
    }
}

// CLI Interface
function main() {
    const monitor = new TimestampMonitor();
    const args = process.argv.slice(2);

    console.log('🕐 Timestamp Monitor for Roadmap Progress Tracking');
    console.log('==================================================\n');

    // Handle Ctrl+C gracefully
    process.on('SIGINT', () => {
        console.log('\n🛑 Shutting down...');
        monitor.stopAll();
        process.exit(0);
    });

    if (args.length === 0) {
        // Auto-discover mode
        console.log('🔍 Auto-discovering roadmap files...\n');
        const discovered = monitor.autoDiscover();
        
        if (discovered.length === 0) {
            console.log('❌ No roadmap files found. Usage:');
            console.log('   node monitor.js [file1.md] [file2.md] ...');
            console.log('   or place roadmap files in current directory or active-project/');
            process.exit(1);
        }
    } else {
        // Manual file specification
        args.forEach(filePath => {
            monitor.startWatching(filePath);
        });
    }

    monitor.listWatched();
    console.log('✅ Monitor active. Status changes will be timestamped automatically.');
    console.log('   Supported: ⬜ -> ✅/🔄/❌ (with {{TSx}} placeholders)');
    console.log('   Press Ctrl+C to stop\n');

    // Keep the process alive
    setInterval(() => {
        // Heartbeat every 30 seconds
    }, 30000);
}

if (require.main === module) {
    main();
}

module.exports = TimestampMonitor;
```

---

## Step 3: Create PowerShell Launcher

**File**: `master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1`

```powershell
#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Timestamp Monitor for Roadmap Progress Tracking
.DESCRIPTION
    Monitors markdown files for emoji status changes and automatically adds timestamps
.PARAMETER Files
    Specific files to monitor (optional - will auto-discover if not specified)
.EXAMPLE
    .\start-monitor.ps1
    .\start-monitor.ps1 roadmap.md progress.md
#>

param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Files
)

# Colors for output
$Colors = @{
    Success = 'Green'
    Info = 'Cyan' 
    Warning = 'Yellow'
    Error = 'Red'
}

function Write-ColorOutput {
    param($Message, $Color = 'White')
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

# Get script directory and repo root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..\..") | Select-Object -ExpandProperty Path

Write-ColorOutput "🚀 Timestamp Monitor Starting..." "Success"
Write-ColorOutput "📁 Repo Root: $RepoRoot" "Info"
Write-ColorOutput "🔧 Script Dir: $ScriptDir" "Info"

# Verify Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-ColorOutput "❌ Node.js not found! Please install Node.js first." "Error"
    Write-ColorOutput "   Download from: https://nodejs.org/" "Info"
    Read-Host "Press Enter to exit"
    exit 1
}

$NodeVersion = & node --version
Write-ColorOutput "✅ Node.js Version: $NodeVersion" "Success"

# Change to repo root
try {
    Set-Location $RepoRoot -ErrorAction Stop
    Write-ColorOutput "✅ Changed to repo root directory" "Success"
} catch {
    Write-ColorOutput "❌ Failed to change to repo root: $_" "Error"
    exit 1
}

# Execute monitor script
$MonitorScript = Join-Path $ScriptDir "monitor.js"

if (-not (Test-Path $MonitorScript)) {
    Write-ColorOutput "❌ Monitor script not found: $MonitorScript" "Error"
    exit 1
}

Write-ColorOutput "🎯 Launching monitor with files: $($Files -join ', ')" "Info"
Write-ColorOutput "⌨️  Press Ctrl+C to stop monitoring" "Warning"
Write-ColorOutput "📚 Supported patterns: ⬜ -> ✅/🔄/❌ (with {{TSx}} placeholders)" "Info"
Write-ColorOutput "" 

try {
    if ($Files.Count -gt 0) {
        & node $MonitorScript @Files
    } else {
        & node $MonitorScript
    }
} catch {
    Write-ColorOutput "❌ Error running monitor: $_" "Error"
    Read-Host "Press Enter to exit"
    exit 1
}
```

---

## Step 4: Create Configuration File

**File**: `master-knowledge-base\tools\utilities\timestamp-monitor\config.json`

```json
{
    "searchPaths": [
        "./",
        "./active-project",
        "./active-project/*",
        "./active-project/*/*"
    ],
    "filePatterns": [
        "*roadmap*.md",
        "*progress*.md",
        "*checklist*.md",
        "*tracker*.md"
    ],
    "excludePaths": [
        "node_modules",
        ".git",
        "archive",
        "test-environment"
    ],
    "timestampFormat": "YYYYMMDD-HHMM",
    "watchInterval": 500,
    "updateDelay": 300,
    "supportedEmojis": {
        "notStarted": "⬜",
        "inProgress": "🔄", 
        "completed": "✅",
        "blocked": "❌"
    }
}
```

---

## Step 5: Create README Documentation

**File**: `master-knowledge-base\tools\utilities\timestamp-monitor\README.md`

```markdown
# Timestamp Monitor for Roadmap Progress Tracking

Automatically timestamps task status changes in markdown roadmap files.

## Quick Start

### 1. Start Monitoring (Auto-Discovery)
```powershell
# From repo root
.\master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1
```

### 2. Start Monitoring (Specific Files)
```powershell
.\master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1 roadmap.md progress.md
```

## How It Works

### Status Changes Monitored:
- `⬜` → `✅` (Task completed)
- `⬜` → `🔄` (Task started)  
- `⬜` → `❌` (Task blocked)
- `🔄` → `✅` (In-progress task completed)
- `🔄` → `❌` (In-progress task blocked)

### Timestamp Format:
- Pattern: `YYYYMMDD-HHMM`
- Example: `20241201-1430` (Dec 1, 2024 at 2:30 PM)

### Template Structure:
```markdown
⬜ Task description {{TS1}} *Note: [Additional info]*
🔄 Another task {{TS2}}
✅ Completed task 20241201-1430
```

## File Discovery

```markdown
File Discovery

Auto-discovers files matching:
- `*roadmap*.md`
- `*progress*.md` 
- `*checklist*.md`
- `*tracker*.md`

In directories:
- Root directory
- `./active-project/`
- `./active-project/*/` (subdirectories)

## Usage Examples

### Auto-Discovery Mode
```powershell
# Finds and watches all roadmap files automatically
.\master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1
```

### Manual File Selection
```powershell
# Watch specific files
.\master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1 my-roadmap.md active-project\progress.md
```

### Direct Node.js Usage
```powershell
# From repo root
node master-knowledge-base\tools\utilities\timestamp-monitor\monitor.js
```

## Requirements
- Node.js (any recent version)
- Windows PowerShell
- Markdown files with {{TSx}} placeholders

## Troubleshooting
- Ensure you're in the repo root when starting
- Check that Node.js is in your PATH
- Verify file paths are correct
- Use Ctrl+C to stop monitoring
```

---

## Step 6: Update Template File

**File**: `active-project\roadmap-progress-tracker-template.md`

**UPDATE THIS FILE** by adding the monitor instructions at the top:

```markdown
---
# 🕐 TIMESTAMP MONITOR INSTRUCTIONS
# 
# 1. START MONITOR: Run this command from repo root:
#    .\master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1
#
# 2. USAGE: Simply change status emojis:
#    ⬜ → 🔄 (starting task)
#    ⬜ → ✅ (completing task)
#    ⬜ → ❌ (blocking task)
#    🔄 → ✅ (completing in-progress task)
#
# 3. DO NOT MODIFY {{TSx}} placeholders - they auto-update!
#
# 4. STOP MONITOR: Press Ctrl+C in the monitor terminal
---

# Project Progress Tracker Template

## STATUS LEGEND
⬜ **NOT STARTED** - Task hasn't been initiated
🔄 **IN PROGRESS** - Currently working on task
✅ **COMPLETED** - Task finished successfully  
❌ **BLOCKED** - Task cannot proceed (issue/dependency)

*Note: [🔤]* **ONE-LINER NOTE PLACEHOLDER** - Replace with specific details

---

## Phase 1: Initial Setup
⬜ Project initialization {{TS1}} *Note: [🔤]*
⬜ Environment configuration {{TS2}} *Note: [🔤]*
⬜ Dependencies installation {{TS3}} *Note: [🔤]*

## Phase 2: Core Development  
⬜ Database schema design {{TS4}} *Note: [🔤]*
⬜ API endpoint creation {{TS5}} *Note: [🔤]*
⬜ Authentication system {{TS6}} *Note: [🔤]*
⬜ User interface components {{TS7}} *Note: [🔤]*

## Phase 3: Integration & Testing
⬜ Unit tests implementation {{TS8}} *Note: [🔤]*
⬜ Integration testing {{TS9}} *Note: [🔤]*
⬜ End-to-end testing {{TS10}} *Note: [🔤]*
⬜ Performance optimization {{TS11}} *Note: [🔤]*

## Phase 4: Deployment
⬜ Production environment setup {{TS12}} *Note: [🔤]*
⬜ CI/CD pipeline configuration {{TS13}} *Note: [🔤]*
⬜ Documentation completion {{TS14}} *Note: [🔤]*
⬜ Go-live preparation {{TS15}} *Note: [🔤]*

---

## USAGE NOTES FOR LLMs:

### 🤖 LLM Instructions:
1. **NEVER** manually edit {{TSx}} placeholders
2. **ONLY** change emoji status (⬜ → 🔄/✅/❌)
3. Update *Note: [🔤]* sections with relevant details
4. Keep task descriptions concise but clear
5. Add new tasks following the same pattern: `⬜ Task description {{TSxx}} *Note: [details]*`

### 📝 Example Status Updates:
```markdown
# BEFORE:
⬜ Database schema design {{TS4}} *Note: [PostgreSQL setup required]*

# AFTER (when starting):
🔄 Database schema design {{TS4}} *Note: [PostgreSQL setup required]*
# Monitor auto-converts to:
🔄 Database schema design 20241201-1430 *Note: [PostgreSQL setup required]*

# AFTER (when completing):
✅ Database schema design {{TS4}} *Note: [PostgreSQL setup required]*  
# Monitor auto-converts to:
✅ Database schema design 20241201-1445 *Note: [PostgreSQL setup required]*
```
```

---

## Step 7: Create PowerShell Commands for File Creation

**Execute these commands in PowerShell:**

```powershell
# Navigate to timestamp monitor directory
cd "C:\Users\E L I A N A\Downloads\_apmdd_vault\master-knowledge-base\tools\utilities\timestamp-monitor"

# Create monitor.js file
New-Item -ItemType File -Path "monitor.js" -Force
# Then copy-paste the monitor.js content from Step 2

# Create PowerShell launcher
New-Item -ItemType File -Path "start-monitor.ps1" -Force  
# Then copy-paste the start-monitor.ps1 content from Step 3

# Create config file
New-Item -ItemType File -Path "config.json" -Force
# Then copy-paste the config.json content from Step 4

# Create README
New-Item -ItemType File -Path "README.md" -Force
# Then copy-paste the README.md content from Step 5

# Set PowerShell execution policy (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Navigate back to repo root
cd "C:\Users\E L I A N A\Downloads\_apmdd_vault"
```

---

## Step 8: Test the Installation

**Execute these commands to verify everything works:**

```powershell
# From repo root
cd "C:\Users\E L I A N A\Downloads\_apmdd_vault"

# Test Node.js
node --version
# Should show: v22.14.0

# Test the monitor (dry run)
.\master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1
# Should show: Monitor starting, auto-discovering files, etc.

# If it finds roadmap files, it will start monitoring
# If not, it will show "No roadmap files found" - this is OK for initial test
```

---

## Step 9: LLM Usage Instructions

### For the LLM to Use This System:

**1. Start Monitor (One-time per session):**
```powershell
cd "C:\Users\E L I A N A\Downloads\_apmdd_vault"
.\master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1
```

**2. LLM Task Updates:**
- **ONLY** change emoji status: `⬜` → `🔄`/`✅`/`❌`
- **NEVER** modify `{{TSx}}` placeholders
- Update `*Note: [🔤]*` sections with details
- The monitor will automatically replace `{{TSx}}` with timestamps

**3. Example LLM Workflow:**
```markdown
# When starting a task:
⬜ Setup database schema {{TS1}} *Note: [Need PostgreSQL]*
# ↓ LLM changes to:
🔄 Setup database schema {{TS1}} *Note: [Installing PostgreSQL 15]*
# ↓ Monitor auto-converts to:
🔄 Setup database schema 20241201-1430 *Note: [Installing PostgreSQL 15]*

# When completing:
🔄 Setup database schema 20241201-1430 *Note: [Installing PostgreSQL 15]*
# ↓ LLM changes to:
✅ Setup database schema {{TS1}} *Note: [PostgreSQL 15 installed and configured]*
# ↓ Monitor auto-converts to:
✅ Setup database schema 20241201-1445 *Note: [PostgreSQL 15 installed and configured]*
```

---

## Summary of Files Created:

1. ✅ `master-knowledge-base\tools\utilities\timestamp-monitor\monitor.js`
2. ✅ `master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1`
3. ✅ `master-knowledge-base\tools\utilities\timestamp-monitor\config.json`
4. ✅ `master-knowledge-base\tools\utilities\timestamp-monitor\README.md`
5. ✅ Updated `active-project\roadmap-progress-tracker-template.md`

## Final Verification Command:
```powershell
# Test complete setup
cd "C:\Users\E L I A N A\Downloads\_apmdd_vault"
.\master-knowledge-base\tools\utilities\timestamp-monitor\start-monitor.ps1

# Should show green success messages and start monitoring
# Press Ctrl+C to stop when testing is complete
```

**The system is now ready for LLM-driven roadmap progress tracking with automatic timestamps!** 🚀