"""Dokumen, kalimat, token, dan tokenisasi kata (pelajaran Level 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.preprocessing import pisah_kalimat, tokenisasi

# --8<-- [start:split_biasa]
dokumen = "Banjir di Jl. Melati, tolong! Air hati-hati naik."
print(dokumen.split())
# --8<-- [end:split_biasa]

# --8<-- [start:regex]
print(tokenisasi(dokumen.lower()))
# --8<-- [end:regex]

# --8<-- [start:token_vs_tipe]
korpus = [
    "rumah-rumah warga terendam",
    "warga mengungsi, rumah terendam",
]
semua_token = [t for d in korpus for t in tokenisasi(d.lower())]
print(semua_token)
print(len(semua_token), len(set(semua_token)))
# --8<-- [end:token_vs_tipe]

# --8<-- [start:kalimat_naif]
teks = "Banjir di Jl. Melati No. 5. Air naik! Tolong?"
print(teks.split("."))
# --8<-- [end:kalimat_naif]

# --8<-- [start:kalimat_aturan]
for kalimat in pisah_kalimat(teks):
    print(repr(kalimat))
# --8<-- [end:kalimat_aturan]

# --8<-- [start:kalimat_gagal]
print(pisah_kalimat("Banjir tinggi.Tolong cepat"))
print(pisah_kalimat("Lapor ke Sdr. Andi. Air naik"))
print(pisah_kalimat("tolong banget... air naik terus"))
# --8<-- [end:kalimat_gagal]
