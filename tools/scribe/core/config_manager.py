#!/usr/bin/env python3
"""
Scribe Config Manager

Handles loading, validation, and hot-reloading of configuration files.
Implements atomic configuration swapping with JSON Schema validation.
"""

import json
import threading
import time
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
import structlog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import jsonschema

from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class ConfigChangeHandler(FileSystemEventHandler):
    """File system event handler for configuration file changes."""
    
    def __init__(self, config_manager: 'ConfigManager'):
        self.config_manager = config_manager
        super().__init__()
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
        
        # Check if the modified file is our config file
        if Path(event.src_path).name == self.config_manager.config_filename:
            logger.info("Configuration file change detected", 
                       file_path=event.src_path)
            self.config_manager._reload_config()


class ConfigManager:
    """
    Configuration manager with hot-reloading and validation.
    
    Provides thread-safe access to configuration with automatic reloading
    when the configuration file changes.
    """
    
    DEFAULT_CONFIG_PATH = "scribe-config.json"
    
    def __init__(self, 
                 config_path: str = "tools/scribe/config/config.json",
                 schema_path: str = "tools/scribe/schemas/scribe_config.schema.json",
                 auto_reload: bool = True):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file
            schema_path: Path to the JSON schema file
            auto_reload: Whether to enable automatic reloading on file changes
        """
        self.config_path = Path(config_path)
        self.schema_path = Path(schema_path)
        self.auto_reload = auto_reload
        self.config_filename = self.config_path.name
        self.repo_root = self._find_repo_root()

        # Thread safety
        self._config_lock = threading.RLock()
        self._config: Optional[Dict[str, Any]] = None
        self._schema: Optional[Dict[str, Any]] = None
        
        # Hot-reloading components
        self._observer: Optional[Observer] = None
        self._change_handler: Optional[ConfigChangeHandler] = None
        
        # Change callbacks
        self._change_callbacks: list[Callable[[Dict[str, Any]], None]] = []
        
        # Load initial configuration
        self._load_schema()
        self._load_and_validate_config()
        
        # Start hot-reloading if enabled
        if self.auto_reload:
            self._start_hot_reload()
        
        logger.info("ConfigManager initialized",
                   config_path=str(self.config_path),
                   schema_path=str(self.schema_path),
                   auto_reload=auto_reload)
    
    def _find_repo_root(self) -> str:
        """Find the repository root from the current path."""
        # A simple way is to look for a known marker, like .git directory
        current_path = Path.cwd()
        for parent in [current_path] + list(current_path.parents):
            if (parent / ".git").exists():
                return str(parent)
        return str(current_path) # Fallback to current dir

    def get_repo_root(self) -> str:
        """Get the repository root path."""
        return self.repo_root

    def _load_schema(self) -> None:
        """Load and parse the JSON schema."""
        try:
            if not self.schema_path.exists():
                raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
            
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                self._schema = json.load(f)
            
            logger.debug("JSON schema loaded successfully",
                        schema_path=str(self.schema_path))
            
        except Exception as e:
            logger.error("Failed to load JSON schema",
                        schema_path=str(self.schema_path),
                        error=str(e),
                        exc_info=True)
            raise
    
    def _load_and_validate_config(self) -> None:
        """Load configuration file and validate against schema."""
        try:
            # Load configuration file
            if not self.config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                temp_config = json.load(f)
            
            # Validate against schema
            if self._schema:
                try:
                    jsonschema.validate(temp_config, self._schema)
                    logger.debug("Configuration validation successful")
                except jsonschema.ValidationError as e:
                    logger.error("Configuration validation failed",
                                validation_error=str(e),
                                error_path=list(e.absolute_path) if e.absolute_path else None)
                    raise
                except jsonschema.SchemaError as e:
                    logger.error("Schema validation error",
                                schema_error=str(e))
                    raise
            
            # Atomic swap of configuration
            with self._config_lock:
                old_config = self._config
                self._config = temp_config
            
            logger.info("Configuration loaded and validated successfully",
                       config_version=temp_config.get('config_version', 'unknown'),
                       rules_count=len(temp_config.get('rules', [])))
            
            # Notify change callbacks
            self._notify_change_callbacks(temp_config)
            
        except Exception as e:
            logger.error("Failed to load configuration",
                        config_path=str(self.config_path),
                        error=str(e),
                        exc_info=True)
            
            # If this is initial load, re-raise the exception
            if self._config is None:
                raise
            
            # If this is a reload, keep the old configuration
            logger.warning("Keeping previous configuration due to load failure")
    
    def _reload_config(self) -> None:
        """Reload configuration file (called by file watcher)."""
        logger.info("Reloading configuration file")
        
        # Add a small delay to handle rapid file changes
        time.sleep(0.1)
        
        try:
            self._load_and_validate_config()
            logger.info("Configuration reloaded successfully")
        except Exception as e:
            logger.error("Configuration reload failed", error=str(e))
    
    def _start_hot_reload(self) -> None:
        """Start the file system watcher for hot-reloading."""
        try:
            self._change_handler = ConfigChangeHandler(self)
            self._observer = Observer()
            
            # Watch the directory containing the config file
            watch_dir = self.config_path.parent
            self._observer.schedule(self._change_handler, str(watch_dir), recursive=False)
            self._observer.start()
            
            logger.info("Hot-reload watcher started",
                       watch_directory=str(watch_dir))
            
        except Exception as e:
            logger.error("Failed to start hot-reload watcher",
                        error=str(e),
                        exc_info=True)
            # Don't raise - hot-reload is optional
    
    def stop(self) -> None:
        """Stop the configuration manager and cleanup resources."""
        if self._observer:
            try:
                self._observer.stop()
                self._observer.join(timeout=5.0)
                logger.info("Hot-reload watcher stopped")
            except Exception as e:
                logger.error("Error stopping hot-reload watcher", error=str(e))
        
        logger.info("ConfigManager stopped")
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the current configuration.
        
        Returns:
            A copy of the current configuration dictionary
        """
        with self._config_lock:
            if self._config is None:
                raise RuntimeError("Configuration not loaded")
            return self._config.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        config = self.get_config()
        
        # Support dot notation for nested keys
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def get_engine_settings(self) -> Dict[str, Any]:
        """Get engine settings from configuration."""
        config = self.get_config()
        return config.get('engine_settings', {})
    
    def get_security_settings(self) -> Dict[str, Any]:
        """Get security settings from configuration."""
        config = self.get_config()
        return config.get('security', {})
    
    def get_rules(self) -> list[Dict[str, Any]]:
        """Get list of rules from configuration."""
        config = self.get_config()
        return config.get('rules', [])
    
    def get_enabled_rules(self) -> list[Dict[str, Any]]:
        """Get list of enabled rules from configuration."""
        return [rule for rule in self.get_rules() if rule.get('enabled', False)]
    
    def get_plugin_settings(self) -> Dict[str, Any]:
        """Get plugin settings from configuration."""
        config = self.get_config()
        return config.get('plugins', {
            'directories': ['actions'],
            'auto_reload': False,
            'load_order': ['actions']
        })
    
    def get_plugin_directories(self) -> List[str]:
        """Get list of plugin directories from configuration."""
        plugin_settings = self.get_plugin_settings()
        return plugin_settings.get('directories', ['actions'])
    
    def get_plugin_auto_reload(self) -> bool:
        """Get plugin auto-reload setting from configuration."""
        plugin_settings = self.get_plugin_settings()
        return plugin_settings.get('auto_reload', False)
    
    def get_plugin_load_order(self) -> List[str]:
        """Get plugin load order from configuration."""
        plugin_settings = self.get_plugin_settings()
        return plugin_settings.get('load_order', [])
    
    def get_rule_by_id(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific rule by its ID.
        
        Args:
            rule_id: The rule ID to search for
            
        Returns:
            The rule dictionary if found, None otherwise
        """
        for rule in self.get_rules():
            if rule.get('id') == rule_id:
                return rule
        return None
    
    def add_change_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Add a callback to be called when configuration changes.
        
        Args:
            callback: Function to call with the new configuration
        """
        self._change_callbacks.append(callback)
        logger.debug("Configuration change callback added")
    
    def remove_change_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Remove a configuration change callback.
        
        Args:
            callback: The callback function to remove
        """
        if callback in self._change_callbacks:
            self._change_callbacks.remove(callback)
            logger.debug("Configuration change callback removed")
    
    def _notify_change_callbacks(self, new_config: Dict[str, Any]) -> None:
        """Notify all registered callbacks of configuration changes."""
        for callback in self._change_callbacks:
            try:
                callback(new_config)
            except Exception as e:
                logger.error("Error in configuration change callback",
                           callback=str(callback),
                           error=str(e),
                           exc_info=True)
    
    def validate_config_dict(self, config_dict: Dict[str, Any]) -> bool:
        """
        Validate a configuration dictionary against the schema.
        
        Args:
            config_dict: Configuration dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not self._schema:
            logger.warning("No schema loaded, cannot validate configuration")
            return False
        
        try:
            jsonschema.validate(config_dict, self._schema)
            return True
        except (jsonschema.ValidationError, jsonschema.SchemaError) as e:
            logger.error("Configuration validation failed",
                        validation_error=str(e))
            return False
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop() 