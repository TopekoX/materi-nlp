"""Uji RNN/LSTM/GRU/attention NumPy (Level 6)."""
import numpy as np
import pytest

from nlp_hub.atensi import (
    atensi_titik_skala, jalankan_urutan, langkah_gru, langkah_lstm, langkah_rnn, mask_kausal, multi_head,
    positional_encoding, self_attention, softmax,
)

RNG = np.random.default_rng(0)


def test_softmax_jumlah_satu_dan_stabil():
    s = softmax(np.array([[1000.0, 1001.0, 999.0]]))
    assert np.isfinite(s).all() and s.sum() == pytest.approx(1.0)


def test_rnn_keluaran_dalam_rentang_tanh():
    Wx, Wh = RNG.normal(size=(3, 4)), RNG.normal(size=(4, 4))
    h = jalankan_urutan(lambda x, h: langkah_rnn(x, h, Wx, Wh, 0), RNG.normal(size=(5, 3)) * 10, np.zeros(4))
    assert h.shape == (5, 4) and np.abs(h).max() <= 1.0


def test_lstm_gerbang_dalam_0_1_dan_bentuk():
    W, b = RNG.normal(size=(3 + 4, 16)), np.zeros(16)
    h, c, g = langkah_lstm(RNG.normal(size=3), np.zeros(4), np.zeros(4), W, b)
    assert h.shape == c.shape == (4,)
    assert all(((v > 0) & (v < 1)).all() for k, v in g.items() if k != "g")


def test_lstm_gerbang_lupa_dan_masuk_nol_menghapus_memori():
    d = 4
    W, b = np.zeros((3 + d, 4 * d)), np.zeros(4 * d)
    b[:d] = -50.0                                   # gerbang lupa ~ 0
    b[d:2 * d] = -50.0                              # gerbang masuk ~ 0
    _, c, _ = langkah_lstm(np.zeros(3), np.zeros(d), np.ones(d) * 5, W, b)
    assert np.allclose(c, 0, atol=1e-6)


def test_gru_gerbang_pembaruan_nol_mempertahankan_keadaan():
    d = 4
    Z = np.zeros((3 + d, d))
    h0 = np.linspace(-0.5, 0.5, d)
    h, _ = langkah_gru(np.ones(3), h0, Z, Z, Z, np.full(d, -50.0), np.zeros(d), np.zeros(d))
    assert np.allclose(h, h0, atol=1e-6)


def test_atensi_baris_berjumlah_satu_dan_bentuk():
    Q, K, V = RNG.normal(size=(3, 4)), RNG.normal(size=(5, 4)), RNG.normal(size=(5, 6))
    o, w = atensi_titik_skala(Q, K, V)
    assert o.shape == (3, 6) and w.shape == (3, 5) and np.allclose(w.sum(axis=1), 1)


def test_mask_kausal_nol_di_atas_diagonal():
    X = RNG.normal(size=(4, 8))
    W = [RNG.normal(size=(8, 8)) for _ in range(3)]
    _, w = self_attention(X, *W, mask=mask_kausal(4))
    assert np.allclose(np.triu(w, 1), 0) and np.allclose(w.sum(axis=1), 1)


def test_self_attention_ekuivarian_permutasi_tanpa_posisi():
    X = RNG.normal(size=(4, 8))
    W = [RNG.normal(size=(8, 8)) for _ in range(3)]
    acak = [2, 0, 3, 1]
    assert np.allclose(self_attention(X, *W)[0][acak], self_attention(X[acak], *W)[0])


def test_posisi_membuat_urutan_berpengaruh():
    X = RNG.normal(size=(4, 8))
    W = [RNG.normal(size=(8, 8)) for _ in range(3)]
    p = positional_encoding(4, 8)
    acak = [2, 0, 3, 1]
    assert not np.allclose(self_attention(X + p, *W)[0][acak], self_attention(X[acak] + p, *W)[0])


def test_positional_encoding_nilai_dan_galat():
    pe = positional_encoding(3, 4)
    assert np.allclose(pe[0], [0, 1, 0, 1]) and pe[1, 0] == pytest.approx(np.sin(1.0))
    with pytest.raises(ValueError):
        positional_encoding(3, 5)


def test_multi_head_bentuk_dan_galat_pembagian():
    X = RNG.normal(size=(4, 8))
    W = [RNG.normal(size=(8, 8)) for _ in range(4)]
    o, w = multi_head(X, *W, n_kepala=2)
    assert o.shape == (4, 8) and w.shape == (2, 4, 4)
    with pytest.raises(ValueError, match="habis dibagi"):
        multi_head(X, *W, n_kepala=3)
