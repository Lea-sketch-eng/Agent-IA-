# Agent IA « Debug-Tester »

Agent Claude Code spécialisé dans le **debug**, la **correction de code** et les **tests** (unitaires, données, modèle, **tests utilisateurs**), conçu à partir du cadre de test IA / MLOps en 5 piliers : Code → Données → Modèle → Feedback utilisateur → Monitoring.

## Contenu

| Fichier | Rôle |
|---|---|
| `.claude/agents/debug-tester.md` | Définition du subagent (rôle, méthode de debug, 5 piliers, tests utilisateurs, format de rapport) |
| `.claude/skills/debug-test/SKILL.md` | Commande `/debug-test` pour invoquer l'agent à la demande |
| `templates/tests/user/PLAN_TESTS_UTILISATEURS.md` | Modèle de plan de tests utilisateurs (personas, Given/When/Then, session exploratoire) |
| `templates/scripts/validate_data.py` | Data Testing : schéma, types, plages, valeurs manquantes, dérive (KS) |
| `templates/github-actions-ml-tests.yml` | Workflow CI MLOps (pytest + validation données + évaluation + rapport CML) |

## Installation dans un autre projet

```bash
# Depuis la racine de votre projet
cp -r /chemin/vers/Agent-IA-/.claude/agents  .claude/
cp -r /chemin/vers/Agent-IA-/.claude/skills  .claude/
# Ou, pour tous vos projets :
cp .claude/agents/debug-tester.md ~/.claude/agents/
cp -r .claude/skills/debug-test ~/.claude/skills/
```

## Utilisation

- **Commande** :
  - `/debug-test` → lance la suite de tests, analyse et corrige les échecs
  - `/debug-test TypeError dans src/api/users.py ligne 42`
  - `/debug-test tests utilisateurs sur le formulaire d'inscription`
  - `/debug-test ci` → analyse et répare le workflow GitHub Actions
- **Mention directe** : `@debug-tester corrige le test test_predict qui échoue`
- **Automatique** : Claude délègue de lui-même à l'agent quand un bug ou un test en échec apparaît.

## Ce que fait l'agent

- Reproduit le bug (écrit un test de régression qui échoue s'il n'en existe pas)
- Isole la cause racine (hypothèses, logs, `git bisect`…)
- Applique un correctif minimal, sans jamais désactiver ni affaiblir un test
- Vérifie (tests, lint, typage) et montre le résultat avant / après
- Exécute des tests utilisateurs réels (CLI, API, web via Playwright, modèle IA / LLM) avec personas et cas limites
- Contrôle les aspects IA : qualité et dérive des données, métriques ≥ 80 %, fuite de données, biais (impact disparate)
- Rend un rapport structuré : diagnostic, correctif, vérification, tests utilisateurs, risques

## Corrections apportées au workflow fourni

- `cml-publish` / `cml-send-comment` (dépréciés) remplacés par `cml comment create` + `iterative/setup-cml@v2`
- Ajout des `permissions` nécessaires pour commenter la PR
- Rapport CML publié uniquement sur les pull requests
- Validation des données avec un jeu de référence pour détecter la dérive
- ⚠️ `scripts/train_and_evaluate.py` reste à écrire dans votre projet (il doit produire `results/metrics.txt` et les images)
