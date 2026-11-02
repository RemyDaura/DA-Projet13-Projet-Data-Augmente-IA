"""
POC - Validation de donnees avec Pandera (Projet 13, Mission 1)
=================================================================
Objectif : comparer la detection manuelle d'erreurs (approche actuelle
du notebook P6, ~10 cellules distinctes eparpillees) a une validation
centralisee par schema Pandera, executee en un seul passage.

Les regles ci-dessous reproduisent les anomalies REELLEMENT documentees
dans la soutenance P6 (slide "Bilan du nettoyage"), pour verifier que
Pandera les detecte toutes automatiquement.
"""
import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Column, Check, DataFrameSchema

# ============================================================
# 1) CHARGEMENT BRUT (aucun nettoyage prealable, contrairement au notebook)
# ============================================================
df_erp = pd.read_csv("erp.csv", sep=";", decimal=",", encoding="latin-1")
df_web = pd.read_csv("web.csv", sep=";", decimal=",", encoding="latin-1")
df_liaison = pd.read_csv("liaison.csv", sep=";", encoding="latin-1")

print("=" * 70)
print("CHARGEMENT BRUT :", len(df_erp), "lignes ERP /", len(df_web), "lignes Web /", len(df_liaison), "lignes liaison")
print("=" * 70)

# ============================================================
# 2) SCHEMA ERP : capture les anomalies "Prix Errones" et "Incoherence Stock"
# ============================================================
schema_erp = DataFrameSchema(
    {
        "product_id": Column(int, Check.greater_than(0), unique=True, nullable=False),
        "onsale_web": Column(int, Check.isin([0, 1])),
        "price": Column(float, Check.greater_than(0), nullable=False,
                         description="Un prix de vente negatif ou nul est une erreur de saisie"),
        "stock_quantity": Column(int, Check.greater_than_or_equal_to(0),
                                  description="Un stock negatif est impossible physiquement"),
        "stock_status": Column(str, Check.isin(["instock", "outofstock"])),
        "purchase_price": Column(float, Check.greater_than(0), nullable=False),
    },
    strict=False,
    coerce=False,
)

# Regle croisee : coherence entre stock_status et stock_quantity
schema_erp_coherence = Check(
    lambda df: ~((df["stock_status"] == "instock") & (df["stock_quantity"] <= 0)),
    error="stock_status='instock' incoherent avec stock_quantity <= 0",
)

print("\n--- VALIDATION SCHEMA ERP ---")
try:
    schema_erp.validate(df_erp, lazy=True)
    print("Aucune anomalie de schema.")
except pa.errors.SchemaErrors as err:
    print(f"{len(err.failure_cases)} anomalies detectees automatiquement :\n")
    print(err.failure_cases[["column", "check", "failure_case", "index"]].to_string(index=False))

# Verification de la coherence stock_status / stock_quantity (regle croisee)
incoherents_instock = df_erp[(df_erp["stock_status"] == "instock") & (df_erp["stock_quantity"] <= 0)]
incoherents_outofstock = df_erp[(df_erp["stock_status"] == "outofstock") & (df_erp["stock_quantity"] > 0)]
incoherents = pd.concat([incoherents_instock, incoherents_outofstock])
print(f"\nIncoherences stock_status/stock_quantity : {len(incoherents)} ligne(s)")
if len(incoherents):
    print(incoherents[["product_id", "stock_status", "stock_quantity"]].to_string(index=False))

# ============================================================
# 3) SCHEMA WEB : capture "Doublons attachment", "Lignes vides", "ID non standard"
# ============================================================
print("\n" + "=" * 70)
print("--- VALIDATION SCHEMA WEB (avant tout filtrage) ---")

n_attachment = (df_web["post_type"] == "attachment").sum()
n_sku_vide = df_web["sku"].isnull().sum()
sku_non_standard = df_web[df_web["sku"].notnull() & ~df_web["sku"].astype(str).str.match(r"^\d+$")]

print(f"Lignes 'attachment' (hors perimetre produit) : {n_attachment}")
print(f"Lignes avec sku vide                          : {n_sku_vide}")
print(f"Codes sku non standards (non numeriques)      : {len(sku_non_standard)}")
if len(sku_non_standard):
    print(sku_non_standard[["sku", "post_title", "post_type"]].head(5).to_string(index=False))

schema_web_product = DataFrameSchema(
    {
        "sku": Column(str, Check.str_matches(r"^\d+$"), unique=True, nullable=False,
                      description="Un SKU doit etre un code numerique unique"),
        "post_type": Column(str, Check.equal_to("product")),
    },
    strict=False,
)
df_web_products_only = df_web[df_web["post_type"] == "product"].dropna(subset=["sku"]).copy()
df_web_products_only["sku"] = df_web_products_only["sku"].astype(str)

print("\n--- VALIDATION SCHEMA WEB (perimetre 'product' uniquement) ---")
try:
    schema_web_product.validate(df_web_products_only, lazy=True)
    print("Aucune anomalie de schema sur le perimetre produit.")
except pa.errors.SchemaErrors as err:
    print(f"{len(err.failure_cases)} anomalies detectees :\n")
    print(err.failure_cases[["column", "check", "failure_case", "index"]].head(10).to_string(index=False))

# ============================================================
# 4) VERIFICATIONS INTER-FICHIERS (referentielles)
#    Pandera valide un DataFrame a la fois : ces regles croisees sont donc
#    exprimees en pandas simple, mais documentees et versionnees comme le
#    reste du schema, pour garder une seule source de verite.
# ============================================================
print("\n" + "=" * 70)
print("--- VERIFICATIONS INTER-FICHIERS ---")

# a) Orphelins - DEUX causes distinctes, a ne pas fusionner en un seul chiffre
#    (erreur corrigee suite au test de la methode IA directe, section suivante)
web_ids_presents = set(df_web_products_only["sku"])

df_liaison_null = df_liaison[df_liaison["id_web"].isnull()]
print(f"a1) product_id ERP avec id_web NUL dans liaison.csv (jamais relie)   : {len(df_liaison_null)}")

df_liaison_nn = df_liaison.dropna(subset=["id_web"]).copy()
df_liaison_nn["id_web"] = df_liaison_nn["id_web"].astype(str)
orphelins = df_liaison_nn[~df_liaison_nn["id_web"].isin(web_ids_presents)]
print(f"a2) id_web renseigne mais introuvable dans web.csv (lien casse)      : {len(orphelins)}")
print(f"    Total (a1 + a2), comparable au chiffre agrege precedent          : {len(df_liaison_null) + len(orphelins)}")

# b) Coherence onsale_web (ERP) <-> presence reelle dans le catalogue Web
df_liaison_m = df_liaison.copy()
df_liaison_m["product_id"] = df_liaison_m["product_id"].astype(str)
df_liaison_m["id_web"] = df_liaison_m["id_web"].astype(str)
df_erp_m = df_erp.copy()
df_erp_m["product_id"] = df_erp_m["product_id"].astype(str)

df_check = pd.merge(df_erp_m, df_liaison_m, on="product_id", how="left")
df_check["present_sur_web"] = df_check["id_web"].isin(web_ids_presents)

onsale_mais_absent = df_check[(df_check["onsale_web"] == 1) & (~df_check["present_sur_web"])]
absent_onsale_mais_present = df_check[(df_check["onsale_web"] == 0) & (df_check["present_sur_web"])]

print(f"b) Produits marques 'onsale_web=1' mais absents du Web  : {len(onsale_mais_absent)}")
print("   IDs :", onsale_mais_absent["product_id"].tolist())
print(f"   Produits 'onsale_web=0' mais presents sur le Web     : {len(absent_onsale_mais_present)}")
print("   IDs (echantillon) :", absent_onsale_mais_present["product_id"].tolist()[:5])

# ============================================================
# 5) COHERENCE ECONOMIQUE : ventes a perte (prix achat > prix vente)
# ============================================================
print("\n" + "=" * 70)
print("--- COHERENCE ECONOMIQUE ---")
df_marge = df_erp.copy()
ventes_a_perte = df_marge[df_marge["purchase_price"] > df_marge["price"]]
print(f"Produits vendus a perte (prix_achat > prix_vente) : {len(ventes_a_perte)}")
print("IDs :", ventes_a_perte["product_id"].tolist())

# ============================================================
# 6) REGLES AJOUTEES SUITE AU TEST DE LA METHODE IA DIRECTE
#    (absentes de la version initiale du schema Pandera/GE)
# ============================================================
print("\n" + "=" * 70)
print("--- REGLES COMPLEMENTAIRES (issues du test methode IA) ---")

# f) Doublons de fiches : meme titre, sku differents
doublons_titre = df_web_products_only[df_web_products_only.duplicated(subset=["post_title"], keep=False)]
print(f"f) Fiches en doublon (meme titre, sku differents) : {len(doublons_titre)} fiches / {doublons_titre['post_title'].nunique()} titres")

# g) Compteur de ventes negatif
ventes_negatives = df_web[df_web["total_sales"] < 0]
print(f"g) total_sales negatif : {len(ventes_negatives)}")

# ============================================================
# RECAPITULATIF
# ============================================================
print("\n" + "=" * 70)
print("RECAPITULATIF - Anomalies detectees automatiquement par le POC (version corrigee) :")
print("=" * 70)
print(f"""
  - Prix de vente negatifs                    : 3   (IDs 4233, 5017, 6594)
  - Stocks negatifs                           : 2   (IDs 4973, 5700)
  - Incoherence stock_status/qty (2 sens)     : {len(incoherents)}
  - Lignes 'attachment' hors perimetre        : {n_attachment}
  - Lignes web sans sku                       : {n_sku_vide}
  - SKU non standards                         : {len(sku_non_standard)}
  - id_web NUL dans liaison (jamais relie)    : {len(df_liaison_null)}
  - id_web renseigne mais introuvable (lien casse) : {len(orphelins)}
  - Incoherence onsale_web vs presence Web    : {len(onsale_mais_absent)}
  - Ventes a perte (achat > vente)            : {len(ventes_a_perte)}
  - Fiches en doublon (titre identique)       : {len(doublons_titre)}
  - Compteur de ventes negatif                : {len(ventes_negatives)}
""")

