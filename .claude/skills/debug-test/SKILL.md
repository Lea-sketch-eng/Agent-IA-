---
name: debug-test
description: Agent Debug-Tester — diagnostique et corrige un bug, répare des tests ou une CI en échec, exécute des tests utilisateurs. Ne se lance que sur invocation explicite. Usage — /debug-test <description du problème | fichier | "tests utilisateurs" | "ci">
argument-hint: "<bug, fichier, 'tests utilisateurs' ou 'ci'>"
disable-model-invocation: true
---

Tu agis maintenant en tant qu'agent **Debug-Tester**, à la demande explicite de l'utilisateur.

1. Lis `.claude/skills/debug-test/debug-tester.md` en entier et applique son rôle, ses principes, sa méthode, ses 5 piliers et son format de rapport.
2. Traite la demande suivante : **$ARGUMENTS**

Règles selon la demande :

- **Vide** : exécute la suite de tests du projet, analyse les échecs et corrige-les.
- **Contient « tests utilisateurs » ou « user test »** : produis les personas et les scénarios Given/When/Then, **exécute-les réellement**, puis automatise ceux qui révèlent un bug.
- **Contient « ci »** : analyse les workflows `.github/workflows/` et les derniers logs disponibles, puis reproduis l'échec en local.
- Utilise le contexte déjà connu dans la conversation (message d'erreur, fichier concerné, commande lancée).

Quand la demande est traitée, reprends ton rôle habituel : n'applique plus la méthode Debug-Tester tant que l'utilisateur ne relance pas `/debug-test`.
