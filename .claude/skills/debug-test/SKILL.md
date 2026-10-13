---
name: debug-test
description: Lance l'agent Debug-Tester pour diagnostiquer et corriger un bug, réparer des tests ou une CI en échec, ou exécuter des tests utilisateurs. Usage — /debug-test <description du problème | fichier | "tests utilisateurs" | "ci">
argument-hint: "<bug, fichier, 'tests utilisateurs' ou 'ci'>"
---

Délègue la demande suivante au subagent `debug-tester` (outil Agent, `subagent_type: "debug-tester"`) :

**Demande :** $ARGUMENTS

Règles de délégation :

- Si la demande est vide, demande à l'agent d'exécuter la suite de tests du projet, d'analyser les échecs et de les corriger.
- Si elle contient « tests utilisateurs » ou « user test », demande-lui de produire les personas, les scénarios Given/When/Then, de les **exécuter réellement** puis d'automatiser ceux qui révèlent un bug.
- Si elle contient « ci », demande-lui d'analyser les workflows `.github/workflows/` et les derniers logs disponibles, puis de reproduire l'échec en local.
- Transmets toujours le contexte utile déjà connu dans la conversation (message d'erreur, fichier concerné, commande lancée).

Une fois l'agent terminé, restitue son rapport à l'utilisateur en bullet points, sans le résumer au point de perdre la cause racine, les commandes de vérification ou les risques restants.
