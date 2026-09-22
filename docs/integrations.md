# VEXO AI — Integrations

## Integration Strategy

External systems are isolated behind explicit contracts and adapters.

The integration boundary is responsible for:

- authentication
- request construction
- response validation
- normalization
- error classification
- bounded retries
- observability
- security checks

Business logic consumes normalized results instead of embedding provider-specific response shapes throughout the application.

## Shopify

The commerce integration uses server-side authentication and Shopify Admin GraphQL for authenticated workflows.

Representative flow:

```text
Shop / organization match
        ↓
Authentication
        ↓
Admin GraphQL request
        ↓
Response validation
        ↓
Normalized commerce evidence
        ↓
Evidence Ledger
        ↓
Decision / guarded action
```

Activation-sensitive product actions are separated from data acquisition. A validated product can remain in a draft or non-active state until the required decision state is satisfied.

### Webhooks

Webhook verification uses HMAC-SHA256.

The important sequence is:

1. Receive the raw request body.
2. Obtain the provider signature header.
3. Recompute the expected signature from the raw body and shared secret.
4. Compare signatures using a timing-safe comparison.
5. Reject before business processing when verification fails.

A sanitized example is provided in [examples/webhook-verification.py](../examples/webhook-verification.py).

## Supplier / CJ Dropshipping

Supplier integration is contract-driven.

Representative capabilities include:

- product lookup
- pricing retrieval
- inventory retrieval
- response normalization
- validation
- bounded retries
- explicit failure classification

Supplier values are not treated as authoritative merely because a request returned HTTP success. The normalized response is validated before it becomes downstream evidence.

## AI Providers

The AI execution layer supports multiple provider adapters.

The adapter boundary separates:

- provider credentials
- API request/response details
- capability metadata
- error classification
- health state

The orchestrator can therefore choose an available provider based on capability and health rather than hard-coding one provider throughout the workflow.

Representative providers used across the private project include cloud and local execution paths such as OpenAI, Gemini, Grok, Azure OpenAI, Arvan Cloud, Ollama and llama.cpp.

The public repository does not include production credentials or provider-specific operational configuration.

## Security at Integration Boundaries

Every external integration should answer four questions:

### Who is calling?
Authentication or signature verification.

### What did they send?
Schema and payload validation.

### What does it mean?
Normalization and business-level validation.

### Can this action happen?
Decision gates and authorization/approval state.

This keeps transport-level success separate from business-level acceptance.

## Observability

Integration requests and failures are designed to be traceable through:

- correlation IDs
- structured events
- request tracing
- safe error logging
- credential scrubbing
- Sentry reporting

The goal is to identify the failing integration path without leaking secrets into logs.
