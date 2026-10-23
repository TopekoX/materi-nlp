"""List, tuple, set, dictionary."""
# --8<-- [start:list]
kata = ["banjir", "tolong", "banjir", "evakuasi"]
print(kata, len(kata))
kata.append("air")
print(kata)
kata[1] = "mohon"
print(kata, kata.count("banjir"))
# --8<-- [end:list]

# --8<-- [start:tuple]
koordinat = (-6.2, 106.8)   # tuple: tidak bisa diubah
lat, lon = koordinat
print(lat, lon)
try:
    koordinat[0] = 0
except TypeError as e:
    print("TypeError:", e)
# --8<-- [end:tuple]

# --8<-- [start:set]
unik = set(kata)
print(sorted(unik), len(unik))
print({"banjir", "gempa"} & {"banjir", "longsor"})
print("air" in unik)
# --8<-- [end:set]

# --8<-- [start:dict]
laporan = {"teks": "banjir di Jl. Melati", "label": "Emergency", "korban": 3}
print(laporan["label"], laporan.get("lokasi", "tidak diketahui"))
laporan["lokasi"] = "Jakarta"
print(list(laporan.keys()))
try:
    laporan["waktu"]
except KeyError as e:
    print("KeyError:", e)
# --8<-- [end:dict]

# --8<-- [start:frekuensi]
frekuensi = {}
for k in kata:
    frekuensi[k] = frekuensi.get(k, 0) + 1
print(frekuensi)
# --8<-- [end:frekuensi]

# --8<-- [start:alias]
a = ["x"]
b = a
b.append("y")
print(a, a is b)
c = a.copy()
c.append("z")
print(a, c)
# --8<-- [end:alias]
