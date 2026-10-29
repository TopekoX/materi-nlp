"""Neural network dasar dengan NumPy: hitungan tangan, pemeriksaan gradien, XOR, dan optimizer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np

from nlp_hub.jaringan import MLPBiner, loss_bce, periksa_gradien, relu, sigmoid
from nlp_hub.konsol import pakai_utf8

pakai_utf8()
np.set_printoptions(precision=3, suppress=True)

# --8<-- [start:tangan]
# Dua fitur: x1 = ada kata "tolong" (1/0), x2 = ada kata "bantuan" (1/0). Label y = 1 (Emergency).
x = np.array([1.0, 0.0])
W1 = np.array([[0.5, -0.4], [0.3, 0.8]])   # (2 masukan x 2 neuron tersembunyi)
b1 = np.array([0.1, -0.2])
W2 = np.array([[1.0], [-0.5]])             # (2 tersembunyi x 1 keluaran)
b2 = np.array([0.0])
y = 1.0

z1 = x @ W1 + b1
a1 = relu(z1)
z2 = a1 @ W2 + b2
p = sigmoid(z2)[0]
print("z1 =", z1, "-> a1 =", a1)
print("z2 =", z2, "-> p(Emergency) =", round(float(p), 4))
print("loss BCE =", round(loss_bce(np.array([p]), np.array([y])), 4))
# --8<-- [end:tangan]

# --8<-- [start:mundur_tangan]
dz2 = p - y                         # turunan loss terhadap z2 (BCE + sigmoid)
dW2 = a1.reshape(-1, 1) * dz2       # turunan terhadap W2
da1 = dz2 * W2.ravel()              # dikirim mundur ke lapisan tersembunyi
dz1 = da1 * (z1 > 0)                # ReLU memblokir neuron yang z1-nya <= 0
dW1 = np.outer(x, dz1)              # turunan terhadap W1
print("dz2 =", round(float(dz2), 4))
print("dW2 =", dW2.ravel())
print("dz1 =", dz1)
print("dW1 =\n", dW1)
# --8<-- [end:mundur_tangan]

# --8<-- [start:periksa]
rng = np.random.default_rng(0)
X_kecil = rng.normal(size=(6, 5))
y_kecil = np.array([0, 1, 0, 1, 1, 0])
model = MLPBiner(n_masuk=5, n_tersembunyi=4, l2=0.01, seed=1)
selisih = periksa_gradien(model, X_kecil, y_kecil)
print(f"selisih relatif terbesar gradien analitik vs numerik: {selisih:.2e}")
print("lolos (< 1e-6):", selisih < 1e-6)
# --8<-- [end:periksa]

# --8<-- [start:xor]
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y_xor = np.array([0, 1, 1, 0])
from sklearn.linear_model import LogisticRegression

linear = LogisticRegression().fit(X_xor, y_xor)
print("regresi logistik, akurasi XOR:", linear.score(X_xor, y_xor))
jaringan = MLPBiner(n_masuk=2, n_tersembunyi=8, seed=3)
riwayat = jaringan.latih(X_xor, y_xor, epoch=500, lr=0.05, optimizer="adam", ukuran_batch=4)
print("MLP, prediksi XOR:", jaringan.prediksi(X_xor), "| benar:", y_xor)
print("MLP, akurasi XOR:", float((jaringan.prediksi(X_xor) == y_xor).mean()))
print(f"loss awal {riwayat['loss_latih'][0]:.3f} -> loss akhir {riwayat['loss_latih'][-1]:.4f}")
# --8<-- [end:xor]

# --8<-- [start:optimizer]
for nama, lr in (("sgd", 0.05), ("sgd", 0.5), ("adam", 0.05)):
    m = MLPBiner(n_masuk=2, n_tersembunyi=8, seed=3)
    r = m.latih(X_xor, y_xor, epoch=200, lr=lr, optimizer=nama, ukuran_batch=4)
    print(f"{nama:4} lr={lr:<4} loss epoch 1: {r['loss_latih'][0]:.3f} | epoch 50: {r['loss_latih'][49]:.3f} | epoch 200: {r['loss_latih'][-1]:.3f}")
# --8<-- [end:optimizer]
