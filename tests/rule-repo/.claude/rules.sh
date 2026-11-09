#!/bin/sh
FILE="$1"
[ -f "$FILE" ] || exit 0
FAIL=0
hit() {
  echo "$1"
  FAIL=1
}
if grep -nE 'console\.log|debugger' "$FILE"; then
  hit "Không để console.log/debugger"
fi
if grep -nE 'sk_live_|BEGIN PRIVATE KEY|AKIA[0-9A-Z]{16}' "$FILE"; then
  hit "Không để secret trong source"
fi
if grep -nE 'dangerouslySetInnerHTML' "$FILE"; then
  hit "Không gắn HTML thô vào DOM"
fi
if grep -nE 'catch[[:space:]]*(\([^)]*\))?[[:space:]]*\{[[:space:]]*\}' "$FILE"; then
  hit "Không nuốt lỗi bằng catch rỗng"
fi
if grep -nE 'key=\{index\}' "$FILE"; then
  hit "Không dùng index làm key"
fi
exit $FAIL
