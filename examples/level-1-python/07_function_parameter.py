"""Function dan parameter."""
# --8<-- [start:dasar]
def hitung_kemunculan(teks, kata, huruf_kecil=True):
    """Mengembalikan berapa kali `kata` muncul pada teks."""
    if huruf_kecil:
        teks = teks.lower()
    return teks.split().count(kata)


print(hitung_kemunculan("Banjir banjir BANJIR naik", "banjir"))
print(hitung_kemunculan("Banjir banjir BANJIR naik", "banjir", huruf_kecil=False))
# --8<-- [end:dasar]

# --8<-- [start:keyword_only]
def ringkas(teks, *, maks=20):
    return teks if len(teks) <= maks else teks[:maks] + "..."


print(ringkas("Banjir setinggi dada di Jl. Melati"))
print(ringkas("Banjir setinggi dada di Jl. Melati", maks=10))
try:
    ringkas("Banjir setinggi dada", 10)
except TypeError as e:
    print("TypeError:", e)
# --8<-- [end:keyword_only]

# --8<-- [start:banyak]
def statistik(angka):
    return min(angka), max(angka), sum(angka) / len(angka)


hasil = statistik([3, 5, 4])
print(hasil, type(hasil).__name__)
kecil, besar, rata = hasil
print(kecil, besar, rata)
# --8<-- [end:banyak]

# --8<-- [start:default]
def tambah_salah(item, daftar=[]):
    daftar.append(item)
    return daftar


print(tambah_salah(1), tambah_salah(2))


def tambah(item, daftar=None):
    if daftar is None:
        daftar = []
    daftar.append(item)
    return daftar


print(tambah(1), tambah(2))
# --8<-- [end:default]

# --8<-- [start:lingkup]
jumlah_global = 10


def ubah_lokal():
    jumlah_global = 99      # variabel BARU di dalam fungsi
    return jumlah_global


print(ubah_lokal(), jumlah_global)
# --8<-- [end:lingkup]

# --8<-- [start:tanpa_return]
def cetak_saja(x):
    print("nilai:", x)


hasil = cetak_saja(5)
print(hasil)
# --8<-- [end:tanpa_return]

# --8<-- [start:anotasi]
def rasio_kapital(teks: str) -> float:
    """Proporsi huruf kapital terhadap seluruh huruf (0.0 bila tidak ada huruf)."""
    huruf = [c for c in teks if c.isalpha()]
    if not huruf:
        return 0.0
    return sum(c.isupper() for c in huruf) / len(huruf)


print(rasio_kapital("TOLONG banjir"), rasio_kapital("123"))
# --8<-- [end:anotasi]
