#!/usr/bin/env python3
"""Panoramix emulate entrypoint for httpbin (binds PLATFORM_LISTEN_HTTP)."""

from __future__ import annotations

import os

from httpbin.core import app


def main() -> None:
    port = int(os.environ.get("PLATFORM_LISTEN_HTTP", "18080"))
    # Flask's built-in server is enough for emulate dogfood.
    app.run(host="127.0.0.1", port=port, threaded=True)


if __name__ == "__main__":
    main()
