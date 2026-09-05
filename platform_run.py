#!/usr/bin/env python3
"""Panoramix entrypoint for httpbin (binds PLATFORM_LISTEN_HTTP)."""

from __future__ import annotations

import os

from httpbin.core import app


def parse_listen(raw: str) -> tuple[str, int]:
    """Accept port, :port, or host:port. Port-only keeps emulate loopback."""
    raw = (raw or "18080").strip()
    if raw.startswith(":"):
        return "0.0.0.0", int(raw[1:])
    if ":" in raw:
        host, port = raw.rsplit(":", 1)
        if host in ("", "*", "[::]"):
            host = "0.0.0.0"
        return host, int(port)
    return "127.0.0.1", int(raw)


def main() -> None:
    raw = (
        os.environ.get("PLATFORM_LISTEN_HTTP")
        or os.environ.get("PLATFORM_LISTEN_http")
        or "18080"
    )
    host, port = parse_listen(raw)
    # Flask's built-in server is enough for emulate dogfood / container lab.
    # Reloader off so apply SIGTERM does not leave an orphan child.
    app.run(host=host, port=port, threaded=True, use_reloader=False)


if __name__ == "__main__":
    main()
