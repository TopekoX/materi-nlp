"""Kondisional if/elif/else."""


def tingkat(tinggi_air_cm):
    if tinggi_air_cm >= 100:
        return "siaga 1"
    elif tinggi_air_cm >= 50:
        return "siaga 2"
    elif tinggi_air_cm > 0:
        return "waspada"
    else:
        return "aman"


for t in [0, 20, 50, 120]:
    print(t, "->", tingkat(t))

teks = "tolong banjir"
if "tolong" in teks and "banjir" in teks:
    print("mengandung permintaan bantuan banjir")
label = "Emergency" if "tolong" in teks else "Non-Emergency"
print(label)
print(bool(""), bool("a"), bool([]), bool(0), bool(None))
