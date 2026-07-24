"""Suave — a pay-per-call agent that generates landing pages with sourced design taste.

Two phases (see BUILD.md):
  Phase A (offline): 20 reference screenshots -> 20 .md style specs in /library.
  Phase B (runtime, this package): product brief + style id -> one HTML landing page.

At runtime Suave reads *specs*, never images.
"""

__version__ = "0.1.0"
