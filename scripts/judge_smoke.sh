#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: scripts/judge_smoke.sh <dir> [image]" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$1"
if [[ $# -ge 2 ]]; then
  export DETECTOR_IMAGE="$2"
fi

WORKDIR="${HOME}/.dsmoke/judge_smoke.$$"
mkdir -p "$WORKDIR"
OUT="${WORKDIR}/out.json"

if [[ -n "${DETECTOR_PYTHON:-}" ]]; then
  PY="${DETECTOR_PYTHON}"
elif [[ -x "${ROOT}/.venv/bin/python" ]]; then
  PY="${ROOT}/.venv/bin/python"
else
  PY="python3"
fi

set +e
if [[ -n "${JUDGE_SMOKE_REQUIRE_ENGINES:-}" ]]; then
  "${ROOT}/run.sh" "$DIR" > "$OUT" 2> "${WORKDIR}/run.err"
  run_exit=$?
  cat "${WORKDIR}/run.err" >&2
else
  "${ROOT}/run.sh" "$DIR" > "$OUT"
  run_exit=$?
fi
set -e

_require_engines() {
  local engines="${JUDGE_SMOKE_REQUIRE_ENGINES:-}"
  if [[ -z "$engines" ]]; then
    return 0
  fi
  local err="${WORKDIR}/run.err"
  local raw e
  local IFS=','
  local -a wanted
  read -ra wanted <<< "$engines"
  for raw in "${wanted[@]}"; do
    e="$(printf '%s' "$raw" | tr -d '[:space:]')"
    if [[ -z "$e" ]]; then
      continue
    fi
    if ! grep -E -q "\[ensemble\] ${e}: [0-9]+ rows" "$err"; then
      echo "judge_smoke: engine check failed: missing [ensemble] ${e}: N rows" >&2
      exit 1
    fi
  done
  if grep -q DEGRADED "$err"; then
    echo "judge_smoke: engine check failed: DEGRADED present" >&2
    exit 1
  fi
  echo "judge_smoke: engines ok: ${engines}"
}

if command -v check-jsonschema >/dev/null 2>&1; then
  set +e
  check-jsonschema --schemafile "${ROOT}/detector/schema/judge.schema.json" "$OUT" >&2
  val_exit=$?
  set -e
else
  set +e
  "$PY" -m detector.submission --validate "$OUT"
  val_exit=$?
  set -e
fi

if command -v jq >/dev/null 2>&1; then
  jq -r '.[] | "\(.file)\t\(.verdict)"' "$OUT"
  n="$(jq 'length' "$OUT")"
  m="$(jq '[.[] | select(.verdict=="MALICIOUS")] | length' "$OUT")"
  b="$(jq '[.[] | select(.verdict=="BENIGN")] | length' "$OUT")"
  u="$(jq '[.[] | select(.verdict=="UNCERTAIN")] | length' "$OUT")"
  _require_engines
  echo "judge_smoke: ${n} files, ${m} MALICIOUS, ${b} BENIGN, ${u} UNCERTAIN, run.sh exit=${run_exit}"
else
  "$PY" -c '
import json
import sys

path = sys.argv[1]
counts_path = sys.argv[2]
obj = json.load(open(path, encoding="utf-8"))
if not (isinstance(obj, list) and obj):
    raise SystemExit("expected a non-empty JSON array")
n = len(obj)
m = sum(1 for row in obj if row.get("verdict") == "MALICIOUS")
b = sum(1 for row in obj if row.get("verdict") == "BENIGN")
u = sum(1 for row in obj if row.get("verdict") == "UNCERTAIN")
for row in obj:
    print("%s\t%s" % (row["file"], row["verdict"]))
with open(counts_path, "w", encoding="utf-8") as fh:
    fh.write("%s %s %s %s\n" % (n, m, b, u))
' "$OUT" "${WORKDIR}/counts.txt"
  _require_engines
  read -r n m b u < "${WORKDIR}/counts.txt"
  echo "judge_smoke: ${n} files, ${m} MALICIOUS, ${b} BENIGN, ${u} UNCERTAIN, run.sh exit=${run_exit}"
fi

if [[ "$run_exit" -ne 0 || "$val_exit" -ne 0 ]]; then
  exit 1
fi
