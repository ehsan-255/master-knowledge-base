# Scribe Solutions Roadmap: Complete HMA v2.2 Compliance

## Executive Summary

This roadmap provides concrete solutions to achieve full HMA v2.2 compliance for the Scribe tool. Based on comprehensive analysis, Scribe requires **complete architectural restructuring** rather than incremental fixes. The solutions are organized by priority and provide specific implementation steps.

**Estimated Timeline**: 12-16 weeks for complete implementation
**Team Size**: 4-6 developers with HMA v2.2 expertise
**Risk Level**: High (complete rewrite required)

---

## Priority 1: Critical Mandatory Compliance Failures (Weeks 1-4)

### 1.1 Fix Plugin Manifest Schema Compliance

**Problem**: Plugin manifests claim version "2.0" but HMA v2.2 requires "2.2"

**Solution**:
```json
// Current (WRONG):
{
  "manifest_version": "2.0"
}

// Required (CORRECT):
{
  "manifest_version": "2.2",
  "hma_compliance": {
    "hma_version": "2.2",
    "tier_classification": {
      "mandatory": ["json_schema", "otel_boundary", "mtls"],
      "recommended": ["kubernetes", "nats", "prometheus"],
      "alternative": []
    },
    "boundary_interfaces": [
      {
        "port_type": "PluginExecutionPort",
        "direction": "inbound",
        "validation": "json_schema",
        "telemetry": "otel_spans"
      }
    ]
  }
}
```

**Implementation Steps**:
1. Update all 7 manifest.json files in `actions/*/manifest.json`
2. Add missing mandatory fields as shown above
3. Create schema validation script: `tools/scripts/validate_manifests.py`
4. Run validation in CI/CD pipeline

### 1.2 Implement Mandatory JSON Schema Validation at Boundaries

**Problem**: No JSON Schema validation at L1 adapter boundaries

**Solution**: Create boundary validation system
```python
# New file: core/boundary_validator.py
import jsonschema
from typing import Dict, Any

class BoundaryValidator:
    """Validates data at HMA boundary interfaces"""
    
    def __init__(self, schema_registry: Dict[str, Dict]):
        self.schemas = schema_registry
    
    def validate_l1_input(self, data: Dict[str, Any], interface: str) -> bool:
        """Validate L1 adapter input against schema"""
        schema = self.schemas.get(f"l1_{interface}_input")
        if not schema:
            raise ValueError(f"No schema found for {interface}")
        
        try:
            jsonschema.validate(data, schema)
            return True
        except jsonschema.ValidationError as e:
            self.logger.error("Boundary validation failed", 
                            interface=interface, error=str(e))
            return False

# Usage in watcher.py:
class ScribeEventHandler(FileSystemEventHandler):
    def __init__(self, event_bus, file_patterns, validator):
        self.validator = validator  # Add validator
    
    def _queue_event(self, event_type: str, file_path: str):
        event_data = {
            'event_id': str(uuid.uuid4()),
            'type': event_type,
            'file_path': file_path,
            'timestamp': time.time()
        }
        
        # MANDATORY: Validate at boundary
        if not self.validator.validate_l1_input(event_data, "file_system"):
            return  # Drop invalid events
            
        self.event_bus.publish('file_event', event_data)
```

**Implementation Steps**:
1. Create `schemas/boundary_schemas.json` with all interface schemas
2. Implement `BoundaryValidator` class
3. Update all L1 adapters to use validation
4. Add validation metrics to observability

### 1.3 Implement Mandatory OpenTelemetry Boundary Telemetry

**Problem**: Missing mandatory OTEL resource attributes and boundary instrumentation

**Solution**: Complete OTEL integration
```python
# New file: core/hma_telemetry.py
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

class HMATelemetry:
    """HMA v2.2 compliant OpenTelemetry implementation"""
    
    def __init__(self, component_type: str, component_id: str, layer: str):
        # MANDATORY: HMA resource attributes
        resource = Resource.create({
            "hma.component.type": component_type,  # L2-Core | L2-Orchestrator | L3-Capability
            "hma.component.id": component_id,
            "hma.layer": layer,  # L2 | L3
            "service.name": component_id,
            "service.version": "2.0.0"
        })
        
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter())
        )
        trace.set_tracer_provider(provider)
        self.tracer = trace.get_tracer(__name__)
    
    def trace_boundary_call(self, operation: str, boundary_type: str):
        """Trace calls across HMA boundaries"""
        return self.tracer.start_as_current_span(
            f"hma.boundary.{boundary_type}.{operation}",
            attributes={
                "hma.boundary.type": boundary_type,
                "hma.operation": operation
            }
        )

# Usage in engine.py:
class ScribeEngine:
    def __init__(self):
        # Initialize HMA telemetry
        self.telemetry = HMATelemetry("L2-Core", "scribe-engine", "L2")
    
    def start(self):
        with self.telemetry.trace_boundary_call("engine_start", "l2_core"):
            # Existing start logic
            pass
```

**Implementation Steps**:
1. Install OTEL dependencies: `opentelemetry-api`, `opentelemetry-sdk`, `opentelemetry-exporter-otlp`
2. Create `HMATelemetry` class with mandatory attributes
3. Update all boundary crossings to emit traces
4. Configure OTEL collector endpoint
5. Add dashboards for HMA boundary metrics

### 1.4 Implement Mandatory mTLS for Inter-Plugin Communication

**Problem**: Plugin-to-plugin communication lacks mTLS security

**Solution**: Add mTLS to EventBus and Core communication
```python
# Enhanced: core/mtls.py
import ssl
import socket
from pathlib import Path

class HMASecureTransport:
    """HMA v2.2 compliant mTLS transport"""
    
    def __init__(self, cert_path: str, key_path: str, ca_path: str):
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_cert_chain(cert_path, key_path)
        self.context.load_verify_locations(ca_path)
    
    def create_secure_connection(self, host: str, port: int):
        """Create mTLS connection for plugin communication"""
        sock = socket.create_connection((host, port))
        secure_sock = self.context.wrap_socket(sock, server_hostname=host)
        return secure_sock

# Enhanced: core/event_bus.py  
class SecureEventBus:
    """HMA v2.2 compliant EventBus with mTLS"""
    
    def __init__(self, transport: HMASecureTransport):
        self.transport = transport
        self.subscribers = {}
        self.message_queue = asyncio.Queue()
    
    async def publish_secure(self, event_type: str, data: dict, target_plugin: str):
        """Publish event with mTLS to specific plugin"""
        with self.telemetry.trace_boundary_call("event_publish", "inter_plugin"):
            # Encrypt and send via mTLS
            connection = self.transport.create_secure_connection(
                target_plugin, 
                self.get_plugin_port(target_plugin)
            )
            encrypted_data = self.encrypt_event(data)
            connection.send(encrypted_data)
```

**Implementation Steps**:
1. Generate CA and plugin certificates using script
2. Update `SecureEventBus` with mTLS support
3. Modify all plugin communication to use secure channels
4. Add certificate rotation mechanism
5. Update configuration to include certificate paths

---

## Priority 2: Architectural Restructuring (Weeks 5-8)

### 2.1 Implement Proper HMA Port Abstractions

**Problem**: Missing mandatory HMA port types

**Solution**: Create complete port system
```python
# New file: core/hma_ports.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class PluginExecutionPort(ABC):
    """HMA v2.2 mandatory port for plugin execution"""
    
    @abstractmethod
    async def execute_plugin(self, plugin_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute plugin with validated input"""
        pass
    
    @abstractmethod
    def get_plugin_status(self, plugin_id: str) -> str:
        """Get current plugin execution status"""
        pass

class CredBrokerQueryPort(ABC):
    """HMA v2.2 mandatory port for credential access"""
    
    @abstractmethod
    async def get_credential(self, credential_id: str, requesting_plugin: str) -> Optional[str]:
        """Retrieve credential with access control"""
        pass
    
    @abstractmethod
    async def validate_access(self, credential_id: str, plugin_id: str) -> bool:
        """Validate plugin access to credential"""
        pass

class EventBusPort(ABC):
    """HMA v2.2 mandatory port for event communication"""
    
    @abstractmethod
    async def publish_event(self, event: Dict[str, Any], target: Optional[str] = None):
        """Publish event with optional targeting"""
        pass
    
    @abstractmethod
    async def subscribe_to_events(self, event_types: List[str], callback):
        """Subscribe to specific event types"""
        pass

class ObservabilityPort(ABC):
    """HMA v2.2 mandatory port for telemetry"""
    
    @abstractmethod
    def emit_metric(self, name: str, value: float, labels: Dict[str, str]):
        """Emit metric with HMA labels"""
        pass
    
    @abstractmethod
    def start_span(self, operation: str, parent=None):
        """Start distributed trace span"""
        pass

# Implementation classes:
class ScribePluginExecutionAdapter(PluginExecutionPort):
    """Concrete implementation of plugin execution"""
    
    def __init__(self, plugin_loader, security_manager, telemetry):
        self.plugin_loader = plugin_loader
        self.security_manager = security_manager
        self.telemetry = telemetry
    
    async def execute_plugin(self, plugin_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        with self.telemetry.start_span(f"plugin.execute.{plugin_id}"):
            # Validate plugin access
            if not await self.security_manager.validate_plugin_access(plugin_id):
                raise PermissionError(f"Plugin {plugin_id} access denied")
            
            # Load and execute plugin
            plugin = self.plugin_loader.get_plugin(plugin_id)
            result = await plugin.execute_async(input_data)
            return result
```

**Implementation Steps**:
1. Create all mandatory HMA ports as abstract base classes
2. Implement concrete adapter classes for each port
3. Update existing components to use ports instead of direct calls
4. Add port registry system for dependency injection
5. Create port validation tests

### 2.2 Restructure Core as Minimal Router/Lifecycle Manager

**Problem**: Core contains business logic violating microkernel principle

**Solution**: Redesign core architecture
```python
# Redesigned: core/minimal_core.py
class HMAMinimalCore:
    """HMA v2.2 compliant minimal core - routing and lifecycle only"""
    
    def __init__(self, ports: Dict[str, Any]):
        self.plugin_execution_port = ports['plugin_execution']
        self.cred_broker_port = ports['cred_broker']
        self.event_bus_port = ports['event_bus']
        self.observability_port = ports['observability']
        
        self.plugin_registry = {}
        self.routing_table = {}
        self.lifecycle_manager = PluginLifecycleManager()
    
    async def route_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Core responsibility: Route requests to appropriate plugins"""
        with self.observability_port.start_span("core.route_request"):
            # Determine target plugin based on request
            plugin_id = self._resolve_plugin(request)
            
            # Route to plugin via port (no business logic here)
            return await self.plugin_execution_port.execute_plugin(plugin_id, request)
    
    def _resolve_plugin(self, request: Dict[str, Any]) -> str:
        """Simple routing logic - no business processing"""
        event_type = request.get('type')
        return self.routing_table.get(event_type, 'default_handler')
    
    async def register_plugin(self, plugin_manifest: Dict[str, Any]):
        """Core responsibility: Plugin lifecycle management"""
        plugin_id = plugin_manifest['plugin']['id']
        
        # Validate manifest schema
        if not self._validate_manifest(plugin_manifest):
            raise ValueError(f"Invalid manifest for {plugin_id}")
        
        # Register with lifecycle manager
        await self.lifecycle_manager.register(plugin_id, plugin_manifest)
        self.plugin_registry[plugin_id] = plugin_manifest
        
        # Update routing table
        self._update_routing(plugin_id, plugin_manifest)

# Separate business logic to L2 Orchestrator Plugin:
class LLMWorkflowOrchestrator:
    """L2 Orchestrator Plugin for complex workflows"""
    
    def __init__(self, core_ports):
        self.plugin_port = core_ports['plugin_execution']
        self.event_port = core_ports['event_bus']
    
    async def orchestrate_file_processing(self, file_event: Dict[str, Any]):
        """Orchestrate multi-plugin workflow for file processing"""
        # This is business logic - belongs in L2 Orchestrator, not Core
        
        # Step 1: Frontmatter enhancement
        result1 = await self.plugin_port.execute_plugin('frontmatter_enhancer', file_event)
        
        # Step 2: Naming validation
        result2 = await self.plugin_port.execute_plugin('naming_validator', result1)
        
        # Step 3: Graph validation  
        result3 = await self.plugin_port.execute_plugin('graph_validator', result2)
        
        return result3
```

**Implementation Steps**:
1. Extract all business logic from current core
2. Implement `HMAMinimalCore` with only routing/lifecycle
3. Create separate L2 Orchestrator plugins for workflows
4. Update all components to use new core interface
5. Add comprehensive core functionality tests

### 2.3 Implement Proper L2 Orchestrator Plugins

**Problem**: LLM-driven coordination treated as L3 capabilities instead of L2 orchestrators

**Solution**: Create dedicated L2 orchestrator system
```python
# New file: orchestrators/base_orchestrator.py
from abc import ABC, abstractmethod

class BaseOrchestrator(ABC):
    """Base class for L2 Orchestrator Plugins"""
    
    def __init__(self, orchestrator_id: str, core_ports: Dict[str, Any]):
        self.orchestrator_id = orchestrator_id
        self.plugin_port = core_ports['plugin_execution']
        self.event_port = core_ports['event_bus']
        self.observability_port = core_ports['observability']
    
    @abstractmethod
    async def orchestrate(self, trigger_event: Dict[str, Any]) -> Dict[str, Any]:
        """Main orchestration logic"""
        pass
    
    @abstractmethod
    def get_orchestration_pattern(self) -> Dict[str, Any]:
        """Return orchestration pattern this handles"""
        pass

# New file: orchestrators/llm_file_orchestrator.py
class LLMFileProcessingOrchestrator(BaseOrchestrator):
    """L2 Orchestrator for LLM-driven file processing workflows"""
    
    def __init__(self, core_ports, llm_client):
        super().__init__('llm_file_processor', core_ports)
        self.llm_client = llm_client
    
    async def orchestrate(self, trigger_event: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate file processing using LLM for decision making"""
        
        with self.observability_port.start_span("orchestrator.llm_file_processing"):
            file_path = trigger_event['file_path']
            
            # Use LLM to determine processing strategy
            strategy = await self._determine_strategy(file_path, trigger_event)
            
            # Execute strategy by coordinating L3 plugins
            if strategy == 'markdown_enhancement':
                return await self._orchestrate_markdown_enhancement(trigger_event)
            elif strategy == 'validation_only':
                return await self._orchestrate_validation(trigger_event)
            else:
                return await self._orchestrate_default(trigger_event)
    
    async def _determine_strategy(self, file_path: str, event: Dict[str, Any]) -> str:
        """Use LLM to determine optimal processing strategy"""
        prompt = f"""
        Analyze this file event and determine the best processing strategy:
        File: {file_path}
        Event: {event['type']}
        
        Available strategies:
        1. markdown_enhancement - Full frontmatter + validation
        2. validation_only - Just validate existing content  
        3. default - Basic processing
        
        Return strategy name only.
        """
        
        response = await self.llm_client.complete(prompt)
        return response.strip().lower()
    
    async def _orchestrate_markdown_enhancement(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate multiple L3 plugins for full markdown enhancement"""
        
        # Plugin 1: Enhanced frontmatter
        step1_result = await self.plugin_port.execute_plugin(
            'enhanced_frontmatter_action', 
            event
        )
        
        # Plugin 2: Naming enforcement
        step2_result = await self.plugin_port.execute_plugin(
            'naming_enforcement_action',
            step1_result
        )
        
        # Plugin 3: Graph validation
        final_result = await self.plugin_port.execute_plugin(
            'graph_validation_action',
            step2_result
        )
        
        return final_result

# Orchestrator manifest:
# orchestrators/llm_file_orchestrator/manifest.json
{
  "manifest_version": "2.2",
  "plugin_metadata": {
    "name": "llm_file_orchestrator",
    "version": "2.0.0",
    "type": "L2-Orchestrator",
    "description": "LLM-driven orchestrator for file processing workflows"
  },
  "hma_compliance": {
    "hma_version": "2.2",
    "tier_classification": {
      "mandatory": ["plugin_execution_port", "event_bus_port"],
      "recommended": ["llm_integration"],
      "alternative": []
    }
  }
}
```

**Implementation Steps**:
1. Create `BaseOrchestrator` abstract class
2. Move LLM logic from L3 plugins to L2 orchestrators
3. Create orchestrator registry and lifecycle management
4. Update core to route complex workflows to orchestrators
5. Add orchestrator health monitoring

---

## Priority 3: Windows-Specific Fixes (Weeks 9-10)

### 3.1 Fix File Path Handling

**Problem**: Manual path separator replacement and missing Windows-specific handling

**Solution**: Proper Windows path handling
```python
# Enhanced: core/windows_file_utils.py
import os
import ctypes
from ctypes import wintypes
from pathlib import Path, PurePath
import win32file
import win32api

class WindowsFileHandler:
    """Windows-specific file handling with proper path support"""
    
    @staticmethod
    def normalize_path(path_input: str) -> Path:
        """Properly normalize paths for Windows"""
        # Use pathlib for cross-platform normalization
        path = Path(path_input).resolve()
        
        # Handle long path names on Windows
        if os.name == 'nt' and len(str(path)) > 260:
            # Use \\?\ prefix for long paths
            return Path(f"\\\\?\\{path}")
        
        return path
    
    @staticmethod
    def is_case_sensitive_match(path1: str, path2: str) -> bool:
        """Check if paths match considering Windows case insensitivity"""
        if os.name == 'nt':
            return Path(path1).resolve() == Path(path2).resolve()
        else:
            return path1 == path2
    
    @staticmethod
    def get_windows_permissions(file_path: str) -> Dict[str, bool]:
        """Get Windows ACL permissions"""
        try:
            # Get Windows ACL information
            security_descriptor = win32api.GetFileSecurity(
                file_path, 
                win32file.OWNER_SECURITY_INFORMATION | win32file.DACL_SECURITY_INFORMATION
            )
            
            return {
                'readable': os.access(file_path, os.R_OK),
                'writable': os.access(file_path, os.W_OK),
                'executable': os.access(file_path, os.X_OK)
            }
        except Exception as e:
            logger.warning(f"Failed to get Windows permissions: {e}")
            return {'readable': False, 'writable': False, 'executable': False}

# Updated: core/rule_processor.py
class RuleProcessor:
    def _normalize_file_path(self, file_path: str) -> str:
        """Properly normalize file paths cross-platform"""
        # WRONG (current implementation):
        # full_path_str = str(path_obj).replace('\\', '/')
        
        # CORRECT (new implementation):
        if os.name == 'nt':
            return str(WindowsFileHandler.normalize_path(file_path))
        else:
            return str(Path(file_path).resolve())
    
    def matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if file matches pattern with case sensitivity handling"""
        normalized_path = self._normalize_file_path(file_path)
        
        if os.name == 'nt':
            # Windows case-insensitive matching
            return Path(normalized_path).match(pattern.lower())
        else:
            # Unix case-sensitive matching
            return Path(normalized_path).match(pattern)
```

**Implementation Steps**:
1. Install Windows dependencies: `pywin32`
2. Replace all manual path operations with `WindowsFileHandler`
3. Update all file pattern matching to handle case insensitivity
4. Add comprehensive Windows path tests
5. Test with paths > 260 characters

### 3.2 Enhanced Atomic Write Operations for Windows

**Problem**: Windows file locking issues causing write failures

**Solution**: Robust Windows atomic write implementation
```python
# Enhanced: core/windows_atomic_write.py
import os
import tempfile
import time
import ctypes
from ctypes import wintypes
import win32file
import win32con
import win32api
from pathlib import Path

class WindowsAtomicWriter:
    """Windows-optimized atomic write operations"""
    
    def __init__(self):
        self.max_retries = 10
        self.base_delay = 0.05
        self.max_delay = 2.0
    
    def atomic_write(self, filepath: str, data: str, encoding: str = 'utf-8') -> bool:
        """Atomic write with Windows-specific optimizations"""
        filepath = Path(filepath)
        temp_path = None
        
        try:
            # Create temp file with Windows-specific flags
            temp_fd, temp_path = tempfile.mkstemp(
                dir=filepath.parent,
                prefix=f".{filepath.name}.tmp.",
                suffix=".atomic"
            )
            
            temp_path = Path(temp_path)
            
            # Write data with proper encoding
            with os.fdopen(temp_fd, 'w', encoding=encoding) as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            
            temp_fd = None  # File is closed
            
            # Atomic move with Windows retry logic
            return self._atomic_move_windows(temp_path, filepath)
            
        except Exception as e:
            logger.error(f"Atomic write failed: {e}")
            return False
        finally:
            if temp_fd is not None:
                try:
                    os.close(temp_fd)
                except:
                    pass
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                except:
                    pass
    
    def _atomic_move_windows(self, src: Path, dst: Path) -> bool:
        """Windows-specific atomic move with comprehensive retry logic"""
        
        for attempt in range(self.max_retries):
            try:
                # Method 1: Try standard os.replace (fastest)
                os.replace(str(src), str(dst))
                return True
                
            except PermissionError as e:
                if "being used by another process" in str(e):
                    # File is locked - wait and retry
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    time.sleep(delay)
                    continue
                else:
                    # Permission issue - try alternative method
                    if self._try_win32_move(src, dst):
                        return True
                    
            except FileExistsError:
                # Target exists - try to remove and retry
                try:
                    dst.unlink()
                    continue
                except Exception:
                    pass
                    
            except OSError as e:
                if e.winerror == 32:  # ERROR_SHARING_VIOLATION
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    time.sleep(delay)
                    continue
                else:
                    break
        
        logger.error(f"Failed to atomically move after {self.max_retries} attempts")
        return False
    
    def _try_win32_move(self, src: Path, dst: Path) -> bool:
        """Fallback using Win32 API for stubborn files"""
        try:
            # Use MoveFileEx with replace existing flag
            win32file.MoveFileEx(
                str(src), 
                str(dst), 
                win32file.MOVEFILE_REPLACE_EXISTING | win32file.MOVEFILE_WRITE_THROUGH
            )
            return True
        except Exception as e:
            logger.debug(f"Win32 move failed: {e}")
            return False
```

**Implementation Steps**:
1. Replace existing `atomic_write.py` with Windows-optimized version
2. Add comprehensive retry logic for file locking
3. Implement Win32 API fallbacks for stubborn files
4. Add file lock detection and graceful handling
5. Test with high-concurrency scenarios

### 3.3 Windows Process Management

**Problem**: Process execution issues on Windows

**Solution**: Windows-specific process handling
```python
# Enhanced: core/windows_process_manager.py
import subprocess
import signal
import os
import threading
import win32process
import win32api
import win32con
from typing import List, Optional, Tuple

class WindowsProcessManager:
    """Windows-optimized process execution and management"""
    
    def execute_command_safely(self, 
                             command_list: List[str], 
                             cwd: Optional[str] = None,
                             timeout: int = 30,
                             allowed_env_vars: Optional[List[str]] = None) -> Tuple[bool, str, str]:
        """Execute command with Windows-specific optimizations"""
        
        try:
            # Prepare environment
            env = self._prepare_windows_env(allowed_env_vars)
            
            # Set Windows-specific creation flags
            creation_flags = (
                subprocess.CREATE_NEW_PROCESS_GROUP |  # Allow clean termination
                subprocess.CREATE_NO_WINDOW           # No console window
            )
            
            # Execute with proper Windows handling
            process = subprocess.Popen(
                command_list,
                cwd=cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                text=True,
                shell=False,  # Never use shell=True
                creationflags=creation_flags
            )
            
            # Windows-specific timeout handling
            stdout, stderr = self._communicate_with_timeout(process, timeout)
            
            success = process.returncode == 0
            return success, stdout, stderr
            
        except Exception as e:
            logger.error(f"Process execution failed: {e}")
            return False, "", str(e)
    
    def _communicate_with_timeout(self, process, timeout: int) -> Tuple[str, str]:
        """Windows-specific process communication with timeout"""
        
        def kill_process():
            """Kill process tree on Windows"""
            try:
                # Kill entire process tree
                win32process.TerminateProcess(process._handle, 1)
            except:
                # Fallback to SIGTERM
                try:
                    os.kill(process.pid, signal.SIGTERM)
                except:
                    pass
        
        # Set up timeout timer
        timer = threading.Timer(timeout, kill_process)
        timer.start()
        
        try:
            stdout, stderr = process.communicate()
            timer.cancel()
            return stdout or "", stderr or ""
        except Exception as e:
            timer.cancel()
            kill_process()
            raise e
    
    def _prepare_windows_env(self, allowed_vars: Optional[List[str]]) -> Dict[str, str]:
        """Prepare Windows environment variables"""
        if allowed_vars is None:
            # Use current environment
            return dict(os.environ)
        
        # Filter environment variables
        env = {}
        for var in allowed_vars:
            if var in os.environ:
                env[var] = os.environ[var]
        
        # Always include essential Windows variables
        essential_vars = ['SYSTEMROOT', 'PATH', 'PATHEXT', 'COMSPEC']
        for var in essential_vars:
            if var in os.environ:
                env[var] = os.environ[var]
        
        return env
```

**Implementation Steps**:
1. Install Windows process dependencies: `pywin32`
2. Replace process execution in `security_manager.py`
3. Add proper process tree termination
4. Implement Windows environment variable filtering
5. Test process timeout and termination scenarios

---

## Priority 4: Security and Performance Enhancements (Weeks 11-12)

### 4.1 Implement Comprehensive Plugin Sandboxing

**Problem**: Inadequate plugin security isolation

**Solution**: Multi-layer plugin sandboxing
```python
# New file: core/plugin_sandbox.py
import os
import tempfile
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List

class PluginSandbox:
    """Comprehensive plugin sandboxing system"""
    
    def __init__(self, sandbox_root: str):
        self.sandbox_root = Path(sandbox_root)
        self.sandbox_root.mkdir(parents=True, exist_ok=True)
    
    def create_plugin_sandbox(self, plugin_id: str) -> str:
        """Create isolated sandbox for plugin"""
        plugin_sandbox = self.sandbox_root / plugin_id
        plugin_sandbox.mkdir(parents=True, exist_ok=True)
        
        # Create restricted directory structure
        subdirs = ['input', 'output', 'temp', 'logs']
        for subdir in subdirs:
            (plugin_sandbox / subdir).mkdir(exist_ok=True)
        
        # Set restrictive permissions
        if os.name == 'nt':
            self._set_windows_permissions(plugin_sandbox)
        else:
            os.chmod(plugin_sandbox, 0o750)
        
        return str(plugin_sandbox)
    
    def execute_plugin_sandboxed(self, 
                                plugin_id: str, 
                                plugin_code: str, 
                                input_data: Dict[str, Any],
                                timeout: int = 60) -> Dict[str, Any]:
        """Execute plugin in complete isolation"""
        
        sandbox_path = self.create_plugin_sandbox(plugin_id)
        
        try:
            # Write input data to sandbox
            input_file = Path(sandbox_path) / 'input' / 'data.json'
            with open(input_file, 'w') as f:
                json.dump(input_data, f)
            
            # Create isolated Python environment
            result = self._run_in_isolation(
                plugin_code, 
                sandbox_path, 
                timeout
            )
            
            return result
            
        finally:
            # Cleanup sandbox
            self._cleanup_sandbox(sandbox_path)
    
    def _run_in_isolation(self, plugin_code: str, sandbox_path: str, timeout: int) -> Dict[str, Any]:
        """Run plugin in completely isolated environment"""
        
        # Create wrapper script that limits plugin capabilities
        wrapper_script = f"""
import sys
import os
import json
import tempfile
from pathlib import Path

# Restrict sys.path to prevent escaping sandbox
sys.path = ['{sandbox_path}', '/usr/lib/python3.9', '/usr/lib/python3.9/site-packages']

# Block dangerous modules
blocked_modules = ['subprocess', 'os.system', 'eval', 'exec', '__import__']
for module in blocked_modules:
    sys.modules[module] = None

# Load input data
with open('{sandbox_path}/input/data.json', 'r') as f:
    input_data = json.load(f)

# Execute plugin code with restricted globals
restricted_globals = {{
    '__builtins__': {{
        'len': len, 'str': str, 'int': int, 'float': float, 
        'dict': dict, 'list': list, 'tuple': tuple,
        'print': print, 'open': open
    }},
    'input_data': input_data
}}

try:
    # Execute plugin code
    exec('''{plugin_code}''', restricted_globals)
    
    # Get result from plugin
    result = restricted_globals.get('result', {{}})
    
    # Write result
    with open('{sandbox_path}/output/result.json', 'w') as f:
        json.dump(result, f)
        
except Exception as e:
    error_result = {{'error': str(e), 'success': False}}
    with open('{sandbox_path}/output/result.json', 'w') as f:
        json.dump(error_result, f)
"""
        
        # Execute in isolated subprocess
        wrapper_file = Path(sandbox_path) / 'wrapper.py'
        with open(wrapper_file, 'w') as f:
            f.write(wrapper_script)
        
        # Run with strict limits
        process = subprocess.Popen(
            ['python', str(wrapper_file)],
            cwd=sandbox_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': sandbox_path}
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            
            # Read result
            result_file = Path(sandbox_path) / 'output' / 'result.json'
            if result_file.exists():
                with open(result_file, 'r') as f:
                    return json.load(f)
            else:
                return {'error': 'No result produced', 'success': False}
                
        except subprocess.TimeoutExpired:
            process.kill()
            return {'error': 'Plugin execution timeout', 'success': False}
```

**Implementation Steps**:
1. Create plugin sandbox infrastructure
2. Implement restricted execution environment
3. Add resource limits (memory, CPU, file handles)
4. Create security policy enforcement
5. Add comprehensive sandbox testing

### 4.2 Implement Thread-Safe Event Processing

**Problem**: Thread safety issues in EventBus and Worker components

**Solution**: Thread-safe event processing system
```python
# Enhanced: core/thread_safe_event_bus.py
import asyncio
import threading
from typing import Dict, List, Callable, Any
from concurrent.futures import ThreadPoolExecutor
import queue

class ThreadSafeEventBus:
    """Thread-safe EventBus with proper synchronization"""
    
    def __init__(self, max_workers: int = 4, max_queue_size: int = 1000):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue = queue.Queue(maxsize=max_queue_size)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.RLock()
        self.running = False
        self.worker_thread = None
    
    def start(self):
        """Start event processing"""
        with self.lock:
            if self.running:
                return
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_events, daemon=True)
            self.worker_thread.start()
    
    def stop(self):
        """Stop event processing gracefully"""
        with self.lock:
            self.running = False
            if self.worker_thread:
                self.worker_thread.join(timeout=5.0)
            self.executor.shutdown(wait=True)
    
    def subscribe(self, event_type: str, callback: Callable):
        """Thread-safe subscription"""
        with self.lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """Thread-safe unsubscription"""
        with self.lock:
            if event_type in self.subscribers:
                try:
                    self.subscribers[event_type].remove(callback)
                except ValueError:
                    pass
    
    def publish(self, event_type: str, data: Dict[str, Any]):
        """Thread-safe event publishing with backpressure handling"""
        try:
            self.event_queue.put({
                'type': event_type,
                'data': data,
                'timestamp': time.time()
            }, timeout=1.0)  # Backpressure: drop if queue full
        except queue.Full:
            logger.warning(f"Event queue full, dropping event: {event_type}")
    
    def _process_events(self):
        """Process events in dedicated thread"""
        while self.running:
            try:
                event = self.event_queue.get(timeout=1.0)
                self._handle_event(event)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Event processing error: {e}")
    
    def _handle_event(self, event: Dict[str, Any]):
        """Handle individual event with thread safety"""
        event_type = event['type']
        
        with self.lock:
            callbacks = self.subscribers.get(event_type, []).copy()
        
        # Execute callbacks in thread pool
        for callback in callbacks:
            self.executor.submit(self._safe_callback_execution, callback, event)
    
    def _safe_callback_execution(self, callback: Callable, event: Dict[str, Any]):
        """Execute callback with error handling"""
        try:
            callback(event['data'])
        except Exception as e:
            logger.error(f"Callback execution failed: {e}", 
                        callback=str(callback), event_type=event['type'])

# Enhanced: worker.py
class ThreadSafeWorker:
    """Thread-safe worker with proper synchronization"""
    
    def __init__(self, event_bus: ThreadSafeEventBus):
        self.event_bus = event_bus
        self.running = False
        self.stats_lock = threading.Lock()
        self.events_processed = 0
        self.events_failed = 0
    
    def start(self):
        """Start worker with thread safety"""
        self.running = True
        self.event_bus.subscribe('file_event', self._process_event_safe)
    
    def _process_event_safe(self, event: Dict[str, Any]):
        """Thread-safe event processing"""
        try:
            self._process_event_internal(event)
            with self.stats_lock:
                self.events_processed += 1
        except Exception as e:
            logger.error(f"Event processing failed: {e}")
            with self.stats_lock:
                self.events_failed += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get thread-safe statistics"""
        with self.stats_lock:
            return {
                'events_processed': self.events_processed,
                'events_failed': self.events_failed,
                'success_rate': self.events_processed / max(self.events_processed + self.events_failed, 1) * 100
            }
```

**Implementation Steps**:
1. Replace existing EventBus with thread-safe version
2. Add proper synchronization to all shared resources
3. Implement backpressure handling for event queues
4. Add thread pool management for callback execution
5. Create comprehensive concurrency tests

---

## Priority 5: Production Deployment and Monitoring (Weeks 13-16)

### 5.1 Complete HMA v2.2 Observability Integration

**Problem**: Incomplete observability stack

**Solution**: Full HMA v2.2 compliant observability
```python
# New file: observability/hma_observability_stack.py
from opentelemetry import trace, metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from prometheus_client import start_http_server

class HMAObservabilityStack:
    """Complete HMA v2.2 observability implementation"""
    
    def __init__(self, service_name: str, jaeger_endpoint: str, prometheus_port: int = 8000):
        self.service_name = service_name
        self.setup_tracing(jaeger_endpoint)
        self.setup_metrics(prometheus_port)
        self.setup_logging()
    
    def setup_tracing(self, jaeger_endpoint: str):
        """Setup distributed tracing with Jaeger"""
        tracer_provider = TracerProvider(resource=self._create_hma_resource())
        
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
            collector_endpoint=jaeger_endpoint
        )
        
        tracer_provider.add_span_processor(
            BatchSpanProcessor(jaeger_exporter)
        )
        
        trace.set_tracer_provider(tracer_provider)
        self.tracer = trace.get_tracer(__name__)
    
    def setup_metrics(self, prometheus_port: int):
        """Setup metrics with Prometheus"""
        metric_reader = PrometheusMetricReader()
        meter_provider = MeterProvider(
            resource=self._create_hma_resource(),
            metric_readers=[metric_reader]
        )
        
        metrics.set_meter_provider(meter_provider)
        self.meter = metrics.get_meter(__name__)
        
        # Start Prometheus server
        start_http_server(prometheus_port)
        
        # Create HMA-specific metrics
        self._create_hma_metrics()
    
    def _create_hma_metrics(self):
        """Create HMA v2.2 mandatory metrics"""
        self.boundary_calls_counter = self.meter.create_counter(
            "hma_boundary_calls_total",
            description="Total HMA boundary calls",
            unit="1"
        )
        
        self.plugin_execution_histogram = self.meter.create_histogram(
            "hma_plugin_execution_duration_seconds",
            description="Plugin execution duration",
            unit="s"
        )
        
        self.active_plugins_gauge = self.meter.create_up_down_counter(
            "hma_active_plugins",
            description="Number of active plugins",
            unit="1"
        )
    
    def _create_hma_resource(self):
        """Create HMA v2.2 compliant resource attributes"""
        from opentelemetry.sdk.resources import Resource
        
        return Resource.create({
            "service.name": self.service_name,
            "service.version": "2.0.0",
            "hma.component.type": "L2-Core",
            "hma.component.id": self.service_name,
            "hma.layer": "L2",
            "hma.version": "2.2"
        })
    
    def trace_boundary_operation(self, operation: str, boundary_type: str, component_id: str):
        """Trace HMA boundary operations"""
        return self.tracer.start_as_current_span(
            f"hma.{boundary_type}.{operation}",
            attributes={
                "hma.boundary.type": boundary_type,
                "hma.operation": operation,
                "hma.component.id": component_id
            }
        )
    
    def record_boundary_call(self, boundary_type: str, component_from: str, component_to: str):
        """Record boundary call metrics"""
        self.boundary_calls_counter.add(1, {
            "boundary_type": boundary_type,
            "component_from": component_from,
            "component_to": component_to
        })

# Integration with core components:
# In engine.py:
class ScribeEngine:
    def __init__(self):
        self.observability = HMAObservabilityStack(
            service_name="scribe-engine",
            jaeger_endpoint="http://localhost:14268/api/traces"
        )
    
    def start(self):
        with self.observability.trace_boundary_operation("engine_start", "l2_core", "scribe-engine"):
            # Existing start logic
            self.observability.record_boundary_call("l2_core", "external", "scribe-engine")
```

**Implementation Steps**:
1. Install observability stack: Jaeger, Prometheus, Grafana
2. Implement complete HMA telemetry integration
3. Create HMA-specific dashboards and alerts
4. Add distributed tracing across all components
5. Setup log aggregation and correlation

### 5.2 Production-Ready Configuration Management

**Problem**: Configuration system not production-ready

**Solution**: Enterprise configuration management
```yaml
# New file: config/production.yaml
scribe:
  version: "2.0.0"
  environment: "production"
  
  # HMA v2.2 Mandatory Settings
  hma_compliance:
    version: "2.2"
    mandatory_features:
      - boundary_validation
      - mtls_communication
      - otel_telemetry
      - plugin_manifests
    
  # Security Configuration
  security:
    mtls:
      enabled: true
      cert_path: "/etc/scribe/certs/server.crt"
      key_path: "/etc/scribe/certs/server.key"
      ca_path: "/etc/scribe/certs/ca.crt"
      cipher_suites:
        - "ECDHE-RSA-AES256-GCM-SHA384"
        - "ECDHE-RSA-AES128-GCM-SHA256"
    
    plugin_sandbox:
      enabled: true
      sandbox_root: "/var/lib/scribe/sandbox"
      resource_limits:
        max_memory_mb: 512
        max_cpu_percent: 25
        max_file_handles: 100
        timeout_seconds: 300
    
  # Performance Configuration
  performance:
    event_processing:
      max_workers: 8
      queue_size: 2000
      batch_size: 50
      batch_timeout_ms: 100
    
    caching:
      enabled: true
      max_size: 10000
      ttl_seconds: 3600
      cleanup_interval_seconds: 300
    
  # Observability Configuration
  observability:
    jaeger:
      endpoint: "http://jaeger-collector:14268/api/traces"
      service_name: "scribe-engine"
    
    prometheus:
      port: 8000
      metrics_path: "/metrics"
    
    logging:
      level: "INFO"
      format: "json"
      output: "stdout"
    
  # Plugin Configuration
  plugins:
    directories:
      - "/etc/scribe/plugins"
      - "/var/lib/scribe/custom-plugins"
    
    lifecycle:
      health_check_interval_seconds: 30
      restart_policy: "on-failure"
      max_restarts: 3
    
    communication:
      event_bus:
        type: "nats"
        url: "nats://nats-server:4222"
      
      direct_calls:
        enabled: false  # Force event-driven communication
    
  # Storage Configuration
  storage:
    atomic_writes:
      retry_attempts: 10
      retry_delay_ms: 100
      max_retry_delay_ms: 5000
    
    backup:
      enabled: true
      interval_hours: 6
      retention_days: 30
      location: "/var/backups/scribe"

# Kubernetes deployment:
# deployment/kubernetes/scribe-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scribe-engine
  labels:
    app: scribe-engine
    hma.component.type: L2-Core
spec:
  replicas: 3
  selector:
    matchLabels:
      app: scribe-engine
  template:
    metadata:
      labels:
        app: scribe-engine
        hma.component.type: L2-Core
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: scribe-engine
        image: scribe-engine:v2.0.0
        ports:
        - containerPort: 8000
          name: metrics
        - containerPort: 9469
          name: health
        env:
        - name: SCRIBE_CONFIG_PATH
          value: "/etc/scribe/config/production.yaml"
        - name: SCRIBE_ENVIRONMENT
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "200m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 9469
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 9469
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: config
          mountPath: /etc/scribe/config
        - name: certs
          mountPath: /etc/scribe/certs
        - name: sandbox
          mountPath: /var/lib/scribe/sandbox
      volumes:
      - name: config
        configMap:
          name: scribe-config
      - name: certs
        secret:
          secretName: scribe-tls-certs
      - name: sandbox
        emptyDir:
          sizeLimit: 1Gi
```

**Implementation Steps**:
1. Create environment-specific configuration files
2. Implement configuration validation and hot-reloading
3. Add secrets management integration
4. Create production deployment manifests
5. Setup configuration monitoring and alerting

### 5.3 Comprehensive Testing and Validation Framework

**Problem**: Insufficient testing coverage

**Solution**: Complete HMA v2.2 testing framework
```python
# New file: tests/hma_compliance_tests.py
import pytest
import json
from pathlib import Path
from typing import Dict, Any

class HMAComplianceTestSuite:
    """Comprehensive HMA v2.2 compliance testing"""
    
    def test_mandatory_boundary_compliance(self):
        """Test all mandatory boundary requirements"""
        
        # Test JSON Schema validation at boundaries
        assert self._test_json_schema_boundaries()
        
        # Test OpenAPI documentation
        assert self._test_openapi_documentation()
        
        # Test mTLS communication
        assert self._test_mtls_communication()
        
        # Test OpenTelemetry telemetry
        assert self._test_otel_boundary_telemetry()
    
    def test_plugin_manifest_compliance(self):
        """Test plugin manifest schema compliance"""
        plugin_dirs = Path("actions").glob("*/")
        
        for plugin_dir in plugin_dirs:
            manifest_path = plugin_dir / "manifest.json"
            if manifest_path.exists():
                with open(manifest_path) as f:
                    manifest = json.load(f)
                
                # Test version compliance
                assert manifest["manifest_version"] == "2.2"
                
                # Test HMA compliance section
                assert "hma_compliance" in manifest
                assert manifest["hma_compliance"]["hma_version"] == "2.2"
                
                # Test mandatory fields
                required_fields = [
                    "tier_classification",
                    "boundary_interfaces"
                ]
                for field in required_fields:
                    assert field in manifest["hma_compliance"]
    
    def test_layer_architecture_compliance(self):
        """Test proper layer separation"""
        
        # Test L1 Interface Layer
        assert self._test_l1_layer_compliance()
        
        # Test L2 Core Layer
        assert self._test_l2_core_compliance()
        
        # Test L3 Plugin Layer
        assert self._test_l3_plugin_compliance()
        
        # Test L4 Infrastructure Layer
        assert self._test_l4_infrastructure_compliance()
    
    def _test_l2_core_compliance(self):
        """Test L2 core minimal responsibilities"""
        from core.minimal_core import HMAMinimalCore
        
        core = HMAMinimalCore({})
        
        # Core should only do routing and lifecycle
        core_methods = [method for method in dir(core) 
                       if not method.startswith('_')]
        
        allowed_methods = [
            'route_request', 'register_plugin', 'unregister_plugin',
            'get_plugin_status', 'start', 'stop'
        ]
        
        for method in core_methods:
            assert method in allowed_methods, f"Core has business logic method: {method}"
        
        return True

# Windows-specific tests:
# tests/windows_specific_tests.py
class WindowsSpecificTestSuite:
    """Windows-specific functionality tests"""
    
    @pytest.mark.skipif(os.name != 'nt', reason="Windows-only test")
    def test_windows_path_handling(self):
        """Test Windows path handling"""
        from core.windows_file_utils import WindowsFileHandler
        
        # Test long path handling
        long_path = "C:\\" + "a" * 300
        normalized = WindowsFileHandler.normalize_path(long_path)
        assert str(normalized).startswith("\\\\?\\")
        
        # Test case insensitive matching
        path1 = "C:\\TEMP\\FILE.TXT"
        path2 = "c:\\temp\\file.txt"
        assert WindowsFileHandler.is_case_sensitive_match(path1, path2)
    
    @pytest.mark.skipif(os.name != 'nt', reason="Windows-only test")
    def test_windows_atomic_write(self):
        """Test Windows atomic write operations"""
        from core.windows_atomic_write import WindowsAtomicWriter
        
        writer = WindowsAtomicWriter()
        test_file = Path("test_atomic.txt")
        
        # Test normal write
        assert writer.atomic_write(str(test_file), "test content")
        assert test_file.read_text() == "test content"
        
        # Test concurrent write handling
        import threading
        import time
        
        def concurrent_write(content, delay):
            time.sleep(delay)
            return writer.atomic_write(str(test_file), content)
        
        threads = []
        for i in range(5):
            thread = threading.Thread(
                target=concurrent_write, 
                args=(f"content_{i}", i * 0.1)
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # File should contain one of the contents (atomic)
        final_content = test_file.read_text()
        assert final_content.startswith("content_")
        
        test_file.unlink()

# Performance tests:
# tests/performance_tests.py
class PerformanceTestSuite:
    """Performance and scalability tests"""
    
    def test_event_processing_throughput(self):
        """Test event processing meets performance requirements"""
        from core.thread_safe_event_bus import ThreadSafeEventBus
        
        event_bus = ThreadSafeEventBus(max_workers=8)
        event_bus.start()
        
        processed_events = []
        
        def event_handler(data):
            processed_events.append(data)
        
        event_bus.subscribe('test_event', event_handler)
        
        # Send 1000 events
        start_time = time.time()
        for i in range(1000):
            event_bus.publish('test_event', {'id': i})
        
        # Wait for processing
        while len(processed_events) < 1000:
            time.sleep(0.01)
        
        end_time = time.time()
        throughput = 1000 / (end_time - start_time)
        
        # Should meet 100+ events/second requirement
        assert throughput >= 100, f"Throughput too low: {throughput} events/sec"
        
        event_bus.stop()

# Run tests with coverage:
# pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
```

**Implementation Steps**:
1. Create comprehensive test suites for all components
2. Add HMA v2.2 compliance validation tests
3. Implement Windows-specific test scenarios
4. Add performance and load testing
5. Setup CI/CD pipeline with automated testing

---

## Implementation Timeline and Milestones

### Phase 1: Foundation (Weeks 1-4)
- **Week 1**: Fix plugin manifests and boundary validation
- **Week 2**: Implement OpenTelemetry integration
- **Week 3**: Add mTLS security layer
- **Week 4**: Complete mandatory compliance requirements

### Phase 2: Architecture (Weeks 5-8)
- **Week 5**: Implement HMA port abstractions
- **Week 6**: Restructure core as minimal router
- **Week 7**: Create L2 orchestrator plugins
- **Week 8**: Complete architectural compliance

### Phase 3: Platform (Weeks 9-10)
- **Week 9**: Fix Windows file handling and processes
- **Week 10**: Complete Windows-specific optimizations

### Phase 4: Quality (Weeks 11-12)
- **Week 11**: Implement plugin sandboxing and security
- **Week 12**: Add thread safety and performance enhancements

### Phase 5: Production (Weeks 13-16)
- **Week 13**: Complete observability stack
- **Week 14**: Production configuration and deployment
- **Week 15**: Comprehensive testing framework
- **Week 16**: Final validation and documentation

## Risk Assessment and Mitigation

### High Risks:
1. **Complete rewrite complexity** - Mitigate with incremental approach and comprehensive testing
2. **Windows compatibility issues** - Mitigate with dedicated Windows testing environment
3. **Performance regression** - Mitigate with continuous performance monitoring
4. **Plugin compatibility breakage** - Mitigate with backward compatibility layer

### Success Criteria:
1. ✅ All HMA v2.2 mandatory requirements implemented
2. ✅ Plugin manifests fully compliant with v2.2 schema
3. ✅ Windows-specific issues resolved
4. ✅ Performance requirements met (100+ events/sec)
5. ✅ Security architecture fully implemented
6. ✅ Production deployment successful

## Conclusion

This roadmap provides a complete solution to achieve full HMA v2.2 compliance for the Scribe tool. The implementation requires significant architectural changes but will result in a production-ready, standards-compliant automation engine that fully embraces HMA v2.2 principles.

The key to success is following the phased approach, maintaining comprehensive testing throughout, and ensuring each milestone is fully validated before proceeding to the next phase.