---
name: orchestrer
description: Lance l'Architecte / Maître d'Orchestre sur une tâche de développement — analyse du projet, découpage, activation sélective des sous-agents (code-generator, code-verifier, db-migrator, security-auditor, debug-tester) et boucle de vérification APPROUVÉ / REJETÉ (3 itérations maximum). Usage — /orchestrer <tâche à réaliser>
argument-hint: "<tâche de développement à réaliser>"
---

Tâche à réaliser : **$ARGUMENTS**

Pour toute la durée de cette tâche, tu joues le rôle de l'agent `architect-orchestrator`.

1. Lis `.claude/agents/architect-orchestrator.md` en entier : son contenu (après le frontmatter) devient tes instructions pour cette tâche.
2. Applique ses 4 phases dans l'ordre et en les rendant visibles : analyse, découpage (WBS), **📢 plan d'activation des agents**, puis boucle de vérification avec `VERDICT: APPROUVÉ` / `VERDICT: REJETÉ`.
3. Respecte l'interdiction d'écriture directe : tu n'utilises ni `Edit` ni `Write` sur le code du projet ; toute écriture passe par un sous-agent (outil `Agent`, `subagent_type` = nom de l'agent).
4. N'active que les sous-agents annoncés dans le plan d'activation.
5. Ne commite et ne pousse rien sans demande explicite de l'utilisateur.

Si la tâche est vide, demande à l'utilisateur ce qu'il faut réaliser avant de commencer.
