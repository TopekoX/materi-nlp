"""Operasi string yang sering dipakai dalam NLP."""
# --8<-- [start:dasar]
teks = "  TOLONG!! Banjir di Jl. Melati, air naik cepat  "
print(repr(teks))
print(len(teks))
# --8<-- [end:dasar]

# --8<-- [start:bersihkan]
print(repr(teks.strip()))
print(teks.lower().strip())
print(len(teks.strip()))
# --8<-- [end:bersihkan]

# --8<-- [start:pecah]
print(teks.strip().split())
kata = ["banjir", "naik", "cepat"]
print(" ".join(kata))
# --8<-- [end:pecah]

# --8<-- [start:cari]
print("Jl. Melati" in teks)
print("banjir".startswith("ban"), "banjir".endswith("jir"), "banjir".find("j"), "banjir".find("z"))
print(teks.replace("!!", "!").strip())
# --8<-- [end:cari]

# --8<-- [start:fstring]
nama = "Melati"
print(f"Lokasi: {nama!r}, panjang nama: {len(nama)}")
# --8<-- [end:fstring]

# --8<-- [start:immutable]
kata_tetap = "banjir"
try:
    kata_tetap[0] = "B"
except TypeError as e:
    print("TypeError:", e)
baru = "B" + kata_tetap[1:]
print(baru, kata_tetap)
# --8<-- [end:immutable]
