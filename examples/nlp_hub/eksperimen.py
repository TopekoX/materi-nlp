"""Evaluasi eksperimen yang konsisten untuk Level 2-5.

Satu fungsi, satu protokol: validasi silang berkelompok per `event_id`
(StratifiedGroupKFold) pada data latih sintetis, lalu satu model pada seluruh data
diuji pada set tulis-tangan. Model DIBUAT BARU pada tiap lipatan.
"""
import time

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedGroupKFold

from .data import RANDOM_STATE, kodekan_label


def metrik_emergency(y_benar, y_pred):
    """Metrik kelas Emergency (1) dan F1 makro untuk satu pasang label."""
    return {
        "akurasi": accuracy_score(y_benar, y_pred),
        "f1_makro": f1_score(y_benar, y_pred, average="macro"),
        "presisi_e": precision_score(y_benar, y_pred, pos_label=1, zero_division=0),
        "recall_e": recall_score(y_benar, y_pred, pos_label=1, zero_division=0),
        "f1_e": f1_score(y_benar, y_pred, pos_label=1, zero_division=0),
    }


def evaluasi_pipeline(buat_model, df, uji_tangan, n_lipatan=5, seed=RANDOM_STATE, kolom_grup="event_id"):
    """Menjalankan protokol evaluasi dan mengembalikan kamus ringkasan.

    buat_model : fungsi tanpa argumen yang mengembalikan model BARU (belum dilatih).
    Kunci hasil: `cv` (daftar metrik per lipatan), `cv_rata`, `cv_std`, `tangan` (metrik
    set tulis-tangan), `detik_latih` (waktu melatih satu model pada seluruh data).
    """
    X, y = df["text"].to_numpy(), kodekan_label(df["label"]).to_numpy()
    pembagi = StratifiedGroupKFold(n_splits=n_lipatan, shuffle=True, random_state=seed)
    per_lipatan = []
    for i_latih, i_uji in pembagi.split(X, y, groups=df[kolom_grup]):
        model = buat_model().fit(X[i_latih], y[i_latih])
        per_lipatan.append(metrik_emergency(y[i_uji], model.predict(X[i_uji])))
    kunci = per_lipatan[0].keys()
    mulai = time.perf_counter()
    model = buat_model().fit(X, y)
    detik = time.perf_counter() - mulai
    tangan = metrik_emergency(kodekan_label(uji_tangan["label"]).to_numpy(), model.predict(uji_tangan["text"].to_numpy()))
    return {
        "cv": per_lipatan,
        "cv_rata": {k: float(np.mean([m[k] for m in per_lipatan])) for k in kunci},
        "cv_std": {k: float(np.std([m[k] for m in per_lipatan])) for k in kunci},
        "tangan": tangan,
        "detik_latih": detik,
        "model": model,
    }


def _hitungan_bootstrap(y, p, indeks):
    """TP, TN, FP, FN untuk setiap baris `indeks` (matriks n_resampel x N), secara vektor."""
    yy, pp = y[indeks], p[indeks]
    tp = ((yy == 1) & (pp == 1)).sum(axis=1)
    tn = ((yy == 0) & (pp == 0)).sum(axis=1)
    fp = ((yy == 0) & (pp == 1)).sum(axis=1)
    fn = ((yy == 1) & (pp == 0)).sum(axis=1)
    return tp, tn, fp, fn


def _bagi(a, b):
    """Pembagian aman: 0 bila penyebut 0 (sama dengan zero_division=0 pada scikit-learn)."""
    return np.divide(a, b, out=np.zeros(np.shape(a), dtype=float), where=np.asarray(b) > 0)


def bootstrap_metrik(y, p, metrik, n=2000, seed=RANDOM_STATE):
    """Nilai metrik pada `n` resampel bootstrap (pengambilan dengan pengembalian). metrik: 'recall_e' | 'f1_makro'."""
    y, p = np.asarray(y), np.asarray(p)
    indeks = np.random.RandomState(seed).randint(0, len(y), size=(n, len(y)))
    tp, tn, fp, fn = _hitungan_bootstrap(y, p, indeks)
    if metrik == "recall_e":
        return _bagi(tp, tp + fn)
    if metrik == "f1_makro":
        return (_bagi(2 * tp, 2 * tp + fp + fn) + _bagi(2 * tn, 2 * tn + fp + fn)) / 2
    raise ValueError(f"metrik tidak dikenal: {metrik!r}")


def selisih_recall_bootstrap(y, p_a, p_b, n=2000, seed=RANDOM_STATE):
    """Selisih recall Emergency (A - B) pada resampel bootstrap BERPASANGAN (indeks sama untuk A dan B)."""
    y, p_a, p_b = np.asarray(y), np.asarray(p_a), np.asarray(p_b)
    indeks = np.random.RandomState(seed).randint(0, len(y), size=(n, len(y)))
    tp_a, _, _, fn_a = _hitungan_bootstrap(y, p_a, indeks)
    tp_b, _, _, fn_b = _hitungan_bootstrap(y, p_b, indeks)
    return _bagi(tp_a, tp_a + fn_a) - _bagi(tp_b, tp_b + fn_b)


def selang_persentil(nilai, tingkat=95):
    """Selang persentil dua sisi, mis. [2,5; 97,5] untuk tingkat 95."""
    sisa = (100 - tingkat) / 2
    return tuple(np.percentile(nilai, [sisa, 100 - sisa]))
