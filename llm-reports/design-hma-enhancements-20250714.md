# Design Document: HMA Enhancements for Scribe v1.1

**Date:** 2025-07-14  
**Version:** 1.0  

## Current State Analysis
- Engine directly instantiates Watcher and Worker.
- No central event bus; uses direct queue.
- Implicit adapters without ports.
- Basic resilience via circuit breakers only.
- Health endpoint exists but no metrics/tracing.

## Decomposed Recommendations
1. Event Bus: Implement pub/sub in L2.
2. Ports/Adapters: Define abstract classes for L1/L4.
3. Resilience: Add retries in dispatcher.
4. Observability: Integrate Prometheus and tracing.
5. Factories/DI: Add factories for watcher/worker.
6. Config Extensions: Add 'watchers' section; worker hooks.

## Prioritization
- Event bus → Ports → Resilience → Observability → Factories → Config.

## Design Principles
- Use ABC for ports.
- Factories load from config without L3 plugins.
- Maintain HMA layers.

## Updated Architecture Diagram
```
┌── L1: Driving Adapters (via Ports) ──┐
│ FileSystemWatcher │ APIWatcher │ ... │
└──────────┬──────────┬──────────┘
           │          │
┌──────────▼──────────▼──────────┐
│ L2: Microkernel Core          │
│ EventBus → Worker (with hooks)│
│ ConfigManager │ PluginLoader │
└──────────┬──────────┬──────────┘
           │          │
┌──────────▼──────────▼──────────┐
│ L3: Capability Plugins        │
│ RunCommand │ Frontmatter │ ...│
└──────────┬──────────┬──────────┘
           │          │
┌──────────▼──────────▼──────────┐
│ L4: Driven Adapters (via Ports)│
│ AtomicFileWriter │ DBWriter │...│
└────────────────────────────────┘
``` 