# Agent IA « Debug-Tester »

Agent Claude Code spécialisé dans le **debug**, la **correction de code** et les **tests** (unitaires, données, modèle, **tests utilisateurs**), conçu à partir du cadre de test IA / MLOps en 5 piliers : Code → Données → Modèle → Feedback utilisateur → Monitoring.

## Contenu

| Fichier | Rôle |
|---|---|
| `.claude/agents/debug-tester.md` | Définition du subagent (rôle, méthode de debug, 5 piliers, tests utilisateurs, format de rapport) |
| `.claude/skills/debug-test/SKILL.md` | Commande `/debug-test` pour invoquer l'agent à la demande |
| `.claude/skills/nouveau-projet/SKILL.md` | Commande `/nouveau-projet` : dépôt GitHub, code de départ, PR, Railway et Vercel en une fois |
| `templates/tests/user/PLAN_TESTS_UTILISATEURS.md` | Modèle de plan de tests utilisateurs (personas, Given/When/Then, session exploratoire) |
| `templates/scripts/validate_data.py` | Data Testing : schéma, types, plages, valeurs manquantes, dérive (KS) |
| `templates/github-actions-ml-tests.yml` | Workflow CI MLOps (pytest + validation données + évaluation + rapport CML) |
| `.github/workflows/pr-quality-deploy.yml` | Revue automatique de chaque PR (qualité, déploiement, revue Claude) |
| `scripts/check_claude_config.py` | Vérifie que les agents et skills sont valides avant déploiement |

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

## Revue automatique de chaque PR

Le workflow `.github/workflows/pr-quality-deploy.yml` se lance **automatiquement** à chaque PR ouverte ou mise à jour :

| Job | Vérifications |
|---|---|
| Qualité du code | actionlint (workflows), ruff + pytest avec couverture (Python), lint/test/build (Node.js) — détection automatique de la stack |
| Vérification du déploiement | Validation des agents/skills Claude, build Docker + smoke test HTTP si un `Dockerfile` existe |
| Smoke test de l'environnement déployé | À chaque `deployment_status` réussi (Vercel, Netlify, Render…), vérifie que l'URL déployée répond |
| Revue Claude (Debug-Tester) | Revue de la PR (qualité, sécurité, tests, déploiement, IA/ML), commentaires inline et verdict ✅ / ⚠️ / ❌ |

### Mise en place (une seule fois)

1. Installer l'app GitHub Claude sur le dépôt : <https://github.com/apps/claude>
2. Ajouter le secret `ANTHROPIC_API_KEY` (ou `CLAUDE_CODE_OAUTH_TOKEN`, obtenu avec `claude setup-token`) dans **Settings → Secrets and variables → Actions**. Sans ce secret, les autres jobs tournent et la revue Claude est simplement ignorée.
3. (Optionnel) Variables `APP_PORT` et `HEALTH_PATH` pour le smoke test Docker (par défaut `8080` et `/`).
4. (Recommandé) **Settings → Branches → règle de protection sur `main`** : rendre obligatoires « Qualité du code » et « Vérification du déploiement » pour empêcher le merge d'une PR en échec.

## Corrections apportées au workflow fourni

- `cml-publish` / `cml-send-comment` (dépréciés) remplacés par `cml comment create` + `iterative/setup-cml@v2`
- Ajout des `permissions` nécessaires pour commenter la PR
- Rapport CML publié uniquement sur les pull requests
- Validation des données avec un jeu de référence pour détecter la dérive
- ⚠️ `scripts/train_and_evaluate.py` reste à écrire dans votre projet (il doit produire `results/metrics.txt` et les images)

## Base de données (Railway : PostgreSQL + Redis)

| Étape | Ce qui se passe, automatiquement |
|---|---|
| PR ouverte ou mise à jour | GitHub Actions crée une base PostgreSQL et un Redis **jetables**, applique les migrations deux fois (idempotence) et lance `tests/test_migrate.py`. La production n'est pas touchée. |
| PR mergée sur `main` | Railway redéploie le service de migrations, qui applique `scripts/migrate.py` sur la base de production via le réseau privé. |

- **Ajouter une modification de schéma** : créer `db/migrations/0002_ma_modif.sql` (numérotation croissante). Un fichier déjà appliqué ne doit jamais être modifié : créer une nouvelle migration à la place.
- **Sécurité** : aucun mot de passe de base n'est stocké dans GitHub ; PostgreSQL et Redis ne sont pas exposés sur internet.
- **En local** : `DATABASE_URL=postgresql://... python scripts/migrate.py`
