# Delegation of Authority Protocol

**Version:** 1.0
**Applies to:** AOS v5.0

## Overview
The Delegation of Authority Protocol introduces flexible autonomy to AOS, allowing processes to run in 'HumanInLoop' (human approval at gates) or 'FullAutonomy' (AI decisions via AIDeciderPlugin). It is stored as a 'delegation_policy' attribute in the PDP.

## delegation_policy Structure
- **mode:** 'HumanInLoop' or 'FullAutonomy'
- **step_overrides:** Optional map for per-step modes

## AIDeciderPlugin Role
In FullAutonomy, this L3 plugin acts as the AI decision-maker, using LLM reasoning to approve/adjust at gates, augmented by analysis from other plugins.

## Switching Modes
Humans can delegate steps or switch modes mid-process via UI or API. 

## Error Handling

### Failure Scenarios
- **AIDeciderPlugin Failure:** If the plugin fails (e.g., LLM timeout), default to HumanInLoop mode and notify human via event.
- **Mode Conflict:** If step_overrides conflict with global mode, prioritize overrides and log warning.
- **Human Unavailable in HumanInLoop:** Escalate with timeout; if unresolved, pause process and publish 'aos.delegation.escalation.v1' event.
- **Invalid Policy:** On PDP init, validate policy; if invalid, default to HumanInLoop and alert.

### Resolutions
- All errors publish events via EventBusPort for monitoring.
- Recovery: Retry failed decisions up to 3 times before escalation. 
