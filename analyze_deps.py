#!/usr/bin/env python3
"""
Professional dependency analysis to identify Python >=3.12 requirement
"""

import subprocess
import sys
import json

def check_dependency_python_requirement(dep_name):
    """Check Python version requirement for a specific dependency."""
    try:
        # Use pip show to get dependency info
        result = subprocess.run([
            sys.executable, "-m", "pip", "show", dep_name
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✓ {dep_name}: Available in environment")
            return True
        else:
            print(f"✗ {dep_name}: Not installed - {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ {dep_name}: Error checking - {e}")
        return False

def analyze_pyproject_dependencies():
    """Analyze dependencies from pyproject.toml"""
    print("PROFESSIONAL DEPENDENCY ANALYSIS")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print()
    
    # Key dependencies that might require newer Python
    critical_deps = [
        "opentelemetry-api",
        "opentelemetry-sdk", 
        "opentelemetry-exporter-otlp-proto-grpc",
        "opentelemetry-exporter-prometheus",
        "opentelemetry-instrumentation-fastapi",
        "pandas",
        "fastapi",
        "httpx",
        "uvicorn",
        "cryptography",
        "hvac"
    ]
    
    print("Checking critical dependencies:")
    print("-" * 30)
    
    available = []
    unavailable = []
    
    for dep in critical_deps:
        if check_dependency_python_requirement(dep):
            available.append(dep)
        else:
            unavailable.append(dep)
    
    print(f"\nSUMMARY:")
    print(f"Available: {len(available)}")
    print(f"Unavailable: {len(unavailable)}")
    
    if unavailable:
        print(f"\nUnavailable dependencies: {', '.join(unavailable)}")
        
    return available, unavailable

if __name__ == "__main__":
    analyze_pyproject_dependencies()