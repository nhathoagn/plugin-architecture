#!/bin/sh
dir=${0%/*}
[ "$dir" = "$0" ] && dir=.
dir=$(CDPATH= cd -- "$dir" && pwd) || exit 0
[ -f "$dir/fe-gate.py" ] || exit 0
export FE_ARCH_ROOT=$(CDPATH= cd -- "$dir/.." && pwd) || exit 0
# PATH can be minimal when the host app launches from Finder, so look in the usual places too.
for candidate in python3 /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3; do
  command -v "$candidate" >/dev/null 2>&1 && exec "$candidate" "$dir/fe-gate.py"
done
exit 0
