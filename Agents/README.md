# Agents

Bibliothèque d'agents Claude Code réutilisables. Chaque agent est rangé dans son propre dossier et **s'installe dans le projet où vous voulez l'invoquer**.

> Claude Code ne lit les agents que dans `.claude/` (du projet) ou `~/.claude/` (de votre ordinateur). Ce dossier est la **source** ; `install.sh` copie l'agent au bon endroit.

## Agents disponibles

| Agent | Rôle | Commande après installation |
|---|---|---|
| [`architect-orchestrator`](architect-orchestrator/) | Architecte / Maître d'Orchestre : analyse, découpage, activation sélective des sous-agents, boucle `APPROUVÉ` / `REJETÉ` (3 itérations max) | `/orchestrer <tâche>` ou `claude --agent architect-orchestrator "<tâche>"` |

Structure d'un agent :

```
Agents/<agent>/
├── agents/   # l'agent principal et ses sous-agents (.md)
└── skills/   # ses commandes /… (optionnel)
```

## Installer un agent

```bash
git clone https://github.com/Lea-sketch-eng/Agent-IA-.git
cd Agent-IA-

# Dans un projet précis (à commiter dans ce projet → disponible aussi sur claude.ai/code)
Agents/install.sh architect-orchestrator ~/code/mon-projet

# Pour tous vos projets sur cet ordinateur (terminal / app desktop)
Agents/install.sh architect-orchestrator --global

# Lister les agents disponibles
Agents/install.sh --list
```

- **Installation dans un projet** : les fichiers sont copiés dans `<projet>/.claude/agents/` et `<projet>/.claude/skills/`. Commitez-les dans le projet pour que l'agent soit aussi disponible dans les sessions web (claude.ai/code), qui ne voient pas votre `~/.claude/`.
- **Mise à jour** : modifiez l'agent ici, dans `Agents/`, puis relancez `install.sh` sur vos projets.

## Invoquer l'agent

- `/orchestrer Implémente l'authentification OAuth2`
- `claude --agent architect-orchestrator "Implémente l'authentification OAuth2"` (terminal)
- **Activation uniquement sur demande** : l'agent ne démarre jamais tout seul. Ne mettez pas `"agent": "architect-orchestrator"` dans `.claude/settings.json` : ce réglage le lancerait automatiquement à chaque session.

## Garanties « uniquement sur demande »

| Risque de démarrage automatique | Protection |
|---|---|
| Claude lance `/orchestrer` de lui-même | `disable-model-invocation: true` dans la commande : seul vous pouvez la taper |
| Claude délègue à l'orchestrateur comme sous-agent | Sa description l'interdit, et s'il est lancé ainsi il ne fait rien et rend la main |
| Claude utilise un sous-agent (`code-generator`…) hors orchestration | Leur description l'interdit, et sans brief de l'orchestrateur ils refusent et rendent la main |
| L'orchestrateur devient l'agent par défaut | Aucun réglage `"agent"` n'est installé par `install.sh` |

## Ajouter un nouvel agent

1. Créer `Agents/<nom>/agents/<nom>.md` (frontmatter `name`, `description`, `tools`, `model`…) et, si besoin, `Agents/<nom>/skills/<commande>/SKILL.md`.
2. L'ajouter au tableau ci-dessus.
3. `python scripts/check_claude_config.py` vérifie le format (aussi lancé par la CI à chaque PR).
