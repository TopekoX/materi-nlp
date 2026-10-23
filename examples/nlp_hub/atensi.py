"""RNN, LSTM, GRU, attention, dan positional encoding dengan NumPy (Level 6).

Semua fungsi hanya melakukan propagasi MAJU dengan bobot yang diberikan pemanggil; tidak ada pelatihan.
Tujuannya memperlihatkan hitungan di dalam sel, bukan menggantikan PyTorch.
"""
import numpy as np


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def softmax(z, sumbu=-1):
    """Softmax stabil: mengurangi nilai terbesar sebelum eksponen agar tidak overflow."""
    z = z - np.max(z, axis=sumbu, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=sumbu, keepdims=True)


# ------------------------------------------------------------------ sel rekuren
def langkah_rnn(x, h, Wx, Wh, b):
    """Satu langkah RNN sederhana: h_baru = tanh(x Wx + h Wh + b)."""
    return np.tanh(x @ Wx + h @ Wh + b)


def langkah_lstm(x, h, c, W, b):
    """Satu langkah LSTM. W: (dim_x + dim_h, 4*dim_h); b: (4*dim_h,). Urutan gerbang: lupa, masuk, kandidat, keluar.

    Mengembalikan (h_baru, c_baru, gerbang) dengan gerbang = kamus nilai f, i, g, o agar dapat diperiksa.
    """
    d = h.shape[-1]
    z = np.concatenate([x, h], axis=-1) @ W + b
    f, i, g, o = sigmoid(z[..., :d]), sigmoid(z[..., d:2 * d]), np.tanh(z[..., 2 * d:3 * d]), sigmoid(z[..., 3 * d:])
    c_baru = f * c + i * g
    h_baru = o * np.tanh(c_baru)
    return h_baru, c_baru, {"f": f, "i": i, "g": g, "o": o}


def langkah_gru(x, h, Wz, Wr, Wc, bz, br, bc):
    """Satu langkah GRU. Setiap W berbentuk (dim_x + dim_h, dim_h). Mengembalikan (h_baru, gerbang)."""
    xh = np.concatenate([x, h], axis=-1)
    z = sigmoid(xh @ Wz + bz)                                   # gerbang pembaruan
    r = sigmoid(xh @ Wr + br)                                   # gerbang reset
    kandidat = np.tanh(np.concatenate([x, r * h], axis=-1) @ Wc + bc)
    h_baru = (1 - z) * h + z * kandidat
    return h_baru, {"z": z, "r": r}


def jalankan_urutan(langkah, deret_x, h0):
    """Menjalankan fungsi `langkah(x, h) -> h` sepanjang deret_x (T, dim_x). Mengembalikan semua keadaan tersembunyi (T, dim_h)."""
    h, semua = h0, []
    for x in deret_x:
        h = langkah(x, h)
        semua.append(h)
    return np.stack(semua)


# ------------------------------------------------------------------ attention
def atensi_titik_skala(Q, K, V, mask=None):
    """Scaled dot-product attention: softmax(Q K^T / sqrt(d_k)) V.

    Q: (T_q, d_k), K: (T_k, d_k), V: (T_k, d_v). mask: boolean (T_q, T_k), True = BOLEH melihat.
    Mengembalikan (keluaran (T_q, d_v), bobot (T_q, T_k)); tiap baris bobot berjumlah 1.
    """
    skor = Q @ K.T / np.sqrt(Q.shape[-1])
    if mask is not None:
        skor = np.where(mask, skor, -1e9)
    bobot = softmax(skor, sumbu=-1)
    return bobot @ V, bobot


def mask_kausal(T):
    """Segitiga bawah: posisi t hanya boleh melihat posisi <= t (dipakai decoder)."""
    return np.tril(np.ones((T, T), dtype=bool))


def self_attention(X, Wq, Wk, Wv, mask=None):
    """Self-attention satu kepala: Q, K, V semuanya diproyeksikan dari X yang sama (T, d_model)."""
    return atensi_titik_skala(X @ Wq, X @ Wk, X @ Wv, mask)


def multi_head(X, Wq, Wk, Wv, Wo, n_kepala, mask=None):
    """Multi-head self-attention. Wq/Wk/Wv: (d_model, d_model); Wo: (d_model, d_model). d_model harus habis dibagi n_kepala."""
    T, d = X.shape
    if d % n_kepala:
        raise ValueError(f"d_model={d} tidak habis dibagi n_kepala={n_kepala}")
    dk = d // n_kepala
    keluaran, bobot = [], []
    for k in range(n_kepala):
        s = slice(k * dk, (k + 1) * dk)
        o, w = atensi_titik_skala((X @ Wq)[:, s], (X @ Wk)[:, s], (X @ Wv)[:, s], mask)
        keluaran.append(o)
        bobot.append(w)
    return np.concatenate(keluaran, axis=-1) @ Wo, np.stack(bobot)


def positional_encoding(T, d_model):
    """Sinusoidal (Vaswani dkk., 2017): PE[t, 2i] = sin(t / 10000^(2i/d)), PE[t, 2i+1] = cos(...). d_model harus genap."""
    if d_model % 2:
        raise ValueError("d_model harus genap")
    t = np.arange(T)[:, None]
    i = np.arange(d_model // 2)[None, :]
    sudut = t / np.power(10000.0, 2 * i / d_model)
    pe = np.zeros((T, d_model))
    pe[:, 0::2], pe[:, 1::2] = np.sin(sudut), np.cos(sudut)
    return pe
