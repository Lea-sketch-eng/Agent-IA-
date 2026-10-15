"""Vérifie que les agents et skills Claude du dépôt sont déployables.

Contrôles : frontmatter YAML présent et valide, champs `name` et `description`
renseignés, nom identique au dossier pour les skills, outils, `model` et `effort`
valides pour les agents.
Sort en code 1 au premier problème détecté (bloque la CI).
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
KNOWN_TOOLS = {
    "Read", "Edit", "Write", "Bash", "Grep", "Glob", "WebFetch", "WebSearch",
    "NotebookEdit", "Agent", "Task", "TodoWrite",
}
MODEL_ALIASES = {"inherit", "opus", "sonnet", "haiku"}
EFFORT_LEVELS = {"low", "medium", "high", "xhigh", "max"}
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def load_frontmatter(path):
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError("frontmatter YAML absent (le fichier doit commencer par ---)")
    data = yaml.safe_load(match.group(1)) or {}
    for field in ("name", "description"):
        if not str(data.get(field, "")).strip():
            raise ValueError(f"champ `{field}` manquant ou vide")
    return data


def check_agent(path):
    data = load_frontmatter(path)
    tools = data.get("tools")
    if tools:
        names = tools if isinstance(tools, list) else [t.strip() for t in tools.split(",")]
        unknown = [t for t in names if t not in KNOWN_TOOLS and not t.startswith("mcp__")]
        if unknown:
            raise ValueError(f"outils inconnus : {unknown}")
    model = data.get("model")
    if model and model not in MODEL_ALIASES and not str(model).startswith("claude-"):
        raise ValueError(
            f"`model` invalide ({model}) : utiliser {sorted(MODEL_ALIASES)} ou un ID claude-…"
        )
    effort = data.get("effort")
    if effort and effort not in EFFORT_LEVELS:
        raise ValueError(f"`effort` invalide ({effort}) : utiliser {sorted(EFFORT_LEVELS)}")


def check_skill(path):
    data = load_frontmatter(path)
    if data["name"] != path.parent.name:
        raise ValueError(f"`name` ({data['name']}) différent du dossier ({path.parent.name})")


def main():
    checks = [(p, check_agent) for p in sorted(ROOT.glob(".claude/agents/*.md"))]
    checks += [(p, check_skill) for p in sorted(ROOT.glob(".claude/skills/*/SKILL.md"))]
    errors = []
    for path, check in checks:
        try:
            check(path)
            print(f"✅ {path.relative_to(ROOT)}")
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)} : {exc}")
    for err in errors:
        print(f"❌ {err}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
