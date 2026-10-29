"""Uji embedding berbasis hitungan (Level 6)."""
import numpy as np
import pytest

from nlp_hub.embedding import (
    bangun_kosakata, embedding_svd, kosinus, matriks_koterjadian, ngram_karakter, ppmi, tetangga_terdekat,
    vektor_subword,
)

TOKEN = [["air", "naik", "banjir"], ["banjir", "air", "naik"], ["gempa", "retak"], ["gempa", "retak", "tembok"]]


def test_kosakata_menyaring_kata_jarang():
    assert bangun_kosakata(TOKEN, min_hitung=2) == ["air", "banjir", "gempa", "naik", "retak"]


def test_koterjadian_simetris_dan_benar():
    kos = bangun_kosakata(TOKEN, 2)
    C = matriks_koterjadian(TOKEN, kos, jendela=1)
    assert np.allclose(C, C.T)
    assert C[kos.index("gempa"), kos.index("retak")] == 2
    assert C[kos.index("gempa"), kos.index("air")] == 0


def test_ppmi_tidak_negatif_dan_berhingga():
    kos = bangun_kosakata(TOKEN, 2)
    P = ppmi(matriks_koterjadian(TOKEN, kos, 2))
    assert (P >= 0).all() and np.isfinite(P).all()


def test_bentuk_embedding_dan_kemiripan():
    kos = bangun_kosakata(TOKEN, 2)
    E = embedding_svd(ppmi(matriks_koterjadian(TOKEN, kos, 2)), dimensi=3)
    assert E.shape == (len(kos), 3)
    assert kosinus(E[0], E[0]) == pytest.approx(1.0)


def test_kosinus_vektor_nol_aman():
    assert kosinus(np.zeros(3), np.ones(3)) == 0.0


def test_tetangga_kata_di_luar_kosakata_menimbulkan_galat():
    kos = bangun_kosakata(TOKEN, 2)
    with pytest.raises(ValueError):          # list.index menimbulkan ValueError
        tetangga_terdekat("tsunami", kos, np.eye(len(kos)))


def test_ngram_karakter_memuat_batas_kata():
    assert ngram_karakter("air", 3, 3) == ["<ai", "air", "ir>"]


def test_subword_menangani_kata_di_luar_kosakata():
    kos = ["banjir", "gempa"]
    E = np.array([[1.0, 0.0], [0.0, 1.0]])
    v, dipakai = vektor_subword("banjirnya", kos, E)
    assert dipakai[0] == "banjir" and kosinus(v, E[0]) > 0.7
    v0, kosong = vektor_subword("xyz", kos, E)
    assert kosong == [] and not v0.any()
