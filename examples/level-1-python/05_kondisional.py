"""Kondisional if/elif/else."""
# --8<-- [start:tingkat]
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
# --8<-- [end:tingkat]

# --8<-- [start:logika]
teks = "tolong banjir"
print("tolong" in teks, "banjir" in teks, "gempa" in teks)
if "tolong" in teks and "banjir" in teks:
    print("mengandung permintaan bantuan banjir")
if "gempa" in teks or "banjir" in teks:
    print("terkait bencana")
print(not ("gempa" in teks))
# --8<-- [end:logika]

# --8<-- [start:ternary]
label = "Emergency" if "tolong" in teks else "Non-Emergency"
print(label)
# --8<-- [end:ternary]

# --8<-- [start:truthy]
print(bool(""), bool("a"), bool([]), bool(0), bool(None))
# --8<-- [end:truthy]

# --8<-- [start:urutan]
def tingkat_salah(tinggi_air_cm):
    if tinggi_air_cm > 0:
        return "waspada"
    elif tinggi_air_cm >= 50:
        return "siaga 2"
    return "aman"


print(tingkat_salah(120), tingkat(120))
# --8<-- [end:urutan]
