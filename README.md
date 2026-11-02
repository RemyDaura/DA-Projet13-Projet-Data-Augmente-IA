# Projet 13 : Piloter un projet data augmenté par l'IA

### Contexte
Projet de fin de formation : améliorer un livrable existant grâce à l'IA, de façon critique et documentée. Le point de départ est mon [projet 6 (BottleNeck)](https://github.com/RemyDaura/DA-Projet6-Optimisation-Gestion-Donnees-Python), dont les contrôles qualité étaient manuels, dispersés dans une dizaine de blocs de code et jamais rejoués automatiquement.

**Mon objectif :** centraliser les règles de qualité des données de façon reproductible, sans complexifier l'outillage au-delà des besoins d'une petite structure sans équipe data.

### Missions réalisées
* **Veille technologique :** comparaison sourcée de méthodes de validation de données.
* **Cahier des charges** et **gestion de projet** (backlog, registre des risques).
* **Trois méthodes testées sur les mêmes données :**
    * **Pandera :** schéma de validation Python léger.
    * **Great Expectations :** mêmes règles, pour une comparaison directe.
    * **IA générative :** fichiers bruts transmis sans indication sur ce qu'il fallait chercher.
* **Notebook amélioré :** intégration du schéma retenu dans le notebook du projet 6.

### Résultats
* **8 catégories d'anomalies sur 9** retrouvées automatiquement.
* **2 bugs de reproductibilité** trouvés et corrigés dans le notebook d'origine (une colonne supprimée deux fois, une marge calculée sur le mauvais tableau).
* **+65 % de code** avec Great Expectations pour une couverture identique à Pandera.
* L'IA générative a révélé **deux angles morts dans mon propre schéma** et deux catégories d'anomalies inédites.

**Démarche retenue :** explorer un nouveau jeu de données avec l'IA générative, puis formaliser les règles confirmées dans un schéma Pandera reproductible.

### Compétences & Outils
* **Langage :** Python
* **Librairies :** Pandas, Pandera, Great Expectations
* **Méthode :** veille technologique, cahier des charges, comparaison argumentée d'outils, IA générative

### Reproduire l'analyse
Les données brutes sont dans `data-raw/`. Pour exécuter les notebooks, placez ces fichiers dans le même dossier que le notebook.

### Limites
L'IA générative n'est pas reproductible d'une exécution à l'autre : elle sert à explorer, pas à surveiller en continu.

---
📂 Dossier complet sur mon portfolio : [remydaura.github.io/p13.html](https://remydaura.github.io/p13.html)

*Ce projet fait partie de la formation Data Analyst d'OpenClassrooms.*
