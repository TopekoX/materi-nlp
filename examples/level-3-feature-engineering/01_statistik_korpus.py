"""Statistik korpus, panjang teks, frekuensi kata, dan vocabulary (pelajaran Level 3)."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import pandas as pd

from nlp_hub.data import muat_dataset
from nlp_hub.preprocessing import praproses_token, tokenisasi

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

# --8<-- [start:dasar]
df = muat_dataset(hapus_duplikat=False)
print(df.shape)
print(df.dtypes.to_string())
print(df.isna().sum().to_string())
print("duplikat teks:", df["text"].duplicated().sum())
print(df["label"].value_counts().to_string())
print(df["label"].value_counts(normalize=True).round(3).to_string())
# --8<-- [end:dasar]

# --8<-- [start:panjang]
df = muat_dataset()
df["n_karakter"] = df["text"].str.len()
df["n_token"] = df["text"].apply(lambda t: len(tokenisasi(t.lower())))
print(df.groupby("label")[["n_karakter", "n_token"]].describe().round(1).T.to_string())
# --8<-- [end:panjang]

# --8<-- [start:frekuensi]
token_per_teks = [praproses_token(t) for t in df["text"]]
semua = [t for d in token_per_teks for t in d]
print("token:", len(semua), "tipe:", len(set(semua)))
print(Counter(semua).most_common(10))
# --8<-- [end:frekuensi]

# --8<-- [start:df_kata]
dok_freq = Counter(k for d in token_per_teks for k in set(d))
hapax = [k for k, n in Counter(semua).items() if n == 1]
print("kata yang muncul tepat 1x (hapax):", len(hapax), f"({len(hapax) / len(set(semua)):.1%} dari tipe)")
print("kata di >= 5 dokumen:", sum(n >= 5 for n in dok_freq.values()))
print("DF tertinggi:", dok_freq.most_common(5))
# --8<-- [end:df_kata]

# --8<-- [start:per_kelas]
def top_kata(label, n=8):
    c = Counter(k for d, l in zip(token_per_teks, df["label"]) if l == label for k in set(d))
    return c.most_common(n)


print("Emergency    :", top_kata("Emergency"))
print("Non-Emergency:", top_kata("Non-Emergency"))
# --8<-- [end:per_kelas]
