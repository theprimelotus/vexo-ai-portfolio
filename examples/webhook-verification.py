"""Sanitized HMAC webhook verification example.

This example shows the security boundary only.
It does not include production Shopify configuration or secrets.
"""

from __future__ import annotations

import hashlib
import hmac


def verify_hmac(*, raw_body: bytes, signature: str, secret: bytes) -> bool:
    """Return True only when the signature matches the raw payload."""
    expected = hmac.new(
        secret,
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


if __name__ == "__main__":
    body = b'{"event":"example"}'
    secret = b"development-only-example-secret"

    valid_signature = hmac.new(
        secret,
        body,
        hashlib.sha256,
    ).hexdigest()

    print(verify_hmac(
        raw_body=body,
        signature=valid_signature,
    ))
