"""Normalisasi bahasa informal, huruf berulang, dan typo (pelajaran Level 2)."""
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.data import muat_dataset
from nlp_hub.preprocessing import (
    KonfigurasiPraproses, koreksi_typo, kurangi_huruf_berulang, normalisasi_informal,
    praproses_token, tokenisasi,
)

# --8<-- [start:kamus]
kalimat = "tlg bgt air udh naik, blm ada yg dtg"
token = tokenisasi(kalimat)
print(token)
print([normalisasi_informal(t) for t in token])
# --8<-- [end:kamus]

# --8<-- [start:berulang]
for kata in ["tolooong", "banjiiir", "beeeeterbangan", "saaat", "maaaf"]:
    print(kata, "->", kurangi_huruf_berulang(kata))
# --8<-- [end:berulang]

# --8<-- [start:bug_angka]
print(re.sub(r"(\w)\1{2,}", r"\1", "Rp1000000"))
print(kurangi_huruf_berulang("Rp1000000"))
# --8<-- [end:bug_angka]

# --8<-- [start:typo_skor]
for salah, benar in [("bnjir", "banjir"), ("banjirr", "banjir"), ("banjri", "banjir"), ("banjar", "banjir")]:
    skor = SequenceMatcher(None, salah, benar).ratio()
    print(f"{salah:8} vs {benar:8} kemiripan={skor:.3f}")
# --8<-- [end:typo_skor]

# --8<-- [start:typo_koreksi]
for kata in ["bnjir", "banjri", "banjar", "rumah"]:
    print(kata, koreksi_typo(kata), koreksi_typo(kata, batas=0.8))
# --8<-- [end:typo_koreksi]

# --8<-- [start:korpus]
df = muat_dataset()
tanpa = KonfigurasiPraproses(informal=False, huruf_berulang=False)
dengan = KonfigurasiPraproses()
token_tanpa = [t for teks in df["text"] for t in praproses_token(teks, tanpa)]
token_dengan = [t for teks in df["text"] for t in praproses_token(teks, dengan)]
print("token :", len(token_tanpa), len(token_dengan))
print("tipe  :", len(set(token_tanpa)), len(set(token_dengan)))
berubah = sum(a != b for a, b in zip(token_tanpa, token_dengan))  # panjang sama: normalisasi tidak menambah/membuang token
print("posisi yang berubah:", berubah)
# --8<-- [end:korpus]
