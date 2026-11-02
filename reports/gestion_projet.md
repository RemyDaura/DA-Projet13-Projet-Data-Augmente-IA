# Gestion de projet - Projet 13, Mission 1
## Amélioration IA du contrôle qualité des données Bottleneck

---

## 1. Découpage en lots

| Lot | Objectif |
|---|---|
| Lot 1 - Cadrage | Identifier le besoin, mener la veille, formaliser le cahier des charges |
| Lot 2 - POC | Tester empiriquement les 3 méthodes de validation |
| Lot 3 - Intégration | Intégrer la solution retenue dans le notebook P6 |
| Lot 4 - Documentation | Consolider la démarche, tracer les décisions |
| Lot 5 - Restitution | Portfolio et préparation de la soutenance |

---

## 2. Backlog de tâches

| ID | Tâche | Type | Complexité | Dépendances | Définition de "Terminé" | Statut |
|---|---|---|---|---|---|---|
| T1.1 | Identifier le besoin de veille à partir du notebook P6 existant | US | S | - | 2 pistes d'amélioration identifiées et documentées | Terminé |
| T1.2 | Mener la veille comparative (Pandera vs Great Expectations) | Technique | M | T1.1 | Tableau comparatif sourcé, critères qualité/sobriété/reproductibilité | Terminé |
| T1.3 | Rédiger le cahier des charges fonctionnel | US | M | T1.1 | Document complet : parties prenantes, périmètre, contraintes, KPI | Terminé |
| T2.1 | Développer un schéma Pandera sur les données brutes | Technique | M | T1.2 | Script exécutable détectant les anomalies déjà connues | Terminé |
| T2.2 | Tester Great Expectations sur les mêmes règles | Technique | M | T2.1 | Comparaison chiffrée (lignes de code, résultats) disponible | Terminé |
| T2.3 | Tester la méthode IA générative directe (sans règle prédéfinie) | Exploration | S | T2.1, T2.2 | Prompt et résultat brut documentés, comparés aux 2 autres méthodes | Terminé |
| T2.4 | Corriger les schémas suite aux découvertes de T2.3 | Technique | S | T2.3 | Règles corrigées, re-testées, résultats recoupant les chiffres historiques |  Terminé |
| T3.1 | Intégrer la section "Amélioration IA" dans le notebook P6 | Technique | M | T2.4 | Notebook exécuté de bout en bout sans erreur |  Terminé |
| T3.2 | Corriger les bugs de reproductibilité découverts en intégrant | Technique | S | T3.1 | Ré-exécution complète du notebook sans erreur | Terminé |
| T4.1 | Rédiger la documentation consolidée (veille, tests, décisions) | US | M | T3.2 | Document unique livré, reliant tous les livrables | Terminé |
| T4.2 | Formaliser la gestion de projet (ce document) | US | S | - | Backlog + registre des risques livrés | Terminé |
| T4.3 | Capturer la preuve d'automatisation de la veille (abonnement GitHub) | Technique | S | - | Capture d'écran jointe en annexe | Terminé |
| T5.1 | Construire le portfolio (site + dossiers détaillés) | US | L | T4.1 | Site déployé sur GitHub Pages | Terminé |
| T5.2 | Compléter les dossiers P8 et P10 avec du contenu réel | US | S | T5.1 | Pages sans encadré "à compléter" | Terminé |
| T5.3 | Ajouter CV et coordonnées de contact au portfolio | Technique | S | T5.1 | Liens fonctionnels vérifiés | En cours |
| T5.4 | Préparer la soutenance orale (script minuté, questions anticipées) | US | M | T4.1, T5.1 | Script complet couvrant présentation + discussion | À faire |
| T5.5 | Donner une page dédiée aux 8 projets complémentaires du portfolio | US | M | T5.1 | 8 pages détaillées au même format que les dossiers phares | À faire (optionnel) |

**Légende complexité** : S = quelques heures, M = une session de travail, L = plusieurs sessions.

---

## 3. Registre des risques

| ID | Risque | Catégorie | Probabilité | Impact | Mitigation |
|---|---|---|---|---|---|
| R1 | Fuite de données / non-conformité RGPD | Conformité | Faible | Élevé | Données Bottleneck = catalogue produit, aucune donnée personnelle identifiée ; vérifié et documenté dans le CDC |
| R2 | Biais dans la détection d'anomalies (règles codées à la main incomplètes) | Qualité | Moyenne - **déjà matérialisé** (2 angles morts trouvés) | Moyen | Croiser plusieurs méthodes de détection (fait : Pandera + Great Expectations + IA) ; documenter les limites plutôt que les masquer |
| R3 | Dérive / non-reproductibilité du notebook dans le temps | Technique | Moyenne - **déjà matérialisée** (2 bugs trouvés) | Moyen | Ré-exécution complète systématique avant toute livraison ; tests explicites |
| R4 | Dépendance à un outil IA tiers pour la méthode d'exploration | Fournisseur | Faible à ce stade | Faible | Usage ponctuel et non critique ; ne pas utiliser en contrôle de production continu ; vérifier la politique de confidentialité de l'outil avant tout usage sur données sensibles |
| R5 | Volume de données insuffisant pour généraliser les conclusions | Métier | Faible | Faible | 825 références jugées représentatives du catalogue actuel ; à réévaluer si le catalogue grandit significativement |
| R6 | Délai serré (projet de fin de formation) | Planning | Moyenne | Moyen | Priorisation stricte (Mission 1 avant Mission 2), backlog explicite avec statuts |

---

## 4. Points de contrôle

| Point de contrôle | Objet | Statut |
|---|---|---|
| Revue après Lot 1 | Validation par le mentor de l'axe de veille choisi (fiabilisation des jointures/nettoyage) | ✅ Fait |
| Revue après Lot 2 | Validation des résultats du POC ; demande explicite de tester Great Expectations empiriquement et une 3e méthode | ✅ Fait |
| Revue finale avant soutenance | Relecture de l'ensemble des livrables avec le mentor | ⏳ À planifier |
