"""Variabel dan tipe data dasar pada konteks laporan bencana."""
lokasi = "Jl. Melati"
jumlah_korban = 3
tinggi_air_m = 1.2
darurat = True
catatan = None

for nama, nilai in [("lokasi", lokasi), ("jumlah_korban", jumlah_korban),
                    ("tinggi_air_m", tinggi_air_m), ("darurat", darurat),
                    ("catatan", catatan)]:
    print(f"{nama:14} {nilai!r:14} {type(nilai).__name__}")

print(int("12") + 1)       # string -> integer
print(str(12) + "1")       # integer -> string
print(7 / 2, 7 // 2, 7 % 2)
print(0.1 + 0.2 == 0.3, round(0.1 + 0.2, 2) == 0.3)
