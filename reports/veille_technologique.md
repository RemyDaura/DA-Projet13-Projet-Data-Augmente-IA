# Veille technologique et méthodologique
## Amélioration du contrôle qualité des données - Projet Bottleneck (P13, Mission 1)

**Auteur :** Rémy Daura · **Sujet :** validation automatisée des données catalogue (ERP / Web / liaison)

---

## 1. Besoin de veille

Le notebook P6 identifie manuellement 9 catégories d'anomalies dans les données Bottleneck (prix négatifs, stocks incohérents, doublons, orphelins, ventes à perte...), réparties dans une dizaine de cellules distinctes. Cette approche fonctionne, mais présente trois limites : rien ne garantit qu'elle sera rejouée à l'identique sur les prochains exports mensuels, rien n'alerte automatiquement en cas de nouvelle anomalie, et la logique de contrôle n'est pas centralisée dans une source unique.

**Besoin formulé :** identifier une ou plusieurs méthodes de validation de données qui centralisent ces règles de qualité, de façon reproductible et automatisable, adaptées à une petite structure sans équipe data engineering dédiée.

---

## 2. Solutions comparées

Trois approches ont été comparées, d'abord sur documentation puis par **test empirique réel sur les données Bottleneck** : deux librairies Python de validation de données (**Pandera**, **Great Expectations**), et une **méthode sans code**, consistant à transmettre les données brutes à une IA générative sans règle prédéfinie.

| Critère | Pandera | Great Expectations | IA générative directe |
|---|---|---|---|
| **Qualité / couverture** | Validation de schéma (types, contraintes), tests statistiques. Un schéma unique réutilisable sur plusieurs formats de dataframes [3]. | Couverture plus large : pipelines multi-moteurs (Spark/SQL/pandas), suites partagées, checkpoints [6]. | La plus large sur ce projet : a trouvé 2 catégories d'anomalies que ni Pandera ni Great Expectations ne testaient (voir section 4). |
| **Biais / rigueur** | Conçu pour les dataframes [2] - rigoureux sur son périmètre, plus limité en dehors. | Conçu pour des systèmes prêts pour la production [2] - gouvernance plus large. | Dépend entièrement de la qualité du prompt et du modèle ; aucune garantie de couverture exhaustive ni de stabilité d'une exécution à l'autre. |
| **Temps de mise en œuvre** | Simple à intégrer, syntaxe proche de Pydantic [7][8]. Mesuré sur ce projet : ~9 lignes pour 6 règles. | Plus lourd (Data Context, DataSource, Expectation Suite) [1]. Mesuré sur ce projet : ~15 lignes pour les mêmes règles (+65%). | Quasi nul : coller les fichiers + une consigne en une phrase. Aucune compétence Python requise. |
| **Reproductibilité** | Code Python versionnable, rejouable à l'identique en < 1 seconde. | Idem, plus lourd à versionner ; génère des "Data Docs" HTML automatiques - **confirmé fonctionnel par test réel** (rapport structuré généré avec succès). | Aucune reproductibilité automatique : chaque nouvelle donnée nécessite une nouvelle sollicitation, sans garantie de résultat identique. |
| **Sécurité / conformité** | Exécution 100% locale. | Idem en open source. | Selon l'outil IA utilisé, les données transitent potentiellement par un service tiers - point de vigilance RGPD à vérifier avant tout usage sur des données sensibles. |
| **Sobriété numérique** | **12 dépendances** [2] - installation légère. | **107 dépendances** [2] - environ 9 fois plus lourd. | Aucune installation, mais dépend d'un modèle distant dont le coût de calcul est externalisé et non maîtrisé. |

### Sources

| # | Source | Date | Lien |
|---|---|---|---|
| 1 | Faun.dev - *Data validation in Python: a look into Pandera and Great Expectations* | 5 mai 2023 | https://faun.dev/co/links/faun/data-validation-in-python-a-look-into-pandera-and-great-expectations/ |
| 2 | Endjin - *A look into Pandera and Great Expectations for data validation* (mis à jour) | 23 mars 2026 | https://endjin.com/blog/a-look-into-pandera-and-great-expectations-for-data-validation |
| 3 | GitHub - dépôt officiel `unionai-oss/pandera` | consulté 2026 | https://github.com/unionai-oss/pandera |
| 6 | Medium (Bhagya Rana) - *Great Expectations vs Pandera: Which Fits Your Python Stack?* | 6 oct. 2025 | https://medium.com/@bhagyarana80/8-great-expectations-vs-pandera-which-fits-your-python-stack-a115c9241dcb |
| 7 | Khuyen Tran - *Validate Your pandas DataFrame with Pandera* (cours en ligne) | consulté 2026 | https://khuyentran1401.github.io/reproducible-data-science/testing_data/pandera.html |
| 8 | GitHub - discussion officielle *Great Expectations vs Pandera* | consulté 2026 | https://github.com/unionai-oss/pandera/discussions/598 |
| 9 | Aeturrell - *The data validation landscape in 2025* | 5 mars 2025 | https://aeturrell.com/blog/posts/the-data-validation-landscape-in-2025/ |
| 10 | Techoc Blog - *I Finally Ditched Great Expectations After 6 Months of Midnight Profiling Jobs* | 26 janv. 2026 | https://techoc.blog/i-finally-ditched-great-expectations-after-6-months-of-midnight-profiling-jobs/ |

**Point de vigilance issu de la veille documentaire (source 10, janvier 2026) :** un retour d'expérience récent décrit comment Great Expectations, après une prise en main séduisante, devient progressivement complexe à maintenir sur la durée - un risque direct pour un projet porté par une seule personne côté data chez Bottleneck.

---

## 3. Test empirique - Pandera vs Great Expectations

Au-delà de la comparaison documentaire, les deux librairies ont été testées sur les **mêmes règles, sur les mêmes données brutes** (`erp.csv`). Résultat : détection strictement identique (5/5 anomalies de prix et de stock retrouvées par les deux). La différence se joue uniquement sur la mise en œuvre : Great Expectations demande environ 65% de lignes de code en plus pour la même couverture, en échange d'un rapport HTML auto-généré ("Data Docs") - dont le fonctionnement a été vérifié par génération réelle sur ce projet (capture disponible sur demande).

Scripts complets : `poc_pandera_validation.py` et `poc_great_expectations.py` (livrés séparément).

---

## 4. Test empirique - IA générative directe (méthode 3)

**Protocole :** dans une conversation neuve (sans lien avec les échanges ayant servi à construire les schémas Pandera/Great Expectations), les 3 fichiers bruts ont été transmis à une IA générative avec pour seule consigne d'identifier toute anomalie ou incohérence, sans indication préalable sur ce qu'il fallait chercher.

**Résultat majeur : cette méthode a révélé deux vraies limites dans les schémas construits aux étapes précédentes**, en plus de retrouver la quasi-totalité des anomalies déjà connues :

| Ce que la méthode 3 a mis en évidence | Impact sur Pandera / Great Expectations |
|---|---|
| Un deuxième sens de l'incohérence stock_status/quantité (outofstock avec stock positif), non testé initialement | Règle corrigée (voir POC et notebook mis à jour) |
| La décomposition exacte de l'anomalie "orphelins" en deux causes distinctes (91 identifiants jamais reliés + 20 liens cassés), alors que les schémas initiaux ne produisaient qu'un chiffre agrégé de 111, sans recouper le chiffre historique du P6 (91) | Règle scindée en deux, désormais cohérente avec la documentation P6 d'origine |
| Un risque de collision d'identifiants (deux codes non standards contiennent un numéro de SKU déjà attribué à un autre produit) | Nouvelle règle identifiée, non encore automatisée |
| 6 fiches produit en doublon (même titre, SKU différents) | Nouvelle règle ajoutée aux schémas |
| 2 compteurs de ventes négatifs (`total_sales < 0`) | Nouvelle règle ajoutée aux schémas |

**Ce que cette méthode ne permet pas :** contrairement à un schéma Pandera, son résultat n'est pas automatiquement rejouable sur un futur export - il faut refaire la sollicitation, sans garantie stricte d'obtenir exactement la même formulation d'une fois sur l'autre.

---

## 5. Décision et justification

**Décision retenue : une démarche combinée, pas un choix exclusif entre les trois.**

1. **L'IA générative directe est utilisée en amont, ponctuellement**, pour explorer un nouveau jeu de données et découvrir l'univers des règles de qualité pertinentes - elle a démontré sur ce projet une capacité de découverte supérieure aux deux librairies utilisées seules.
2. **Pandera formalise ensuite les règles confirmées** dans un schéma versionné, rejouable automatiquement sur chaque futur export - au meilleur rapport simplicité/couverture des deux librairies testées.
3. **Great Expectations est écarté de l'usage courant** : couverture strictement identique à Pandera sur ce projet, pour un coût de mise en œuvre et de maintenance plus élevé (12 vs 107 dépendances). À réévaluer si Bottleneck multiplie ses sources de données ou ses équipes, en particulier pour la gouvernance apportée par les Data Docs.

**Amélioration continue :** cette démarche (exploration IA → formalisation Pandera) est reproductible sur tout futur jeu de données Bottleneck, et pas seulement sur celui-ci.

---

## 6. Automatisation du système de veille

- Dépôt surveillé : `unionai-oss/pandera`
- Configuration : bouton **Watch → Custom → Releases** sur la page GitHub du dépôt
- Effet : notification reçue à chaque nouvelle version publiée, sans démarche active répétée.

*(Capture d'écran de l'abonnement actif à joindre en annexe de la documentation finale.)*

---

## 7. Mini-plan de formation - publics non techniques

**Public concerné :** Nicolas et l'équipe commerciale, qui liront les résultats de validation sans écrire de code.

| Objectif pédagogique | Format | Durée | Accessibilité |
|---|---|---|---|
| Comprendre ce qu'est une "règle de validation" (analogie avec un contrôle qualité physique en magasin) | Support d'une page, langage non technique | 15 min | Police lisible ≥ 12pt, contraste élevé, pas d'information codée uniquement par la couleur |
| Savoir lire le résumé produit par le script | Démonstration commentée sur un export réel | 20 min | Tableau structuré, compatible lecteur d'écran si diffusé en PDF/Word balisé |
| Savoir qui contacter en cas d'anomalie détectée | Fiche réflexe (1 page) | 10 min | Alternative textuelle systématique à tout pictogramme |

---

## 8. Ce qui a été gardé / écarté et pourquoi

| Élément | Décision | Pourquoi |
|---|---|---|
| Pandera pour la validation reproductible | **Gardé** | Meilleur rapport simplicité/couverture, confirmé par test empirique |
| Great Expectations en usage courant | **Écarté** | Couverture identique à Pandera, ~65% de code en plus, mesuré sur ce projet |
| IA générative directe comme contrôle de production | **Écartée** | Non reproductible automatiquement ; utilisée en amont comme méthode d'exploration, pas de contrôle continu |
| Règle stock_status bidirectionnelle | **Ajoutée** | Trouvée manquante grâce au test de la méthode 3 |
| Décomposition de la règle "orphelins" | **Corrigée** | Le chiffre agrégé initial (111) ne recoupait pas le chiffre historique P6 (91) ; la méthode 3 a révélé et expliqué l'écart |
| Règles "doublons de titre" et "ventes négatives" | **Ajoutées** | Catégories entièrement nouvelles, trouvées uniquement par la méthode 3 |
| Risque de collision d'identifiants (SKU réutilisé) | **Documenté, non automatisé** | Détecté par la méthode 3 ; nécessite une règle plus complexe qu'une simple contrainte de colonne, à traiter dans une itération future |
