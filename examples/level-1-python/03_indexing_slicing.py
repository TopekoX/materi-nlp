"""Indexing dan slicing."""
# --8<-- [start:indeks]
teks = "banjir bandang"
print(len(teks))
print(teks[0], teks[-1], repr(teks[6]))
# --8<-- [end:indeks]

# --8<-- [start:slice]
print(teks[0:6])
print(teks[7:])
print(teks[:3] + "...")
print(teks[::-1])
# --8<-- [end:slice]

# --8<-- [start:daftar]
kata = teks.split()
print(kata[0], kata[-1], kata[::-1])
# --8<-- [end:daftar]

# --8<-- [start:batas]
try:
    print(teks[100])
except IndexError as e:
    print("IndexError:", e)
print(repr(teks[100:105]), teks[100:105] == "")
# --8<-- [end:batas]

# --8<-- [start:langkah]
print(list(range(10))[::3])
print(teks[0:6:2])
# --8<-- [end:langkah]
