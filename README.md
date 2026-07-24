# Suave

A pay-per-call agent on OKX.AI that generates landing pages with **sourced design
taste**. Not "AI makes you a page." A curated library of real design systems, extracted
from human-made references into structured specs, poured into your product copy with
licensed photography, then slop-checked before it ships.

Why it isn't cloneable by a prompt: raw models default to the average. Suave supplies
*specific sourced direction* — vetted style systems — then strips the model's remaining
tells. Direction + desloppification. Neither half alone gets there.

See **[BUILD.md](BUILD.md)** for the full build plan and **[style-spec-template.md](style-spec-template.md)** for the spec format.

## Two phases

| | Phase A — Library (offline) | Phase B — Service (runtime) |
|---|---|---|
| Input | reference screenshots | product brief + style id |
| Output | `.md` style specs in `/library` | one HTML landing page |
| Sees images? | yes | **no — reads specs, never images** |

The images never ship. At runtime Suave reads *specs*, not pictures — for reliability
(no image handling in the request path) and legality (we sell our own encoded systems).

## Phase A — build the library

```
references/          your reference screenshots (git-ignored, never deployed)
library/             the extracted specs — THIS is the product
SPEC-TEMPLATE.md     the fixed format every entry must fill
EXTRACT.md           the instructions Claude Code follows to do an extraction
```

Drop an image in `references/`, follow `EXTRACT.md`, verify the filled spec against the
original by eye, save to `library/NN-<id>.md`. Perfect one before you do twenty; spread
the twenty across deliberately different aesthetics.

## Phase B — the service

```
suave/
  config.py     env-driven config + timeout budget
  library.py    load specs at startup
  brief.py      parse the request
  style.py      pick a spec (explicit id, or by best_for)
  images.py     Unsplash/Pexels, server-side
  assemble.py   copy + assemble into one self-contained HTML file
  vet.py        Impeccable detector (deterministic slop check)
  payment.py    x402 stub — OFF until Task Zero is resolved
  pipeline.py   brief -> style -> images -> assemble -> vet -> return
  server.py     FastAPI app + FastMCP tool wrapper
```

Request pipeline: `BRIEF -> STYLE -> COPY -> IMAGES -> ASSEMBLE -> VET -> RETURN`.
Output is a single self-contained HTML file (v1): no build step, no dependency that can
404 during OKX's review. Everything is timeout-bounded and degrades to a valid result
rather than hanging — timeouts are how the previous agent died.

## Run locally

```bash
pip install -r requirements.txt
cp .env.example .env          # set GEMINI_API_KEY (image keys optional)
python -m suave.server        # serves on :8000
```

```bash
curl -sX POST localhost:8000/generate \
  -H 'content-type: application/json' \
  -d '{"product":"Ferry","what_it_does":"same-day courier for law firms","tone":"trustworthy"}' \
  > page.html
```

`GET /health` for status, `GET /styles` for the library, `POST /generate` for a page
(`{"format":"json"}` in the body returns metadata + HTML instead of raw HTML).

## Docker

```bash
docker build -t suave .
docker run -p 8000:8000 --env-file .env suave
```

The image bundles Node so the Impeccable detector can run headless in the request path.

## OKX.AI listing

Registering/listing on OKX.AI is a conversational flow via the Onchain OS skills
(`.agents/skills/`, `skills-lock.json`). Suave registers **fresh** as a new ERC-8004
A2MCP ASP — the old football agent is retired. Before submission, resolve **Task Zero**:
confirm the real OKX Payment SDK / x402 spec (BUILD §3.2) before enabling the payment
layer. Do not build the payment layer on a guess — that's the exact thing that failed
last time.
