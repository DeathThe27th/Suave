"""Central configuration for Olise AI. All secrets come from .env."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# --- secrets / external services -------------------------------------------
API_FOOTBALL_KEY = os.environ.get("API_FOOTBALL_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "olise-reports")
XLAYER_PRIVATE_KEY = os.environ.get("XLAYER_PRIVATE_KEY", "")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")

# --- service ----------------------------------------------------------------
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
SELF_URL = os.environ.get("SELF_URL", f"http://127.0.0.1:{PORT}")

# --- API-Football -----------------------------------------------------------
AF_BASE = "https://v3.football.api-sports.io"
WORLD_CUP_LEAGUE_ID = 1
WORLD_CUP_SEASON = 2026

# --- football-data.org (preferred provider when its token is set) ------------
FOOTBALL_DATA_TOKEN = os.environ.get("FOOTBALL_DATA_TOKEN", "")
FD_BASE = "https://api.football-data.org/v4"
WORLD_CUP_CODE = "WC"
FORM_MATCHES = 5

# cache TTLs (seconds) per data family
TTL_STATIC = 30 * 24 * 3600      # finished-fixture stats, H2H of past games
TTL_FIXTURE = 6 * 3600           # fixture lookups / schedules
TTL_VOLATILE = 15 * 60           # lineups, injuries near kickoff
TTL_HEALTH = 10 * 60

# --- Gemini -----------------------------------------------------------------
# gemini-2.5-flash was retired for new API users (verified 2026-07-12)
GEMINI_MODELS = ["gemini-3.5-flash", "gemini-flash-latest"]

# --- X Layer testnet --------------------------------------------------------
XLAYER_RPCS = ["https://testrpc.xlayer.tech", "https://xlayertestrpc.okx.com"]
# Live chain id verified 2026-07-11 (spec expected 195; testnet migrated).
XLAYER_CHAIN_ID = 1952
EXPLORER_TX = "https://www.oklink.com/xlayer-test/tx/{tx}"
EXPLORER_ADDR = "https://www.oklink.com/xlayer-test/address/{addr}"
CHAIN_STATE_FILE = ROOT / ".olise_chain.json"   # persisted deployed address
# env var takes precedence over the json file (ephemeral-disk hosts)
OLISE_CONTRACT_ADDRESS = os.environ.get("OLISE_CONTRACT_ADDRESS", "")

# --- engine / forecasts -----------------------------------------------------
PUBLISH_THRESHOLD = 0.55
GRADE_A = 0.75
GRADE_B = 0.65
MAX_ADJUSTMENT = 0.20            # cap on net context adjustment per market
MAGNITUDE_PCT = {"low": 0.03, "med": 0.07, "high": 0.12}

GOAL_LINES = (1.5, 2.5, 3.5)
CORNER_LINES = (8.5, 9.5, 10.5)
CARD_LINES = (3.5, 4.5, 5.5)
SHOT_LINES = (20.5, 23.5, 26.5)

SQLITE_PATH = ROOT / "olise_local.db"
