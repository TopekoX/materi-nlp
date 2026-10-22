"""Perulangan for dan while."""
teks_list = ["banjir naik", "gempa terasa", "pelatihan besok"]
for i, teks in enumerate(teks_list, start=1):
    print(i, teks, len(teks.split()))

jumlah = 0
for teks in teks_list:
    if "besok" in teks:
        continue
    jumlah += 1
print("tanpa 'besok':", jumlah)

panjang = [len(t.split()) for t in teks_list]
print(panjang)
panjang_teks = {t for t in teks_list if len(t) > 11}
print(sorted(panjang_teks))

n = 5
while n > 0:
    n -= 2
print("n akhir:", n)
for a, b in zip(["a", "b"], [1, 2]):
    print(a, b)
