"""Report rendering (Jinja2 → WeasyPrint PDF) and Supabase storage upload."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import httpx
from jinja2 import Environment, FileSystemLoader

from olise import config

log = logging.getLogger("olise.report")

_env = Environment(
    loader=FileSystemLoader(Path(__file__).resolve().parent),
    autoescape=True,
)


def _build_html(ctx: dict) -> str:
    return _env.get_template("template.html").render(**ctx)


def render_pdf(report: dict) -> bytes:
    """Render the report dict (see main.assemble_report_context) to PDF bytes."""
    from weasyprint import HTML  # imported lazily: heavy
    html = _build_html(report)
    return HTML(string=html).write_pdf()


async def render_pdf_async(report: dict) -> bytes:
    return await asyncio.to_thread(render_pdf, report)


def assemble_context(report_id: str, status: str, dataset: dict, engine: dict,
                     research: dict, forecasts: list[dict], summary: str) -> dict:
    fx = dataset["fixture"]
    adjusted = bool(research.get("factors"))
    matrix = engine["goals_adj"]["matrix"]
    sub = [row[:6] for row in matrix[:6]]
    matrix_max = max(p for row in sub for p in row) if sub else 0
    return {
        "report_id": report_id,
        "status": status,
        "home": dataset["home"]["name"],
        "away": dataset["away"]["name"],
        "competition": fx.get("competition"),
        "stage": fx.get("stage"),
        "kickoff_utc": (fx.get("date_utc") or "")[:16].replace("T", " "),
        "venue": fx.get("venue"),
        "city": fx.get("city"),
        "summary": summary,
        "form_n": config.FORM_MATCHES,
        "home_block": dataset["home"],
        "away_block": dataset["away"],
        "h2h": dataset["h2h"],
        "injuries": dataset["injuries"],
        "lineups": dataset["lineups"],
        "referee": fx.get("referee"),
        "referee_stats": None,
        "factors": research.get("factors", []),
        "research_note": research.get(
            "note", "No verified context findings for this fixture."),
        "engine": engine,
        "adjusted": adjusted,
        "matrix": sub,
        "matrix_max": matrix_max,
        "top_scores": engine["goals_adj"]["most_likely_scores"],
        "forecasts": forecasts,
        "contradictions": engine["contradictions"],
    }


async def upload_pdf(report_id: str, pdf: bytes, version: int = 1) -> str:
    """Upload to the public Supabase bucket; returns the public URL."""
    path = f"{report_id}/v{version}.pdf"
    url = f"{config.SUPABASE_URL}/storage/v1/object/{config.SUPABASE_BUCKET}/{path}"
    headers = {
        "Authorization": f"Bearer {config.SUPABASE_SERVICE_ROLE_KEY}",
        "apikey": config.SUPABASE_SERVICE_ROLE_KEY,
        "Content-Type": "application/pdf",
        "x-upsert": "true",
    }
    async with httpx.AsyncClient(timeout=60) as http:
        r = await http.post(url, content=pdf, headers=headers)
        if r.status_code >= 400:
            raise RuntimeError(f"PDF upload failed: {r.status_code} {r.text[:200]}")
    return (f"{config.SUPABASE_URL}/storage/v1/object/public/"
            f"{config.SUPABASE_BUCKET}/{path}")


async def upload_json(path: str, payload: str) -> str:
    """Upload a JSON document (e.g. settlement results) to the public bucket."""
    url = f"{config.SUPABASE_URL}/storage/v1/object/{config.SUPABASE_BUCKET}/{path}"
    headers = {
        "Authorization": f"Bearer {config.SUPABASE_SERVICE_ROLE_KEY}",
        "apikey": config.SUPABASE_SERVICE_ROLE_KEY,
        "Content-Type": "application/json",
        "x-upsert": "true",
    }
    async with httpx.AsyncClient(timeout=30) as http:
        r = await http.post(url, content=payload.encode(), headers=headers)
        if r.status_code >= 400:
            raise RuntimeError(f"JSON upload failed: {r.status_code} {r.text[:200]}")
    return (f"{config.SUPABASE_URL}/storage/v1/object/public/"
            f"{config.SUPABASE_BUCKET}/{path}")
