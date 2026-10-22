"""Indexing dan slicing."""
teks = "banjir bandang"
print(teks[0], teks[-1])
print(teks[0:6])
print(teks[7:])
print(teks[::-1])
kata = teks.split()
print(kata[0], kata[-1], kata[::-1])
print(teks[:3] + "...")
try:
    print(teks[100])
except IndexError as e:
    print("IndexError:", e)
print(teks[100:105] == "")
