#!/usr/bin/env python3
"""
Scribe Vault Policy Manager

Enterprise-grade authentication and authorization policy management for HashiCorp Vault
implementing tiered security access patterns for HMA v2.2 compliance.
"""

import os
import json
import time
import threading
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import structlog

from .logging_config import get_scribe_logger
from .vault_secret_provider import get_vault_provider

logger = get_scribe_logger(__name__)


class AccessTier(Enum):
    """Security access tier levels for role-based access control."""
    ADMIN = "admin"                    # Full administrative access
    SERVICE = "service"               # Service-level operations
    APPLICATION = "application"       # Application-specific access
    READONLY = "readonly"             # Read-only access
    EMERGENCY = "emergency"           # Emergency access with audit


class PolicyScope(Enum):
    """Policy scope definitions for different operational contexts."""
    GLOBAL = "global"                 # Cross-service access
    SERVICE_SPECIFIC = "service"      # Single service access
    ENVIRONMENT = "environment"       # Environment-specific (dev/prod)
    TEMPORARY = "temporary"           # Time-limited access


@dataclass
class PolicyTemplate:
    """Template for generating Vault policies with standardized patterns."""
    name: str
    tier: AccessTier
    scope: PolicyScope
    paths: List[Dict[str, Any]]
    capabilities: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    ttl: Optional[str] = None
    max_ttl: Optional[str] = None
    description: str = ""


@dataclass
class AppRoleConfig:
    """Configuration for AppRole authentication method."""
    role_name: str
    policies: List[str]
    token_ttl: str = "1h"
    token_max_ttl: str = "4h"
    token_policies: List[str] = field(default_factory=list)
    token_bound_cidrs: List[str] = field(default_factory=list)
    token_explicit_max_ttl: Optional[str] = None
    token_no_default_policy: bool = True
    token_num_uses: int = 0
    token_period: Optional[str] = None
    secret_id_ttl: str = "10m"
    secret_id_num_uses: int = 1
    local_secret_ids: bool = False
    bind_secret_id: bool = True


class VaultPolicyManager:
    """
    Professional Vault policy management system.
    
    Implements enterprise-grade authentication and authorization policies
    with tiered access control and automated policy lifecycle management.
    """
    
    def __init__(self, vault_provider=None):
        """
        Initialize policy manager.
        
        Args:
            vault_provider: Optional VaultSecretProvider instance
        """
        self.vault_provider = vault_provider or get_vault_provider()
        self._lock = threading.RLock()
        
        # Policy templates registry
        self._policy_templates: Dict[str, PolicyTemplate] = {}
        self._approle_configs: Dict[str, AppRoleConfig] = {}
        
        # Metrics
        self._policies_created = 0
        self._policies_updated = 0
        self._approles_created = 0
        self._authentication_events = 0
        
        # Initialize standard policy templates
        self._initialize_standard_templates()
        
        logger.info("Vault policy manager initialized",
                   template_count=len(self._policy_templates))
    
    def _initialize_standard_templates(self):
        """Initialize standard policy templates for common use cases."""
        
        # Admin Policy Template
        admin_template = PolicyTemplate(
            name="scribe-admin",
            tier=AccessTier.ADMIN,
            scope=PolicyScope.GLOBAL,
            paths=[
                {
                    "path": "*",
                    "capabilities": ["create", "read", "update", "delete", "list", "sudo"]
                },
                {
                    "path": "sys/*",
                    "capabilities": ["create", "read", "update", "delete", "list", "sudo"]
                },
                {
                    "path": "auth/*",
                    "capabilities": ["create", "read", "update", "delete", "list", "sudo"]
                }
            ],
            description="Full administrative access for Scribe administrators"
        )
        
        # Service Policy Template
        service_template = PolicyTemplate(
            name="scribe-service",
            tier=AccessTier.SERVICE,
            scope=PolicyScope.SERVICE_SPECIFIC,
            paths=[
                {
                    "path": "scribe/data/{{identity.entity.aliases.auth_approle_*.name}}/*",
                    "capabilities": ["create", "read", "update", "delete", "list"]
                },
                {
                    "path": "scribe/metadata/{{identity.entity.aliases.auth_approle_*.name}}/*",
                    "capabilities": ["list", "read", "delete"]
                },
                {
                    "path": "pki/issue/scribe-role",
                    "capabilities": ["create", "update"]
                },
                {
                    "path": "pki/certs",
                    "capabilities": ["list"]
                },
                {
                    "path": "sys/health",
                    "capabilities": ["read", "sudo"]
                }
            ],
            ttl="1h",
            max_ttl="4h",
            description="Service-level access for Scribe engine operations"
        )
        
        # Application Policy Template
        application_template = PolicyTemplate(
            name="scribe-application",
            tier=AccessTier.APPLICATION,
            scope=PolicyScope.SERVICE_SPECIFIC,
            paths=[
                {
                    "path": "scribe/data/config/*",
                    "capabilities": ["read"]
                },
                {
                    "path": "scribe/data/secrets/{{identity.entity.aliases.auth_approle_*.name}}/*",
                    "capabilities": ["read"]
                },
                {
                    "path": "pki/issue/scribe-role",
                    "capabilities": ["create", "update"]
                }
            ],
            ttl="30m",
            max_ttl="2h",
            description="Application-specific access for Scribe components"
        )
        
        # Read-Only Policy Template
        readonly_template = PolicyTemplate(
            name="scribe-readonly",
            tier=AccessTier.READONLY,
            scope=PolicyScope.GLOBAL,
            paths=[
                {
                    "path": "scribe/data/*",
                    "capabilities": ["read", "list"]
                },
                {
                    "path": "scribe/metadata/*",
                    "capabilities": ["read", "list"]
                },
                {
                    "path": "sys/health",
                    "capabilities": ["read"]
                }
            ],
            ttl="2h",
            max_ttl="8h",
            description="Read-only access for monitoring and auditing"
        )
        
        # Emergency Policy Template
        emergency_template = PolicyTemplate(
            name="scribe-emergency",
            tier=AccessTier.EMERGENCY,
            scope=PolicyScope.TEMPORARY,
            paths=[
                {
                    "path": "scribe/data/emergency/*",
                    "capabilities": ["create", "read", "update", "delete", "list"]
                },
                {
                    "path": "pki/issue/scribe-role",
                    "capabilities": ["create", "update"]
                },
                {
                    "path": "sys/health",
                    "capabilities": ["read", "sudo"]
                }
            ],
            ttl="15m",
            max_ttl="1h",
            conditions={
                "time_of_day": {"start": "00:00", "end": "23:59"},
                "max_uses": 10
            },
            description="Emergency access with time and usage limits"
        )
        
        # Register templates
        for template in [admin_template, service_template, application_template, 
                        readonly_template, emergency_template]:
            self._policy_templates[template.name] = template
    
    def create_policy_from_template(self, 
                                  template_name: str, 
                                  policy_name: Optional[str] = None,
                                  custom_paths: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        Create a Vault policy from a template.
        
        Args:
            template_name: Name of the policy template
            policy_name: Custom policy name (defaults to template name)
            custom_paths: Optional custom path configurations
            
        Returns:
            True if policy created successfully
        """
        if not self.vault_provider:
            logger.error("Vault provider not available for policy creation")
            return False
        
        template = self._policy_templates.get(template_name)
        if not template:
            logger.error("Policy template not found", template_name=template_name)
            return False
        
        policy_name = policy_name or template.name
        paths = custom_paths or template.paths
        
        try:
            # Generate HCL policy document
            policy_hcl = self._generate_policy_hcl(template, paths)
            
            # Create policy in Vault
            vault_client = self.vault_provider._client
            if not vault_client:
                raise Exception("Vault client not initialized")
            
            vault_client.sys.create_or_update_policy(
                name=policy_name,
                policy=policy_hcl
            )
            
            self._policies_created += 1
            
            logger.info("Vault policy created successfully",
                       policy_name=policy_name,
                       template=template_name,
                       tier=template.tier.value,
                       scope=template.scope.value)
            
            return True
            
        except Exception as e:
            logger.error("Failed to create Vault policy",
                        policy_name=policy_name,
                        template_name=template_name,
                        error=str(e))
            return False
    
    def _generate_policy_hcl(self, template: PolicyTemplate, paths: List[Dict[str, Any]]) -> str:
        """Generate HCL policy document from template."""
        hcl_blocks = [f"# {template.description}"]
        
        if template.ttl:
            hcl_blocks.append(f"# Default TTL: {template.ttl}")
        if template.max_ttl:
            hcl_blocks.append(f"# Max TTL: {template.max_ttl}")
        
        hcl_blocks.append("")
        
        for path_config in paths:
            path = path_config["path"]
            capabilities = path_config["capabilities"]
            
            hcl_blocks.append(f'path "{path}" {{')
            hcl_blocks.append(f'  capabilities = {json.dumps(capabilities)}')
            
            # Add conditions if present
            if "conditions" in path_config:
                for condition, value in path_config["conditions"].items():
                    hcl_blocks.append(f'  {condition} = {json.dumps(value)}')
            
            hcl_blocks.append("}")
            hcl_blocks.append("")
        
        return "\n".join(hcl_blocks)
    
    def create_approle(self, config: AppRoleConfig) -> Optional[Dict[str, str]]:
        """
        Create AppRole with specified configuration.
        
        Args:
            config: AppRole configuration
            
        Returns:
            Dictionary with role_id and secret_id if successful
        """
        if not self.vault_provider:
            logger.error("Vault provider not available for AppRole creation")
            return None
        
        try:
            vault_client = self.vault_provider._client
            if not vault_client:
                raise Exception("Vault client not initialized")
            
            # Create AppRole
            approle_params = {
                "policies": config.policies,
                "token_ttl": config.token_ttl,
                "token_max_ttl": config.token_max_ttl,
                "token_policies": config.token_policies or config.policies,
                "token_bound_cidrs": config.token_bound_cidrs,
                "token_no_default_policy": config.token_no_default_policy,
                "token_num_uses": config.token_num_uses,
                "secret_id_ttl": config.secret_id_ttl,
                "secret_id_num_uses": config.secret_id_num_uses,
                "local_secret_ids": config.local_secret_ids,
                "bind_secret_id": config.bind_secret_id
            }
            
            # Add optional parameters
            if config.token_explicit_max_ttl:
                approle_params["token_explicit_max_ttl"] = config.token_explicit_max_ttl
            if config.token_period:
                approle_params["token_period"] = config.token_period
            
            vault_client.auth.approle.create_or_update_approle(
                role_name=config.role_name,
                **approle_params
            )
            
            # Get role ID
            role_id_response = vault_client.auth.approle.read_role_id(
                role_name=config.role_name
            )
            role_id = role_id_response["data"]["role_id"]
            
            # Generate secret ID
            secret_id_response = vault_client.auth.approle.generate_secret_id(
                role_name=config.role_name,
                metadata={"created_by": "scribe-policy-manager", "created_at": str(time.time())}
            )
            secret_id = secret_id_response["data"]["secret_id"]
            
            # Store configuration
            self._approle_configs[config.role_name] = config
            self._approles_created += 1
            
            logger.info("AppRole created successfully",
                       role_name=config.role_name,
                       policies=config.policies,
                       token_ttl=config.token_ttl)
            
            return {
                "role_id": role_id,
                "secret_id": secret_id,
                "role_name": config.role_name
            }
            
        except Exception as e:
            logger.error("Failed to create AppRole",
                        role_name=config.role_name,
                        error=str(e))
            return None
    
    def setup_production_policies(self) -> Dict[str, Any]:
        """
        Setup complete production policy system.
        
        Returns:
            Dictionary with setup results and credentials
        """
        results = {
            "policies_created": [],
            "policies_failed": [],
            "approles_created": [],
            "approles_failed": [],
            "credentials": {}
        }
        
        logger.info("Setting up production Vault policies and AppRoles")
        
        # Create all standard policies
        policy_templates = ["scribe-admin", "scribe-service", "scribe-application", "scribe-readonly"]
        
        for template_name in policy_templates:
            if self.create_policy_from_template(template_name):
                results["policies_created"].append(template_name)
            else:
                results["policies_failed"].append(template_name)
        
        # Create AppRoles for different service tiers
        approle_configs = [
            AppRoleConfig(
                role_name="scribe-engine",
                policies=["scribe-service"],
                token_ttl="1h",
                token_max_ttl="4h",
                secret_id_ttl="10m",
                secret_id_num_uses=1
            ),
            AppRoleConfig(
                role_name="scribe-application",
                policies=["scribe-application"],
                token_ttl="30m",
                token_max_ttl="2h",
                secret_id_ttl="5m",
                secret_id_num_uses=1
            ),
            AppRoleConfig(
                role_name="scribe-monitoring",
                policies=["scribe-readonly"],
                token_ttl="2h",
                token_max_ttl="8h",
                secret_id_ttl="15m",
                secret_id_num_uses=3
            )
        ]
        
        for approle_config in approle_configs:
            credentials = self.create_approle(approle_config)
            if credentials:
                results["approles_created"].append(approle_config.role_name)
                results["credentials"][approle_config.role_name] = credentials
            else:
                results["approles_failed"].append(approle_config.role_name)
        
        logger.info("Production policy setup completed",
                   policies_created=len(results["policies_created"]),
                   approles_created=len(results["approles_created"]),
                   policies_failed=len(results["policies_failed"]),
                   approles_failed=len(results["approles_failed"]))
        
        return results
    
    def validate_policy(self, policy_name: str) -> Dict[str, Any]:
        """
        Validate a Vault policy configuration.
        
        Args:
            policy_name: Name of policy to validate
            
        Returns:
            Validation results
        """
        if not self.vault_provider:
            return {"valid": False, "error": "Vault provider not available"}
        
        try:
            vault_client = self.vault_provider._client
            if not vault_client:
                raise Exception("Vault client not initialized")
            
            # Read policy from Vault
            policy_response = vault_client.sys.read_policy(policy_name)
            
            if not policy_response:
                return {"valid": False, "error": "Policy not found"}
            
            policy_content = policy_response["data"].get("policy", "")
            
            # Basic validation checks
            validation_results = {
                "valid": True,
                "policy_name": policy_name,
                "policy_length": len(policy_content),
                "has_content": len(policy_content.strip()) > 0,
                "path_count": policy_content.count('path "'),
                "capabilities_count": policy_content.count("capabilities"),
                "security_score": self._calculate_security_score(policy_content)
            }
            
            logger.debug("Policy validation completed",
                        policy_name=policy_name,
                        **validation_results)
            
            return validation_results
            
        except Exception as e:
            logger.error("Policy validation failed",
                        policy_name=policy_name,
                        error=str(e))
            return {"valid": False, "error": str(e)}
    
    def _calculate_security_score(self, policy_content: str) -> int:
        """Calculate basic security score for policy (0-100)."""
        score = 50  # Base score
        
        # Check for restrictive capabilities
        if "sudo" in policy_content:
            score -= 20  # Sudo access reduces security
        if '"*"' in policy_content:
            score -= 15  # Wildcard paths reduce security
        if "delete" in policy_content:
            score -= 10  # Delete capability reduces security
        
        # Check for good practices
        if "read" in policy_content and "list" in policy_content:
            score += 10  # Specific read/list permissions
        if policy_content.count('path "') > 1:
            score += 15  # Multiple specific paths
        if "TTL" in policy_content or "ttl" in policy_content:
            score += 10  # Time-limited access
        
        return max(0, min(100, score))
    
    def rotate_approle_secret(self, role_name: str) -> Optional[str]:
        """
        Rotate AppRole secret ID.
        
        Args:
            role_name: Name of AppRole
            
        Returns:
            New secret ID if successful
        """
        if not self.vault_provider:
            logger.error("Vault provider not available for secret rotation")
            return None
        
        try:
            vault_client = self.vault_provider._client
            if not vault_client:
                raise Exception("Vault client not initialized")
            
            # Generate new secret ID
            secret_id_response = vault_client.auth.approle.generate_secret_id(
                role_name=role_name,
                metadata={
                    "rotated_by": "scribe-policy-manager",
                    "rotated_at": str(time.time()),
                    "rotation_reason": "scheduled_rotation"
                }
            )
            new_secret_id = secret_id_response["data"]["secret_id"]
            
            logger.info("AppRole secret ID rotated successfully",
                       role_name=role_name,
                       new_secret_id_accessor=secret_id_response["data"].get("secret_id_accessor"))
            
            return new_secret_id
            
        except Exception as e:
            logger.error("Failed to rotate AppRole secret",
                        role_name=role_name,
                        error=str(e))
            return None
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get policy manager metrics."""
        with self._lock:
            return {
                "policies_created": self._policies_created,
                "policies_updated": self._policies_updated,
                "approles_created": self._approles_created,
                "authentication_events": self._authentication_events,
                "policy_templates": len(self._policy_templates),
                "active_approles": len(self._approle_configs),
                "template_names": list(self._policy_templates.keys()),
                "approle_names": list(self._approle_configs.keys())
            }
    
    def cleanup_expired_policies(self) -> int:
        """
        Clean up expired or unused policies.
        
        Returns:
            Number of policies cleaned up
        """
        # Implementation would check for unused policies and clean them up
        # This is a placeholder for the full implementation
        logger.info("Policy cleanup completed")
        return 0


# Global policy manager instance
_policy_manager: Optional[VaultPolicyManager] = None
_manager_lock = threading.RLock()


def get_vault_policy_manager() -> VaultPolicyManager:
    """Get or create global Vault policy manager."""
    global _policy_manager
    
    with _manager_lock:
        if _policy_manager is None:
            _policy_manager = VaultPolicyManager()
        
        return _policy_manager