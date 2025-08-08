# Archive Logging Script
# Usage: .\archive-logger.ps1 -Action "READ" -FilePath "archive/documentation/file.md" -Purpose "Review"

param(
    [Parameter(Mandatory=$true)]
    [string]$Action,
    
    [Parameter(Mandatory=$true)]
    [string]$FilePath,
    
    [Parameter(Mandatory=$true)]
    [string]$Purpose,
    
    [string]$UserId = $env:USERNAME,
    [string]$LogType = "access"
)

# Get current timestamp in required format
$Timestamp = Get-Date -Format "yyyyMMdd-HHmm"
$Date = Get-Date -Format "yyyyMM"

# Get IP address
try {
    $IpAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -ne "127.0.0.1" -and $_.PrefixOrigin -eq "Dhcp"} | Select-Object -First 1).IPAddress
    if (-not $IpAddress) {
        $IpAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -ne "127.0.0.1"} | Select-Object -First 1).IPAddress
    }
    if (-not $IpAddress) { $IpAddress = "localhost" }
} catch {
    $IpAddress = "unknown"
}

# Ensure log directory exists
$LogDir = "archive/metadata/$LogType-logs"
if (-not (Test-Path $LogDir)) {
    New-Item -Path $LogDir -ItemType Directory -Force | Out-Null
}

# Create log entry based on type
switch ($LogType) {
    "access" {
        $LogEntry = "$Timestamp | $UserId | $Action | $FilePath | $IpAddress | $Purpose"
        $LogFile = "$LogDir/access-log-$Date.txt"
    }
    "activity" {
        # For activity logs, assume FilePath is source and Purpose contains destination
        $LogEntry = "$Timestamp | $UserId | $Action | $FilePath | $Purpose | Archive Operation"
        $LogFile = "$LogDir/activity-log-$Date.txt"
    }
    default {
        $LogEntry = "$Timestamp | $UserId | $Action | $FilePath | $IpAddress | $Purpose"
        $LogFile = "$LogDir/access-log-$Date.txt"
    }
}

# Write to log file
Add-Content -Path $LogFile -Value $LogEntry

# Display confirmation
Write-Host "Logged: $LogEntry" -ForegroundColor Green
Write-Host "File: $LogFile" -ForegroundColor Cyan

# Optional: Display recent log entries
$RecentEntries = Get-Content $LogFile | Select-Object -Last 5
Write-Host "`nRecent log entries:" -ForegroundColor Yellow
$RecentEntries | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray } 