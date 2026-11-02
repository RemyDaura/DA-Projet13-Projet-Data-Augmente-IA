N# Annexe - Essai IA directe (méthode 3)

**Traçabilité de l'essai, conforme à l'exigence de documentation du Projet 13** : outil utilisé, prompt exact, résultat brut obtenu sans retouche.

---

## Protocole

- **Contexte :** nouvelle conversation IA, indépendante de celle utilisée pour construire les schémas Pandera et Great Expectations - aucune connaissance préalable des 9 catégories d'anomalies déjà documentées lors du P6.
- **Outil utilisé :** *(à préciser par Rémy - nom exact et version de l'IA utilisée pour cet essai)*
- **Données fournies :** `erp.csv`, `web.csv`, `liaison.csv` (fichiers bruts, sans aucun prétraitement)
- **Date de l'essai :** *(à préciser par Rémy)*

## Prompt exact utilisé

```
Voici trois fichiers exports d'un catalogue produits (un caviste) : un export
ERP, un export du site web, et une table de liaison entre les deux systèmes.
Analyse ces données et identifie toutes les anomalies, incohérences ou
erreurs de qualité que tu peux détecter, sans indication préalable sur ce
qu'il faut chercher. Présente tes résultats sous forme de liste structurée,
avec pour chaque anomalie le nombre de lignes concernées et les identifiants
précis si possible.
```

## Résultat brut obtenu (sans retouche)

> Le séparateur est ; et il y a des retours à la ligne dans certains champs texte (probablement post_content). Voyons cela plus précisément avec le module csv en gérant les guillemets correctement.
>
> J'ai croisé les trois fichiers (erp.csv, web.csv, liaison.csv). Voici les anomalies détectées, avec volumes et identifiants.
>
> **1. Problèmes structurels des fichiers**
> web.csv mélange trois natures de lignes dans un même export produits : 1 513 lignes au total, mais seulement 716 sont de vraies fiches produit (post_type = product). Les 714 autres lignes sont des pièces jointes images (post_type = attachment, post_mime_type = image/jpeg) et 83 lignes sont quasi vides (seuls virtual, downloadable, rating_count sont renseignés à 0, tout le reste est vide). Toute analyse faite sans filtrer sur post_type = product fausse les comptages (ex : le product_type semble représenter 1 318+ "Vin" alors qu'il n'y a que 660 vrais vins).
>
> Encodage et format incohérents entre fichiers : erp.csv et liaison.csv sont en ASCII pur avec séparateur ;, web.csv est en Windows-1252/latin1 avec séparateur ; et guillemets doublés dans les champs HTML (post_content). Les prix (price, purchase_price) utilisent la virgule décimale sous forme de texte, pas un nombre.
>
> **2. Identifiants et liens cassés entre systèmes**
> 91 product_id de l'ERP n'ont aucun id_web renseigné dans liaison.csv (donc aucun lien vers le site). Parmi eux, 3 sont pourtant marqués onsale_web = 1 (en vente en ligne) sans fiche web associée : product_id 4594, 5070, 5075.
>
> 20 id_web présents dans liaison.csv ne correspondent à aucun sku existant dans web.csv (fiche supprimée ou jamais créée côté site) : product_id 4289, 4568, 4584, 4741, 4864, 4869, 4921, 4922, 5018, 5021, 5505, 5559, 5570, 5800, 5953, 5954, 5955, 5957, 6100, 7329.
>
> Format d'identifiant non standard pour 3 entrées de liaison.csv, alors que tous les autres id_web sont numériques :
> - product_id 4954 → id_web = "bon-cadeau-25-euros" (un slug texte, pas un ID)
> - product_id 7247 → id_web = "13127-1" (le sku 13127 « propre » est déjà utilisé par le product_id 4053, ce qui crée une ambiguïté)
> - product_id 7329 → id_web = "14680-1" (orpheline, cf. point précédent, le sku 14680 est déjà pris par product_id 4757)
>
> 2 fiches produit dans web.csv n'ont pas de sku du tout : « Pierre Jean Villa Condrieu Jardin Suspendu 2018 » et « Pierre Jean Villa Côte Rôtie Fongeant 2017 ». Impossible de les relier à l'ERP.
>
> **3. Prix (erp.csv)**
> 3 prix négatifs : product_id 4233 (-20 €), 5017 (-8 €), 6594 (-9,1 €) - tous les trois passés à l'as en stock ou pas nul.
>
> 7 produits avec une marge négative (purchase_price > price, donc vente à perte) :
>
> | product_id | prix vente | prix d'achat |
> |---|---|---|
> | 4233 | -20,00 € | 10,33 € |
> | 4355 | 12,65 € | 77,48 € |
> | 4864 | 8,30 € | 9,99 € |
> | 5017 | -8,00 € | 4,34 € |
> | 6324 | 92,00 € | 99,00 € |
> | 6594 | -9,10 € | 4,61 € |
> | 7196 | 31,00 € | 31,20 € |
>
> (le reste du catalogue suit un ratio prix de vente / prix d'achat très régulier, autour de ×1,9 - ces 7 cas sortent nettement du lot)
>
> **4. Stock (erp.csv)**
> Stock négatif : product_id 4973 (-10), product_id 5700 (-1).
>
> Incohérence statut / quantité :
> - product_id 4885 : stock_status = instock mais stock_quantity = 0
> - product_id 4039 : stock_status = outofstock mais stock_quantity = 3
>
> **5. Incohérence disponibilité ERP / publication web**
> product_id 4200 (id_web 16295, « Moulin de Gassac IGP Pays d'Hérault Guilhem Rosé 2019 ») : onsale_web = 0 côté ERP, mais la fiche est bien publish sur le site.
>
> **6. Doublons de catalogue (fiches quasi identiques)**
> 3 titres strictement identiques portés par 2 sku différents chacun (6 fiches concernées), probablement des doublons de saisie :
> - « Clos du Mont-Olivet Châteauneuf-du-Pape 2007 » - sku 13127-1 et 16034
> - « Domaine Hauvette IGP Alpilles Jaspe 2017 » - sku 15292 et 16068
> - « Marc Colin Et Fils Chassagne-Montrachet Blanc Les Vide-Bourses 1er Cru 2016 » - sku 14828 et 14000
>
> **7. Valeurs aberrantes diverses**
> total_sales négatif pour 2 produits - les mêmes 2 fiches sans sku du point 2 : -56 ventes et -17 ventes. Un compteur de ventes ne peut pas être négatif ; ces deux lignes cumulent donc plusieurs défauts (pas de sku, pas de lien ERP, ventes négatives).
>
> **Résumé chiffré :** sur 825 références catalogue (ERP), on dénombre au moins 91 sans lien web, 20 liens cassés, 3 identifiants au format non standard, 10 anomalies de prix/marge, 4 anomalies de stock, 6 fiches en doublon, et 2 fiches web orphelines avec compteur de ventes négatif - soit une bonne partie du catalogue à faire vérifier avant toute exploitation fiable des données.

---

## Validation croisée (post-essai)

Chaque chiffre ci-dessus a été revérifié par calcul direct sur les données (voir `poc_pandera_validation.py`, section "vérifications inter-fichiers" et "règles complémentaires") : tous confirmés exacts, y compris la décomposition 91 + 20 = 111.
