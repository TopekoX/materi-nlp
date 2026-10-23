"""Negasi: tidak, belum, bukan, jangan (pelajaran Level 2)."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.data import muat_dataset
from nlp_hub.kamus import KATA_NEGASI
from nlp_hub.preprocessing import KonfigurasiPraproses, praproses_token, tandai_negasi, tokenisasi

# --8<-- [start:dasar]
token = tokenisasi("tidak ada korban jiwa")
print(token)
print(tandai_negasi(token))
# --8<-- [end:dasar]

# --8<-- [start:jendela]
token = tokenisasi("belum ada bantuan masuk ke desa")
for jendela in [1, 2, 3]:
    print(jendela, tandai_negasi(token, jendela=jendela))
# --8<-- [end:jendela]

# --8<-- [start:beda_makna]
for teks in ["Belum ada bantuan, air terus naik", "Tidak ada korban jiwa", "Jangan panik, tetap tenang"]:
    print(teks, "->", tandai_negasi(tokenisasi(teks.lower())))
# --8<-- [end:beda_makna]

# --8<-- [start:salah]
print(tandai_negasi(tokenisasi("tidak hanya banjir tetapi juga longsor")))
print(tandai_negasi(tokenisasi("bukan gempa, hanya truk lewat")))
# --8<-- [end:salah]

# --8<-- [start:korpus]
df = muat_dataset()
k = KonfigurasiPraproses(negasi=True)
hitung = {"Emergency": Counter(), "Non-Emergency": Counter()}
for teks, label in zip(df["text"], df["label"]):
    for t in praproses_token(teks, k):
        if t in KATA_NEGASI:
            hitung[label][t] += 1
print(hitung["Emergency"])
print(hitung["Non-Emergency"])
# --8<-- [end:korpus]
