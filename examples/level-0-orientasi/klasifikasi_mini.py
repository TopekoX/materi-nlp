"""Klasifikator pencacah kata paling sederhana (ILUSTRATIF, bukan eksperimen).

Hanya memakai pustaka standar Python. Data latih sengaja sangat kecil agar
seluruh perhitungan bisa diikuti dengan tangan.
"""
from collections import Counter

DATA_LATIH = [
    ("banjir setinggi dada mohon evakuasi", "Emergency"),
    ("rumah terbakar tolong kirim bantuan", "Emergency"),
    ("korban tertimpa reruntuhan butuh ambulans", "Emergency"),
    ("jalan sudah bersih setelah banjir kemarin", "Non-Emergency"),
    ("pelatihan mitigasi gempa akan digelar besok", "Non-Emergency"),
    ("berita bmkg gempa kemarin sudah dilaporkan", "Non-Emergency"),
]


def latih(data):
    """Menghitung frekuensi kata per kelas."""
    hitung = {}
    for teks, label in data:
        hitung.setdefault(label, Counter()).update(teks.split())
    return hitung


def prediksi(teks, hitung):
    """Memberi skor tiap kelas = jumlah kemunculan kata teks pada data latih kelas itu."""
    skor = {label: sum(c[kata] for kata in teks.split()) for label, c in hitung.items()}
    terbaik = max(skor, key=skor.get)
    return terbaik, skor


if __name__ == "__main__":
    model = latih(DATA_LATIH)
    for teks in ["tolong evakuasi banjir", "pelatihan mitigasi besok", "halo apa kabar"]:
        label, skor = prediksi(teks, model)
        print(f"{teks!r} -> {label} {skor}")
