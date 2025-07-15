# The AOS Plain Language Handbook

**Version:** 1.0
**Applies to:** AOS v4.0

---

## 1. Goal: From Jargon to Clarity

AOS integrates many powerful academic and business theories. However, the specialized terminology from these fields can be intimidating and obscure the practical value of the framework. This handbook addresses Critique #4 (Appeal to Jargon) by providing a "translation layer" from theoretical terms to simple, problem-focused language.

Its purpose is to make the framework accessible to a wider audience, from executives to new team members.

## 2. The Plain Language Abstraction Layer

Every major artifact and concept in AOS v4.0 is required to have a `plain_language_summary` field in its schema. This field describes the purpose and findings of the artifact without using jargon.

## 3. Key Concept Translations

This section serves as a living glossary.

| Theoretical Term / Jargon | Plain Language Translation | Business Problem It Solves |
| :--- | :--- | :--- |
| **Antifragility** | Gaining strength from surprises, shocks, and uncertainty. | How do we get better and stronger when unexpected problems happen, instead of just breaking? |
| **Wardley Map** | A map of your business landscape, showing how different parts evolve over time. | Where should we build custom solutions, where should we use off-the-shelf products, and where should we use utilities? |
| **Theory of Constraints (TOC)**| Finding and fixing the one single biggest bottleneck that is slowing everything down. | What is the #1 thing we need to fix right now to improve our entire system's performance? |
| **Cynefin Framework** | A sense-making framework that helps you understand what kind of problem you have, so you can use the right approach to solve it. | Are we dealing with a simple, complicated, complex, or chaotic problem? How should we act? |
| **Project Digital Twin (PDP)** | A single, living document that contains everything about a project: the plan, the data, the decisions, and the results. | How can we have a single source of truth for a project that everyone can see and that updates in real-time? |
| **Hexagonal Microkernel (HMA)** | An architectural blueprint for building flexible, resilient software where different "capability plugins" can be easily added, removed, or swapped out. | How do we build a system that can easily adapt and evolve over time without requiring a complete rewrite? |
| **L3 Capability Plugin** | A self-contained piece of software that does one specific job, like "analyze user feedback" or "generate a Wardley Map". | How can we add new features to our system without breaking existing ones? |
| **L2 Orchestrator Plugin** | A "manager" plugin that coordinates a complex workflow by telling different capability plugins what to do and when. | How do we manage a complex, multi-step process like onboarding a new customer? |
| **Event-Driven Communication** | A style of communication where components announce that something has happened, and other components can choose to react to it, rather than components giving each other direct orders. | How can we make our system components less dependent on each other, so a failure in one doesn't bring down the whole system? |

This handbook should be regularly updated as the AOS framework evolves. 