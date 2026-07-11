"""Persistence layer.

Primary backend: Supabase Postgres via PostgREST (tables in schema.sql).
The service role key cannot run DDL, so if the tables don't exist yet the
store falls back to a local SQLite database with the same shape and logs
how to enable the Supabase backend (run schema.sql in the SQL editor).
"""

from __future__ import annotations

import json
import logging
import sqlite3
import threading
from datetime import datetime, timezone

from olise import config

log = logging.getLogger("olise.store")

TABLES = ("api_cache", "reports", "forecasts", "results")

REPORT_COLS = [
    "report_id", "fixture_id", "cache_key", "home", "away", "kickoff_utc",
    "competition", "stage", "status", "input_hash", "pdf_url", "pdf_sha256",
    "commit_hash", "tx_hash", "explorer_url", "settled", "report_json",
    "versions", "created_at", "updated_at",
]
FORECAST_COLS = [
    "report_id", "idx", "market", "selection", "probability", "grade",
    "drivers", "contradiction", "outcome",
]
RESULT_COLS = [
    "report_id", "fixture_id", "results_json", "correct", "total",
    "settle_tx", "results_uri", "settled_at",
]

_JSON_FIELDS = {"report_json", "versions", "drivers", "results_json", "params", "payload"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SQLiteBackend:
    name = "sqlite"

    def __init__(self):
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(str(config.SQLITE_PATH), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS api_cache (
                cache_key TEXT PRIMARY KEY, endpoint TEXT, params TEXT,
                payload TEXT, fetched_at TEXT);
            CREATE TABLE IF NOT EXISTS reports (
                report_id TEXT PRIMARY KEY, fixture_id INTEGER, cache_key TEXT,
                home TEXT, away TEXT, kickoff_utc TEXT, competition TEXT,
                stage TEXT, status TEXT, input_hash TEXT, pdf_url TEXT,
                pdf_sha256 TEXT, commit_hash TEXT, tx_hash TEXT,
                explorer_url TEXT, settled INTEGER DEFAULT 0, report_json TEXT,
                versions TEXT, created_at TEXT, updated_at TEXT);
            CREATE TABLE IF NOT EXISTS forecasts (
                report_id TEXT, idx INTEGER, market TEXT, selection TEXT,
                probability REAL, grade TEXT, drivers TEXT,
                contradiction INTEGER DEFAULT 0, outcome TEXT DEFAULT 'pending',
                PRIMARY KEY (report_id, idx));
            CREATE TABLE IF NOT EXISTS results (
                report_id TEXT PRIMARY KEY, fixture_id INTEGER,
                results_json TEXT, correct INTEGER, total INTEGER,
                settle_tx TEXT, results_uri TEXT, settled_at TEXT);
            """
        )
        self._conn.commit()

    @staticmethod
    def _encode(row: dict) -> dict:
        out = {}
        for k, v in row.items():
            if k in _JSON_FIELDS and v is not None and not isinstance(v, str):
                v = json.dumps(v)
            if isinstance(v, bool):
                v = int(v)
            out[k] = v
        return out

    @staticmethod
    def _decode(row) -> dict:
        d = dict(row)
        for k in _JSON_FIELDS:
            if d.get(k) and isinstance(d[k], str):
                try:
                    d[k] = json.loads(d[k])
                except (json.JSONDecodeError, ValueError):
                    pass
        for k in ("settled", "contradiction"):
            if k in d and d[k] is not None:
                d[k] = bool(d[k])
        return d

    def upsert(self, table: str, row: dict, pk: list[str]):
        row = self._encode(row)
        cols = ", ".join(row)
        ph = ", ".join("?" for _ in row)
        with self._lock:
            self._conn.execute(
                f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({ph})",
                list(row.values()),
            )
            self._conn.commit()

    def select(self, table: str, where: dict | None = None) -> list[dict]:
        sql = f"SELECT * FROM {table}"
        args = []
        if where:
            sql += " WHERE " + " AND ".join(f"{k} = ?" for k in where)
            args = [int(v) if isinstance(v, bool) else v for v in where.values()]
        with self._lock:
            rows = self._conn.execute(sql, args).fetchall()
        return [self._decode(r) for r in rows]

    def delete(self, table: str, where: dict):
        sql = f"DELETE FROM {table} WHERE " + " AND ".join(f"{k} = ?" for k in where)
        with self._lock:
            self._conn.execute(sql, list(where.values()))
            self._conn.commit()


class SupabaseBackend:
    name = "supabase"

    def __init__(self):
        from supabase import create_client
        self.client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)
        # probe: raises if tables are missing
        for t in TABLES:
            self.client.table(t).select("*").limit(1).execute()

    def upsert(self, table: str, row: dict, pk: list[str]):
        self.client.table(table).upsert(row, on_conflict=",".join(pk)).execute()

    def select(self, table: str, where: dict | None = None) -> list[dict]:
        q = self.client.table(table).select("*")
        for k, v in (where or {}).items():
            q = q.eq(k, v)
        return q.execute().data or []

    def delete(self, table: str, where: dict):
        q = self.client.table(table).delete()
        for k, v in where.items():
            q = q.eq(k, v)
        q.execute()


class Store:
    """Backend-agnostic persistence API used by the rest of the app."""

    def __init__(self):
        try:
            self.backend = SupabaseBackend()
            log.info("store: using Supabase Postgres backend")
        except Exception as e:  # tables missing or network issue
            self.backend = SQLiteBackend()
            log.warning(
                "store: Supabase tables unavailable (%s) — using local SQLite "
                "fallback. Run schema.sql in the Supabase SQL editor and "
                "restart to enable the Postgres backend.", str(e)[:200],
            )

    # --- api cache -----------------------------------------------------
    def cache_get(self, key: str, max_age: float) -> dict | None:
        rows = self.backend.select("api_cache", {"cache_key": key})
        if not rows:
            return None
        row = rows[0]
        try:
            age = (datetime.now(timezone.utc)
                   - datetime.fromisoformat(row["fetched_at"])).total_seconds()
        except (ValueError, TypeError, KeyError):
            return None
        if age > max_age:
            return None
        payload = row["payload"]
        return json.loads(payload) if isinstance(payload, str) else payload

    def cache_set(self, key: str, endpoint: str, params: dict, payload: dict):
        self.backend.upsert("api_cache", {
            "cache_key": key, "endpoint": endpoint, "params": params,
            "payload": payload, "fetched_at": _now(),
        }, pk=["cache_key"])

    # --- reports ---------------------------------------------------------
    def upsert_report(self, rec: dict):
        rec = {k: rec.get(k) for k in REPORT_COLS}
        rec["updated_at"] = _now()
        rec.setdefault("created_at", rec["updated_at"])
        if not rec.get("created_at"):
            rec["created_at"] = rec["updated_at"]
        self.backend.upsert("reports", rec, pk=["report_id"])

    def get_report(self, report_id: str) -> dict | None:
        rows = self.backend.select("reports", {"report_id": report_id})
        return rows[0] if rows else None

    def find_report_by_cache_key(self, cache_key: str) -> dict | None:
        rows = self.backend.select("reports", {"cache_key": cache_key})
        return rows[0] if rows else None

    def find_reports_by_fixture(self, fixture_id: int) -> list[dict]:
        return self.backend.select("reports", {"fixture_id": fixture_id})

    def list_reports(self, **where) -> list[dict]:
        return self.backend.select("reports", where or None)

    # --- forecasts -------------------------------------------------------
    def save_forecasts(self, report_id: str, forecasts: list[dict]):
        self.backend.delete("forecasts", {"report_id": report_id})
        for i, f in enumerate(forecasts):
            row = {
                "report_id": report_id, "idx": i,
                "market": f["market"], "selection": f["selection"],
                "probability": f["model_probability"], "grade": f["grade"],
                "drivers": f.get("drivers", []),
                "contradiction": bool(f.get("contradiction", False)),
                "outcome": f.get("outcome", "pending"),
            }
            self.backend.upsert("forecasts", row, pk=["report_id", "idx"])

    def get_forecasts(self, report_id: str) -> list[dict]:
        rows = self.backend.select("forecasts", {"report_id": report_id})
        return sorted(rows, key=lambda r: r.get("idx", 0))

    def update_forecast_outcome(self, report_id: str, idx: int, outcome: str):
        rows = self.backend.select("forecasts", {"report_id": report_id, "idx": idx})
        if rows:
            row = rows[0]
            row["outcome"] = outcome
            self.backend.upsert("forecasts", row, pk=["report_id", "idx"])

    def all_forecasts(self) -> list[dict]:
        return self.backend.select("forecasts")

    # --- results -----------------------------------------------------------
    def save_result(self, rec: dict):
        rec = {k: rec.get(k) for k in RESULT_COLS}
        rec.setdefault("settled_at", _now())
        self.backend.upsert("results", rec, pk=["report_id"])

    def get_result(self, report_id: str) -> dict | None:
        rows = self.backend.select("results", {"report_id": report_id})
        return rows[0] if rows else None

    def all_results(self) -> list[dict]:
        return self.backend.select("results")
