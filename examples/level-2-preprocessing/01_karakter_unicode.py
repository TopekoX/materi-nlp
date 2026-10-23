"""Karakter, Unicode, dan encoding UTF-8 (pelajaran Level 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor
import unicodedata

from nlp_hub.konsol import pakai_utf8

pakai_utf8()

# --8<-- [start:panjang]
teks = "Tolong 🙏"
print(len(teks))
print(len(teks.encode("utf-8")))
# --8<-- [end:panjang]

# --8<-- [start:titik_kode]
for karakter in teks:
    print(repr(karakter), ord(karakter), hex(ord(karakter)))
# --8<-- [end:titik_kode]

# --8<-- [start:encode]
byte_utf8 = "é🙏".encode("utf-8")
print(list(byte_utf8))
print(byte_utf8.decode("utf-8"))
# --8<-- [end:encode]

# --8<-- [start:mojibake]
rusak = "Rumah warga terendam – tolong 🙏".encode("utf-8").decode("latin-1")
print(ascii(rusak))
perbaikan = rusak.encode("latin-1").decode("utf-8")
print(perbaikan)
# --8<-- [end:mojibake]

# --8<-- [start:normalisasi]
gaya = "𝐁𝐀𝐍𝐉𝐈𝐑 ｇｅｍｐａ"
print(gaya == "BANJIR gempa")
bersih = unicodedata.normalize("NFKC", gaya)
print(bersih)
print(bersih == "BANJIR gempa")
# --8<-- [end:normalisasi]

# --8<-- [start:tak_terlihat]
tersembunyi = "ban​jir"
print(tersembunyi, len(tersembunyi), len("banjir"))
print(tersembunyi == "banjir")
print([unicodedata.name(c) for c in tersembunyi if not c.isalpha()])
# --8<-- [end:tak_terlihat]
