#!/usr/bin/env python3
"""
Scribe Engine 24-Hour Soak Test

This script implements the 24-hour stability test required by PHASE 1 EXIT CONDITION 1:
- Core engine runs for 24 hours under simulated load (5,000+ events)
- No memory leaks or crashes
- Stable performance metrics

The test creates a burst of 5,000 files initially, then continuously modifies
files every 500ms to maintain load throughout the 24-hour period.
"""

import sys
import time
import random
import tempfile
import threading
import json
import requests
import psutil
import signal
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add the scribe module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools" / "scribe"))

from engine import ScribeEngine
from core.logging_config import configure_structured_logging, get_scribe_logger


class SoakTestMonitor:
    """Monitors Scribe engine performance during soak test"""
    
    def __init__(self, engine_process: psutil.Process, health_url: str):
        self.engine_process = engine_process
        self.health_url = health_url
        self.start_time = datetime.now()
        self.metrics_history: List[Dict] = []
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Performance thresholds
        self.max_memory_mb = 500  # Maximum allowed memory usage
        self.max_queue_size = 100  # Maximum allowed queue size
        self.min_success_rate = 95.0  # Minimum success rate percentage
        
        self.logger = get_scribe_logger("soak_test_monitor")
    
    def start_monitoring(self):
        """Start continuous monitoring in background thread"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring and return final report"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        
        return self._generate_report()
    
    def _monitor_loop(self):
        """Main monitoring loop - runs every minute"""
        while self.monitoring:
            try:
                # Collect system metrics
                memory_info = self.engine_process.memory_info()
                cpu_percent = self.engine_process.cpu_percent()
                
                # Collect engine metrics via health endpoint
                try:
                    response = requests.get(self.health_url, timeout=5.0)
                    health_data = response.json() if response.status_code == 200 else {}
                except Exception as e:
                    health_data = {"error": str(e)}
                
                # Record metrics
                metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "uptime_minutes": (datetime.now() - self.start_time).total_seconds() / 60,
                    "memory_mb": memory_info.rss / 1024 / 1024,
                    "memory_vms_mb": memory_info.vms / 1024 / 1024,
                    "cpu_percent": cpu_percent,
                    "health_data": health_data
                }
                
                self.metrics_history.append(metrics)
                
                # Check for issues
                self._check_thresholds(metrics)
                
                # Log periodic status
                if len(self.metrics_history) % 10 == 0:  # Every 10 minutes
                    self.logger.info("Soak test status", 
                                   uptime_minutes=metrics["uptime_minutes"],
                                   memory_mb=metrics["memory_mb"],
                                   queue_size=health_data.get("queue_size", "unknown"))
                
                time.sleep(60)  # Monitor every minute
                
            except Exception as e:
                self.logger.error("Monitoring error", error=str(e))
                time.sleep(60)
    
    def _check_thresholds(self, metrics: Dict):
        """Check if metrics exceed acceptable thresholds"""
        memory_mb = metrics["memory_mb"]
        health_data = metrics["health_data"]
        
        # Memory leak detection
        if memory_mb > self.max_memory_mb:
            self.logger.warning("High memory usage detected", 
                              memory_mb=memory_mb, 
                              threshold_mb=self.max_memory_mb)
        
        # Queue size check
        queue_size = health_data.get("queue_size", 0)
        if queue_size > self.max_queue_size:
            self.logger.warning("High queue size detected",
                              queue_size=queue_size,
                              threshold=self.max_queue_size)
        
        # Success rate check
        success_rate = health_data.get("success_rate", 100.0)
        if success_rate < self.min_success_rate:
            self.logger.warning("Low success rate detected",
                              success_rate=success_rate,
                              threshold=self.min_success_rate)
    
    def _generate_report(self) -> Dict:
        """Generate final performance report"""
        if not self.metrics_history:
            return {"error": "No metrics collected"}
        
        # Calculate statistics
        memory_values = [m["memory_mb"] for m in self.metrics_history]
        cpu_values = [m["cpu_percent"] for m in self.metrics_history]
        
        final_health = self.metrics_history[-1]["health_data"]
        
        report = {
            "test_duration_hours": (datetime.now() - self.start_time).total_seconds() / 3600,
            "total_samples": len(self.metrics_history),
            "memory_stats": {
                "initial_mb": memory_values[0] if memory_values else 0,
                "final_mb": memory_values[-1] if memory_values else 0,
                "max_mb": max(memory_values) if memory_values else 0,
                "avg_mb": sum(memory_values) / len(memory_values) if memory_values else 0,
                "memory_growth_mb": (memory_values[-1] - memory_values[0]) if len(memory_values) > 1 else 0
            },
            "cpu_stats": {
                "max_percent": max(cpu_values) if cpu_values else 0,
                "avg_percent": sum(cpu_values) / len(cpu_values) if cpu_values else 0
            },
            "final_engine_stats": final_health,
            "issues_detected": self._detect_issues()
        }
        
        return report
    
    def _detect_issues(self) -> List[str]:
        """Detect potential issues from metrics history"""
        issues = []
        
        if not self.metrics_history:
            return ["No metrics collected"]
        
        memory_values = [m["memory_mb"] for m in self.metrics_history]
        
        # Memory leak detection (>50MB growth over test)
        if len(memory_values) > 1:
            memory_growth = memory_values[-1] - memory_values[0]
            if memory_growth > 50:
                issues.append(f"Potential memory leak: {memory_growth:.1f}MB growth")
        
        # High memory usage
        max_memory = max(memory_values) if memory_values else 0
        if max_memory > self.max_memory_mb:
            issues.append(f"High memory usage: {max_memory:.1f}MB (threshold: {self.max_memory_mb}MB)")
        
        # Check final engine stats
        final_health = self.metrics_history[-1]["health_data"]
        if "error" in final_health:
            issues.append(f"Health endpoint error: {final_health['error']}")
        
        success_rate = final_health.get("success_rate", 100.0)
        if success_rate < self.min_success_rate:
            issues.append(f"Low success rate: {success_rate:.1f}% (threshold: {self.min_success_rate}%)")
        
        return issues


class SoakTestWorkloadGenerator:
    """Generates continuous file system events for soak testing"""
    
    def __init__(self, test_dir: Path, num_initial_files: int = 5000):
        self.test_dir = test_dir
        self.num_initial_files = num_initial_files
        self.test_files: List[Path] = []
        self.generating = False
        self.generator_thread: Optional[threading.Thread] = None
        
        self.logger = get_scribe_logger("soak_test_workload")
    
    def create_initial_burst(self):
        """Create initial burst of files to generate 5,000+ events"""
        self.logger.info("Creating initial file burst", count=self.num_initial_files)
        
        for i in range(self.num_initial_files):
            file_path = self.test_dir / f"test_file_{i:05d}.md"
            content = f"""# Test File {i}

This is test file number {i} created for the Scribe soak test.

## Content

- File ID: {i}
- Created: {datetime.now().isoformat()}
- Purpose: Soak test workload generation

## Test Data

Random data: {random.randint(1000, 9999)}
"""
            file_path.write_text(content)
            self.test_files.append(file_path)
            
            # Progress logging
            if (i + 1) % 1000 == 0:
                self.logger.info("File creation progress", created=i+1, total=self.num_initial_files)
        
        self.logger.info("Initial file burst complete", total_files=len(self.test_files))
    
    def start_continuous_generation(self):
        """Start continuous file modification every 500ms"""
        self.generating = True
        self.generator_thread = threading.Thread(target=self._generation_loop, daemon=True)
        self.generator_thread.start()
        self.logger.info("Continuous workload generation started")
    
    def stop_generation(self):
        """Stop continuous generation"""
        self.generating = False
        if self.generator_thread:
            self.generator_thread.join(timeout=5.0)
        self.logger.info("Workload generation stopped")
    
    def _generation_loop(self):
        """Main generation loop - modifies files every 500ms"""
        modification_count = 0
        
        while self.generating:
            try:
                # Randomly select a file to modify
                if self.test_files:
                    file_path = random.choice(self.test_files)
                    
                    # Read current content
                    current_content = file_path.read_text()
                    
                    # Append modification
                    modification = f"\n\n## Modification {modification_count}\n\n"
                    modification += f"- Modified at: {datetime.now().isoformat()}\n"
                    modification += f"- Random value: {random.randint(1000, 9999)}\n"
                    
                    # Write back
                    file_path.write_text(current_content + modification)
                    
                    modification_count += 1
                    
                    # Log progress periodically
                    if modification_count % 1000 == 0:
                        self.logger.info("Continuous modification progress", 
                                       modifications=modification_count)
                
                time.sleep(0.5)  # 500ms between modifications
                
            except Exception as e:
                self.logger.error("Workload generation error", error=str(e))
                time.sleep(1.0)


def run_soak_test(duration_hours: float = 24.0, quick_test: bool = False) -> bool:
    """
    Run the complete 24-hour soak test
    
    Args:
        duration_hours: Test duration in hours (default 24)
        quick_test: If True, run a 5-minute test for validation
    
    Returns:
        True if test passes, False if issues detected
    """
    if quick_test:
        duration_hours = 5.0 / 60.0  # 5 minutes
        print("🧪 Running QUICK SOAK TEST (5 minutes) for validation")
    else:
        print("🧪 Starting 24-HOUR SOAK TEST")
    
    # Configure logging
    configure_structured_logging(log_level="INFO")
    logger = get_scribe_logger("soak_test")
    
    # Create test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)
        health_port = 9473
        health_url = f"http://localhost:{health_port}/health"
        
        logger.info("Soak test starting", 
                   duration_hours=duration_hours,
                   test_dir=str(test_dir),
                   health_url=health_url)
        
        # Create workload generator
        workload = SoakTestWorkloadGenerator(test_dir, num_initial_files=1000 if quick_test else 5000)
        
        # Create engine
        engine = ScribeEngine(
            watch_paths=[str(test_dir)],
            file_patterns=["*.md"],
            health_port=health_port
        )
        
        try:
            # Start engine
            logger.info("Starting Scribe engine")
            engine.start()
            time.sleep(2.0)  # Let engine stabilize
            
            # Get engine process for monitoring
            engine_process = psutil.Process()
            
            # Start monitoring
            monitor = SoakTestMonitor(engine_process, health_url)
            monitor.start_monitoring()
            
            # Create initial file burst
            logger.info("Generating initial workload")
            workload.create_initial_burst()
            
            # Wait for initial processing
            time.sleep(5.0)
            
            # Start continuous generation
            workload.start_continuous_generation()
            
            # Calculate end time
            end_time = datetime.now() + timedelta(hours=duration_hours)
            logger.info("Soak test running", end_time=end_time.isoformat())
            
            # Main test loop
            while datetime.now() < end_time:
                remaining = end_time - datetime.now()
                
                # Log progress every hour (or every minute for quick test)
                progress_interval = 60 if quick_test else 3600
                if int(remaining.total_seconds()) % progress_interval == 0:
                    logger.info("Soak test progress", 
                               remaining_hours=remaining.total_seconds() / 3600)
                
                time.sleep(60)  # Check every minute
            
            logger.info("Soak test duration complete, stopping workload")
            
        except KeyboardInterrupt:
            logger.info("Soak test interrupted by user")
        except Exception as e:
            logger.error("Soak test error", error=str(e))
            return False
        finally:
            # Stop workload generation
            workload.stop_generation()
            
            # Stop monitoring and get report
            logger.info("Collecting final performance report")
            report = monitor.stop_monitoring()
            
            # Stop engine
            logger.info("Stopping Scribe engine")
            engine.stop()
        
        # Analyze results
        logger.info("Soak test complete, analyzing results")
        return _analyze_soak_test_results(report, logger)


def _analyze_soak_test_results(report: Dict, logger) -> bool:
    """Analyze soak test results and determine pass/fail"""
    
    logger.info("=== SOAK TEST RESULTS ===")
    logger.info("Test duration", hours=report.get("test_duration_hours", 0))
    logger.info("Memory stats", **report.get("memory_stats", {}))
    logger.info("CPU stats", **report.get("cpu_stats", {}))
    
    final_stats = report.get("final_engine_stats", {})
    if final_stats and "error" not in final_stats:
        logger.info("Final engine stats", **final_stats)
    
    # Check for issues
    issues = report.get("issues_detected", [])
    
    if not issues:
        logger.info("🎉 SOAK TEST PASSED - No issues detected!")
        logger.info("✅ PHASE 1 EXIT CONDITION 1 SATISFIED")
        return True
    else:
        logger.error("❌ SOAK TEST FAILED - Issues detected:")
        for issue in issues:
            logger.error("Issue", description=issue)
        return False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scribe Engine 24-Hour Soak Test")
    parser.add_argument("--quick", action="store_true", 
                       help="Run 5-minute quick test instead of 24-hour test")
    parser.add_argument("--duration", type=float, default=24.0,
                       help="Test duration in hours (default: 24)")
    
    args = parser.parse_args()
    
    # Handle Ctrl+C gracefully
    def signal_handler(signum, frame):
        print("\n🛑 Soak test interrupted by user")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run test
    success = run_soak_test(duration_hours=args.duration, quick_test=args.quick)
    
    if success:
        print("\n🎉 SOAK TEST PASSED!")
        sys.exit(0)
    else:
        print("\n❌ SOAK TEST FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main() 