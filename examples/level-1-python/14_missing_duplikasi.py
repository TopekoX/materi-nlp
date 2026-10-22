"""Missing values dan duplikasi."""
from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).parent / "data" / "laporan_contoh.csv")
print(df.isna().sum())
print("duplikat teks:", df["teks"].duplicated().sum())
print(df[df["teks"].duplicated(keep=False)][["id", "teks"]])

bersih = df.dropna(subset=["teks"]).drop_duplicates(subset="teks", keep="first")
print(df.shape, "->", bersih.shape)
print(df["lokasi"].fillna("tidak diketahui").tolist()[:6])
