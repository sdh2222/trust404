# TRUST404 Track 1 — ensemble image: detector (Python/Slither) + noexit (TypeScript AST), one entry point.
# Built FROM the hardened detector image so solc pins, OpenZeppelin trees, any-uid and read-only guarantees carry over.
#   docker build --platform linux/amd64 --build-arg BASE=ghcr.io/sdh2222/trust404-detector:latest -t trust404/ensemble:latest .
#   docker run --rm --network none -e ENSEMBLE_MODE=judge -v "$PWD/cases":/input:ro trust404/ensemble:latest > out.json
ARG BASE=ghcr.io/sdh2222/trust404-detector:latest
FROM ${BASE}

RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY noexit/package.json noexit/package-lock.json /app/noexit/
RUN cd /app/noexit && npm ci --ignore-scripts
COPY noexit/tsconfig.json noexit/run.sh /app/noexit/
COPY noexit/src /app/noexit/src
RUN cd /app/noexit && npx tsc -p tsconfig.json && npm prune --omit=dev \
    && rm -rf "${HOME}/.npm" /root/.npm

COPY tools/ensemble.py /app/tools/ensemble.py
RUN chmod -R a+rX /app/noexit /app/tools /opt/detector-home

ENV ENSEMBLE_NODE=node
ENTRYPOINT ["python3", "/app/tools/ensemble.py"]
CMD ["/input"]
