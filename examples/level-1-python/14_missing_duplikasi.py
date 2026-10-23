"""Missing values dan duplikasi."""
from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).parent / "data" / "laporan_contoh.csv")

# --8<-- [start:missing]
print(df.isna().sum())
print(df[df["teks"].isna()][["id", "label"]])
# --8<-- [end:missing]

# --8<-- [start:duplikat]
print("duplikat teks:", df["teks"].duplicated().sum())
print(df[df["teks"].duplicated(keep=False)][["id", "teks"]])
# --8<-- [end:duplikat]

# --8<-- [start:bersih]
bersih = df.dropna(subset=["teks"]).drop_duplicates(subset="teks", keep="first")
print(df.shape, "->", bersih.shape)
print(bersih["id"].tolist())
# --8<-- [end:bersih]

# --8<-- [start:isi]
print(df["lokasi"].fillna("tidak diketahui").tolist()[:6])
print(df["lokasi"].isna().sum(), df.fillna({"lokasi": "tidak diketahui"})["lokasi"].isna().sum())
# --8<-- [end:isi]

# --8<-- [start:kapital]
kecil = pd.Series(["Banjir naik", "banjir naik ", "BANJIR NAIK"])
print(kecil.duplicated().sum())
print(kecil.str.lower().str.strip().duplicated().sum())
# --8<-- [end:kapital]

# --8<-- [start:nan_bukan_sama]
print(float("nan") == float("nan"), pd.isna(float("nan")))
# --8<-- [end:nan_bukan_sama]
