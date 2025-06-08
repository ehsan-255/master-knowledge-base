#!/usr/bin/env python3
"""
Scribe Plugin Loader

Handles dynamic discovery and loading of action plugins.
Implements secure plugin loading with error handling and validation.
"""

import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Type, Optional, Any
import structlog

from .logging_config import get_scribe_logger

# Import BaseAction for type checking
sys.path.insert(0, str(Path(__file__).parent.parent))
from actions.base import BaseAction

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
    """Information about a loaded plugin."""
    
    def __init__(self, 
                 action_class: Type[BaseAction], 
                 module_path: str, 
                 action_type: str):
        """
        Initialize plugin information.
        
        Args:
            action_class: The action class
            module_path: Path to the module file
            action_type: The action type identifier
        """
        self.action_class = action_class
        self.module_path = module_path
        self.action_type = action_type
        self.class_name = action_class.__name__
        self.module_name = action_class.__module__
    
    def create_instance(self) -> BaseAction:
        """
        Create an instance of the action plugin.
        
        Returns:
            New instance of the action plugin
        """
        return self.action_class(self.action_type)
    
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
    
    def __init__(self, plugins_directory: str = "actions"):
        """
        Initialize the plugin loader.
        
        Args:
            plugins_directory: Directory containing plugin files (relative to scribe root)
        """
        # Determine the absolute path to the plugins directory
        scribe_root = Path(__file__).parent.parent
        self.plugins_directory = scribe_root / plugins_directory
        
        # Plugin registry
        self._plugins: Dict[str, PluginInfo] = {}
        self._loaded_modules: Dict[str, Any] = {}
        
        logger.info("PluginLoader initialized",
                   plugins_directory=str(self.plugins_directory))
    
    def discover_plugins(self) -> List[str]:
        """
        Discover all Python files in the plugins directory.
        
        Returns:
            List of plugin file paths
        """
        plugin_files = []
        
        if not self.plugins_directory.exists():
            logger.warning("Plugins directory does not exist",
                          directory=str(self.plugins_directory))
            return plugin_files
        
        # Find all .py files except __init__.py and base.py
        for file_path in self.plugins_directory.glob("*.py"):
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
            module_name = f"scribe_plugin_{file_path_obj.stem}"
            
            # Create module spec
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                raise PluginLoadError(file_path, "Could not create module spec")
            
            if spec.loader is None:
                raise PluginLoadError(file_path, "Module spec has no loader")
            
            # Create and load module
            module = importlib.util.module_from_spec(spec)
            
            # Add to sys.modules to support relative imports
            sys.modules[module_name] = module
            
            # Execute the module
            spec.loader.exec_module(module)
            
            logger.debug("Plugin module loaded successfully",
                        file_path=file_path,
                        module_name=module_name)
            
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
    
    def load_plugin(self, file_path: str) -> List[PluginInfo]:
        """
        Load a single plugin file and extract action classes.
        
        Args:
            file_path: Path to the plugin file
            
        Returns:
            List of PluginInfo objects for loaded actions
        """
        plugins = []
        
        try:
            # Load the module
            module = self.load_plugin_module(file_path)
            self._loaded_modules[file_path] = module
            
            # Extract action classes
            action_classes = self.extract_action_classes(module, file_path)
            
            # Create PluginInfo for each action class
            for action_class in action_classes:
                try:
                    action_type = self.determine_action_type(action_class, file_path)
                    
                    plugin_info = PluginInfo(action_class, file_path, action_type)
                    plugins.append(plugin_info)
                    
                    logger.info("Plugin loaded successfully",
                               file_path=file_path,
                               class_name=action_class.__name__,
                               action_type=action_type)
                    
                except Exception as e:
                    logger.error("Error creating plugin info",
                                file_path=file_path,
                                class_name=action_class.__name__,
                                error=str(e),
                                exc_info=True)
            
        except PluginLoadError:
            # Re-raise plugin load errors
            raise
        except Exception as e:
            raise PluginLoadError(file_path, "Unexpected error during plugin loading", e)
        
        return plugins
    
    def load_all_plugins(self) -> Dict[str, PluginInfo]:
        """
        Load all plugins from the plugins directory.
        
        Returns:
            Dictionary mapping action types to PluginInfo objects
        """
        self._plugins.clear()
        self._loaded_modules.clear()
        
        plugin_files = self.discover_plugins()
        
        total_loaded = 0
        total_errors = 0
        
        for file_path in plugin_files:
            try:
                plugins = self.load_plugin(file_path)
                
                for plugin_info in plugins:
                    if plugin_info.action_type in self._plugins:
                        logger.warning("Duplicate action type found, overriding",
                                     action_type=plugin_info.action_type,
                                     existing_class=self._plugins[plugin_info.action_type].class_name,
                                     new_class=plugin_info.class_name)
                    
                    self._plugins[plugin_info.action_type] = plugin_info
                    total_loaded += 1
                
            except PluginLoadError as e:
                logger.error("Plugin load error", error=str(e))
                total_errors += 1
            except Exception as e:
                logger.error("Unexpected error loading plugin",
                           file_path=file_path,
                           error=str(e),
                           exc_info=True)
                total_errors += 1
        
        logger.info("Plugin loading complete",
                   total_plugins=total_loaded,
                   total_errors=total_errors,
                   action_types=list(self._plugins.keys()))
        
        return self._plugins.copy()
    
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
            action_type: The action type to instantiate
            
        Returns:
            Action instance if found, None otherwise
        """
        plugin_info = self.get_plugin(action_type)
        if plugin_info is None:
            logger.warning("Action type not found", action_type=action_type)
            return None
        
        try:
            instance = plugin_info.create_instance()
            logger.debug("Action instance created",
                        action_type=action_type,
                        class_name=plugin_info.class_name)
            return instance
        except Exception as e:
            logger.error("Error creating action instance",
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
        """
        Get statistics about loaded plugins.
        
        Returns:
            Dictionary with plugin statistics
        """
        return {
            'total_plugins': len(self._plugins),
            'action_types': list(self._plugins.keys()),
            'plugin_files': len(self._loaded_modules),
            'plugins_directory': str(self.plugins_directory)
        } 