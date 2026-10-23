"""Variabel dan tipe data dasar pada konteks laporan bencana."""
import math

# --8<-- [start:variabel]
lokasi = "Jl. Melati"
jumlah_korban = 3
tinggi_air_m = 1.2
darurat = True
catatan = None
# --8<-- [end:variabel]

# --8<-- [start:tipe]
for nama, nilai in [("lokasi", lokasi), ("jumlah_korban", jumlah_korban),
                    ("tinggi_air_m", tinggi_air_m), ("darurat", darurat),
                    ("catatan", catatan)]:
    print(f"{nama:14} {nilai!r:14} {type(nilai).__name__}")
# --8<-- [end:tipe]

# --8<-- [start:konversi]
print(int("12") + 1)       # string -> integer
print(str(12) + "1")       # integer -> string
print(type(int("12")).__name__, type(str(12)).__name__)
# --8<-- [end:konversi]

# --8<-- [start:aritmetika]
print(7 / 2, 7 // 2, 7 % 2)
# --8<-- [end:aritmetika]

# --8<-- [start:desimal]
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3, round(0.1 + 0.2, 2) == 0.3, math.isclose(0.1 + 0.2, 0.3))
# --8<-- [end:desimal]

# --8<-- [start:galat]
try:
    "5" + 5
except TypeError as e:
    print("TypeError:", e)
print(None == 0, None == "", None is None)
# --8<-- [end:galat]
