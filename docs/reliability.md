# VEXO AI — Reliability & Verification

## Reliability Model

Reliability is treated as a set of explicit failure modes rather than as a generic quality claim.

The main failure classes are:

- provider timeout or malformed AI response
- duplicate job delivery
- worker interruption
- stale ownership
- datastore interruption
- invalid supplier data
- webhook spoofing or malformed payloads
- incomplete decision evidence
- external API rejection

Each class has a corresponding control and a verification path.

## Redis Job Runtime

The background runtime uses Redis to coordinate work.

Key controls include:

### Atomic idempotency
A job/event identity is registered atomically so retries or duplicate delivery do not accidentally execute the same logical work more than once.

### Worker ownership
A worker claims a job with an ownership marker and lease semantics.

### Leases
Ownership expires when a worker disappears. The runtime can then identify stale work rather than leaving it permanently "running".

### Bounded retries
Failures are classified. Retryable failures receive bounded retry attempts; terminal failures are moved to dead-letter handling.

### Heartbeats
Long-running work can refresh its lease while it remains active.

### Graceful shutdown
Workers stop accepting new work and release or preserve state in a controlled manner rather than abandoning in-flight ownership without a recovery path.

## Provider Resilience

AI providers can fail independently.

The execution layer therefore treats these as normal operational cases:

```text
request
  ↓
capability match
  ↓
provider health check
  ↓
attempt
  ├── success → response validation
  ├── retryable failure → bounded retry
  └── terminal/provider failure → alternate provider
```

A provider should not become a hidden single point of failure for the rest of the application.

## Failure-Mode Verification

Representative tests exercise cases such as:

| Failure | Expected control |
| --- | --- |
| Duplicate job | Idempotent guard |
| Worker crash | Lease expiry + stale recovery |
| Temporary provider timeout | Bounded retry |
| Repeated provider failure | Failover / terminal classification |
| Invalid webhook signature | Reject before processing |
| Missing required evidence | Hold / reject sensitive action |
| Invalid supplier data | Validation failure + fail-closed behaviour |
| Database/Redis unavailable | Explicit operational failure, no unsafe continuation |

## CI Verification

The private implementation uses automated checks covering:

- Python compilation
- linting
- unit tests
- integration tests
- disposable PostgreSQL environments
- disposable Redis environments
- failure-injection scenarios
- Docker builds

The public repository does not claim a specific production uptime or transaction volume. Its purpose is to show how reliability is engineered and verified.

## Reliability Design Rules

### 1. Make recovery stateful
Recovery should depend on explicit state such as lease ownership and retry counters, not on assumptions about what a worker "probably" did.

### 2. Keep retry budgets finite
A bounded system is easier to reason about than one that can create infinite work under persistent failure.

### 3. Verify before side effects
The closer an operation is to an irreversible external mutation, the stronger its validation boundary should be.

### 4. Preserve evidence
When a decision is challenged later, the system should be able to distinguish direct observation from inference.

### 5. Treat partial failure as normal
External providers, networks, workers and services fail independently. The design should assume this rather than treating it as exceptional.
