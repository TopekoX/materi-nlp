"""Pembangun model standar untuk Level 4-5: TF-IDF + salah satu dari tiga algoritma."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from .data import RANDOM_STATE
from .preprocessing import KonfigurasiPraproses, PraprosesTeks

ALGORITMA = ("nb", "lr", "svm")


def buat_pipeline(algoritma, konfigurasi=None, vektor=None, **param_model):
    """Mengembalikan Pipeline BARU (belum dilatih): praproses -> TF-IDF -> model.

    algoritma    : 'nb' (MultinomialNB), 'lr' (LogisticRegression), atau 'svm' (LinearSVC).
    konfigurasi  : KonfigurasiPraproses; bawaan = konfigurasi dasar.
    vektor       : TfidfVectorizer siap pakai; bawaan = TfidfVectorizer() unigram.
    param_model  : parameter tambahan untuk model, menimpa nilai bawaan di bawah.
    """
    bawaan = {
        "nb": (MultinomialNB, {"alpha": 1.0}),
        "lr": (LogisticRegression, {"max_iter": 1000, "random_state": RANDOM_STATE}),
        "svm": (LinearSVC, {"random_state": RANDOM_STATE}),
    }
    if algoritma not in bawaan:
        raise ValueError(f"algoritma tidak dikenal: {algoritma!r}; pilih salah satu dari {ALGORITMA}")
    kelas, param = bawaan[algoritma]
    param = {**param, **param_model}
    return Pipeline([
        ("praproses", PraprosesTeks(konfigurasi or KonfigurasiPraproses())),
        ("tfidf", vektor or TfidfVectorizer()),
        ("model", kelas(**param)),
    ])
