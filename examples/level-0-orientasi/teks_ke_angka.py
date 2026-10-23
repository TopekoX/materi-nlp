"""Teks menjadi angka dengan pencacah kata (ILUSTRATIF)."""
from collections import Counter

kalimat = ["korban tidak selamat", "selamat tidak ada korban"]

# --8<-- [start:counter]
for k in kalimat:
    print(sorted(Counter(k.split()).items()))
# --8<-- [end:counter]

# --8<-- [start:kosakata]
kosakata = sorted({kata for k in kalimat for kata in k.split()})
print(kosakata)
vektor = [[k.split().count(kata) for kata in kosakata] for k in kalimat]
for k, v in zip(kalimat, vektor):
    print(v, "<-", k)
# --8<-- [end:kosakata]

# --8<-- [start:urutan]
a = "air naik cepat"
b = "cepat naik air"
print(Counter(a.split()) == Counter(b.split()))
# --8<-- [end:urutan]

# --8<-- [start:variasi]
varian = ["tolong", "tlong", "tolooong", "TOLONG!!"]
print(len(set(varian)), len({v.lower() for v in varian}), len({v.lower().strip("!") for v in varian}))
# --8<-- [end:variasi]
