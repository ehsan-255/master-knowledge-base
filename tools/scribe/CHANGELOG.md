# Changelog

## [1.1.0] - 2025-07-15

### Added
- Central Event Bus for decoupled event handling (Rec 1).
- Explicit Ports and Adapters for improved swappability (Rec 2).
- Resilience features with retries and fallbacks (Rec 3).
- Comprehensive observability with Prometheus metrics (Rec 4).
- Factories and Dependency Injection for core components (Swappability Rec 1).
- Config-driven extensions with pre/post hooks (Swappability Rec 2).

### Changed
- Updated watcher and worker to use Event Bus.
- Enhanced engine startup with factories.
- Improved README and documentation for v1.1 features. 