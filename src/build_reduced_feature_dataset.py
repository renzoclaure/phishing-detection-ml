import pandas as pd

INPUT = "data/processed/url_features_dataset_full.csv"
OUTPUT = "data/processed/url_features_dataset_reduced.csv"

df = pd.read_csv(INPUT)

remove_cols = [
    "UsoIP",
    "HTTPS",
    "NoPuertoStd",
    "PrefijoSufijo",
    "EnlacesApuntanPagina",
    "HTTPSURLDominio"
]

df_reduced = df.drop(columns=remove_cols)

df_reduced.to_csv(OUTPUT, index=False)

print("Reduced-feature dataset created:", df_reduced.shape)
print("Removed columns:", remove_cols)
