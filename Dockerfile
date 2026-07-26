# Suave service image. Node + the Impeccable detector are baked in so the vet step
# runs headless inside the request path with no mid-call download (BUILD.md §2 vet step).
FROM python:3.12-slim

# Node.js for the Impeccable detector.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Pre-install the detector globally so the request path calls the `impeccable` binary
# directly (~0.2s) instead of a cold `npx --yes` resolve (~26s, which blows vet_timeout_s
# on the first request). We only ever scan HTML *files* (static analysis), never URLs, so
# skip puppeteer's ~150MB chromium download — it is never launched.
ENV PUPPETEER_SKIP_DOWNLOAD=1
# Pinned for reproducibility — the detector's rule set is part of the product; a silent
# `latest` bump must not change vetting under us. Bump deliberately after re-verifying.
# 3.3.1 is the version the vet step was verified against (0.9s on a page, `detect` CLI
# surface as vet.py calls it). Do not pin backwards: 2.x is a different rule set.
RUN npm install -g impeccable@3.3.1 --no-fund --no-audit \
    && impeccable --version \
    && npm cache clean --force

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY suave ./suave
COPY library ./library

ENV PORT=8000
EXPOSE 8000

CMD ["python", "-m", "suave.server"]
