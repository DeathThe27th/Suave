-- Olise AI — Supabase Postgres schema.
-- Run this once in the Supabase SQL editor to enable the Postgres backend.
-- Until these tables exist the service transparently uses a local SQLite
-- fallback (olise_local.db) with the identical shape.

create table if not exists api_cache (
    cache_key  text primary key,
    endpoint   text,
    params     jsonb,
    payload    jsonb,
    fetched_at timestamptz
);

create table if not exists reports (
    report_id    text primary key,
    fixture_id   bigint,
    cache_key    text,
    home         text,
    away         text,
    kickoff_utc  text,
    competition  text,
    stage        text,
    status       text,            -- provisional | final
    input_hash   text,
    pdf_url      text,
    pdf_sha256   text,
    commit_hash  text,
    tx_hash      text,
    explorer_url text,
    settled      boolean default false,
    report_json  jsonb,
    versions     jsonb,
    created_at   timestamptz,
    updated_at   timestamptz
);
create index if not exists reports_fixture_idx on reports (fixture_id);
create index if not exists reports_cache_key_idx on reports (cache_key);

create table if not exists forecasts (
    report_id     text,
    idx           integer,
    market        text,
    selection     text,
    probability   double precision,
    grade         text,            -- A | B | C
    drivers       jsonb,
    contradiction boolean default false,
    outcome       text default 'pending',  -- pending | correct | incorrect | void
    primary key (report_id, idx)
);

create table if not exists results (
    report_id    text primary key,
    fixture_id   bigint,
    results_json jsonb,
    correct      integer,
    total        integer,
    settle_tx    text,
    results_uri  text,
    settled_at   timestamptz
);

-- Service role key bypasses RLS; tables are not exposed to anon users.
alter table api_cache enable row level security;
alter table reports enable row level security;
alter table forecasts enable row level security;
alter table results enable row level security;
