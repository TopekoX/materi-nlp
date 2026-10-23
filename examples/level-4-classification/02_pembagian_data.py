"""Pembagian data: latih/validasi/uji, stratified, kelompok, dan seed (pelajaran Level 4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

from nlp_hub.data import bagi_latih_uji, bagi_latih_val_uji, kodekan_label, muat_dataset
from nlp_hub.modeling import buat_pipeline

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

df = muat_dataset()

# --8<-- [start:tiga_arah]
latih, val, uji = bagi_latih_val_uji(df)
for nama, bagian in [("latih", latih), ("validasi", val), ("uji", uji)]:
    e = int((bagian["label"] == "Emergency").sum())
    print(f"{nama:9} baris={len(bagian):3}  Emergency={e:3} ({e / len(bagian):.1%})  kejadian={bagian['event_id'].nunique()}")
print("kejadian tumpang tindih:", len(set(latih["event_id"]) & set(val["event_id"]) | set(latih["event_id"]) & set(uji["event_id"]) | set(val["event_id"]) & set(uji["event_id"])))
# --8<-- [end:tiga_arah]

# --8<-- [start:stratifikasi]
y = kodekan_label(df["label"]).to_numpy()
def proporsi_uji(strat, seed):
    _, y_uji = train_test_split(y, test_size=0.1, random_state=seed, stratify=y if strat else None)
    return y_uji.mean()

tanpa = [proporsi_uji(False, s) for s in range(200)]
dengan = [proporsi_uji(True, s) for s in range(200)]
print(f"proporsi Emergency seluruh data: {y.mean():.3f}")
print(f"tanpa stratify : min={min(tanpa):.3f}  maks={max(tanpa):.3f}")
print(f"dengan stratify: min={min(dengan):.3f}  maks={max(dengan):.3f}")
# --8<-- [end:stratifikasi]

# --8<-- [start:kelompok]
idx_latih, idx_uji = train_test_split(np.arange(len(df)), test_size=0.2, random_state=42, stratify=y)
acak_latih, acak_uji = df.iloc[idx_latih], df.iloc[idx_uji]
ada = acak_uji["event_id"].isin(set(acak_latih["event_id"])).mean()
print(f"pembagian acak: {ada:.1%} teks uji berasal dari kejadian yang juga ada di data latih")
kel_latih, kel_uji = bagi_latih_uji(df)
print(f"pembagian kelompok: {kel_uji['event_id'].isin(set(kel_latih['event_id'])).mean():.1%}")
# --8<-- [end:kelompok]

# --8<-- [start:seed]
skor = []
for seed in range(10):
    l, u = bagi_latih_uji(df, seed=seed)
    m = buat_pipeline("lr").fit(l["text"], kodekan_label(l["label"]))
    skor.append(f1_score(kodekan_label(u["label"]), m.predict(u["text"]), average="macro"))
print("F1 makro tiap seed:", [round(s, 3) for s in skor])
print(f"rata-rata={np.mean(skor):.3f}  std={np.std(skor):.3f}  min={min(skor):.3f}  maks={max(skor):.3f}")
# --8<-- [end:seed]
