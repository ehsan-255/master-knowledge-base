#!/usr/bin/env python3
"""
Setup configuration for Scribe HMA v2.2 Engine
"""

from setuptools import setup, find_packages

setup(
    name="scribe-engine",
    version="2.2.0",
    description="Scribe HMA v2.2 Compliant File Processing Engine",
    author="Scribe Development Team",
    author_email="dev@scribe.local",
    packages=find_packages(),
    install_requires=[
        "watchdog>=3.0.0",
        "structlog>=23.0.0", 
        "jsonschema>=4.0.0",
        "pyyaml>=6.0.0",
        "click>=8.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "opentelemetry-api>=1.20.0",
        "opentelemetry-sdk>=1.20.0",
        "opentelemetry-exporter-otlp-proto-grpc>=1.20.0",
        "opentelemetry-exporter-prometheus>=1.12.0rc1",
        "opentelemetry-instrumentation-fastapi>=0.41b0",
        "opentelemetry-instrumentation-requests>=0.41b0",
        "opentelemetry-instrumentation-urllib3>=0.41b0",
        "nats-py>=2.6.0",
        "requests>=2.31.0",
        "httpx>=0.25.0",
        "cryptography>=41.0.0",
        "hvac>=2.0.0",
        "schedule>=1.2.0",
        "pandas>=2.0.0",
        "rdflib>=7.0.0",
        "pyshacl>=0.25.0",
        "portalocker>=2.8.0"
    ],
    extras_require={
        "test": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0", 
            "pytest-timeout>=2.1.0",
            "pytest-cov>=4.1.0"
        ],
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0"
        ]
    },
    entry_points={
        'console_scripts': [
            'scribe=tools.scribe.main:main',
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: System :: Filesystems",
        "Topic :: System :: Monitoring"
    ],
    long_description="HMA v2.2 compliant file processing engine with sophisticated boundary validation, telemetry, and plugin architecture.",
    long_description_content_type="text/plain"
)