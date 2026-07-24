 use # Suave — Build Plan

**What it is:** a pay-per-call agent on OKX.AI that generates landing pages with
*sourced* design taste. Not "AI makes you a page." A curated library of 20 real
design systems, extracted from human-made references, poured into your product copy
with licensed photography, then slop-checked before it ships.

**Why it isn't cloneable by a prompt:** raw models default to the average. Skills fix
reflexes but don't supply direction. Suave supplies *specific sourced direction* —
20 vetted style systems — and then runs Impeccable's detector to strip the model's
remaining tells. Direction + desloppification. Neither half alone gets there.

---

## 0. The two phases (read this first)

Everything below splits into two clearly separate phases. Confusing them is the
main way this build goes wrong.

| | **Phase A — Library (offline, one time)** | **Phase B — Service (runtime, per call)** |
|---|---|---|
| When | Now, on Codespaces, by you + Claude Code | Every paid API call, on the VPS |
| Input | 20 Pinterest screenshots | product brief + style id |
| Output | 20 `.md` style specs | one HTML landing page |
| Sees the images? | Yes | **No — never** |
| Cost | Your time | Model tokens + image API |

**The images never ship.** They exist only during Phase A. At runtime Suave reads
*specs*, not pictures. This matters for reliability (no image handling in the request
path) and for legality (you sell your own encoded systems, not someone's artwork).

---

## 1. Phase A — building the library

### Does it "copy each style"? No. It *extracts* each style.

Copying = reproducing a specific design. Fragile, drifts back to generic when you
change the content, and legally dicey to resell.

Extracting = reading a reference and filling a **fixed structured spec** — exact hex
values, exact type scale, section order, the signature moves, the spacing rules.
The spec is yours, it's abstract, and it survives being recolored and reused with
completely different content.

### The workflow

```
/references/          ← your 20 Pinterest screenshots (git-ignored, never deployed)
/library/             ← 20 extracted specs. THIS is the product.
  01-swiftlogix-warm.md
  02-...
/SPEC-TEMPLATE.md     ← the fixed format every entry must fill
/EXTRACT.md           ← the instructions Claude Code follows to do an extraction
```

1. Drop image into `/references/`
2. Run the extraction prompt (see `EXTRACT.md`) in Claude Code, pointed at that image
3. Claude Code fills every field of `SPEC-TEMPLATE.md` — no blanks, no vibe words
4. **You verify** against the original: are the hexes right? did it catch the
   signature moves, or just say "modern and clean"?
5. Save to `/library/`

### The spec fields (non-negotiable)

Full worked example already exists as `style-spec-template.md`. Fields:

- **identity** — id, one-liner, best_for, avoid_for
- **palette** — named hex per role + the *accent usage rule* (where accent may touch)
- **type** — display/body faces, weights, exact clamp sizes, letter-spacing
- **layout skeleton** — numbered section order and structure
- **signature moves** — the specific memorable things (ghost watermark, `//` eyebrows,
  clipped floating card, black pill + arrow). ← the field that decides quality
- **shape & spacing** — radii, section padding, shadow character, border weight
- **imagery** — photo style, treatment, source
- **recolor slots** — what may change on remix, what must NOT

### Two rules that keep the library from rotting

**Rule 1: perfect one before you do twenty.** Get a single extraction genuinely tight
and verified. If the format is mushy, you'll mass-produce 20 mushy specs and every
generated page will drift to average. One good spec > twenty vague ones.

**Rule 2: spread the taste deliberately.** Pick your 20 to span real range — warm
editorial, dark technical, brutalist, soft consumer, minimal luxury, playful,
maximalist, swiss/grid. If you grab 20 SwiftLogix lookalikes, "mix and match" is a lie
and the library is one style in 20 coats.

---

## 2. Phase B — the service

### Request pipeline

```
1. BRIEF     parse product name, what it does, audience, tone, sections needed
2. STYLE     load spec from /library/ (user picks id, or Suave picks by best_for)
3. COPY      write landing copy grounded in the brief — no filler adjectives
4. IMAGES    Unsplash/Pexels API, server-side, matched to spec's imagery rules
5. ASSEMBLE  pour copy + images into the spec's skeleton, honoring signature moves
6. VET       Impeccable detector → fix flagged slop → re-check
7. RETURN    single self-contained HTML file
```

### Output format

Single-file HTML for v1. Self-contained, no build step, no dependency that can 404
during OKX's review. React output is phase 2.

### Images: API, not hotlink

Call the Unsplash/Pexels API server-side and embed properly. Do **not** hotlink
scraped CDN URLs — they break unpredictably (this already happened once during
prototyping). Both APIs are free with commercial-use licenses.

### The vet step (Impeccable)

`npx impeccable detect src/` — 46 deterministic rules, **no LLM call**, returns exit
codes. This is the right vet for us precisely because it's deterministic: no extra
tokens, no extra latency, no new timeout risk.

- Wire it as a post-assembly check on the generated file
- On failure, feed the flagged anti-patterns back for one repair pass, then re-detect
- Hard-cap at one repair loop — a runaway loop is a timeout, and timeouts are how
  Olise died

**Must verify before depending on it:** that the detector runs headless on the VPS
inside the request path, and how long it takes. Impeccable is built as a dev-time
tool; runtime use is adjacent to its design. Test early, and keep a bypass flag so a
detector failure degrades to "return unvetted page" instead of "return nothing."

---

## 3. OKX compliance — fixing what killed Olise

The rejection had three reasons. They were one root cause wearing three hats: the
endpoint wasn't reachable, so x402 couldn't be validated, so the task timed out.

### 3.1 Reachability — the fix your VPS mostly solves

Per the A2MCP guide, the endpoint must be:
- On a **public server reachable worldwide**
- Served over **HTTPS**
- **Tied to a domain** — the docs are explicit that MCP requires an HTTPS address
  on a domain. A bare IP will not pass.

**So the VPS alone is not enough. You need:**
- [ ] A domain name pointed at the VPS
- [ ] An HTTPS certificate (Let's Encrypt / certbot, free)
- [ ] Nginx reverse proxy → your app
- [ ] Firewall open on 80/443
- [ ] A process manager (systemd or pm2) so it restarts on crash/reboot
- [ ] An uptime ping so you find out it's down before OKX does

Node placement note from the docs: Singapore/Tokyo for overseas audiences, Hong Kong
if you want both sides of the China firewall. If your VPS is elsewhere, it still
works — just confirm it's reachable from Asia.

### 3.2 x402 / payment — the biggest open unknown

**Honest status: unresolved.** The x402 doc URL in the rejection email
(`/okxai/howtokmcp`) returns a 404 — it looks like a typo for `/okxai/howtomcp`,
which is the A2MCP guide and contains no x402 detail.

What the docs *do* say (ASP Registration, step 4): for A2MCP, once listed, every API
call triggers billing and is **settled instantly via the OKX Payment SDK**, fully
automated, no manual intervention. Registration asks for name, description,
**price per call**, and endpoint.

That reads like the platform handles settlement — but the rejection explicitly told
you to integrate x402 on *your* server so unpaid requests return a standard 402
challenge. Those two things need reconciling and I can't reconcile them from public
docs.

**→ TASK ZERO, before any Suave code:** find the real OKX Payment SDK / x402 spec.
Ask OKX support directly (they invited resubmission via chat — use that channel to
ask what exactly failed x402 validation on Olise). Also check the Onchain OS skills
package, which likely contains the answer:

```
npx skills add okx/onchainos-skills --yes -g
```

Do not build the payment layer on a guess. This is the exact thing that failed.

### 3.3 Timeouts

- Hard timeout budget per call, well under whatever OKX's tester tolerates
- One repair loop maximum on the vet step
- Every external call (model API, image API) gets its own timeout + fallback
- If generation exceeds budget, return a valid degraded result rather than hanging
- Load-test with concurrent calls before submitting

### 3.4 Registration path

From the docs, registration is conversational via Onchain OS skills:

1. `npx skills add okx/onchainos-skills --yes -g`, log into Agentic Wallet with email
2. "Help me register an A2MCP ASP on OKX.AI using Onchain OS"
   → provide name, description, price per call, endpoint
3. "Help me list my ASP on OKX.AI using Onchain OS"
4. **Review takes up to 2 business days**, result emailed to your Agentic Wallet email

### 3.5 Pre-submit checklist

- [ ] MCP Inspector connects and successfully calls the tool
- [ ] A real AI client can call it end-to-end
- [ ] Unpaid request returns a correct 402 challenge (once 3.2 is resolved)
- [ ] Endpoint reachable from outside your network, over HTTPS, on a domain
- [ ] Survives a VPS reboot
- [ ] Returns within timeout budget under concurrent load
- [ ] The agent responds to `"I would like to use the services of agent ID {id}"`

---

## 4. Stack

- **Server:** Ubuntu VPS, FastAPI, wrapped as MCP with FastMCP (both named in OKX docs)
- **Proxy/TLS:** Nginx + certbot
- **Model:** API-based (the VPS can't run a decent local LLM — no GPU)
- **Images:** Unsplash or Pexels API, server-side
- **Vet:** Impeccable detector CLI
- **Library:** flat `.md` files in the repo, loaded at startup

---

## 5. Money

Not free to run. The model calls are the real cost — a few tenths of a cent to a
couple cents per generation depending on model and page size.

**Rule: price per call above your worst-case per-call cost.** Registration asks for a
per-call price up front, so compute it before you register. Measure actual token cost
on 10 real generations, take the worst, add margin.

Market context: the runaway best-seller on OKX (PixelBrief, brand kits) prices at
0.02 USDT and has done 10k+ sales. Cheap + instant + tangible artifact is the pattern
that's working. Price in that neighborhood, not at $2.

---

## 6. Build order

**Task Zero — resolve x402** (blocks submission, not development)
Ask OKX support what failed on Olise. Install onchainos-skills. Find the real spec.

**Day 1 — foundation**
1. Domain → VPS, Nginx, HTTPS, systemd. Prove a hello-world endpoint is publicly
   reachable over HTTPS on the domain. *Do this before any Suave logic.*
2. Perfect ONE style extraction. Verify it against the reference yourself.

**Day 2 — core**
3. Extract remaining 19 specs
4. Build the pipeline (brief → style → copy → images → assemble)
5. Wire Impeccable detector + one repair loop

**Day 3 — ship**
6. FastMCP wrap, MCP Inspector test
7. x402 layer per Task Zero findings
8. Timeout + concurrency testing
9. Register, list, submit

---

## 7. Known risks

| Risk | Mitigation |
|---|---|
| **x402 spec unknown** — killed Olise, still unresolved | Task Zero. Ask support directly. Don't guess. |
| Extraction too loose → specs generate slop | Perfect one, verify by eye, before scaling to 20 |
| Impeccable detector too slow / won't run headless | Test early, bypass flag, hard loop cap |
| Model cost exceeds call price | Measure 10 real generations before setting price |
| Library lacks range | Choose the 20 across deliberately different aesthetics |
| 2-day review + unknown hackathon deadline | Confirm the deadline. This is not a same-day ship. |

---

## 8. Naming

**Suave.** Matches the GitHub handle. Fits the product — pages that look effortless.
