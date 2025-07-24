#!/usr/bin/env python3
"""
File Processing Orchestrator - L2 Orchestrator Plugin

This L2 Orchestrator plugin coordinates complex file processing workflows
by invoking L3 capability plugins in the correct sequence. It replaces the
legacy Worker logic with proper HMA v2.2 orchestration patterns.
"""

import re
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..base import BaseAction, ActionExecutionError


class FileProcessingOrchestrator(BaseAction):
    """
    L2 Orchestrator plugin for coordinating file processing workflows.
    
    This plugin implements the HMA v2.2 L2 Orchestrator pattern, replacing
    the legacy Worker's orchestration logic with proper port-based coordination
    of L3 capability plugins.
    
    HMA Layer: L2-Orchestrator
    Purpose: Coordinates multi-step file processing workflows
    """
    
    def get_required_params(self) -> List[str]:
        """Get required parameters for the orchestrator."""
        return ["workflow_config"]
    
    def get_optional_params(self) -> Dict[str, Any]:
        """Get optional parameters and their defaults."""
        return {
            "parallel_processing": False,
            "error_strategy": "fail_fast",  # fail_fast, continue_on_error, retry
            "max_retries": 3,
            "timeout_seconds": 300
        }
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate orchestrator parameters."""
        try:
            workflow_config = params.get("workflow_config")
            if not isinstance(workflow_config, dict):
                raise ActionExecutionError(
                    self.action_type,
                    "workflow_config must be a dictionary"
                )
            
            # Validate workflow stages
            stages = workflow_config.get("stages", [])
            if not isinstance(stages, list) or len(stages) == 0:
                raise ActionExecutionError(
                    self.action_type,
                    "workflow_config must contain at least one stage"
                )
            
            # Validate each stage
            for i, stage in enumerate(stages):
                if not isinstance(stage, dict):
                    raise ActionExecutionError(
                        self.action_type,
                        f"Stage {i} must be a dictionary"
                    )
                
                if "plugin_id" not in stage:
                    raise ActionExecutionError(
                        self.action_type,
                        f"Stage {i} missing required 'plugin_id' field"
                    )
            
            return True
            
        except ActionExecutionError:
            raise
        except Exception as e:
            raise ActionExecutionError(
                self.action_type,
                f"Parameter validation failed: {e}"
            )
    
    async def execute(self, 
                      file_content: str, 
                      match: re.Match, 
                      file_path: str, 
                      params: Dict[str, Any]) -> str:
        """
        Execute the file processing orchestration workflow.
        
        Args:
            file_content: The full content of the file being processed
            match: The regex match object that triggered the rule
            file_path: The path to the file being processed
            params: Orchestrator parameters including workflow_config
            
        Returns:
            The final processed file content after all stages
            
        Raises:
            ActionExecutionError: If orchestration fails
        """
        try:
            # Validate parameters
            self.validate_params(params)
            
            # Extract orchestration parameters
            workflow_config = params["workflow_config"]
            stages = workflow_config["stages"]
            parallel_processing = params.get("parallel_processing", False)
            error_strategy = params.get("error_strategy", "fail_fast")
            max_retries = params.get("max_retries", 3)
            timeout_seconds = params.get("timeout_seconds", 300)
            
            # Log orchestration start
            self.log_port.log_info("Starting file processing orchestration",
                                  file_path=file_path,
                                  workflow_name=workflow_config.get("name", "default"),
                                  stage_count=len(stages),
                                  parallel_processing=parallel_processing,
                                  plugin_id=self.context.get_plugin_id())
            
            # Publish orchestration start event
            await self.publish_event(
                "orchestration_started",
                {
                    "file_path": file_path,
                    "workflow_name": workflow_config.get("name", "default"),
                    "stage_count": len(stages),
                    "orchestrator_id": self.context.get_plugin_id()
                }
            )
            
            # Execute workflow based on processing mode
            if parallel_processing:
                final_content = await self._execute_parallel_workflow(
                    file_content, match, file_path, stages, error_strategy, max_retries, timeout_seconds
                )
            else:
                final_content = await self._execute_sequential_workflow(
                    file_content, match, file_path, stages, error_strategy, max_retries, timeout_seconds
                )
            
            # Log orchestration completion
            self.log_port.log_info("File processing orchestration completed successfully",
                                  file_path=file_path,
                                  workflow_name=workflow_config.get("name", "default"),
                                  content_changed=final_content != file_content,
                                  plugin_id=self.context.get_plugin_id())
            
            # Publish orchestration completion event
            await self.publish_event(
                "orchestration_completed",
                {
                    "file_path": file_path,
                    "workflow_name": workflow_config.get("name", "default"),
                    "success": True,
                    "content_changed": final_content != file_content,
                    "orchestrator_id": self.context.get_plugin_id()
                }
            )
            
            return final_content
            
        except ActionExecutionError:
            raise
        except Exception as e:
            self.log_port.log_error("File processing orchestration failed",
                                   file_path=file_path,
                                   error=str(e),
                                   plugin_id=self.context.get_plugin_id())
            
            # Publish orchestration failure event
            await self.publish_event(
                "orchestration_failed",
                {
                    "file_path": file_path,
                    "error": str(e),
                    "orchestrator_id": self.context.get_plugin_id()
                }
            )
            
            raise ActionExecutionError(
                self.action_type,
                f"Orchestration failed: {e}"
            )
    
    async def _execute_sequential_workflow(self,
                                         file_content: str,
                                         match: re.Match,
                                         file_path: str,
                                         stages: List[Dict[str, Any]],
                                         error_strategy: str,
                                         max_retries: int,
                                         timeout_seconds: int) -> str:
        """Execute workflow stages sequentially."""
        current_content = file_content
        
        for stage_index, stage in enumerate(stages):
            plugin_id = stage["plugin_id"]
            stage_params = stage.get("params", {})
            
            try:
                # Log stage start
                self.log_port.log_info("Executing workflow stage",
                                      stage_index=stage_index,
                                      plugin_id=plugin_id,
                                      file_path=file_path)
                
                # Execute stage with retry logic
                for attempt in range(max_retries + 1):
                    try:
                        # Get plugin execution port
                        plugin_port = self.context.get_port("plugin_execution")
                        
                        # Prepare execution data
                        input_data = {
                            "file_content": current_content,
                            "match": match,
                            "file_path": file_path,
                            "params": stage_params
                        }
                        
                        # Execute the plugin
                        result = await asyncio.wait_for(
                            plugin_port.execute_plugin(plugin_id, input_data),
                            timeout=timeout_seconds
                        )
                        
                        if result.get("success", False):
                            current_content = result.get("result", current_content)
                            self.log_port.log_info("Workflow stage completed successfully",
                                                  stage_index=stage_index,
                                                  plugin_id=plugin_id,
                                                  attempt=attempt + 1)
                            break
                        else:
                            error_msg = result.get("error", "Unknown error")
                            raise ActionExecutionError(plugin_id, error_msg)
                            
                    except asyncio.TimeoutError:
                        if attempt < max_retries:
                            self.log_port.log_warning("Stage execution timed out, retrying",
                                                     stage_index=stage_index,
                                                     plugin_id=plugin_id,
                                                     attempt=attempt + 1)
                            continue
                        else:
                            raise ActionExecutionError(
                                plugin_id,
                                f"Stage timed out after {max_retries} attempts"
                            )
                    except Exception as e:
                        if attempt < max_retries:
                            self.log_port.log_warning("Stage execution failed, retrying",
                                                     stage_index=stage_index,
                                                     plugin_id=plugin_id,
                                                     attempt=attempt + 1,
                                                     error=str(e))
                            continue
                        else:
                            raise
                
            except Exception as e:
                self.log_port.log_error("Workflow stage failed",
                                       stage_index=stage_index,
                                       plugin_id=plugin_id,
                                       error=str(e))
                
                # Handle error based on strategy
                if error_strategy == "fail_fast":
                    raise ActionExecutionError(
                        self.action_type,
                        f"Stage {stage_index} ({plugin_id}) failed: {e}"
                    )
                elif error_strategy == "continue_on_error":
                    self.log_port.log_warning("Continuing workflow despite stage failure",
                                             stage_index=stage_index,
                                             plugin_id=plugin_id)
                    continue
                else:
                    raise ActionExecutionError(
                        self.action_type,
                        f"Unknown error strategy: {error_strategy}"
                    )
        
        return current_content
    
    async def _execute_parallel_workflow(self,
                                        file_content: str,
                                        match: re.Match,
                                        file_path: str,
                                        stages: List[Dict[str, Any]],
                                        error_strategy: str,
                                        max_retries: int,
                                        timeout_seconds: int) -> str:
        """Execute workflow stages in parallel (for independent operations)."""
        # For parallel execution, all stages receive the same input content
        # and their results are merged or the first successful result is returned
        
        self.log_port.log_info("Starting parallel workflow execution",
                              stage_count=len(stages),
                              file_path=file_path)
        
        tasks = []
        for stage_index, stage in enumerate(stages):
            plugin_id = stage["plugin_id"]
            stage_params = stage.get("params", {})
            
            task = asyncio.create_task(
                self._execute_single_stage(
                    file_content, match, file_path, plugin_id, stage_params, 
                    stage_index, max_retries, timeout_seconds
                )
            )
            tasks.append((stage_index, plugin_id, task))
        
        # Wait for all tasks with error handling
        results = []
        for stage_index, plugin_id, task in tasks:
            try:
                result = await task
                results.append((stage_index, plugin_id, result, None))
            except Exception as e:
                results.append((stage_index, plugin_id, None, e))
                
                if error_strategy == "fail_fast":
                    # Cancel remaining tasks
                    for _, _, remaining_task in tasks:
                        remaining_task.cancel()
                    raise ActionExecutionError(
                        self.action_type,
                        f"Parallel stage {stage_index} ({plugin_id}) failed: {e}"
                    )
        
        # Process results - for now, return the content from the first successful stage
        # In a more sophisticated implementation, this could merge results or apply other logic
        for stage_index, plugin_id, result, error in results:
            if error is None and result:
                self.log_port.log_info("Using result from parallel stage",
                                      stage_index=stage_index,
                                      plugin_id=plugin_id)
                return result
        
        # If no stage succeeded, return original content
        self.log_port.log_warning("No parallel stages succeeded, returning original content")
        return file_content
    
    async def _execute_single_stage(self,
                                   file_content: str,
                                   match: re.Match,
                                   file_path: str,
                                   plugin_id: str,
                                   stage_params: Dict[str, Any],
                                   stage_index: int,
                                   max_retries: int,
                                   timeout_seconds: int) -> str:
        """Execute a single stage with retry logic."""
        for attempt in range(max_retries + 1):
            try:
                # Get plugin execution port
                plugin_port = self.context.get_port("plugin_execution")
                
                # Prepare execution data
                input_data = {
                    "file_content": file_content,
                    "match": match,
                    "file_path": file_path,
                    "params": stage_params
                }
                
                # Execute the plugin
                result = await asyncio.wait_for(
                    plugin_port.execute_plugin(plugin_id, input_data),
                    timeout=timeout_seconds
                )
                
                if result.get("success", False):
                    return result.get("result", file_content)
                else:
                    error_msg = result.get("error", "Unknown error")
                    raise ActionExecutionError(plugin_id, error_msg)
                    
            except asyncio.TimeoutError:
                if attempt < max_retries:
                    self.log_port.log_warning("Single stage execution timed out, retrying",
                                             stage_index=stage_index,
                                             plugin_id=plugin_id,
                                             attempt=attempt + 1)
                    continue
                else:
                    raise ActionExecutionError(
                        plugin_id,
                        f"Stage timed out after {max_retries} attempts"
                    )
            except Exception as e:
                if attempt < max_retries:
                    self.log_port.log_warning("Single stage execution failed, retrying",
                                             stage_index=stage_index,
                                             plugin_id=plugin_id,
                                             attempt=attempt + 1,
                                             error=str(e))
                    continue
                else:
                    raise
        
        # Should not reach here
        raise ActionExecutionError(
            plugin_id,
            f"Stage failed after {max_retries} attempts"
        )
    
    def get_description(self) -> str:
        """Get description of the orchestrator."""
        return "L2 Orchestrator plugin for coordinating complex file processing workflows"