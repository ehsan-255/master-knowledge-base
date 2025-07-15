### Appendix G: Sustainability & Environmental Impact (Critique 50)

AOS v4.0 acknowledges that high-compute operations have an environmental cost. The following Green-Ops guidelines are recommended for any implementation.

- **Efficiency Measurement:** Track and report on energy-efficiency metrics. The `telemetry` object SHOULD be extended with a `sustainability_metrics` block.
  - `watts_per_1k_queries`: Target for knowledge graph query efficiency.
  - `compute_idle_percentage`: Target for scaling down unused resources.
- **Carbon Budgeting:** Projects with high expected compute loads (e.g., large-scale ML model training) SHOULD include a `carbon_budget_kg_co2` in their `problem_definition` as a non-functional requirement.
- **Offset Policy:** The organization SHOULD maintain a policy to offset unavoidable emissions through certified programs, funded by a small percentage of the IT operational budget. 