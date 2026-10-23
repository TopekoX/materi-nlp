"""Dasar pandas."""
from pathlib import Path

import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 10)
pd.set_option("display.max_colwidth", 40)

# --8<-- [start:baca]
df = pd.read_csv(Path(__file__).parent / "data" / "laporan_contoh.csv")
print(df.shape)
print(df.dtypes)
print(df.head(3))
# --8<-- [end:baca]

# --8<-- [start:kolom]
print(type(df["label"]).__name__, type(df[["id", "label"]]).__name__)
print(df["label"].value_counts())
# --8<-- [end:kolom]

# --8<-- [start:kolom_baru]
df["jumlah_kata"] = df["teks"].str.split().str.len()
print(df[["id", "jumlah_kata"]].head(3))
# --8<-- [end:kolom_baru]

# --8<-- [start:saring]
print(df[df["label"] == "Emergency"]["lokasi"].tolist())
print(df[(df["label"] == "Emergency") & (df["jumlah_kata"] > 6)]["id"].tolist())
# --8<-- [end:saring]

# --8<-- [start:groupby]
print(df.groupby("label")["jumlah_kata"].mean().round(2))
# --8<-- [end:groupby]

# --8<-- [start:galat]
try:
    df["teks_laporan"]
except KeyError as e:
    print("KeyError:", e)
print(df.loc[0, "teks"])
print(df.iloc[0, 1] == df.loc[0, "teks"])
# --8<-- [end:galat]
