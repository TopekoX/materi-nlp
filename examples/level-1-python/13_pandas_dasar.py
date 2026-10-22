"""Dasar pandas."""
from pathlib import Path

import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 10)
pd.set_option("display.max_colwidth", 40)

df = pd.read_csv(Path(__file__).parent / "data" / "laporan_contoh.csv")
print(df.shape)
print(df.dtypes)
print(df.head(3))
print(df["label"].value_counts())
df["jumlah_kata"] = df["teks"].str.split().str.len()
print(df[["id", "jumlah_kata"]].head(3))
print(df[df["label"] == "Emergency"]["lokasi"].tolist())
print(df.groupby("label")["jumlah_kata"].mean().round(2))
