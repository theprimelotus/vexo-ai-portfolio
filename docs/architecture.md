# VEXO AI — Architecture

## Scope

This document describes the architectural approach used by the private VEXO implementation. It is intentionally high-level and omits production source, credentials, infrastructure addresses and operational configuration.

## Core Pipeline

```text
Sources
  ↓
Adapters
  ↓
Normalization
  ↓
Product Intelligence
  ↓
Evidence Ledger
  ↓
Decision Policy
  ↓
Guarded Action
  ↓
External Commerce / Supplier Systems
```

The pipeline is not designed as a single mutable workflow. Each stage has a defined contract and produces state that downstream stages can validate.

## Boundary: Evidence vs Decision

A central design choice is separating:

1. **Evidence acquisition**
2. **Evidence representation**
3. **Decision policy**
4. **Side-effecting execution**

The Evidence Ledger records what the system knows and how that knowledge was obtained.

The decision layer consumes validated evidence and determines whether an action is permissible.

This prevents a common automation failure mode: a downstream executor interpreting "the previous function returned successfully" as proof that the business condition has been established.

## Evidence States

The implementation uses explicit evidence states:

| State | Meaning |
| --- | --- |
| `observed` | Directly obtained from an external or authoritative source |
| `derived` | Computed deterministically from known evidence |
| `inferred` | Estimated from available signals |
| `interpreted` | Produced by a higher-level interpretation process |
| `missing` | Required evidence was not available |
| `failed` | Evidence acquisition or validation failed |

These states remain distinct instead of collapsing everything into a generic "value exists" flag.

## Product Intelligence

Product records from different sources are normalized into a canonical representation.

Matching can consider:

- title
- brand
- category
- attributes
- external IDs
- variants
- pricing
- dimensions

The goal is to make identity decisions deterministic where possible and to surface conflicts when the available evidence is insufficient.

## AI Execution Layer

The AI layer is provider-agnostic at the orchestration boundary.

A provider adapter exposes a common execution contract while the runtime maintains:

- capability metadata
- provider health
- retry policy
- timeout policy
- failure classification
- fallback selection

The orchestrator can therefore change providers without rewriting business logic around provider-specific APIs.

## Background Runtime

Long-running and asynchronous work is handled through an explicit job runtime.

Representative state:

```text
queued
  ↓
claimed
  ↓
running
  ├──→ completed
  ├──→ retryable failure → queued
  ├──→ terminal failure → dead-letter
  └──→ worker loss → stale recovery
```

Redis primitives are used for atomic state transitions, idempotency and worker ownership.

## Side Effects

Commerce and supplier actions are treated as side effects that require validated state.

Where an action is activation-sensitive, the design prefers:

```text
validated evidence
    ↓
decision state
    ↓
guard
    ↓
draft / reversible action
    ↓
explicit activation boundary
```

This reduces accidental writes caused by ambiguous or partially validated upstream state.

## Data and Observability

PostgreSQL provides durable relational persistence for structured state.

Redis provides transient execution state and coordination.

Observability includes:

- structured logs
- correlation IDs
- request tracing
- health checks
- Sentry error reporting
- credential scrubbing

The purpose is not merely to collect logs, but to make failures attributable to a particular execution path and state transition.

## Architecture Principles

### Explicit state
Important conditions are represented as state rather than inferred from control flow.

### Bounded retries
Retries are finite and policy-driven. Repeating a failing operation forever is not considered recovery.

### Fail closed
When a required validation or security condition fails, the system stops the sensitive action.

### Idempotent execution
Repeated delivery of the same job or event should not create an unintended duplicate side effect.

### Guarded side effects
The path from evidence to an external mutation is deliberately narrower than the path used to collect information.

### Test the failure modes
A workflow is not considered adequately verified merely because the happy path works.
