"""Tokenizer subword mini: BPE dipelajari dari dataset sintetis, WordPiece dengan kosakata kecil."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.data import muat_dataset
from nlp_hub.konsol import pakai_utf8
from nlp_hub.preprocessing import praproses_token
from nlp_hub.subword import hitung_kata, latih_bpe, pecah_wordpiece, terapkan_bpe

pakai_utf8()

# --8<-- [start:hitung]
df = muat_dataset()
semua_kata = [t for teks in df["text"] for t in praproses_token(teks) if t.isalpha()]
hitung = hitung_kata(semua_kata)
print("jumlah token kata:", len(semua_kata), "| jenis kata unik:", len(hitung))
print("lima kata tersering:", hitung.most_common(5))
# --8<-- [end:hitung]

# --8<-- [start:bpe]
aturan = latih_bpe(hitung, n_gabung=300)
print("10 aturan gabung pertama:", aturan[:10])
for kata in ("banjir", "banjirnya", "kebanjiran", "gempa", "tolooong", "xyz"):
    print(f"{kata:11} -> {terapkan_bpe(kata, aturan)}")
# --8<-- [end:bpe]

# --8<-- [start:ukuran]
for n in (0, 20, 100, 300):
    a = latih_bpe(hitung, n_gabung=n)
    rata = sum(len(terapkan_bpe(k, a)) * c for k, c in hitung.items()) / sum(hitung.values())
    print(f"{n:3} aturan gabung -> rata-rata {rata:.2f} potongan per kata")
# --8<-- [end:ukuran]

# --8<-- [start:wordpiece]
kosakata_wp = {"banjir", "##nya", "air", "ke", "##an", "##banjir", "gempa", "tolong", "[UNK]"}
for kata in ("banjirnya", "kebanjiran", "airnya", "gempa", "meluap"):
    print(f"{kata:11} -> {pecah_wordpiece(kata, kosakata_wp)}")
# --8<-- [end:wordpiece]
