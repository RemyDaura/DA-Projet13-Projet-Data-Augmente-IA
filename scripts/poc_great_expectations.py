"""
POC - Validation de donnees avec Great Expectations (Projet 13, Mission 1)
============================================================================
Objectif : test empirique reel de Great Expectations sur les memes donnees
et les memes regles que le POC Pandera, pour permettre une comparaison
directe (temps de mise en place, lignes de code, lisibilite des resultats).
"""
import time
import pandas as pd
import great_expectations as gx

t0 = time.time()

# ============================================================
# 1) CHARGEMENT BRUT (identique au POC Pandera)
# ============================================================
df_erp_brut = pd.read_csv("erp.csv", sep=";", decimal=",", encoding="latin-1")
print(f"{len(df_erp_brut)} lignes ERP chargees")

# ============================================================
# 2) MISE EN PLACE GREAT EXPECTATIONS
#    (Data Context -> Data Source -> Data Asset -> Batch Definition)
# ============================================================
context = gx.get_context(mode="ephemeral")

data_source = context.data_sources.add_pandas("erp_pandas_source")
data_asset = data_source.add_dataframe_asset(name="erp_asset")
batch_definition = data_asset.add_batch_definition_whole_dataframe("erp_batch_def")

suite = context.suites.add(gx.ExpectationSuite(name="erp_suite"))

# Memes regles que le schema Pandera, pour comparaison directe
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="product_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="product_id"))
suite.add_expectation(gx.expectations.ExpectColumnDistinctValuesToBeInSet(column="onsale_web", value_set=[0, 1]))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="price", min_value=0, strict_min=True))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="stock_quantity", min_value=0))
suite.add_expectation(gx.expectations.ExpectColumnDistinctValuesToBeInSet(column="stock_status", value_set=["instock", "outofstock"]))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="purchase_price", min_value=0, strict_min=True))

t_setup = time.time()

# ============================================================
# 3) VALIDATION
# ============================================================
batch = batch_definition.get_batch(batch_parameters={"dataframe": df_erp_brut})
results = batch.validate(suite)

t_validate = time.time()

print(f"\nTemps de mise en place (schema)  : {t_setup - t0:.2f} s")
print(f"Temps de validation                : {t_validate - t_setup:.2f} s")
print(f"\nValidation globale reussie : {results.success}")

print("\n--- Detail par regle ---")
for r in results.results:
    expectation_type = r.expectation_config.type
    column = r.expectation_config.kwargs.get("column")
    success = r.success
    unexpected_count = r.result.get("unexpected_count", 0) if not success else 0
    status = "OK" if success else f"ECHEC ({unexpected_count} valeur(s) en anomalie)"
    print(f"  {expectation_type:45s} [{column}] : {status}")
