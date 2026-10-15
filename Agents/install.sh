#!/usr/bin/env bash
# Installe un agent du dossier Agents/ dans un projet ou pour tous vos projets.
#
# Usage :
#   Agents/install.sh <agent> <chemin-du-projet>   # installe dans <projet>/.claude/
#   Agents/install.sh <agent> --global             # installe dans ~/.claude/ (tous vos projets)
#   Agents/install.sh --list                       # liste les agents disponibles
#
# Exemple : Agents/install.sh architect-orchestrator ~/code/mon-projet
set -euo pipefail

AGENTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

list_agents() {
  for dir in "$AGENTS_DIR"/*/; do
    [ -d "$dir/agents" ] && basename "$dir"
  done
}

usage() {
  sed -n '2,9p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  echo
  echo "Agents disponibles :"
  list_agents | sed 's/^/  - /'
  exit "${1:-1}"
}

[ "${1:-}" = "--list" ] && { list_agents; exit 0; }
[ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ] && usage 0
[ $# -eq 2 ] || usage

package="$AGENTS_DIR/$1"
[ -d "$package/agents" ] || { echo "❌ Agent inconnu : $1" >&2; usage; }

if [ "$2" = "--global" ]; then
  target="$HOME/.claude"
else
  [ -d "$2" ] || { echo "❌ Dossier de projet introuvable : $2" >&2; exit 1; }
  target="$(cd "$2" && pwd)/.claude"
fi

mkdir -p "$target/agents"
for file in "$package"/agents/*.md; do
  cp "$file" "$target/agents/"
  echo "✅ agent  $(basename "$file" .md) → $target/agents/"
done

if [ -d "$package/skills" ]; then
  mkdir -p "$target/skills"
  for skill in "$package"/skills/*/; do
    name="$(basename "$skill")"
    rm -rf "${target:?}/skills/$name"
    cp -R "$skill" "$target/skills/$name"
    echo "✅ skill  /$name → $target/skills/"
  done
fi

echo "Terminé. Redémarrez Claude Code dans le projet pour charger l'agent."
