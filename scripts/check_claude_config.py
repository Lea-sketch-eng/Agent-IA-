"""Vérifie que les agents et skills Claude du dépôt sont déployables.

Contrôles : frontmatter YAML présent et valide, champs `name` et `description`
renseignés, nom identique au dossier pour les skills, outils connus pour les agents.
Aucun agent ni aucune skill ne doit pouvoir se déclencher sans invocation explicite :
les skills doivent porter `disable-model-invocation: true` et la description d'un
agent ne doit pas inviter Claude à l'utiliser de lui-même.
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
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
AUTO_TRIGGER = re.compile(r"proactiv|automatique|automatically|without being asked", re.IGNORECASE)


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
    if AUTO_TRIGGER.search(data["description"]):
        raise ValueError("la description invite à un déclenchement automatique")
    tools = data.get("tools")
    if tools:
        names = tools if isinstance(tools, list) else [t.strip() for t in tools.split(",")]
        unknown = [t for t in names if t not in KNOWN_TOOLS and not t.startswith("mcp__")]
        if unknown:
            raise ValueError(f"outils inconnus : {unknown}")


def check_skill(path):
    data = load_frontmatter(path)
    if data["name"] != path.parent.name:
        raise ValueError(f"`name` ({data['name']}) différent du dossier ({path.parent.name})")
    if data.get("disable-model-invocation") is not True:
        raise ValueError("`disable-model-invocation: true` manquant (lancement auto possible)")


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
