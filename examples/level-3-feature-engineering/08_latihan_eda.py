"""Kunci latihan: EDA dan pemeriksaan kebocoran pada dataset sintetis (Level 3)."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import pandas as pd

from nlp_hub.data import bagi_latih_uji, muat_dataset
from nlp_hub.preprocessing import praproses_token

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

mentah = muat_dataset(hapus_duplikat=False)

# --8<-- [start:duplikat]
dup = mentah[mentah["text"].duplicated(keep=False)]
print("baris yang terlibat duplikat:", len(dup), "| teks unik:", dup["text"].nunique())
print("duplikat selalu satu kejadian:", bool((dup.groupby("text")["event_id"].nunique() == 1).all()))
print(dup["label"].value_counts().to_dict())
# --8<-- [end:duplikat]

# --8<-- [start:templat]
df = muat_dataset()
kejadian_per_templat = df.groupby("template_id")["event_id"].nunique()
print("templat:", df["template_id"].nunique(), "| dipakai di >1 kejadian:", int((kejadian_per_templat > 1).sum()))
print("rata-rata kejadian per templat:", round(float(kejadian_per_templat.mean()), 2))
latih, uji = bagi_latih_uji(df)
print("kejadian di latih dan uji sekaligus:", len(set(latih["event_id"]) & set(uji["event_id"])))
print("templat di latih dan uji sekaligus :", len(set(latih["template_id"]) & set(uji["template_id"])), "dari", uji["template_id"].nunique(), "templat uji")
# --8<-- [end:templat]

# --8<-- [start:eksklusif]
token = [set(praproses_token(t)) for t in df["text"]]
n_e = Counter(k for s, l in zip(token, df["label"]) if l == "Emergency" for k in s)
n_n = Counter(k for s, l in zip(token, df["label"]) if l == "Non-Emergency" for k in s)
hanya_e = sorted([(k, n) for k, n in n_e.items() if n >= 10 and n_n.get(k, 0) == 0], key=lambda x: -x[1])
hanya_n = sorted([(k, n) for k, n in n_n.items() if n >= 10 and n_e.get(k, 0) == 0], key=lambda x: -x[1])
print("kata (DF>=10) hanya di Emergency    :", hanya_e[:6])
print("kata (DF>=10) hanya di Non-Emergency:", hanya_n[:6])
# --8<-- [end:eksklusif]

# --8<-- [start:silang]
print(pd.crosstab(df["post_type"], df["label"]).to_string())
# --8<-- [end:silang]
