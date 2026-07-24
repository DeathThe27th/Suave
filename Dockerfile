# Suave service image. Node is included so the Impeccable detector (npx impeccable)
# can run headless inside the request path — verify its runtime cost on the VPS
# before depending on it (BUILD.md §2 vet step).
FROM python:3.12-slim

# Node.js for `npx impeccable detect`.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY suave ./suave
COPY library ./library

ENV PORT=8000
EXPOSE 8000

CMD ["python", "-m", "suave.server"]
