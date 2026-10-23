"""Fitur buatan tangan untuk teks kebencanaan (pelajaran Level 3).

Semua fungsi TANPA STATE: nilai satu teks tidak bergantung pada teks lain.
Daftar kata isyarat di bawah adalah HEURISTIK buatan penulis, bukan temuan ilmiah.
"""
import re

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from .preprocessing import (
    KonfigurasiPraproses, POLA_EMOJI, POLA_MENTION, POLA_URL, POLA_WAKTU, normalisasi_lokasi, praproses_token,
)

KATA_PERMINTAAN = frozenset({"tolong", "mohon", "butuh", "bantu", "bantuan", "segera", "evakuasi"})
KATA_BARU_TERJADI = frozenset({"barusan", "tadi", "sekarang", "masih", "sedang"})
KATA_LAMPAU = frozenset({"kemarin", "lalu", "semalam", "tahun", "bulan", "minggu"})
KATA_NEGASI_FITUR = frozenset({"tidak", "bukan", "belum", "jangan"})

NAMA_FITUR = [
    "n_karakter", "n_token", "rasio_kapital", "n_seru", "n_tanya", "ada_url", "ada_mention",
    "n_hashtag", "n_emoji", "ada_angka", "ada_waktu", "ada_lokasi",
    "kata_permintaan", "kata_baru_terjadi", "kata_lampau", "ada_negasi",
]


def fitur_tangan(teks):
    """Mengembalikan kamus 16 fitur numerik untuk satu teks mentah."""
    if not isinstance(teks, str):
        raise TypeError(f"teks harus str, bukan {type(teks).__name__}")
    huruf = [c for c in teks if c.isalpha()]
    token = set(praproses_token(teks, KonfigurasiPraproses()))
    kecil = teks.lower()
    return {
        "n_karakter": len(teks),
        "n_token": len(praproses_token(teks, KonfigurasiPraproses())),
        "rasio_kapital": (sum(c.isupper() for c in huruf) / len(huruf)) if huruf else 0.0,
        "n_seru": teks.count("!"),
        "n_tanya": teks.count("?"),
        "ada_url": int(bool(POLA_URL.search(teks))),
        "ada_mention": int(bool(POLA_MENTION.search(teks))),
        "n_hashtag": len(re.findall(r"#\w+", teks)),
        "n_emoji": len(POLA_EMOJI.findall(teks)),
        "ada_angka": int(any(c.isdigit() for c in teks)),
        "ada_waktu": int(bool(POLA_WAKTU.search(kecil))),
        "ada_lokasi": int("tok_lokasi" in normalisasi_lokasi(kecil).split()),
        "kata_permintaan": int(bool(token & KATA_PERMINTAAN)),
        "kata_baru_terjadi": int(bool(token & KATA_BARU_TERJADI)),
        "kata_lampau": int(bool(token & KATA_LAMPAU)),
        "ada_negasi": int(bool(token & KATA_NEGASI_FITUR)),
    }


class FiturTangan(BaseEstimator, TransformerMixin):
    """Pembungkus scikit-learn: teks -> matriks 16 fitur. Tanpa state."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([[fitur_tangan(t)[nama] for nama in NAMA_FITUR] for t in X], dtype=float)

    def get_feature_names_out(self, input_features=None):
        return np.array(NAMA_FITUR)


def tabel_fitur(teks_seri):
    """DataFrame fitur untuk deret teks (praktis untuk analisis per kelas)."""
    return pd.DataFrame([fitur_tangan(t) for t in teks_seri], index=getattr(teks_seri, "index", None))
