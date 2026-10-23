"""Uji fungsi evaluasi bersama."""
import numpy as np
import pytest
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from nlp_hub.data import muat_dataset, muat_uji_tangan
from nlp_hub.eksperimen import evaluasi_pipeline, metrik_emergency


def test_metrik_emergency_nilai_diketahui():
    y = np.array([1, 1, 0, 0, 1])
    p = np.array([1, 0, 0, 1, 1])
    m = metrik_emergency(y, p)
    assert m["recall_e"] == pytest.approx(2 / 3)
    assert m["presisi_e"] == pytest.approx(2 / 3)
    assert m["f1_e"] == pytest.approx(2 / 3)


def test_metrik_tanpa_prediksi_positif_tidak_error():
    m = metrik_emergency(np.array([1, 0]), np.array([0, 0]))
    assert m["recall_e"] == 0.0 and m["presisi_e"] == 0.0


def test_evaluasi_pipeline_bentuk_dan_deterministik():
    def buat():
        return Pipeline([("t", TfidfVectorizer()), ("lr", LogisticRegression(max_iter=500, random_state=42))])

    df, uji = muat_dataset(), muat_uji_tangan()
    a = evaluasi_pipeline(buat, df, uji)
    b = evaluasi_pipeline(buat, df, uji)
    assert len(a["cv"]) == 5
    assert a["cv_rata"] == b["cv_rata"] and a["tangan"] == b["tangan"]
    assert 0.0 <= a["tangan"]["recall_e"] <= 1.0


def test_baseline_mayoritas_tidak_menemukan_emergency():
    def buat():
        return DummyClassifier(strategy="most_frequent")

    hasil = evaluasi_pipeline(buat, muat_dataset(), muat_uji_tangan())
    assert hasil["cv_rata"]["recall_e"] == 0.0
    assert hasil["tangan"]["recall_e"] in (0.0, 1.0)  # uji tulis-tangan seimbang: mayoritas = salah satu kelas


def test_bootstrap_cocok_dengan_metrik_sklearn_pada_resampel_yang_sama():
    from nlp_hub.eksperimen import bootstrap_metrik

    rng = np.random.RandomState(0)
    y = rng.randint(0, 2, 60)
    p = np.where(rng.rand(60) < 0.8, y, 1 - y)
    n, seed = 50, 7
    indeks = np.random.RandomState(seed).randint(0, len(y), size=(n, len(y)))
    for metrik in ("recall_e", "f1_makro"):
        diharapkan = [metrik_emergency(y[i], p[i])[metrik] for i in indeks]
        np.testing.assert_allclose(bootstrap_metrik(y, p, metrik, n=n, seed=seed), diharapkan)


def test_selisih_berpasangan_nol_untuk_model_sama_dan_selang_urut():
    from nlp_hub.eksperimen import selang_persentil, selisih_recall_bootstrap

    y = np.array([1, 1, 1, 0, 0, 1, 0, 1])
    p = np.array([1, 0, 1, 0, 1, 1, 0, 0])
    assert np.all(selisih_recall_bootstrap(y, p, p, n=100) == 0)
    lo, hi = selang_persentil(np.arange(101))
    assert lo == 2.5 and hi == 97.5


def test_bootstrap_metrik_tidak_dikenal():
    from nlp_hub.eksperimen import bootstrap_metrik

    with pytest.raises(ValueError):
        bootstrap_metrik(np.array([1, 0]), np.array([1, 0]), "auc")
