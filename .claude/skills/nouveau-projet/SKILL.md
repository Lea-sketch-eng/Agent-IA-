---
name: nouveau-projet
description: Démarre un nouveau projet de code de bout en bout — dépôt GitHub, code de départ (site + API + base de données), CI, première PR, projet Railway (API, PostgreSQL, Redis) et projet Vercel (site) reliés au dépôt. Usage — /nouveau-projet <description de ce qu'il faut construire>
argument-hint: "<ce que vous voulez construire>"
disable-model-invocation: true
---

Démarre le projet suivant de bout en bout : **$ARGUMENTS**

Réponds en français, en bullet points. Annonce chaque grande étape en une ligne avant de la faire.

## 0. Cadrage (une seule question au maximum)

- Déduis de la demande : nom du projet (kebab-case), description courte, besoin d'un site, d'une API, d'une base de données.
- Pile par défaut, à garder sauf demande contraire :
  - **Site** : Next.js (TypeScript) dans `web/`, hébergé sur **Vercel**.
  - **API** : FastAPI (Python 3.11) dans `api/`, hébergée sur **Railway**, avec une route `GET /health`.
  - **Données** : PostgreSQL + Redis sur Railway, migrations SQL dans `db/migrations/`.
- Ne pose une question (outil AskUserQuestion) que si un choix change vraiment le résultat et ne peut pas être déduit. Sinon, choisis et dis ce que tu as choisi.

## 1. Dépôt GitHub

- Crée le dépôt avec l'outil GitHub `create_repository` : privé, `autoInit: true` (pour que `main` existe et serve de base aux PR).
- Ajoute-le à la session avec `add_repo` (accès `push`), puis clone-le et enregistre-le avec `register_repo_root`.
- Si l'accès est refusé (app GitHub Claude limitée à certains dépôts), donne à l'utilisateur la raison exacte renvoyée par l'outil et le lien d'installation de l'app, puis attends.
- Travaille sur une branche `claude/initialisation`, jamais directement sur `main`.

## 2. Code de départ

- Génère le squelette minimal qui fonctionne (pas de fonctionnalités non demandées) :
  - `api/` : FastAPI avec `/health` qui vérifie PostgreSQL et Redis, lecture de `DATABASE_URL` et `REDIS_URL` depuis l'environnement, tests pytest.
  - `web/` : Next.js qui affiche l'état de l'API via `NEXT_PUBLIC_API_URL`.
  - `db/migrations/0001_init.sql` : schéma initial correspondant au besoin.
- Recopie depuis le dépôt modèle `Lea-sketch-eng/Agent-IA-` (lis-le avec les outils GitHub, adapte les chemins) :
  - `.claude/skills/debug-test/` (agent Debug-Tester, à la demande uniquement), `.claude/skills/nouveau-projet/`, `.github/workflows/debug-tester-on-demand.yml` (pour que cette commande existe aussi dans le nouveau dépôt) ;
  - `.github/workflows/pr-quality-deploy.yml` — adapte la détection de stack aux sous-dossiers `api/` et `web/` (`working-directory`) ;
  - `scripts/migrate.py`, `scripts/check_claude_config.py`, `tests/test_migrate.py`, `pyproject.toml`.
- `railway.json` dans `api/` : démarrage de l'API avec les migrations en `preDeployCommand`, pour qu'elles s'appliquent à chaque déploiement de `main`.
- Aucun secret dans le dépôt : ni mot de passe, ni clé, ni URL de base de données.

## 3. Vérifier, pousser, ouvrir la PR

- Lance localement lint, tests (API + site), `actionlint`, build du site. Corrige jusqu'à ce que tout passe.
- Commit, push sur `claude/initialisation`, ouvre la PR vers `main` (suis le modèle de PR du dépôt s'il existe).
- Abonne la session à la PR (`subscribe_pr_activity`) et mène-la au vert.

## 4. Railway (API + PostgreSQL + Redis)

- Crée le projet Railway du même nom, puis déploie les modèles `postgres` et `redis`.
- Crée le service API depuis le dépôt (`create-deployment`, branche `main`, dossier racine `api/`). **C'est un déploiement en production : demande l'accord explicite de l'utilisateur juste avant.**
- Variables du service API, uniquement par référence (jamais de valeur recopiée) :
  - `DATABASE_URL=${{Postgres.DATABASE_URL}}`
  - `REDIS_URL=${{Redis.REDIS_URL}}`
- Génère un domaine public pour l'API seulement. PostgreSQL et Redis restent privés : ne crée jamais de proxy TCP sans accord explicite.
- Offre Hobby : 5 services maximum par projet. Si la pile dépasse, préviens avant de déployer.

## 5. Vercel (site)

- Crée le projet Vercel relié au dépôt, dossier racine `web/`.
- Variable `NEXT_PUBLIC_API_URL` = domaine public de l'API Railway (production et preview).
- Vercel publie automatiquement une preview à chaque PR ; le workflow fait alors son smoke test sur `deployment_status`.

## 6. Compte rendu final

- Liens : dépôt, PR, site Vercel, API Railway.
- Ce qui est vérifié (avec les résultats) et ce qui ne l'est pas.
- Ce qui reste à faire par l'utilisateur (merger la PR, secret `ANTHROPIC_API_KEY` pour la revue Claude, permissions refusées éventuelles).

## Règles

- Ne demande jamais de mot de passe, de clé d'API ou d'URL de base de données à l'utilisateur, et n'en écris jamais dans un fichier, un commit ou une conversation. Si l'utilisateur en colle un, ne le réutilise pas et conseille de le régénérer.
- Toute action qui déploie en production, expose une base sur internet ou supprime une ressource demande un accord explicite juste avant.
- Si une permission est refusée, ne la contourne pas : explique ce qui bloque et propose la marche à suivre.
