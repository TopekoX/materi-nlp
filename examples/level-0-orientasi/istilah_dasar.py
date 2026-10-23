"""Dataset, fitur, label, training, dan inference dalam satu contoh kecil (ILUSTRATIF).

Aturan "model" di sini sengaja dibuat sangat sederhana. Data sintetis, bukan eksperimen.
"""

# --8<-- [start:data]
# Dataset: kumpulan contoh. Tiap contoh = (teks, label).
dataset = [
    ("banjir setinggi dada mohon evakuasi", "Emergency"),
    ("rumah terbakar tolong kirim bantuan", "Emergency"),
    ("jalan sudah bersih setelah banjir kemarin", "Non-Emergency"),
    ("pelatihan mitigasi gempa besok", "Non-Emergency"),
]
print(len(dataset), dataset[0])
# --8<-- [end:data]


# --8<-- [start:fitur]
# Fitur sederhana: jumlah kata dan apakah ada kata "tolong"/"mohon".
def ekstrak_fitur(teks):
    kata = teks.split()
    return {
        "jumlah_kata": len(kata),
        "ada_permintaan": int("tolong" in kata or "mohon" in kata),
    }


print(ekstrak_fitur("tolong kirim bantuan"))
# --8<-- [end:fitur]


# --8<-- [start:xy]
# Pisahkan X (fitur) dan y (label).
X = [ekstrak_fitur(teks) for teks, _ in dataset]
y = [label for _, label in dataset]
print("X[0] =", X[0])
print("y    =", y)
# --8<-- [end:xy]


# --8<-- [start:latih]
# "Training": aturan sangat sederhana yang dipelajari dari data latih.
# Model = label yang paling sering muncul bersama ada_permintaan == 1.
dari_permintaan = [label for fitur, label in zip(X, y) if fitur["ada_permintaan"]]
model = max(set(dari_permintaan), key=dari_permintaan.count)
print("dari_permintaan =", dari_permintaan)
print("model =", model)
# --8<-- [end:latih]


# --8<-- [start:prediksi]
# Inference: memakai model pada teks baru.
def prediksi(teks):
    return model if ekstrak_fitur(teks)["ada_permintaan"] else "Non-Emergency"


for teks in ["tolong ada kebakaran di pasar", "berita gempa hari ini"]:
    print(f"{teks!r} -> {prediksi(teks)}")
# --8<-- [end:prediksi]


# --8<-- [start:uji]
# Data uji: contoh yang TIDAK dipakai saat training.
data_uji = [
    ("mohon bantuan air naik cepat", "Emergency"),
    ("tolong follow akun saya", "Non-Emergency"),
    ("gempa terasa kuat warga menjauhi bangunan rusak", "Emergency"),
    ("saya membaca berita gempa tahun lalu", "Non-Emergency"),
]


def akurasi(data):
    benar = sum(prediksi(teks) == label for teks, label in data)
    return benar / len(data)


print("akurasi data latih:", akurasi(dataset))
print("akurasi data uji  :", akurasi(data_uji))
for teks, label in data_uji:
    print(f"{teks!r}: asli={label}, prediksi={prediksi(teks)}")
# --8<-- [end:uji]
