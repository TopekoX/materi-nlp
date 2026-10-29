"""Tahap A: definisi operasional label sebagai aturan yang dapat diperiksa, dan ukuran kesepakatan antaranotator."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # folder examples/

from sklearn.metrics import cohen_kappa_score

from nlp_hub.anotasi import label_menurut_aturan
from nlp_hub.konsol import pakai_utf8

pakai_utf8()




# --8<-- [start:kasus]
# (postingan sintetis, kejadian berlangsung?, melaporkan/meminta bantuan?, waktu & ancaman jelas?, label yang dimaksud)
KASUS = [
    ("Banjir setinggi dada di Jl. Melati, mohon evakuasi!", True, True, True, "Emergency"),
    ("Ada yang tahu cara bikin tas siaga bencana?", False, False, True, "Non-Emergency"),
    ("Gempa tadi bikin lemari roboh, ada tetangga terluka, butuh ambulans", True, True, True, "Emergency"),
    ("Gempa tadi cuma terasa sebentar, semua aman", False, True, True, "Non-Emergency"),
    ("Doakan korban longsor minggu lalu ya", False, False, True, "Non-Emergency"),
    ("Tolong follow akun saya, giveaway!", False, True, True, "Non-Emergency"),
    ("Asap tebal dari gudang dekat pasar, terdengar ledakan", True, True, True, "Emergency"),
    ("Jembatan dekat rumah kayaknya mau ambruk", True, True, False, "uncertain"),
]
cocok = 0
for teks, a, b, c, harapan in KASUS:
    hasil = label_menurut_aturan(a, b, c)
    cocok += hasil == harapan
    print(f"{hasil:13} | harapan {harapan:13} | {teks[:58]}")
print(f"aturan cocok dengan label tabel: {cocok} dari {len(KASUS)}")
# --8<-- [end:kasus]

# --8<-- [start:kappa]
# Dua anotator melabeli 10 postingan yang sama (contoh buatan untuk menunjukkan perhitungan, BUKAN data nyata).
anotator_1 = ["E", "E", "N", "N", "E", "N", "N", "E", "N", "N"]
anotator_2 = ["E", "E", "N", "E", "E", "N", "N", "N", "N", "N"]
sama = sum(x == y for x, y in zip(anotator_1, anotator_2))
print(f"kesepakatan mentah: {sama}/10 = {sama / 10:.2f}")
print(f"Cohen's kappa    : {cohen_kappa_score(anotator_1, anotator_2):.3f}")
# --8<-- [end:kappa]
