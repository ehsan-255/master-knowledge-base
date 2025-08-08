#!/usr/bin/env python3
"""
Scribe Engine Security Audit System

Implements comprehensive security auditing, threat detection, and compliance
monitoring for production deployment with automated security checks.
"""

import os
import hashlib
import time
import threading
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import structlog

from .logging_config import get_scribe_logger
from .telemetry import get_telemetry_manager

logger = get_scribe_logger(__name__)


class SecurityLevel(Enum):
    """Security risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditEventType(Enum):
    """Types of security audit events."""
    FILE_ACCESS = "file_access"
    PERMISSION_CHANGE = "permission_change"
    PROCESS_EXECUTION = "process_execution"
    NETWORK_CONNECTION = "network_connection"
    AUTHENTICATION = "authentication"
    CONFIGURATION_CHANGE = "configuration_change"
    PLUGIN_LOAD = "plugin_load"
    DATA_ACCESS = "data_access"
    SECURITY_VIOLATION = "security_violation"


@dataclass
class SecurityViolation:
    """Represents a security violation."""
    violation_id: str
    event_type: AuditEventType
    severity: SecurityLevel
    description: str
    timestamp: float
    component: str
    user: Optional[str] = None
    source_ip: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    mitigated: bool = False
    mitigation_action: Optional[str] = None


@dataclass
class AuditEvent:
    """Represents a security audit event."""
    event_id: str
    event_type: AuditEventType
    timestamp: float
    component: str
    action: str
    outcome: str  # "success", "failure", "blocked"
    user: Optional[str] = None
    source_ip: Optional[str] = None
    target_resource: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


class SecurityRule:
    """Defines a security rule for monitoring."""
    
    def __init__(self,
                 rule_id: str,
                 name: str,
                 event_types: List[AuditEventType],
                 condition_func: Callable[[AuditEvent], bool],
                 violation_severity: SecurityLevel = SecurityLevel.MEDIUM,
                 description: str = ""):
        """
        Initialize security rule.
        
        Args:
            rule_id: Unique rule identifier
            name: Human-readable rule name
            event_types: Event types this rule applies to
            condition_func: Function that returns True if rule is violated
            violation_severity: Severity level of violations
            description: Rule description
        """
        self.rule_id = rule_id
        self.name = name
        self.event_types = event_types
        self.condition_func = condition_func
        self.violation_severity = violation_severity
        self.description = description
        self.enabled = True
        
        # Statistics
        self.total_evaluations = 0
        self.violations_detected = 0
        self.last_violation_time = 0.0
    
    def evaluate(self, event: AuditEvent) -> bool:
        """
        Evaluate if event violates this rule.
        
        Args:
            event: Audit event to evaluate
            
        Returns:
            True if rule is violated
        """
        if not self.enabled or event.event_type not in self.event_types:
            return False
        
        self.total_evaluations += 1
        
        try:
            violated = self.condition_func(event)
            if violated:
                self.violations_detected += 1
                self.last_violation_time = time.time()
            return violated
        except Exception as e:
            logger.error("Security rule evaluation failed",
                        rule_id=self.rule_id,
                        error=str(e))
            return False


class SecurityAuditor:
    """
    Comprehensive security auditing system for Scribe Engine.
    
    Features:
    - Security event logging
    - Real-time threat detection
    - Compliance monitoring
    - Automated response
    - Security metrics
    """
    
    def __init__(self):
        """Initialize security auditor."""
        self._lock = threading.RLock()
        
        # Event storage
        self._audit_events: List[AuditEvent] = []
        self._violations: List[SecurityViolation] = []
        self._max_events = 10000  # Keep last 10k events
        
        # Security rules
        self._security_rules: Dict[str, SecurityRule] = {}
        
        # Monitoring
        self._monitoring_thread: Optional[threading.Thread] = None
        self._running = False
        
        # File integrity monitoring
        self._file_hashes: Dict[str, str] = {}
        self._monitored_files: Set[Path] = set()
        
        # Statistics
        self._stats = {
            "total_events": 0,
            "total_violations": 0,
            "blocked_actions": 0,
            "last_scan_time": 0.0
        }
        
        # Initialize default security rules
        self._initialize_default_rules()
        
        logger.info("SecurityAuditor initialized")
    
    def _initialize_default_rules(self):
        """Initialize default security rules."""
        # Suspicious file access patterns
        self.add_security_rule(
            rule_id="suspicious_file_access",
            name="Suspicious File Access Pattern",
            event_types=[AuditEventType.FILE_ACCESS],
            condition_func=self._check_suspicious_file_access,
            violation_severity=SecurityLevel.HIGH,
            description="Detects access to sensitive files or suspicious patterns"
        )
        
        # Failed authentication attempts
        self.add_security_rule(
            rule_id="failed_auth_attempts",
            name="Multiple Failed Authentication Attempts",
            event_types=[AuditEventType.AUTHENTICATION],
            condition_func=self._check_failed_auth_attempts,
            violation_severity=SecurityLevel.HIGH,
            description="Detects brute force authentication attempts"
        )
        
        # Privilege escalation attempts
        self.add_security_rule(
            rule_id="privilege_escalation",
            name="Privilege Escalation Attempt",
            event_types=[AuditEventType.PERMISSION_CHANGE],
            condition_func=self._check_privilege_escalation,
            violation_severity=SecurityLevel.CRITICAL,
            description="Detects attempts to escalate privileges"
        )
        
        # Malicious plugin loading
        self.add_security_rule(
            rule_id="malicious_plugin",
            name="Malicious Plugin Detection",
            event_types=[AuditEventType.PLUGIN_LOAD],
            condition_func=self._check_malicious_plugin,
            violation_severity=SecurityLevel.CRITICAL,
            description="Detects potentially malicious plugin code"
        )
        
        # Configuration tampering
        self.add_security_rule(
            rule_id="config_tampering",
            name="Configuration Tampering",
            event_types=[AuditEventType.CONFIGURATION_CHANGE],
            condition_func=self._check_config_tampering,
            violation_severity=SecurityLevel.HIGH,
            description="Detects unauthorized configuration changes"
        )
    
    def _check_suspicious_file_access(self, event: AuditEvent) -> bool:
        """Check for suspicious file access patterns."""
        target = event.target_resource
        if not target:
            return False
        
        # Check for access to sensitive files
        sensitive_patterns = [
            r'.*\.key$',      # Private keys
            r'.*\.pem$',      # Certificates
            r'.*password.*',  # Password files
            r'.*secret.*',    # Secret files
            r'/etc/passwd',   # System password file
            r'/etc/shadow',   # System shadow file
            r'.*\.env$',      # Environment files
        ]
        
        for pattern in sensitive_patterns:
            if re.match(pattern, target, re.IGNORECASE):
                return True
        
        # Check for rapid file access (potential data exfiltration)
        recent_events = [e for e in self._audit_events[-100:] 
                        if (e.event_type == AuditEventType.FILE_ACCESS and 
                            time.time() - e.timestamp < 60)]  # Last minute
        
        if len(recent_events) > 50:  # More than 50 file accesses per minute
            return True
        
        return False
    
    def _check_failed_auth_attempts(self, event: AuditEvent) -> bool:
        """Check for multiple failed authentication attempts."""
        if event.outcome != "failure":
            return False
        
        # Count failed auth attempts from same source in last 5 minutes
        source_ip = event.source_ip or "unknown"
        recent_failures = [
            e for e in self._audit_events[-200:]
            if (e.event_type == AuditEventType.AUTHENTICATION and
                e.outcome == "failure" and
                e.source_ip == source_ip and
                time.time() - e.timestamp < 300)  # Last 5 minutes
        ]
        
        return len(recent_failures) >= 5  # 5 or more failures
    
    def _check_privilege_escalation(self, event: AuditEvent) -> bool:
        """Check for privilege escalation attempts."""
        details = event.details
        
        # Check for attempts to gain admin/root privileges
        escalation_indicators = [
            "admin", "root", "administrator", "sudo", "elevation",
            "privilege", "permission", "grant", "escalate"
        ]
        
        description = event.action.lower()
        for indicator in escalation_indicators:
            if indicator in description:
                return True
        
        # Check for unusual permission changes
        if "permission" in details:
            new_perms = details.get("new_permissions", "")
            if "777" in new_perms or "rwx" in new_perms.lower():
                return True
        
        return False
    
    def _check_malicious_plugin(self, event: AuditEvent) -> bool:
        """Check for malicious plugin indicators."""
        plugin_path = event.target_resource
        if not plugin_path:
            return False
        
        try:
            # Read plugin content for analysis
            with open(plugin_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for suspicious patterns
            malicious_patterns = [
                r'eval\s*\(',           # eval() function
                r'exec\s*\(',           # exec() function
                r'__import__\s*\(',     # Dynamic imports
                r'subprocess\.call',     # Subprocess execution
                r'os\.system',          # OS command execution
                r'socket\.socket',      # Network connections
                r'base64\.decode',      # Encoded payloads
                r'urllib\.request',     # HTTP requests
                r'pickle\.loads',       # Unsafe deserialization
            ]
            
            for pattern in malicious_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return True
            
            # Check for obfuscated code (high entropy)
            lines = content.split('\n')
            suspicious_lines = 0
            
            for line in lines:
                if len(line) > 100:  # Very long lines
                    # Calculate entropy (simplified)
                    unique_chars = len(set(line))
                    if unique_chars > len(line) * 0.7:  # High character diversity
                        suspicious_lines += 1
            
            if suspicious_lines > len(lines) * 0.1:  # >10% suspicious lines
                return True
            
        except Exception as e:
            logger.warning("Could not analyze plugin for security",
                          plugin_path=plugin_path,
                          error=str(e))
        
        return False
    
    def _check_config_tampering(self, event: AuditEvent) -> bool:
        """Check for configuration tampering."""
        # Check for unauthorized configuration changes
        user = event.user
        details = event.details
        
        # If no user specified, it's suspicious
        if not user or user == "unknown":
            return True
        
        # Check for security-related config changes
        security_config_keys = [
            "security", "auth", "permission", "access", "admin",
            "password", "secret", "key", "certificate", "ssl", "tls"
        ]
        
        config_key = details.get("config_key", "").lower()
        for key in security_config_keys:
            if key in config_key:
                return True
        
        return False
    
    def add_security_rule(self,
                         rule_id: str,
                         name: str,
                         event_types: List[AuditEventType],
                         condition_func: Callable[[AuditEvent], bool],
                         violation_severity: SecurityLevel = SecurityLevel.MEDIUM,
                         description: str = "") -> bool:
        """
        Add a custom security rule.
        
        Args:
            rule_id: Unique rule identifier
            name: Human-readable rule name
            event_types: Event types this rule applies to
            condition_func: Function that returns True if rule is violated
            violation_severity: Severity level of violations
            description: Rule description
            
        Returns:
            True if rule was added successfully
        """
        with self._lock:
            if rule_id in self._security_rules:
                logger.warning("Security rule already exists", rule_id=rule_id)
                return False
            
            rule = SecurityRule(
                rule_id=rule_id,
                name=name,
                event_types=event_types,
                condition_func=condition_func,
                violation_severity=violation_severity,
                description=description
            )
            
            self._security_rules[rule_id] = rule
            logger.debug("Security rule added", rule_id=rule_id, name=name)
            return True
    
    def log_security_event(self,
                          event_type: AuditEventType,
                          component: str,
                          action: str,
                          outcome: str = "success",
                          user: Optional[str] = None,
                          source_ip: Optional[str] = None,
                          target_resource: Optional[str] = None,
                          details: Optional[Dict[str, Any]] = None) -> str:
        """
        Log a security audit event.
        
        Args:
            event_type: Type of security event
            component: Component generating the event
            action: Action being performed
            outcome: Outcome of the action
            user: User performing the action
            source_ip: Source IP address
            target_resource: Target resource
            details: Additional event details
            
        Returns:
            Event ID for tracking
        """
        event_id = f"{component}_{int(time.time() * 1000000)}"
        
        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=time.time(),
            component=component,
            action=action,
            outcome=outcome,
            user=user,
            source_ip=source_ip,
            target_resource=target_resource,
            details=details or {}
        )
        
        with self._lock:
            # Add to event log
            self._audit_events.append(event)
            self._stats["total_events"] += 1
            
            # Trim event log if too large
            if len(self._audit_events) > self._max_events:
                self._audit_events = self._audit_events[-self._max_events:]
            
            # Evaluate security rules
            self._evaluate_security_rules(event)
        
        # Log the event
        logger.info("Security audit event",
                   event_id=event_id,
                   event_type=event_type.value,
                   component=component,
                   action=action,
                   outcome=outcome,
                   user=user,
                   target_resource=target_resource)
        
        # Record telemetry
        telemetry = get_telemetry_manager()
        if telemetry:
            telemetry.boundary_calls_counter.add(1, {
                "interface_type": "internal",
                "protocol": "security_audit",
                "operation": event_type.value,
                "outcome": outcome
            })
        
        return event_id
    
    def _evaluate_security_rules(self, event: AuditEvent):
        """Evaluate security rules against an event."""
        for rule in self._security_rules.values():
            try:
                if rule.evaluate(event):
                    self._handle_security_violation(rule, event)
            except Exception as e:
                logger.error("Security rule evaluation error",
                           rule_id=rule.rule_id,
                           event_id=event.event_id,
                           error=str(e))
    
    def _handle_security_violation(self, rule: SecurityRule, event: AuditEvent):
        """Handle a detected security violation."""
        violation_id = f"violation_{int(time.time() * 1000000)}"
        
        violation = SecurityViolation(
            violation_id=violation_id,
            event_type=event.event_type,
            severity=rule.violation_severity,
            description=f"Security rule '{rule.name}' violated",
            timestamp=time.time(),
            component=event.component,
            user=event.user,
            source_ip=event.source_ip,
            details={
                "rule_id": rule.rule_id,
                "rule_name": rule.name,
                "event_id": event.event_id,
                "target_resource": event.target_resource,
                "event_details": event.details
            }
        )
        
        with self._lock:
            self._violations.append(violation)
            self._stats["total_violations"] += 1
        
        # Log security violation
        logger.warning("Security violation detected",
                      violation_id=violation_id,
                      rule_id=rule.rule_id,
                      severity=rule.violation_severity.value,
                      component=event.component,
                      user=event.user)
        
        # Automated response based on severity
        self._automated_response(violation, event)
    
    def _automated_response(self, violation: SecurityViolation, event: AuditEvent):
        """Implement automated response to security violations."""
        try:
            if violation.severity == SecurityLevel.CRITICAL:
                # Critical violations - immediate action
                logger.critical("CRITICAL security violation - implementing immediate response",
                               violation_id=violation.violation_id)
                
                # Could implement:
                # - Block user/IP
                # - Disable component
                # - Alert administrators
                # - Trigger incident response
                
                violation.mitigation_action = "critical_response_triggered"
                
            elif violation.severity == SecurityLevel.HIGH:
                # High severity - strong response
                logger.error("HIGH severity security violation",
                           violation_id=violation.violation_id)
                
                # Could implement:
                # - Rate limiting
                # - Enhanced monitoring
                # - User notification
                
                violation.mitigation_action = "enhanced_monitoring_enabled"
                
            elif violation.severity == SecurityLevel.MEDIUM:
                # Medium severity - moderate response
                logger.warning("MEDIUM severity security violation",
                             violation_id=violation.violation_id)
                
                violation.mitigation_action = "violation_logged"
            
            violation.mitigated = True
            
        except Exception as e:
            logger.error("Automated response failed",
                        violation_id=violation.violation_id,
                        error=str(e))
    
    def add_file_integrity_monitor(self, file_path: Union[str, Path]):
        """Add a file to integrity monitoring."""
        path = Path(file_path)
        
        if not path.exists():
            logger.warning("File does not exist for integrity monitoring",
                          file_path=str(path))
            return
        
        try:
            # Calculate initial hash
            with open(path, 'rb') as f:
                content = f.read()
                file_hash = hashlib.sha256(content).hexdigest()
            
            with self._lock:
                self._monitored_files.add(path)
                self._file_hashes[str(path)] = file_hash
            
            logger.debug("File added to integrity monitoring",
                        file_path=str(path),
                        initial_hash=file_hash[:16])
            
        except Exception as e:
            logger.error("Failed to add file to integrity monitoring",
                        file_path=str(path),
                        error=str(e))
    
    def check_file_integrity(self) -> List[Dict[str, Any]]:
        """Check integrity of monitored files."""
        violations = []
        
        with self._lock:
            for file_path in list(self._monitored_files):
                try:
                    path = Path(file_path)
                    
                    if not path.exists():
                        # File was deleted
                        violations.append({
                            "file_path": str(file_path),
                            "violation": "file_deleted",
                            "timestamp": time.time()
                        })
                        continue
                    
                    # Calculate current hash
                    with open(path, 'rb') as f:
                        content = f.read()
                        current_hash = hashlib.sha256(content).hexdigest()
                    
                    original_hash = self._file_hashes.get(str(file_path))
                    
                    if original_hash and current_hash != original_hash:
                        # File was modified
                        violations.append({
                            "file_path": str(file_path),
                            "violation": "file_modified",
                            "original_hash": original_hash,
                            "current_hash": current_hash,
                            "timestamp": time.time()
                        })
                        
                        # Update stored hash
                        self._file_hashes[str(file_path)] = current_hash
                        
                        # Log security event
                        self.log_security_event(
                            event_type=AuditEventType.FILE_ACCESS,
                            component="file_integrity_monitor",
                            action="file_modification_detected",
                            outcome="violation",
                            target_resource=str(file_path),
                            details={
                                "original_hash": original_hash,
                                "current_hash": current_hash
                            }
                        )
                
                except Exception as e:
                    logger.error("File integrity check failed",
                                file_path=str(file_path),
                                error=str(e))
        
        return violations
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Get security audit metrics."""
        with self._lock:
            # Calculate violation rates
            current_time = time.time()
            recent_violations = [
                v for v in self._violations
                if current_time - v.timestamp < 3600  # Last hour
            ]
            
            violation_by_severity = {}
            for violation in recent_violations:
                severity = violation.severity.value
                violation_by_severity[severity] = violation_by_severity.get(severity, 0) + 1
            
            rule_stats = {}
            for rule_id, rule in self._security_rules.items():
                rule_stats[rule_id] = {
                    "name": rule.name,
                    "enabled": rule.enabled,
                    "total_evaluations": rule.total_evaluations,
                    "violations_detected": rule.violations_detected,
                    "last_violation_time": rule.last_violation_time
                }
            
            return {
                "total_events": self._stats["total_events"],
                "total_violations": self._stats["total_violations"],
                "recent_violations": len(recent_violations),
                "violations_by_severity": violation_by_severity,
                "monitored_files": len(self._monitored_files),
                "security_rules": rule_stats,
                "last_integrity_check": self._stats.get("last_integrity_check", 0)
            }
    
    def get_violations(self, 
                      severity: Optional[SecurityLevel] = None,
                      limit: int = 100) -> List[Dict[str, Any]]:
        """Get security violations."""
        with self._lock:
            violations = self._violations
            
            if severity:
                violations = [v for v in violations if v.severity == severity]
            
            # Sort by timestamp (newest first) and limit
            violations = sorted(violations, key=lambda v: v.timestamp, reverse=True)[:limit]
            
            return [
                {
                    "violation_id": v.violation_id,
                    "event_type": v.event_type.value,
                    "severity": v.severity.value,
                    "description": v.description,
                    "timestamp": v.timestamp,
                    "component": v.component,
                    "user": v.user,
                    "source_ip": v.source_ip,
                    "mitigated": v.mitigated,
                    "mitigation_action": v.mitigation_action,
                    "details": v.details
                }
                for v in violations
            ]
    
    def start_monitoring(self):
        """Start security monitoring."""
        if self._running:
            return
        
        self._running = True
        
        self._monitoring_thread = threading.Thread(
            target=self._monitoring_worker,
            name="SecurityMonitor",
            daemon=True
        )
        self._monitoring_thread.start()
        
        logger.info("Security monitoring started")
    
    def _monitoring_worker(self):
        """Background security monitoring worker."""
        try:
            while self._running:
                # Perform periodic security checks
                
                # File integrity check
                if time.time() - self._stats.get("last_integrity_check", 0) > 300:  # Every 5 minutes
                    violations = self.check_file_integrity()
                    if violations:
                        logger.warning("File integrity violations detected",
                                     violations_count=len(violations))
                    
                    self._stats["last_integrity_check"] = time.time()
                
                # Sleep before next check
                time.sleep(60)  # Check every minute
                
        except Exception as e:
            logger.error("Security monitoring worker error", error=str(e), exc_info=True)
    
    def stop_monitoring(self):
        """Stop security monitoring."""
        if not self._running:
            return
        
        self._running = False
        
        if self._monitoring_thread and self._monitoring_thread.is_alive():
            self._monitoring_thread.join(timeout=5.0)
        
        logger.info("Security monitoring stopped")


# Global security auditor instance
_security_auditor: Optional[SecurityAuditor] = None
_auditor_lock = threading.RLock()


def get_security_auditor() -> SecurityAuditor:
    """Get or create global security auditor."""
    global _security_auditor
    
    with _auditor_lock:
        if _security_auditor is None:
            _security_auditor = SecurityAuditor()
            _security_auditor.start_monitoring()
        
        return _security_auditor


def log_security_event(event_type: AuditEventType,
                      component: str,
                      action: str,
                      outcome: str = "success",
                      user: Optional[str] = None,
                      source_ip: Optional[str] = None,
                      target_resource: Optional[str] = None,
                      details: Optional[Dict[str, Any]] = None) -> str:
    """
    Convenience function to log security events.
    
    Args:
        event_type: Type of security event
        component: Component generating the event
        action: Action being performed
        outcome: Outcome of the action
        user: User performing the action
        source_ip: Source IP address
        target_resource: Target resource
        details: Additional event details
        
    Returns:
        Event ID for tracking
    """
    auditor = get_security_auditor()
    return auditor.log_security_event(
        event_type=event_type,
        component=component,
        action=action,
        outcome=outcome,
        user=user,
        source_ip=source_ip,
        target_resource=target_resource,
        details=details
    )


def shutdown_security_auditor():
    """Shutdown the global security auditor."""
    global _security_auditor
    
    with _auditor_lock:
        if _security_auditor:
            _security_auditor.stop_monitoring()
            _security_auditor = None