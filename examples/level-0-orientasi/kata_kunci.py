"""Aturan kata kunci vs aturan dengan petunjuk konteks (ILUSTRATIF, bukan eksperimen)."""

# --8<-- [start:data]
postingan = [
    "Banjir setinggi dada di Jl. Melati, mohon evakuasi",
    "Banjir 2020 itu parah ya, jangan sampai terulang",
    "Kemarin banjir sudah surut, jalan bisa dilewati",
]
# --8<-- [end:data]


# --8<-- [start:aturan1]
def tandai_dengan_kata_kunci(teks):
    return "banjir" in teks.lower()


for teks in postingan:
    print(tandai_dengan_kata_kunci(teks), "|", teks)
# --8<-- [end:aturan1]


# --8<-- [start:aturan2]
PETUNJUK_LAMPAU = ["kemarin", "sudah surut", "2020", "terulang"]


def tandai_dengan_konteks(teks):
    kecil = teks.lower()
    if "banjir" not in kecil:
        return False
    return not any(p in kecil for p in PETUNJUK_LAMPAU)


for teks in postingan:
    print(tandai_dengan_konteks(teks), "|", teks)
# --8<-- [end:aturan2]


# --8<-- [start:gagal]
uji = [
    "Banjir bandang barusan, tolong kirim perahu karet",
    "Banjir hari ini sudah surut tapi kami masih butuh makanan, tolong",
    "Tolong, air sudah masuk rumah",
]
for teks in uji:
    print(tandai_dengan_konteks(teks), "|", teks)
# --8<-- [end:gagal]
