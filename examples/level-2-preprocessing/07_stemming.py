"""Stemming dengan Sastrawi dan perbedaannya dengan lemmatization (pelajaran Level 2)."""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.data import muat_dataset
from nlp_hub.preprocessing import KonfigurasiPraproses, praproses_token, stem_kata

# --8<-- [start:dasar]
for kata in ["banjir", "kebanjiran", "membanjiri", "mengungsi", "pengungsi", "pengungsian"]:
    print(f"{kata:12} -> {stem_kata(kata)}")
# --8<-- [end:dasar]

# --8<-- [start:masalah]
for kata in ["memadamkan", "pemadam", "padam", "kebakaran", "pembakaran", "terbakar", "korban", "bantuan", "terjebak"]:
    print(f"{kata:12} -> {stem_kata(kata)}")
# --8<-- [end:masalah]

# --8<-- [start:kolaps]
kelompok = defaultdict(set)
for kata in ["kebakaran", "pembakaran", "terbakar", "membakar", "bakar", "pemadam", "memadamkan", "padam", "madam"]:
    kelompok[stem_kata(kata)].add(kata)
for dasar, bentuk in sorted(kelompok.items()):
    print(dasar, "<-", sorted(bentuk))
# --8<-- [end:kolaps]

# --8<-- [start:korpus]
df = muat_dataset()
tanpa = [t for teks in df["text"] for t in praproses_token(teks)]
dengan = [t for teks in df["text"] for t in praproses_token(teks, KonfigurasiPraproses(stem=True))]
print("tipe tanpa stem:", len(set(tanpa)))
print("tipe dengan stem:", len(set(dengan)))
berubah = sorted({(a, b) for a, b in zip(tanpa, dengan) if a != b})
print("pasangan unik yang berubah:", len(berubah))
print(berubah[:8])
# --8<-- [end:korpus]

# --8<-- [start:lemma]
LEMMA_CONTOH = {"memadamkan": "padam", "pemadam": "pemadam", "kebakaran": "kebakaran", "pengungsian": "pengungsian"}
for kata in LEMMA_CONTOH:
    print(f"{kata:12} stem={stem_kata(kata):10} lemma_contoh={LEMMA_CONTOH[kata]}")
# --8<-- [end:lemma]
