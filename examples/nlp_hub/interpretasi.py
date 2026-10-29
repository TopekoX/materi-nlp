"""Penjelasan prediksi model linear TF-IDF (Level 7): kontribusi fitur dan oklusi kata."""
import numpy as np


def kontribusi_linear(pipeline, teks, atas=5):
    """Kontribusi tiap fitur ke skor: nilai TF-IDF x koefisien. Mengembalikan (daftar_kontribusi, intersep).

    Skor keputusan = jumlah semua kontribusi + intersep. Daftar berisi `atas` fitur dengan |kontribusi| terbesar
    sebagai (fitur, kontribusi). Berlaku untuk pipeline bernama praproses -> tfidf -> model linear.
    """
    x = pipeline.named_steps["tfidf"].transform(pipeline.named_steps["praproses"].transform([teks]))
    model = pipeline.named_steps["model"]
    nama = pipeline.named_steps["tfidf"].get_feature_names_out()
    x = x.tocoo()
    kontribusi = [(nama[j], float(v * model.coef_[0][j])) for j, v in zip(x.col, x.data)]
    kontribusi.sort(key=lambda kv: -abs(kv[1]))
    return kontribusi[:atas], float(model.intercept_[0])


def oklusi_kata(model, teks):
    """Perubahan skor keputusan bila SATU kata (dipisah spasi) dihapus. Positif = kata itu menaikkan skor.

    Metode ini hanya memakai `decision_function`, jadi berlaku untuk model apa pun, termasuk yang non-linear.
    Biayanya satu prediksi per kata.
    """
    kata = teks.split()
    dasar = float(model.decision_function([teks])[0])
    varian = [" ".join(kata[:i] + kata[i + 1:]) or "." for i in range(len(kata))]
    skor = model.decision_function(varian)
    return [(k, float(dasar - s)) for k, s in zip(kata, skor)], dasar


def cakupan_kosakata(pipeline, daftar_teks):
    """Proporsi token (setelah praproses) yang ada di kosakata TF-IDF. Rendah = banyak kata asing bagi model."""
    kosakata = set(pipeline.named_steps["tfidf"].vocabulary_)
    token = [t for s in pipeline.named_steps["praproses"].transform(daftar_teks) for t in s.split()]
    return float(np.mean([t in kosakata for t in token])) if token else 0.0
