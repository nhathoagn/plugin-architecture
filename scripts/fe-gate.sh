#!/bin/sh
dir=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
export FE_ARCH_ROOT=$(CDPATH= cd -- "$dir/.." && pwd)
exec python3 "$dir/fe-gate.py"
