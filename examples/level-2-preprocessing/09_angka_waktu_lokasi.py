"""Normalisasi angka, waktu, dan lokasi (pelajaran Level 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.data import muat_dataset
from nlp_hub.preprocessing import (
    KonfigurasiPraproses, normalisasi_angka, normalisasi_lokasi, normalisasi_waktu, praproses_token,
)

# --8<-- [start:waktu]
for teks in ["gempa pukul 08.12 tadi", "api terlihat jam 22:15 wib", "air setinggi 1.50 m", "magnitudo 4,1"]:
    print(f"{teks!r:30} -> {' '.join(normalisasi_waktu(teks).split())!r}")
# --8<-- [end:waktu]

# --8<-- [start:angka]
for teks in ["setinggi 50 cm", "ada 2 lansia dan 3 balita", "dana Rp50.000", "gempa m4,1"]:
    print(f"{teks!r:30} -> {' '.join(normalisasi_angka(teks).split())!r}")
# --8<-- [end:angka]

# --8<-- [start:lokasi]
for teks in [
    "banjir di jl. melati rt 08",
    "warga kelurahan sukamaju mengungsi",
    "di kota ini aman",
    "desa cikaramas terendam",
    "dekat sukajadi tadi",
]:
    print(f"{teks!r:40} -> {' '.join(normalisasi_lokasi(teks).split())!r}")
# --8<-- [end:lokasi]

# --8<-- [start:korpus]
df = muat_dataset()
k0 = KonfigurasiPraproses()
k1 = KonfigurasiPraproses(angka_waktu_lokasi=True)
t0 = [praproses_token(t, k0) for t in df["text"]]
t1 = [praproses_token(t, k1) for t in df["text"]]
print("tipe:", len({x for d in t0 for x in d}), "->", len({x for d in t1 for x in d}))
ada = ["tok_lokasi" in d for d in t1]
df["ada_lokasi"] = ada
print(df.groupby("label")["ada_lokasi"].agg(["sum", "count", "mean"]).round(3))
# --8<-- [end:korpus]
