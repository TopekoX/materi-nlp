"""Attention, self-attention, positional encoding, multi-head, dan mask dengan NumPy."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np

from nlp_hub.atensi import (
    atensi_titik_skala, mask_kausal, multi_head, positional_encoding, self_attention, softmax,
)
from nlp_hub.konsol import pakai_utf8

pakai_utf8()
np.set_printoptions(precision=3, suppress=True, linewidth=110)

# --8<-- [start:softmax]
skor = np.array([2.0, 1.0, 0.1])
print("skor mentah     :", skor)
print("softmax         :", softmax(skor), "| jumlah =", float(softmax(skor).sum()))
print("softmax(skor*5) :", softmax(skor * 5), "(skor diperbesar -> perhatian makin tajam)")
# --8<-- [end:softmax]

# --8<-- [start:tangan]
# Tiga kata, vektor 2 dimensi dipilih tangan agar mudah dibaca. Q = K = V = X (self-attention tanpa proyeksi).
kata = ["tolong", "air", "masuk"]
X = np.array([[1.0, 0.0], [0.8, 0.6], [0.0, 1.0]])
keluaran, bobot = atensi_titik_skala(X, X, X)
print("bobot perhatian (baris = kata yang bertanya, kolom = kata yang dilihat):")
for k, baris in zip(kata, bobot):
    print(f"  {k:7}", baris, "| jumlah baris =", round(float(baris.sum()), 3))
print("keluaran 'air' = campuran vektor tertimbang:", keluaran[1])
print("cek manual     :", bobot[1] @ X)
# --8<-- [end:tangan]

# --8<-- [start:proyeksi]
rng = np.random.default_rng(11)
T, d_model = 4, 8
X4 = rng.normal(size=(T, d_model))
Wq, Wk, Wv = (rng.normal(scale=0.4, size=(d_model, d_model)) for _ in range(3))
keluaran, bobot = self_attention(X4, Wq, Wk, Wv)
print("masukan  X:", X4.shape, "-> keluaran:", keluaran.shape, "| bobot:", bobot.shape)
print("jumlah tiap baris bobot:", bobot.sum(axis=1))
# --8<-- [end:proyeksi]

# --8<-- [start:mask]
_, bobot_kausal = self_attention(X4, Wq, Wk, Wv, mask=mask_kausal(T))
print("bobot dengan mask kausal (posisi t tidak boleh melihat masa depan):")
print(bobot_kausal)
print("semua bobot di atas diagonal = 0:", bool(np.allclose(np.triu(bobot_kausal, k=1), 0)))
# --8<-- [end:mask]

# --8<-- [start:posisi]
pe = positional_encoding(T=6, d_model=8)
print("bentuk PE:", pe.shape)
print("PE posisi 0:", pe[0])
print("PE posisi 1:", pe[1])
# Self-attention tanpa posisi tidak peduli urutan: mengacak kata hanya mengacak keluaran.
acak = [2, 0, 3, 1]
k1, _ = self_attention(X4, Wq, Wk, Wv)
k2, _ = self_attention(X4[acak], Wq, Wk, Wv)
print("tanpa posisi: keluaran kata yang diacak = keluaran asli yang diacak:", bool(np.allclose(k1[acak], k2)))
p = positional_encoding(T, d_model)
k3, _ = self_attention(X4 + p, Wq, Wk, Wv)
k4, _ = self_attention(X4[acak] + p, Wq, Wk, Wv)
print("dengan posisi: sifat itu hilang (urutan kini berpengaruh):", not bool(np.allclose(k3[acak], k4)))
# --8<-- [end:posisi]

# --8<-- [start:multihead]
Wo = rng.normal(scale=0.4, size=(d_model, d_model))
keluaran, bobot_kepala = multi_head(X4, Wq, Wk, Wv, Wo, n_kepala=2)
print("keluaran multi-head:", keluaran.shape, "| bobot per kepala:", bobot_kepala.shape, "(kepala, T, T)")
print("kepala 0 vs kepala 1 berbeda pola:", not bool(np.allclose(bobot_kepala[0], bobot_kepala[1])))
try:
    multi_head(X4, Wq, Wk, Wv, Wo, n_kepala=3)
except ValueError as e:
    print("galat yang diharapkan:", e)
# --8<-- [end:multihead]

# --8<-- [start:biaya]
for T in (64, 128, 256):
    print(f"panjang urutan T={T:3}: matriks perhatian {T}x{T} = {T * T:6} bobot per kepala per lapis")
# --8<-- [end:biaya]
