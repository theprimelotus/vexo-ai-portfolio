"""Sanitized provider-execution example.

This is intentionally not the production VEXO implementation.
It demonstrates the architectural boundary used by a multi-provider
execution layer without exposing private adapters, credentials, or
operational configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Provider(Protocol):
    name: str

    def supports(self, capability: str) -> bool:
        ...

    def health(self) -> bool:
        ...

    def generate(self, prompt: str) -> str:
        ...


@dataclass(frozen=True)
class ExecutionResult:
    provider: str
    output: str


class ProviderExecutor:
    def __init__(self, providers: list[Provider]) -> None:
        self._providers = providers

    def execute(self, *, capability: str, prompt: str) -> ExecutionResult:
        candidates = [
            provider
            for provider in self._providers
            if provider.supports(capability) and provider.health()
        ]

        if not candidates:
            raise RuntimeError("no healthy provider supports the requested capability")

        last_error: Exception | None = None

        for provider in candidates:
            try:
                output = provider.generate(prompt)
                if not output.strip():
                    raise ValueError("provider returned an empty response")
                return ExecutionResult(provider=provider.name, output=output)
            except (TimeoutError, ConnectionError, ValueError) as exc:
                last_error = exc

        raise RuntimeError("all eligible providers failed") from last_error


class DemoProvider:
    def __init__(self, name: str, response: str, healthy: bool = True) -> None:
        self.name = name
        self._response = response
        self._healthy = healthy

    def supports(self, capability: str) -> bool:
        return capability == "text-generation"

    def health(self) -> bool:
        return self._healthy

    def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("prompt must not be empty")
        return self._response


if __name__ == "__main__":
    executor = ProviderExecutor(
        [
            DemoProvider("primary", response="demo response"),
            DemoProvider("fallback", response="fallback response"),
        ]
    )

    result = executor.execute(
        capability="text-generation",
        prompt="Return a short diagnostic response.",
    )
    print(f"{result.provider}: {result.output}")
