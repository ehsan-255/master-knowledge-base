#!/usr/bin/env python3
"""
Test individual dependency installation to identify Python >=3.12 requirement
"""

import subprocess
import sys

def test_dependency_install(dep_spec):
    """Test installing a single dependency to identify Python version conflicts."""
    print(f"\n{'='*60}")
    print(f"TESTING: {dep_spec}")
    print(f"{'='*60}")
    
    try:
        # Try dry-run installation to check compatibility
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--dry-run", dep_spec
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✓ COMPATIBLE: {dep_spec}")
            print("Output:", result.stdout.strip()[:200] + "..." if len(result.stdout) > 200 else result.stdout.strip())
            return True
        else:
            print(f"✗ INCOMPATIBLE: {dep_spec}")
            print("Error:", result.stderr.strip()[:300] + "..." if len(result.stderr) > 300 else result.stderr.strip())
            
            # Check if it's specifically a Python version issue
            if "requires a different Python" in result.stderr or ">=3.12" in result.stderr:
                print("🚨 IDENTIFIED: This dependency requires Python >=3.12")
                return False
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {dep_spec} took too long to resolve")
        return False
    except Exception as e:
        print(f"❌ ERROR: {dep_spec} - {e}")
        return False

def main():
    """Test critical dependencies individually."""
    print(f"SYSTEMATIC DEPENDENCY TESTING")
    print(f"Python: {sys.version}")
    print(f"Executable: {sys.executable}")
    
    # Test the most likely culprits first
    critical_deps = [
        "pandas>=2.0.0",
        "fastapi>=0.100.0", 
        "httpx>=0.25.0",
        "opentelemetry-exporter-otlp-proto-grpc>=1.20.0",
        "opentelemetry-exporter-prometheus>=0.56b0",
        "opentelemetry-instrumentation-fastapi>=0.41b0",
        "cryptography>=41.0.0",
        "hvac>=2.0.0",
        "uvicorn>=0.23.0"
    ]
    
    compatible = []
    incompatible = []
    
    for dep in critical_deps:
        if test_dependency_install(dep):
            compatible.append(dep)
        else:
            incompatible.append(dep)
    
    print(f"\n{'='*60}")
    print(f"FINAL ANALYSIS")
    print(f"{'='*60}")
    print(f"Compatible dependencies: {len(compatible)}")
    for dep in compatible:
        print(f"  ✓ {dep}")
    
    print(f"\nIncompatible dependencies: {len(incompatible)}")
    for dep in incompatible:
        print(f"  ✗ {dep}")

if __name__ == "__main__":
    main()