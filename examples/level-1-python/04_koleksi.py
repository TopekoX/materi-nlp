"""List, tuple, set, dictionary."""
kata = ["banjir", "tolong", "banjir", "evakuasi"]
print(kata, len(kata))
kata.append("air")
print(kata)

koordinat = (-6.2, 106.8)   # tuple: tidak bisa diubah
lat, lon = koordinat
print(lat, lon)

unik = set(kata)
print(sorted(unik), len(unik))
print({"banjir", "gempa"} & {"banjir", "longsor"})

laporan = {"teks": "banjir di Jl. Melati", "label": "Emergency", "korban": 3}
print(laporan["label"], laporan.get("lokasi", "tidak diketahui"))
laporan["lokasi"] = "Jakarta"
print(list(laporan.keys()))

frekuensi = {}
for k in kata:
    frekuensi[k] = frekuensi.get(k, 0) + 1
print(frekuensi)
