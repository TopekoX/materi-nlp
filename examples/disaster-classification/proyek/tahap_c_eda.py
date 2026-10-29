"""Tahap C: analisis data eksploratif dataset sintetis (struktur, kualitas, distribusi, panjang teks, risiko kebocoran)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # folder examples/

import pandas as pd

from nlp_hub.data import bagi_latih_uji, muat_dataset
from nlp_hub.konsol import pakai_utf8

pakai_utf8()
pd.set_option("display.width", 120)

# --8<-- [start:struktur]
df = muat_dataset(hapus_duplikat=False)
print("bentuk:", df.shape)
print(df.dtypes.to_string())
print("nilai hilang per kolom:", df.isna().sum().to_dict())
print("duplikat teks persis  :", int(df["text"].duplicated().sum()))
# --8<-- [end:struktur]

# --8<-- [start:label]
hitung = df["label"].value_counts()
print(hitung.to_string())
print("proporsi Emergency:", round(float((df["label"] == "Emergency").mean()), 3))
print(pd.crosstab(df["post_type"], df["label"]).to_string())
# --8<-- [end:label]

# --8<-- [start:panjang]
df = df.assign(panjang=df["text"].str.len(), n_kata=df["text"].str.split().str.len())
print(df.groupby("label")[["panjang", "n_kata"]].describe().round(1).T.to_string())
# --8<-- [end:panjang]

# --8<-- [start:aman]
print("contoh teks (sintetis; dipotong 70 karakter):")
for label in ("Emergency", "Non-Emergency"):
    for teks in df[df["label"] == label]["text"].head(2):
        print(f"  [{label}] {teks[:70]}")
# --8<-- [end:aman]

# --8<-- [start:bocor]
latih, uji = bagi_latih_uji(muat_dataset())
templat_uji, templat_latih = set(uji["template_id"]), set(latih["template_id"])
print("baris latih/uji:", len(latih), "/", len(uji))
print("event_id beririsan:", len(set(latih["event_id"]) & set(uji["event_id"])))
print(f"templat uji yang juga ada di latih: {len(templat_uji & templat_latih)} dari {len(templat_uji)}")
# --8<-- [end:bocor]
