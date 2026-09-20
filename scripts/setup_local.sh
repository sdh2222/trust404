#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  if command -v uv >/dev/null 2>&1; then
    uv venv --python 3.12 .venv
  else
    python3 -m venv .venv
  fi
fi

if command -v uv >/dev/null 2>&1; then
  uv pip install --python .venv/bin/python -e '.[dev]'
  uv pip install --python .venv/bin/python -r detector/requirements.txt
else
  .venv/bin/pip install -e '.[dev]'
  .venv/bin/pip install -r detector/requirements.txt
fi

installed=0
for v in $(cat detector/solc_versions.txt); do
  dest="${HOME}/.solc-select/artifacts/solc-${v}/solc-${v}"
  if [[ ! -f "$dest" ]]; then
    .venv/bin/solc-select install "$v"
  fi
  installed=$((installed + 1))
done

echo "INSTALLED ${installed}"

if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
  cd noexit
  if [[ ! -d node_modules ]]; then
    npm ci --ignore-scripts
    echo "noexit: ran npm ci --ignore-scripts"
  else
    echo "noexit: node_modules present; skipped npm ci"
  fi
  npx tsc -p tsconfig.json
  echo "noexit: ran npx tsc -p tsconfig.json"
  cd - >/dev/null
else
  echo "node/npm not found: run.sh will run DEGRADED (detector only); install Node 18+ and re-run this script" >&2
fi

echo "hint: ./run.sh <dir>  or  DETECTOR_NO_DOCKER=1 ./run.sh <dir>"
