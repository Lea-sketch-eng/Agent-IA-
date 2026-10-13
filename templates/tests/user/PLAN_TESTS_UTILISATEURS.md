# Plan de tests utilisateurs

> Modèle utilisé par l'agent `debug-tester`. Copier dans le projet et compléter.

## 1. Contexte
- Application / fonctionnalité testée :
- Version / commit :
- Type d'interface : CLI · API · Web · Modèle IA / LLM
- Seuil d'acceptation (ex. ≥ 80 % de scénarios réussis, 0 bug bloquant) :

## 2. Personas
| Persona | Profil | Objectif | Risque principal testé |
|---|---|---|---|
| Novice | Première utilisation | Réussir le parcours nominal | Clarté des messages d'erreur |
| Expert pressé | Usage intensif | Aller vite, raccourcis | Double soumission, performances |
| Malveillant | Cherche à casser | Contourner les règles | Injections, entrées invalides |
| Accessibilité | Clavier / lecteur d'écran | Utiliser sans souris | Labels, focus, contrastes |

## 3. Scénarios (Given / When / Then)
| ID | Persona | Given | When | Then | Priorité |
|---|---|---|---|---|---|
| US-01 | Novice | | | | Haute |
| US-02 | Malveillant | | saisit une valeur vide / très longue / Unicode | un message d'erreur clair s'affiche, aucune erreur 500 | Haute |
| US-03 | Expert | | soumet deux fois de suite | une seule action est enregistrée | Moyenne |

Cas limites à toujours envisager : vide, espaces, très long, emoji/Unicode, négatif, zéro, date invalide, fuseau horaire, fichier corrompu, réseau coupé, droits insuffisants.

Spécifique IA : entrée hors distribution, entrée adverse, prompt injection (LLM), stabilité des réponses entre deux exécutions, biais selon un attribut sensible.

## 4. Session exploratoire
- Durée : 15 min · Charte : « Explorer <zone> pour découvrir <type de risque> »
- Observations :
  -

## 5. Résultats
| ID | Résultat (✅/❌) | Observation | Bug lié | Test automatisé créé |
|---|---|---|---|---|

## 6. Synthèse
- Taux de réussite :
- Bugs bloquants :
- Recommandations :
