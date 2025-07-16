# Experiment Registry and Innovation Policy

**Version:** 1.0
**Applies to:** AOS v5.0

---

## 1. Principle: From Anecdote to Evidence

AOS v5.0 moves away from making sweeping claims based on limited data. Instead, it adopts a culture of scientific discipline where all strategic patterns and methodological claims are treated as falsifiable hypotheses that must be validated through controlled experimentation.

This policy directly addresses Critique #6 (Hasty Generalization) and #45 (Algorithmic Homogenization) by creating a formal system for tracking experiments and actively encouraging novelty.

## 2. The Experiment Registry

The **Experiment Registry** is a central, conceptual component of the AOS Knowledge Graph. It serves as an auditable log of all hypotheses, experiments, and their outcomes. Every time a new pattern or methodology is applied, an entry is created in the registry containing:

*   **`hypothesis`**: The claim being tested (e.g., "Applying TRIZ principle X will reduce development cost by 15%").
*   **`null_hypothesis`**: The condition that would falsify the claim.
*   **`context`**: The project, team, and environmental context of the experiment.
*   **`outcome`**: The measured results and data from the experiment.
*   **`validation_status`**: The current status of the pattern.

## 3. Pattern Validation Status

Every strategic or methodological pattern in the Knowledge Graph **MUST** have a `validation_status`. The AI recommendation engine is governed by this status:

*   **`Hypothesized`**: A new, untested pattern. The AI can propose this, but must clearly label it as experimental.
*   **`Tested`**: The pattern has been tested at least once with a positive result, but lacks sufficient data for broad recommendation.
*   **`Validated`**: The pattern has been successfully replicated across a statistically significant number of varied contexts. Only `Validated` patterns can be recommended by the AI as "best practice."
*   **`Deprecated`**: A pattern that has been superseded or has been proven ineffective through experimentation.

## 4. The "Exploration Bonus" (Anti-Homogenization)

To prevent a methodological monoculture where the AI only recommends historically successful `Validated` patterns, the recommendation engine **MUST** implement an "exploration bonus" policy (such as a multi-armed bandit with an epsilon-greedy algorithm).

*   **Mechanism:** For a certain percentage of recommendations (e.g., ε = 20%), the AI is instructed to deliberately propose a `Hypothesized` or `Tested` pattern instead of the `Validated` optimum.
*   **Goal:** This ensures a continuous pipeline of innovation by structurally forcing the system to test novel approaches. Successful experiments are rewarded and can eventually be promoted to `Validated` status, enriching the entire ecosystem. 
