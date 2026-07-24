"""Step 4 — IMAGES. Fetch photography server-side from Unsplash/Pexels.

Call the API server-side and hand back real URLs (or None). Do NOT hotlink scraped
CDN URLs — they break unpredictably (this already bit us in prototyping; BUILD.md §2).
Both APIs are free with commercial-use licenses. Every call is timeout-bounded and
degrades to None so a slow image API never sinks the whole request.
"""

from __future__ import annotations

import httpx

from .config import CONFIG


def _from_unsplash(query: str, count: int) -> list[str]:
    if not CONFIG.unsplash_access_key:
        return []
    r = httpx.get(
        "https://api.unsplash.com/search/photos",
        params={"query": query, "per_page": count, "orientation": "landscape"},
        headers={"Authorization": f"Client-ID {CONFIG.unsplash_access_key}"},
        timeout=CONFIG.image_timeout_s,
    )
    r.raise_for_status()
    return [p["urls"]["regular"] for p in r.json().get("results", [])][:count]


def _from_pexels(query: str, count: int) -> list[str]:
    if not CONFIG.pexels_api_key:
        return []
    r = httpx.get(
        "https://api.pexels.com/v1/search",
        params={"query": query, "per_page": count, "orientation": "landscape"},
        headers={"Authorization": CONFIG.pexels_api_key},
        timeout=CONFIG.image_timeout_s,
    )
    r.raise_for_status()
    return [p["src"]["large"] for p in r.json().get("photos", [])][:count]


def fetch_images(query: str, count: int = 3) -> list[str]:
    """Best-effort. Try Unsplash, fall back to Pexels, then to []. Never raises."""
    for source in (_from_unsplash, _from_pexels):
        try:
            urls = source(query, count)
            if urls:
                return urls
        except Exception:
            continue
    return []
