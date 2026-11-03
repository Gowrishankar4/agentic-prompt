#!/usr/bin/env bash
# Install the prompt skill into an agent's skills folder.
#   ./install.sh --agent claude|cursor     known folders
#   ./install.sh --dir <path>              any skills folder
#   add --link to symlink instead of copy
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/plugins/prompt/skills/prompt"
DEST=""; MODE=copy
while [ $# -gt 0 ]; do
  case "$1" in
    --agent) case "$2" in claude) DEST="$HOME/.claude/skills" ;; cursor) DEST="$HOME/.cursor/skills" ;; *) echo "Unknown agent '$2' — use --dir"; exit 1 ;; esac; shift 2 ;;
    --dir) DEST="$2"; shift 2 ;;
    --link) MODE=link; shift ;;
    *) echo "usage: $0 (--agent claude|cursor | --dir PATH) [--link]"; exit 1 ;;
  esac
done
[ -n "$DEST" ] || { echo "usage: $0 (--agent claude|cursor | --dir PATH) [--link]"; exit 1; }
mkdir -p "$DEST"; rm -rf "${DEST:?}/prompt"
if [ "$MODE" = link ]; then ln -s "$SRC" "$DEST/prompt"; else cp -r "$SRC" "$DEST/prompt"; fi
echo "✔ prompt → $DEST/prompt ($MODE)"
