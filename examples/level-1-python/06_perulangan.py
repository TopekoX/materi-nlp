"""Perulangan for dan while."""
teks_list = ["banjir naik", "gempa terasa", "pelatihan besok"]

# --8<-- [start:for]
for teks in teks_list:
    print(teks)
for i in range(3):
    print(i, end=" ")
print()
# --8<-- [end:for]

# --8<-- [start:enumerate]
for i, teks in enumerate(teks_list, start=1):
    print(i, teks, len(teks.split()))
# --8<-- [end:enumerate]

# --8<-- [start:continue]
jumlah = 0
for teks in teks_list:
    if "besok" in teks:
        continue
    jumlah += 1
print("tanpa 'besok':", jumlah)
# --8<-- [end:continue]

# --8<-- [start:break]
for teks in teks_list:
    if "gempa" in teks:
        print("ditemukan:", teks)
        break
else:
    print("tidak ada gempa")
# --8<-- [end:break]

# --8<-- [start:comprehension]
panjang = [len(t.split()) for t in teks_list]
print(panjang)
panjang_teks = {t for t in teks_list if len(t) > 11}
print(sorted(panjang_teks))
# --8<-- [end:comprehension]

# --8<-- [start:while]
n = 5
while n > 0:
    n -= 2
print("n akhir:", n)
# --8<-- [end:while]

# --8<-- [start:zip]
for a, b in zip(["a", "b"], [1, 2]):
    print(a, b)
print(list(zip([1, 2, 3], ["a"])))
# --8<-- [end:zip]

# --8<-- [start:ubah]
angka = [2, 4, 6, 8]
for x in angka:
    if x % 2 == 0:
        angka.remove(x)
print(angka)
benar = [x for x in [2, 4, 6, 8] if x % 2 != 0]
print(benar)
# --8<-- [end:ubah]
