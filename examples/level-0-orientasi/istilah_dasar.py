"""Dataset, fitur, label, training, dan inference dalam satu contoh kecil (ILUSTRATIF)."""

# Dataset: kumpulan contoh. Tiap contoh = (teks, label).
dataset = [
    ("banjir setinggi dada mohon evakuasi", "Emergency"),
    ("rumah terbakar tolong kirim bantuan", "Emergency"),
    ("jalan sudah bersih setelah banjir kemarin", "Non-Emergency"),
    ("pelatihan mitigasi gempa besok", "Non-Emergency"),
]

# Fitur sederhana: panjang teks (jumlah kata) dan apakah ada kata "tolong"/"mohon".
def ekstrak_fitur(teks):
    kata = teks.split()
    return {
        "jumlah_kata": len(kata),
        "ada_permintaan": int("tolong" in kata or "mohon" in kata),
    }

# Pisahkan X (fitur) dan y (label).
X = [ekstrak_fitur(teks) for teks, _ in dataset]
y = [label for _, label in dataset]

# "Training": aturan sangat sederhana yang dipelajari dari data latih.
# Model = label yang paling sering muncul bersama ada_permintaan == 1.
dari_permintaan = [label for fitur, label in zip(X, y) if fitur["ada_permintaan"]]
model = max(set(dari_permintaan), key=dari_permintaan.count)

# Inference: memakai model pada teks baru.
def prediksi(teks):
    return model if ekstrak_fitur(teks)["ada_permintaan"] else "Non-Emergency"

if __name__ == "__main__":
    print("X[0] =", X[0])
    print("y    =", y)
    print("model =", model)
    for teks in ["tolong ada kebakaran di pasar", "berita gempa hari ini"]:
        print(f"{teks!r} -> {prediksi(teks)}")
