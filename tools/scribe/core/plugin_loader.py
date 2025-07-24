#!/usr/bin/env python3
"""
Scribe Plugin Loader

Handles dynamic discovery and loading of action plugins.
Implements secure plugin loading with error handling and validation.
"""

import importlib.util
import inspect
import sys
import json
from pathlib import Path
from typing import Dict, List, Type, Optional, Any
import structlog
import jsonschema

from .logging_config import get_scribe_logger
from tools.scribe.actions.base import BaseAction
from .config_manager import ConfigManager
from .security_manager import SecurityManager
from .port_adapters import ScribePluginContextAdapter


logger = get_scribe_logger(__name__)


class PluginLoadError(Exception):
    """Exception raised when a plugin fails to load."""
    
    def __init__(self, plugin_path: str, message: str, original_error: Optional[Exception] = None):
        """
        Initialize the exception.
        
        Args:
            plugin_path: Path to the plugin that failed to load
            message: Error message
            original_error: The original exception that caused this error
        """
        self.plugin_path = plugin_path
        self.original_error = original_error
        
        if original_error:
            super().__init__(f"Failed to load plugin '{plugin_path}': {message} (caused by: {original_error})")
        else:
            super().__init__(f"Failed to load plugin '{plugin_path}': {message}")


class PluginInfo:
    """Information about a loaded plugin with HMA v2.2 manifest support."""
    
    def __init__(self, 
                 action_class: Type[BaseAction], 
                 module_path: str, 
                 action_type: str,
                 manifest: Optional[Dict[str, Any]] = None):
        """
        Initialize plugin information.
        
        Args:
            action_class: The action class
            module_path: Path to the module file
            action_type: The action type identifier
            manifest: Plugin manifest data (HMA v2.2)
        """
        self.action_class = action_class
        self.module_path = module_path
        self.action_type = action_type
        self.class_name = action_class.__name__
        self.module_name = action_class.__module__
        self.manifest = manifest or {}
    
    def create_instance(self, params: Dict[str, Any],
                        port_registry,
                        execution_context: Optional[Dict[str, Any]] = None) -> BaseAction:
        """
        Create an instance of the action plugin with HMA v2.2 port-based access.
        
        Args:
            params: Action-specific parameters from the rule.
            port_registry: The port registry for accessing core functionality.
            execution_context: Plugin execution context.

        Returns:
            New instance of the action plugin.
        """
        # Create plugin context adapter
        plugin_context = ScribePluginContextAdapter(
            plugin_id=self.action_type,
            port_registry=port_registry,
            execution_context=execution_context or {}
        )
        
        return self.action_class(
            action_type=self.action_type,
            params=params,
            plugin_context=plugin_context
        )
    
    def __str__(self) -> str:
        return f"PluginInfo(type='{self.action_type}', class='{self.class_name}')"
    
    def __repr__(self) -> str:
        return f"PluginInfo(action_type='{self.action_type}', class_name='{self.class_name}', module_path='{self.module_path}')"


class PluginLoader:
    """
    Loads and manages action plugins dynamically.
    
    Discovers Python files in the actions directory, loads them as modules,
    and finds classes that inherit from BaseAction.
    """
    
    def __init__(self, plugin_directories: List[str] = None, load_order: List[str] = None):
        """
        Initialize the plugin loader.
        
        Args:
            plugin_directories: List of directories containing plugin files (relative to scribe root)
            load_order: Order in which to load plugin directories (optional)
        """
        # Determine the absolute path to the plugins directories
        scribe_root = Path(__file__).parent.parent
        
        if plugin_directories is None:
            plugin_directories = ["actions"]
        
        # Store both relative and absolute paths
        self.relative_plugin_directories = plugin_directories
        self.plugin_directories = []
        self.directory_map = {}  # Maps relative to absolute paths
        
        for plugin_dir in plugin_directories:
            abs_plugin_dir = scribe_root / plugin_dir
            self.plugin_directories.append(abs_plugin_dir)
            self.directory_map[plugin_dir] = abs_plugin_dir
        
        # Set load order
        self.load_order = load_order or plugin_directories
        
        # Plugin registry with directory tracking
        self._plugins: Dict[str, PluginInfo] = {}
        self._loaded_modules: Dict[str, Any] = {}
        self._plugin_directory_map: Dict[str, str] = {}  # Maps plugin name to directory
        
        # Hot-reload support (Phase 2)
        self._file_watchers = {}
        self._auto_reload = False
        
        logger.info("PluginLoader initialized",
                   plugin_directories=[str(d) for d in self.plugin_directories],
                   load_order=self.load_order)
    
    def discover_plugins(self) -> List[str]:
        """
        Discover all Python files in the plugins directory.
        
        Returns:
            List of plugin file paths
        """
        plugin_files = []
        
        for plugin_dir in self.plugin_directories:
            if not plugin_dir.exists():
                logger.warning("Plugins directory does not exist",
                              directory=str(plugin_dir))
                continue
            
            # Find all .py files except __init__.py and base.py
            for file_path in plugin_dir.glob("*.py"):
                if file_path.name in ["__init__.py", "base.py"]:
                    continue
                
                plugin_files.append(str(file_path))
                logger.debug("Discovered plugin file", file_path=str(file_path))
        
        logger.info("Plugin discovery complete",
                   total_files=len(plugin_files),
                   files=plugin_files)
        
        return plugin_files
    
    def load_plugin_module(self, file_path: str) -> Any:
        """
        Load a Python file as a module.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            The loaded module
            
        Raises:
            PluginLoadError: If the module fails to load
        """
        try:
            file_path_obj = Path(file_path)
            module_name_str = None
            package_name_str = None

            # Determine module and package name relative to a sys.path entry
            # This makes relative imports (..) work correctly.
            abs_file_path = file_path_obj.resolve()

            # Find the longest sys.path entry that is an ancestor of this file
            longest_ancestor_path = None
            for p_str in sys.path:
                p_path = Path(p_str).resolve()
                if abs_file_path.is_relative_to(p_path): # Requires Python 3.9+
                    if longest_ancestor_path is None or len(str(p_path)) > len(str(longest_ancestor_path)):
                        longest_ancestor_path = p_path
            
            if longest_ancestor_path:
                relative_module_path = abs_file_path.relative_to(longest_ancestor_path)
                # Construct module name, e.g., tools.scribe.actions.my_plugin
                module_name_str = ".".join(relative_module_path.parts[:-1] + (file_path_obj.stem,))
                # Construct package name, e.g., tools.scribe.actions
                package_name_str = ".".join(relative_module_path.parts[:-1])
            else:
                # Fallback if no ancestor found in sys.path (should be rare in controlled env)
                module_name_str = f"scribe_plugin_{file_path_obj.stem}"
                package_name_str = "" # Indicates top-level, relative imports will fail
                logger.warning(f"Plugin path {file_path} not found under any sys.path entry. Using fallback module name: {module_name_str}. Relative imports within plugin may fail.")

            # This was the line with the typo (module_name instead of module_name_str in the f-string).
            # It should be module_name_str as corrected in the previous diff application for this file.
            # The error output shows the log still has "module_name" if it's a fallback.
            # Let's ensure all references here use module_name_str for logging the name.
            logger.debug(f"Attempting to load plugin {file_path} as module '{module_name_str}' with package '{package_name_str}'")

            spec = importlib.util.spec_from_file_location(module_name_str, str(file_path))
            if spec is None:
                raise PluginLoadError(file_path, f"Could not create module spec for '{module_name_str}'")
            
            if spec.loader is None:
                raise PluginLoadError(file_path, f"Module spec for '{module_name_str}' has no loader")
            
            module = importlib.util.module_from_spec(spec)
            
            # Set __package__ to allow relative imports from within the plugin
            # This needs to happen BEFORE exec_module
            if package_name_str:
                 module.__package__ = package_name_str
            
            # Add to sys.modules BEFORE exec_module to handle circular dependencies or re-imports within plugin
            sys.modules[module_name_str] = module

            spec.loader.exec_module(module) # Execute the module to make its content available
            
            logger.debug("Plugin module loaded successfully",
                        file_path=file_path,
                        module_name=module_name_str) # Use module_name_str
            
            return module
            
        except Exception as e:
            raise PluginLoadError(file_path, "Failed to load module", e)
    
    def extract_action_classes(self, module: Any, file_path: str) -> List[Type[BaseAction]]:
        """
        Extract action classes from a loaded module.
        
        Args:
            module: The loaded module
            file_path: Path to the module file (for error reporting)
            
        Returns:
            List of action classes found in the module
        """
        action_classes = []
        
        try:
            # Get all members of the module
            for name, obj in inspect.getmembers(module):
                # Check if it's a class
                if not inspect.isclass(obj):
                    continue
                
                # Skip if it's the BaseAction class itself
                if obj is BaseAction:
                    continue
                
                # Check if it's a subclass of BaseAction
                if issubclass(obj, BaseAction) and obj != BaseAction:
                    action_classes.append(obj)
                    logger.debug("Found action class",
                                file_path=file_path,
                                class_name=name)
            
            logger.debug("Action class extraction complete",
                        file_path=file_path,
                        classes_found=len(action_classes))
            
        except Exception as e:
            logger.error("Error extracting action classes",
                        file_path=file_path,
                        error=str(e),
                        exc_info=True)
        
        return action_classes
    
    def determine_action_type(self, action_class: Type[BaseAction], file_path: str) -> str:
        """
        Determine the action type for a plugin class.
        
        This method tries several strategies to determine the action type:
        1. Check if the class has an ACTION_TYPE class attribute
        2. Use the class name converted to snake_case
        3. Use the filename without extension
        
        Args:
            action_class: The action class
            file_path: Path to the module file
            
        Returns:
            The action type string
        """
        # Strategy 1: Check for ACTION_TYPE class attribute
        if hasattr(action_class, 'ACTION_TYPE'):
            action_type = action_class.ACTION_TYPE
            if isinstance(action_type, str) and action_type.strip():
                logger.debug("Using ACTION_TYPE attribute",
                           class_name=action_class.__name__,
                           action_type=action_type)
                return action_type.strip()
        
        # Strategy 2: Convert class name to snake_case
        class_name = action_class.__name__
        if class_name.endswith('Action'):
            class_name = class_name[:-6]  # Remove 'Action' suffix
        
        # Convert CamelCase to snake_case
        import re
        snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
        
        if snake_case:
            logger.debug("Using snake_case class name",
                        class_name=action_class.__name__,
                        action_type=snake_case)
            return snake_case
        
        # Strategy 3: Use filename
        file_name = Path(file_path).stem
        logger.debug("Using filename as action type",
                    class_name=action_class.__name__,
                    action_type=file_name)
        return file_name
    
    def load_plugin_manifest(self, plugin_directory: Path) -> Optional[Dict[str, Any]]:
        """
        Load and validate plugin manifest file.
        
        Args:
            plugin_directory: Directory containing manifest.json
            
        Returns:
            Validated manifest data or None if not found/invalid
        """
        manifest_path = plugin_directory / "manifest.json"
        
        if not manifest_path.exists():
            logger.debug("No manifest found for plugin", plugin_directory=str(plugin_directory))
            return None
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
            
            # HMA v2.2 Mandatory Validation
            manifest_version = manifest_data.get("manifest_version")
            hma_version = manifest_data.get("hma_compliance", {}).get("hma_version")
            
            # Enforce HMA v2.2 compliance
            if manifest_version != "2.2":
                raise jsonschema.ValidationError(
                    f"Plugin manifest version must be '2.2', found '{manifest_version}'"
                )
            
            if hma_version != "2.2":
                raise jsonschema.ValidationError(
                    f"HMA compliance version must be '2.2', found '{hma_version}'"
                )
            
            # Validate mandatory HMA v2.2 fields
            required_hma_fields = ["hma_version", "tier_classification", "boundary_interfaces"]
            hma_compliance = manifest_data.get("hma_compliance", {})
            
            for field in required_hma_fields:
                if field not in hma_compliance:
                    raise jsonschema.ValidationError(
                        f"Missing mandatory HMA v2.2 field: hma_compliance.{field}"
                    )
            
            # Load schema for validation
            schema_path = Path(__file__).parent.parent / "schemas" / "plugin_manifest.schema.json"
            if schema_path.exists():
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
                
                # Validate manifest against schema
                jsonschema.validate(manifest_data, schema)
                logger.debug("Plugin manifest HMA v2.2 validation passed", 
                           plugin_directory=str(plugin_directory),
                           manifest_version=manifest_version,
                           hma_version=hma_version)
            else:
                logger.warning("Plugin manifest schema not found, skipping schema validation",
                              schema_path=str(schema_path))
            
            return manifest_data
            
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in plugin manifest",
                        manifest_path=str(manifest_path),
                        error=str(e))
            return None
        except jsonschema.ValidationError as e:
            logger.error("Plugin manifest validation failed",
                        manifest_path=str(manifest_path),
                        error=str(e))
            return None
        except Exception as e:
            logger.error("Error loading plugin manifest",
                        manifest_path=str(manifest_path),
                        error=str(e))
            return None
    
    def load_plugin(self, file_path: str) -> List[PluginInfo]:
        """
        Load a single plugin file and extract action classes with manifest support.
        
        Args:
            file_path: Path to the plugin file
            
        Returns:
            List of PluginInfo objects for loaded actions
            
        Raises:
            PluginLoadError: If the plugin fails to load
        """
        plugin_infos = []
        
        try:
            # Security validation
            if not self.validate_plugin_security(file_path):
                raise PluginLoadError(file_path, "Plugin failed security validation")
            
            # Check for manifest in plugin directory
            plugin_file_path = Path(file_path)
            plugin_directory = plugin_file_path.parent / plugin_file_path.stem
            manifest = None
            
            if plugin_directory.exists() and plugin_directory.is_dir():
                manifest = self.load_plugin_manifest(plugin_directory)
                if manifest:
                    logger.info("HMA v2.2 manifest loaded for plugin",
                               plugin_path=file_path,
                               manifest_version=manifest.get('manifest_version'),
                               hma_version=manifest.get('hma_compliance', {}).get('hma_version'))
            
            # Determine which directory this plugin belongs to
            plugin_file_path = Path(file_path)
            plugin_directory = None
            
            for rel_dir, abs_dir in self.directory_map.items():
                if plugin_file_path.is_relative_to(abs_dir):
                    plugin_directory = rel_dir
                    break
            
            if plugin_directory is None:
                logger.warning("Plugin file not in any configured directory", 
                              file_path=file_path)
                plugin_directory = "unknown"
            
            # Load the module
            module = self.load_plugin_module(file_path)
            self._loaded_modules[file_path] = module
            
            # Extract action classes
            action_classes = self.extract_action_classes(module, file_path)
            
            if not action_classes:
                logger.warning("No action classes found in plugin", file_path=file_path)
                return plugin_infos
            
            # Create PluginInfo objects for each action class
            for action_class in action_classes:
                action_type = self.determine_action_type(action_class, file_path)
                
                # Check for name conflicts
                if action_type in self._plugins:
                    existing_plugin = self._plugins[action_type]
                    logger.warning("Plugin action type conflict",
                                  action_type=action_type,
                                  new_plugin=file_path,
                                  existing_plugin=existing_plugin.module_path)
                    # Skip this plugin to avoid conflicts
                    continue
                
                plugin_info = PluginInfo(action_class, file_path, action_type, manifest)
                plugin_infos.append(plugin_info)
                
                # Register the plugin
                self._plugins[action_type] = plugin_info
                self._plugin_directory_map[action_type] = plugin_directory
                
                # Log HMA compliance status
                hma_compliance = "HMA v2.2 compliant" if manifest else "Legacy (no manifest)"
                logger.info("Plugin action loaded successfully",
                           action_type=action_type,
                           action_class=action_class.__name__,
                           plugin_file=file_path,
                           plugin_directory=plugin_directory,
                           hma_compliance=hma_compliance)
            
            return plugin_infos
            
        except PluginLoadError:
            raise
        except Exception as e:
            raise PluginLoadError(file_path, f"Unexpected error during plugin loading", e)
    
    def load_all_plugins(self) -> Dict[str, PluginInfo]:
        """
        Discover and load all plugins with dependency resolution.
        
        Returns:
            Dictionary mapping action types to PluginInfo objects
        """
        logger.info("Starting plugin loading process")
        
        # Clear existing plugins
        self._plugins.clear()
        self._loaded_modules.clear()
        self._plugin_directory_map.clear()
        
        # Use dependency-resolved load order
        plugin_files = self.resolve_plugin_load_order()
        
        if not plugin_files:
            logger.warning("No plugin files discovered")
            return self._plugins
        
        loaded_count = 0
        failed_count = 0
        
        for plugin_file in plugin_files:
            try:
                plugin_infos = self.load_plugin(plugin_file)
                
                for plugin_info in plugin_infos:
                    self._plugins[plugin_info.action_type] = plugin_info
                    loaded_count += 1
                
            except PluginLoadError as e:
                logger.error("Plugin load error",
                            plugin_file=plugin_file,
                            error=str(e))
                failed_count += 1
            except Exception as e:
                logger.error("Unexpected error loading plugin",
                            plugin_file=plugin_file,
                            error=str(e),
                            exc_info=True)
                failed_count += 1
        
        logger.info("Plugin loading completed",
                   total_discovered=len(plugin_files),
                   successfully_loaded=loaded_count,
                   failed_to_load=failed_count,
                   action_types=list(self._plugins.keys()))
        
        return self._plugins
    
    def get_plugin(self, action_type: str) -> Optional[PluginInfo]:
        """
        Get plugin information for a specific action type.
        
        Args:
            action_type: The action type to look up
            
        Returns:
            PluginInfo if found, None otherwise
        """
        return self._plugins.get(action_type)
    
    def get_all_plugins(self) -> Dict[str, PluginInfo]:
        """
        Get all loaded plugins.
        
        Returns:
            Dictionary mapping action types to PluginInfo objects
        """
        return self._plugins.copy()
    
    def create_action_instance(self, action_type: str) -> Optional[BaseAction]:
        """
        Create an instance of an action plugin.
        
        Args:
            action_type: The action type to instantiate.
            params: Action-specific parameters from the rule.
            config_manager: The ConfigManager instance.
            security_manager: The SecurityManager instance.
            
        Returns:
            Action instance if found, None otherwise.
        """
        plugin_info = self.get_plugin(action_type)
        if plugin_info is None:
            logger.warning("Action type not found for instantiation", action_type=action_type)
            return None
        
        try:
            instance = plugin_info.create_instance(params, config_manager, security_manager)
            logger.debug("Action instance created with dependencies",
                        action_type=action_type,
                        class_name=plugin_info.class_name,
                        params=params)
            return instance
        except Exception as e:
            logger.error("Error creating action instance with dependencies",
                        action_type=action_type,
                        class_name=plugin_info.class_name,
                        error=str(e),
                        exc_info=True)
            return None
    
    def reload_plugins(self) -> Dict[str, PluginInfo]:
        """
        Reload all plugins from the plugins directory.
        
        Returns:
            Dictionary mapping action types to PluginInfo objects
        """
        logger.info("Reloading all plugins")
        
        # Clear module cache for reloaded modules
        for file_path in self._loaded_modules:
            module_name = f"scribe_plugin_{Path(file_path).stem}"
            if module_name in sys.modules:
                del sys.modules[module_name]
        
        return self.load_all_plugins()
    
    def get_plugin_stats(self) -> Dict[str, Any]:
        """Get plugin loader statistics."""
        return {
            'total_plugins': len(self._plugins),
            'loaded_modules': len(self._loaded_modules),
            'action_types': list(self._plugins.keys()),
            'plugin_files': len(self._loaded_modules),
            'plugins_directory': [str(d) for d in self.plugin_directories]
        }
    
    def enable_hot_reload(self) -> None:
        """Enable hot-reloading of plugin files."""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class PluginFileHandler(FileSystemEventHandler):
                def __init__(self, plugin_loader):
                    self.plugin_loader = plugin_loader
                
                def on_modified(self, event):
                    if event.is_directory:
                        return
                    
                    if event.src_path.endswith('.py'):
                        logger.info("Plugin file changed, reloading", 
                                   file_path=event.src_path)
                        self.plugin_loader.reload_plugins()
            
            self._auto_reload = True
            observer = Observer()
            
            for plugin_dir in self.plugin_directories:
                if plugin_dir.exists():
                    handler = PluginFileHandler(self)
                    observer.schedule(handler, str(plugin_dir), recursive=False)
                    self._file_watchers[str(plugin_dir)] = (observer, handler)
                    logger.info("Hot-reload enabled for plugin directory", 
                               directory=str(plugin_dir))
            
            observer.start()
            logger.info("Plugin hot-reloading enabled")
            
        except ImportError:
            logger.warning("Watchdog not available, hot-reloading disabled")
        except Exception as e:
            logger.error("Failed to enable hot-reloading", error=str(e))
    
    def disable_hot_reload(self) -> None:
        """Disable hot-reloading of plugin files."""
        self._auto_reload = False
        for directory, (observer, handler) in self._file_watchers.items():
            try:
                observer.stop()
                observer.join(timeout=5.0)
                logger.info("Hot-reload disabled for plugin directory", 
                           directory=directory)
            except Exception as e:
                logger.error("Error stopping plugin file watcher", 
                            directory=directory, error=str(e))
        
        self._file_watchers.clear()
        logger.info("Plugin hot-reloading disabled")
    
    def validate_plugin_security(self, plugin_path: str) -> bool:
        """
        Validate plugin security before loading.
        
        Args:
            plugin_path: Path to the plugin file
            
        Returns:
            True if plugin passes security validation
        """
        try:
            # Read plugin file content
            with open(plugin_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Security checks
            dangerous_imports = [
                'subprocess', 'os.system', 'eval', 'exec', '__import__',
                'importlib.import_module', 'open', 'file'
            ]
            
            dangerous_functions = [
                'eval(', 'exec(', 'compile(', '__import__(',
                'getattr(', 'setattr(', 'delattr(', 'globals(', 'locals('
            ]
            
            # Check for dangerous imports
            for dangerous_import in dangerous_imports:
                if dangerous_import in content:
                    logger.warning("Plugin contains potentially dangerous import",
                                  plugin_path=plugin_path,
                                  dangerous_pattern=dangerous_import)
                    return False
            
            # Check for dangerous function calls
            for dangerous_func in dangerous_functions:
                if dangerous_func in content:
                    logger.warning("Plugin contains potentially dangerous function",
                                  plugin_path=plugin_path,
                                  dangerous_pattern=dangerous_func)
                    return False
            
            # Check file permissions (should not be world-writable)
            plugin_file = Path(plugin_path)
            if plugin_file.stat().st_mode & 0o002:  # World-writable
                logger.warning("Plugin file is world-writable",
                              plugin_path=plugin_path)
                return False
            
            logger.debug("Plugin security validation passed",
                        plugin_path=plugin_path)
            return True
            
        except Exception as e:
            logger.error("Plugin security validation failed",
                        plugin_path=plugin_path,
                        error=str(e))
            return False
    
    def add_plugin_directory(self, directory: str, position: int = -1) -> bool:
        """
        Add a new plugin directory at runtime.
        
        Args:
            directory: Directory path (relative to scribe root)
            position: Position in load order (-1 for end)
            
        Returns:
            True if directory was added successfully
        """
        try:
            scribe_root = Path(__file__).parent.parent
            abs_plugin_dir = scribe_root / directory
            
            if directory in self.relative_plugin_directories:
                logger.warning("Plugin directory already exists", directory=directory)
                return False
            
            if not abs_plugin_dir.exists():
                logger.error("Plugin directory does not exist", directory=str(abs_plugin_dir))
                return False
            
            # Add to lists
            if position == -1:
                self.relative_plugin_directories.append(directory)
                self.plugin_directories.append(abs_plugin_dir)
                self.load_order.append(directory)
            else:
                self.relative_plugin_directories.insert(position, directory)
                self.plugin_directories.insert(position, abs_plugin_dir)
                self.load_order.insert(position, directory)
            
            # Update directory map
            self.directory_map[directory] = abs_plugin_dir
            
            # Enable hot-reload for new directory if it's enabled
            if self._auto_reload and directory not in self._file_watchers:
                # Add hot-reload watcher for this directory
                pass  # Implementation would go here
            
            logger.info("Plugin directory added", 
                       directory=directory, 
                       absolute_path=str(abs_plugin_dir))
            return True
            
        except Exception as e:
            logger.error("Failed to add plugin directory",
                        directory=directory,
                        error=str(e))
            return False
    
    def remove_plugin_directory(self, directory: str) -> bool:
        """
        Remove a plugin directory at runtime.
        
        Args:
            directory: Directory path to remove
            
        Returns:
            True if directory was removed successfully
        """
        try:
            if directory not in self.relative_plugin_directories:
                logger.warning("Plugin directory not found", directory=directory)
                return False
            
            # Remove from all lists
            index = self.relative_plugin_directories.index(directory)
            self.relative_plugin_directories.remove(directory)
            self.plugin_directories.pop(index)
            
            if directory in self.load_order:
                self.load_order.remove(directory)
            
            # Remove from directory map
            if directory in self.directory_map:
                del self.directory_map[directory]
            
            # Remove plugins loaded from this directory
            plugins_to_remove = []
            for plugin_name, plugin_dir in self._plugin_directory_map.items():
                if plugin_dir == directory:
                    plugins_to_remove.append(plugin_name)
            
            for plugin_name in plugins_to_remove:
                if plugin_name in self._plugins:
                    del self._plugins[plugin_name]
                del self._plugin_directory_map[plugin_name]
            
            # Stop hot-reload watcher for this directory
            if directory in self._file_watchers:
                observer, handler = self._file_watchers[directory]
                observer.stop()
                del self._file_watchers[directory]
            
            logger.info("Plugin directory removed", 
                       directory=directory,
                       removed_plugins=plugins_to_remove)
            return True
            
        except Exception as e:
            logger.error("Failed to remove plugin directory",
                        directory=directory,
                        error=str(e))
            return False
    
    def get_plugin_dependencies(self, plugin_path: str) -> List[str]:
        """
        Extract plugin dependencies from file.
        
        Args:
            plugin_path: Path to the plugin file
            
        Returns:
            List of dependency names
        """
        dependencies = []
        try:
            with open(plugin_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for dependency declarations in comments
            # Format: # DEPENDENCIES: plugin1, plugin2, plugin3
            import re
            dep_pattern = r'#\s*DEPENDENCIES:\s*([^\n]+)'
            matches = re.findall(dep_pattern, content, re.IGNORECASE)
            
            for match in matches:
                deps = [dep.strip() for dep in match.split(',')]
                dependencies.extend(deps)
            
            # Remove duplicates and empty strings
            dependencies = list(filter(None, list(set(dependencies))))
            
            logger.debug("Plugin dependencies extracted",
                        plugin_path=plugin_path,
                        dependencies=dependencies)
            
        except Exception as e:
            logger.error("Failed to extract plugin dependencies",
                        plugin_path=plugin_path,
                        error=str(e))
        
        return dependencies
    
    def resolve_plugin_load_order(self) -> List[str]:
        """
        Resolve plugin load order based on dependencies.
        
        Returns:
            List of plugin files in dependency order
        """
        try:
            all_plugin_files = self.discover_plugins()
            plugin_deps = {}
            
            # Extract dependencies for each plugin
            for plugin_file in all_plugin_files:
                deps = self.get_plugin_dependencies(plugin_file)
                plugin_name = Path(plugin_file).stem
                plugin_deps[plugin_name] = deps
            
            # Topological sort
            sorted_plugins = []
            visited = set()
            temp_visited = set()
            
            def visit(plugin_name):
                if plugin_name in temp_visited:
                    raise ValueError(f"Circular dependency detected involving {plugin_name}")
                if plugin_name in visited:
                    return
                
                temp_visited.add(plugin_name)
                
                # Visit dependencies first
                for dep in plugin_deps.get(plugin_name, []):
                    visit(dep)
                
                temp_visited.remove(plugin_name)
                visited.add(plugin_name)
                sorted_plugins.append(plugin_name)
            
            # Visit all plugins
            for plugin_name in plugin_deps.keys():
                if plugin_name not in visited:
                    visit(plugin_name)
            
            # Convert back to file paths
            sorted_files = []
            for plugin_name in sorted_plugins:
                for plugin_file in all_plugin_files:
                    if Path(plugin_file).stem == plugin_name:
                        sorted_files.append(plugin_file)
                        break
            
            logger.info("Plugin load order resolved",
                       total_plugins=len(sorted_files),
                       order=[Path(f).stem for f in sorted_files])
            
            return sorted_files
            
        except Exception as e:
            logger.error("Failed to resolve plugin load order", error=str(e))
            # Fallback to simple discovery order
            return self.discover_plugins() 