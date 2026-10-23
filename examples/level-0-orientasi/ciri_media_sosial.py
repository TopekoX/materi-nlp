"""Mengenali ciri teks media sosial dengan regex sederhana (ILUSTRATIF)."""
import re
import sys

# Konsol Windows lama memakai encoding cp1252 yang tidak bisa mencetak emoji.
# Baris ini memaksa keluaran memakai UTF-8 (aman dijalankan di sistem lain).
sys.stdout.reconfigure(encoding="utf-8")

# --8<-- [start:pola]
# Rentang emoji ditulis dengan chr() agar mudah dibaca dan tidak memakai escape.
RENTANG_EMOJI = "[" + chr(0x1F300) + "-" + chr(0x1FAFF) + chr(0x2600) + "-" + chr(0x27BF) + "]"

POLA = {
    "url": re.compile(r"https?://\S+"),
    "mention": re.compile(r"@\w+"),
    "hashtag": re.compile(r"#\w+"),
    "emoji": re.compile(RENTANG_EMOJI),
    "huruf_berulang": re.compile(r"(\w)\1{2,}"),
}
# --8<-- [end:pola]

# --8<-- [start:contoh]
CONTOH = "@bpbd_kota TOLOOONG banjir naik cepet bgt di Jl. Melati 🙏 #banjir https://t.co/xyz123"
print(CONTOH)
# --8<-- [end:contoh]


# --8<-- [start:ekstrak]
def ekstrak_ciri(teks):
    return {nama: [m.group(0) for m in pola.finditer(teks)] for nama, pola in POLA.items()}


for nama, hasil in ekstrak_ciri(CONTOH).items():
    print(f"{nama:15}: {hasil}")
# --8<-- [end:ekstrak]

# --8<-- [start:normalisasi]
anonim = POLA["mention"].sub("@USER", CONTOH)
print(anonim)
hapus_ulang = re.sub(r"(\w)\1{2,}", r"\1", "TOLOOONG")
print(hapus_ulang, hapus_ulang.lower())
# --8<-- [end:normalisasi]

# --8<-- [start:batas]
print(ekstrak_ciri("Tolong!!! #gempaMalang bgt 😭 cek http://contoh.id/berita.")["url"])
print(ekstrak_ciri("Tolong!!! #gempaMalang bgt 😭 cek http://contoh.id/berita.")["hashtag"])
print(ekstrak_ciri("Baaanjir dan sooooorry")["huruf_berulang"])
# --8<-- [end:batas]
