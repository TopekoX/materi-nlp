"""Function dan parameter."""


def hitung_kemunculan(teks, kata, huruf_kecil=True):
    """Mengembalikan berapa kali `kata` muncul pada teks."""
    if huruf_kecil:
        teks = teks.lower()
    return teks.split().count(kata)


print(hitung_kemunculan("Banjir banjir BANJIR naik", "banjir"))
print(hitung_kemunculan("Banjir banjir BANJIR naik", "banjir", huruf_kecil=False))


def ringkas(teks, *, maks=20):
    return teks if len(teks) <= maks else teks[:maks] + "..."


print(ringkas("Banjir setinggi dada di Jl. Melati"))
print(ringkas("Banjir setinggi dada di Jl. Melati", maks=10))


def statistik(angka):
    return min(angka), max(angka), sum(angka) / len(angka)


kecil, besar, rata = statistik([3, 5, 4])
print(kecil, besar, rata)


def tambah(item, daftar=None):
    if daftar is None:
        daftar = []
    daftar.append(item)
    return daftar


print(tambah(1), tambah(2))
