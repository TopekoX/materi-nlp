"""Klasifikator pencacah kata paling sederhana (ILUSTRATIF, bukan eksperimen).

Hanya memakai pustaka standar Python. Data latih sengaja sangat kecil agar
seluruh perhitungan bisa diikuti dengan tangan.
"""
from collections import Counter

# --8<-- [start:data]
DATA_LATIH = [
    ("banjir setinggi dada mohon evakuasi", "Emergency"),
    ("rumah terbakar tolong kirim bantuan", "Emergency"),
    ("korban tertimpa reruntuhan butuh ambulans", "Emergency"),
    ("jalan sudah bersih setelah banjir kemarin", "Non-Emergency"),
    ("pelatihan mitigasi gempa akan digelar besok", "Non-Emergency"),
    ("berita bmkg gempa kemarin sudah dilaporkan", "Non-Emergency"),
]
# --8<-- [end:data]


# --8<-- [start:latih]
def latih(data):
    """Menghitung frekuensi kata per kelas."""
    hitung = {}
    for teks, label in data:
        hitung.setdefault(label, Counter()).update(teks.split())
    return hitung
# --8<-- [end:latih]


# --8<-- [start:prediksi]
def prediksi(teks, hitung):
    """Memberi skor tiap kelas = jumlah kemunculan kata teks pada data latih kelas itu."""
    skor = {label: sum(c[kata] for kata in teks.split()) for label, c in hitung.items()}
    terbaik = max(skor, key=skor.get)
    return terbaik, skor
# --8<-- [end:prediksi]


# --8<-- [start:model]
model = latih(DATA_LATIH)
print(sorted(model))
print(model["Emergency"]["banjir"], model["Non-Emergency"]["banjir"], model["Emergency"]["pelatihan"])
print(sum(model["Emergency"].values()), sum(model["Non-Emergency"].values()))
# --8<-- [end:model]

# --8<-- [start:langkah]
teks = "tolong evakuasi banjir"
for kata in teks.split():
    print(kata, {label: c[kata] for label, c in model.items()})
# --8<-- [end:langkah]

# --8<-- [start:uji]
for teks in ["tolong evakuasi banjir", "pelatihan mitigasi besok", "halo apa kabar"]:
    label, skor = prediksi(teks, model)
    print(f"{teks!r} -> {label} {skor}")
# --8<-- [end:uji]


# --8<-- [start:perbaikan]
def prediksi_hati_hati(teks, hitung):
    label, skor = prediksi(teks, hitung)
    if len(set(skor.values())) == 1:
        return "Tidak yakin", skor
    return label, skor


print(prediksi_hati_hati("halo apa kabar", model)[0], prediksi_hati_hati("tolong evakuasi banjir", model)[0])
# --8<-- [end:perbaikan]
