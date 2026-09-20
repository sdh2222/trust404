#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: ./run.sh <dir> [extra args]" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")" && pwd)"
if [[ ! -d "$1" ]]; then
  echo "run.sh: not a directory: $1" >&2
  exit 2
fi
DIR="$(cd "$1" && pwd)"
shift

export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

_no_backend() {
  echo "run.sh: no usable detector runtime found." >&2
  echo "  (1) docker load < trust404-detector-amd64.tar.gz   # release asset" >&2
  echo "      or docker pull ghcr.io/sdh2222/trust404-detector:latest" >&2
  echo "  (2) docker build --platform linux/amd64 -f detector/Dockerfile -t trust404/detector:latest ." >&2
  echo "  (3) scripts/setup_local.sh" >&2
  echo "  (4) (cd noexit && npm ci --ignore-scripts && npx tsc -p tsconfig.json)   # noexit engine" >&2
  exit 2
}

_image_present() {
  docker image inspect "$1" >/dev/null 2>&1
}

ENSEMBLE_IMAGE="${ENSEMBLE_IMAGE:-trust404/ensemble:latest}"
ENSEMBLE_FALLBACK_IMAGE="ghcr.io/sdh2222/trust404-ensemble:latest"
IMAGE="${DETECTOR_IMAGE:-trust404/detector:latest}"
FALLBACK_IMAGE="ghcr.io/sdh2222/trust404-detector:latest"

if [[ -z "${DETECTOR_NO_DOCKER:-}" ]] && command -v docker >/dev/null 2>&1; then
  ENS_IMG=""
  if _image_present "$ENSEMBLE_IMAGE"; then
    ENS_IMG="$ENSEMBLE_IMAGE"
  elif _image_present "$ENSEMBLE_FALLBACK_IMAGE"; then
    ENS_IMG="$ENSEMBLE_FALLBACK_IMAGE"
  fi
  if [[ -n "$ENS_IMG" ]]; then
    echo "run.sh: backend=docker image=${ENS_IMG} engines=ensemble" >&2
    exec docker run --rm --network none -e ENSEMBLE_MODE=judge ${ENSEMBLE_ENGINES:+-e ENSEMBLE_ENGINES} -v "${DIR}":/input:ro "$ENS_IMG" "$@"
  fi
  if ! _image_present "$IMAGE"; then
    if _image_present "$FALLBACK_IMAGE"; then
      IMAGE="$FALLBACK_IMAGE"
    else
      IMAGE=""
    fi
  fi
  if [[ -n "$IMAGE" ]]; then
    echo "run.sh: backend=docker image=${IMAGE}" >&2
    exec docker run --rm --network none -e DETECTOR_MODE=submission -v "${DIR}":/input:ro "$IMAGE" "$@"
  fi
fi

if [[ -n "${DETECTOR_PYTHON:-}" ]]; then
  PY="${DETECTOR_PYTHON}"
elif [[ -x "${ROOT}/.venv/bin/python" ]]; then
  PY="${ROOT}/.venv/bin/python"
else
  PY="python3"
fi

HAVE_DET=0
if "$PY" -c 'import slither' 2>/dev/null; then
  HAVE_DET=1
fi

NODE="${ENSEMBLE_NODE:-node}"
HAVE_NX=0
if command -v "$NODE" >/dev/null 2>&1 && [[ -f "${ROOT}/noexit/dist/cli.js" ]]; then
  HAVE_NX=1
fi

WANT_DET=1
WANT_NX=1
if [[ -n "${ENSEMBLE_ENGINES:-}" ]]; then
  WANT_DET=0
  WANT_NX=0
  IFS=',' read -ra _wanted <<< "${ENSEMBLE_ENGINES}"
  for _raw in "${_wanted[@]}"; do
    _e="$(printf '%s' "$_raw" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')"
    if [[ "$_e" == "detector" ]]; then
      WANT_DET=1
    fi
    if [[ "$_e" == "noexit" ]]; then
      WANT_NX=1
    fi
  done
  if [[ "$WANT_DET" -eq 0 && "$WANT_NX" -eq 0 ]]; then
    WANT_DET=1
    WANT_NX=1
  fi
fi

AVAIL_DET=0
AVAIL_NX=0
if [[ "$WANT_DET" -eq 1 && "$HAVE_DET" -eq 1 ]]; then
  AVAIL_DET=1
fi
if [[ "$WANT_NX" -eq 1 && "$HAVE_NX" -eq 1 ]]; then
  AVAIL_NX=1
fi

if [[ "$AVAIL_DET" -eq 0 && "$AVAIL_NX" -eq 0 ]]; then
  _no_backend
fi

if [[ "$AVAIL_DET" -eq 1 && "$AVAIL_NX" -eq 0 ]]; then
  echo "run.sh: DEGRADED: noexit unavailable; running detector only" >&2
  export ENSEMBLE_ENGINES=detector
elif [[ "$AVAIL_DET" -eq 0 && "$AVAIL_NX" -eq 1 ]]; then
  echo "run.sh: DEGRADED: detector unavailable; running noexit only" >&2
  export ENSEMBLE_ENGINES=noexit
fi

echo "run.sh: backend=python-ensemble interpreter=${PY} engines=${ENSEMBLE_ENGINES:-detector,noexit}" >&2

RUN_PY="$PY"
if ! "$PY" -c 'import sys' >/dev/null 2>&1; then
  if [[ -x "${ROOT}/.venv/bin/python" ]]; then
    RUN_PY="${ROOT}/.venv/bin/python"
  else
    RUN_PY="python3"
  fi
  export ENSEMBLE_PYTHON="${ENSEMBLE_PYTHON:-$PY}"
fi

exec "$RUN_PY" "${ROOT}/tools/ensemble.py" "${DIR}" "$@"
