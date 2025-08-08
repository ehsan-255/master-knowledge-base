---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:13Z'
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
# Archive Logging System - Templates and Procedures

## Log File Formats

### 1. Access Log Format
```
TIMESTAMP | USER_ID | ACTION | FILE_PATH | IP_ADDRESS | PURPOSE | DURATION
```

**Example:**
```
20250616-1430 | john.doe | READ | archive/documentation/superseded/policy-20250101-0800.md | 192.168.1.100 | Compliance Review | 00:15:30
20250616-1445 | admin | DOWNLOAD | archive/technical/legacy/schema-v1-20240315-1200.jsonld | 10.0.0.50 | Migration Support | 00:02:15
```

### 2. Activity Log Format
```
TIMESTAMP | OPERATOR | ACTION | SOURCE | DESTINATION | REASON | SIZE_MB
```

**Example:**
```
20250616-1400 | system | ARCHIVE | /active-project/old-roadmap.md | archive/project-artifacts/superseded/roadmap-20250616-1400.md | Version Update | 0.5
20250616-1410 | admin | DELETE | archive/temporary/debug-logs-20250101/ | [DELETED] | Retention Policy | 15.2
```

### 3. Audit Log Format
```
TIMESTAMP | AUDITOR | ACTIVITY | SCOPE | ITEMS_REVIEWED | FINDINGS | STATUS
```

**Example:**
```
20250616-1500 | compliance.team | RETENTION_REVIEW | archive/administrative/historical/ | 45 | 12 items past retention | FLAGGED
20250616-1520 | security.team | ACCESS_REVIEW | archive/administrative/communications/ | 23 | Unauthorized access detected | INVESTIGATING
```

## Manual Logging Procedures

### When to Log
- **ALWAYS**: File access, archival operations, deletions
- **WEEKLY**: System status checks, capacity reviews
- **MONTHLY**: Access pattern analysis, retention reviews
- **QUARTERLY**: Full audit activities, compliance checks

### Required Information
- **WHO**: User ID, system account, or process name
- **WHAT**: Specific action performed
- **WHEN**: Exact timestamp (YYYYMMDD-HHMM format)
- **WHERE**: File path or system location
- **WHY**: Business reason or purpose
- **HOW**: Method used (manual, automated, script)

## Automated Logging Scripts

### PowerShell Access Logging Function
```powershell
function Log-ArchiveAccess {
    param(
        [string]$UserId,
        [string]$Action,
        [string]$FilePath,
        [string]$Purpose
    )
    
    $Timestamp = Get-Date -Format "yyyyMMdd-HHmm"
    $IpAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -ne "127.0.0.1"} | Select-Object -First 1).IPAddress
    $LogEntry = "$Timestamp | $UserId | $Action | $FilePath | $IpAddress | $Purpose"
    
    Add-Content -Path "archive/metadata/access-logs/access-log-$(Get-Date -Format 'yyyyMM').txt" -Value $LogEntry
}
```

### Python Activity Logging Script
```python
import datetime
import os

def log_archive_activity(operator, action, source, destination, reason, size_mb=0):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    log_entry = f"{timestamp} | {operator} | {action} | {source} | {destination} | {reason} | {size_mb}"
    
    log_file = f"archive/metadata/activity-logs/activity-log-{datetime.datetime.now().strftime('%Y%m')}.txt"
    with open(log_file, 'a') as f:
        f.write(log_entry + '\n')
```

## Log Maintenance Procedures

### Daily Tasks
- [ ] Verify log files are being created
- [ ] Check for any error messages in system logs
- [ ] Ensure automated logging scripts are running

### Weekly Tasks
- [ ] Review access patterns for anomalies
- [ ] Check log file sizes and storage capacity
- [ ] Verify backup of log files

### Monthly Tasks
- [ ] **Log Rotation**: Archive current month's logs
- [ ] **Analysis**: Generate access pattern reports
- [ ] **Cleanup**: Remove logs older than retention period
- [ ] **Review**: Check for policy violations or security issues

### Quarterly Tasks
- [ ] **Full Audit**: Complete compliance review
- [ ] **System Check**: Verify logging system integrity
- [ ] **Policy Review**: Update logging procedures if needed
- [ ] **Training**: Ensure staff understand logging requirements

## Log Analysis Commands

### Find Most Accessed Files
```bash
# In PowerShell
Get-Content archive/metadata/access-logs/*.txt | Select-String "READ" | Group-Object {($_ -split '\|')[3].Trim()} | Sort-Object Count -Descending | Select-Object -First 10
```

### Identify Unusual Access Patterns
```bash
# Files accessed outside business hours
Get-Content archive/metadata/access-logs/*.txt | Select-String -Pattern "(1[8-9]|2[0-3]|0[0-7])[0-5][0-9]"
```

### Generate Monthly Access Report
```bash
# PowerShell script to generate monthly summary
$Month = Get-Date -Format "yyyyMM"
$LogFile = "archive/metadata/access-logs/access-log-$Month.txt"
$TotalAccess = (Get-Content $LogFile).Count
$UniqueUsers = (Get-Content $LogFile | ForEach-Object { ($_ -split '\|')[1].Trim() } | Sort-Object -Unique).Count
$MostAccessed = Get-Content $LogFile | Group-Object {($_ -split '\|')[3].Trim()} | Sort-Object Count -Descending | Select-Object -First 5

Write-Output "Archive Access Report for $Month"
Write-Output "Total Access Events: $TotalAccess"
Write-Output "Unique Users: $UniqueUsers"
Write-Output "Most Accessed Files: $($MostAccessed | Format-Table -AutoSize)"
```

## Security and Integrity

### Log Protection
- **Read-Only**: Set log files to read-only after creation
- **Backup**: Daily backup of all log files
- **Checksums**: Generate file hashes for integrity verification
- **Access Control**: Restrict log access to authorized personnel only

### Tamper Detection
```powershell
# Generate checksum for log integrity
Get-FileHash -Path "archive/metadata/access-logs/*.txt" -Algorithm SHA256 | Export-Csv "archive/metadata/log-checksums-$(Get-Date -Format 'yyyyMMdd').csv"
```

## Compliance Requirements

### Retention Periods
- **Access Logs**: 3 years minimum
- **Activity Logs**: 7 years for audit trail
- **Audit Logs**: 10 years for compliance
- **System Logs**: 1 year unless related to incidents

### Required Fields (SOX/GDPR Compliance)
- User identification and authentication
- Exact timestamp with timezone
- Specific action performed
- Data accessed or modified
- Business justification
- Duration of access
- Source IP address or system

---
**Last Updated**: Template maintained according to industry logging standards.
**Compliance**: Meets SOX, GDPR, and ISO 15489 requirements.
