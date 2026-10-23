"""Perbandingan adil Naive Bayes, Logistic Regression, dan Linear SVM (pelajaran Level 4).

Semua model: preprocessing dasar -> TF-IDF unigram -> algoritma, parameter bawaan dari
nlp_hub.modeling. Data, pembagian, seed, dan metrik sama untuk semua. Angka dicetak dari eksekusi nyata.
"""
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
import pandas as pd
import sklearn
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedGroupKFold

from nlp_hub.data import RANDOM_STATE, bagi_latih_val_uji, kodekan_label, muat_dataset, muat_uji_tangan
from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.modeling import buat_pipeline

warnings.filterwarnings("ignore")


# --8<-- [start:kandidat]
class BaselineKataKunci(BaseEstimator, ClassifierMixin):
    """Aturan bodoh: Emergency bila teks memuat kata 'tolong'. Tidak belajar apa pun."""

    def fit(self, X, y=None):
        self.classes_ = np.array([0, 1])
        return self

    def predict(self, X):
        return np.array([int("tolong" in t.lower()) for t in X])


KANDIDAT = {
    "Baseline: selalu Non-Emergency": lambda: DummyClassifier(strategy="most_frequent"),
    "Baseline: kata kunci 'tolong'": lambda: BaselineKataKunci(),
    "Multinomial NB": lambda: buat_pipeline("nb"),
    "Logistic Regression": lambda: buat_pipeline("lr"),
    "Linear SVM": lambda: buat_pipeline("svm"),
}
# --8<-- [end:kandidat]

df = muat_dataset()
latih, val, uji = bagi_latih_val_uji(df)
dev = pd.concat([latih, val], ignore_index=True)           # data pengembangan: latih + validasi
X_dev, y_dev = dev["text"].to_numpy(), kodekan_label(dev["label"]).to_numpy()
tangan = muat_uji_tangan()
KOLOM = ["akurasi", "presisi_e", "recall_e", "f1_e", "f1_makro"]


# --8<-- [start:cv]
def cv_dev(buat, seed):
    pembagi = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)
    hasil = []
    for i_latih, i_uji in pembagi.split(X_dev, y_dev, groups=dev["event_id"]):
        model = buat().fit(X_dev[i_latih], y_dev[i_latih])         # model BARU tiap lipatan
        hasil.append(metrik_emergency(y_dev[i_uji], model.predict(X_dev[i_uji])))
    return pd.DataFrame(hasil)


ringkas = {}
for nama, buat in KANDIDAT.items():
    t = cv_dev(buat, RANDOM_STATE)
    ringkas[nama] = {k: f"{t[k].mean():.3f} ± {t[k].std(ddof=0):.3f}" for k in KOLOM}
print(f"scikit-learn {sklearn.__version__} | seed {RANDOM_STATE} | pengembangan: {len(dev)} teks | validasi silang 5 lipatan per kejadian")
print(pd.DataFrame(ringkas).T.to_string())
# --8<-- [end:cv]


# --8<-- [start:akhir]
def uji_akhir(buat, X, y):
    model = buat().fit(X_dev, y_dev)
    pred = model.predict(X)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {**{k: round(v, 3) for k, v in metrik_emergency(y, pred).items() if k in KOLOM}, "TN": tn, "FP": fp, "FN": fn, "TP": tp}


y_uji, y_tangan = kodekan_label(uji["label"]).to_numpy(), kodekan_label(tangan["label"]).to_numpy()
KOLOM_HITUNG = {k: int for k in ["TN", "FP", "FN", "TP"]}
tabel_uji = pd.DataFrame({n: uji_akhir(b, uji["text"].to_numpy(), y_uji) for n, b in KANDIDAT.items()}).T.astype(KOLOM_HITUNG)
tabel_tangan = pd.DataFrame({n: uji_akhir(b, tangan["text"].to_numpy(), y_tangan) for n, b in KANDIDAT.items()}).T.astype(KOLOM_HITUNG)
print(f"\nUJI sintetis ({len(uji)} teks, {int(y_uji.sum())} Emergency), model dilatih pada {len(dev)} teks:")
print(tabel_uji[KOLOM + ["TN", "FP", "FN", "TP"]].to_string())
print(f"\nTULIS-TANGAN ({len(tangan)} teks, {int(y_tangan.sum())} Emergency):")
print(tabel_tangan[KOLOM + ["TN", "FP", "FN", "TP"]].to_string())
# --8<-- [end:akhir]


# --8<-- [start:stabil]
print("\nF1 makro validasi silang pada 5 seed pembagi berbeda:")
for nama, buat in list(KANDIDAT.items())[2:]:
    nilai = [cv_dev(buat, s)["f1_makro"].mean() for s in range(5)]
    print(f"{nama:22} " + " ".join(f"{v:.3f}" for v in nilai) + f"   rata-rata={np.mean(nilai):.3f} std={np.std(nilai):.3f}")
# --8<-- [end:stabil]

if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "hasil"
    out.mkdir(exist_ok=True)
    pd.DataFrame(ringkas).T.to_csv(out / "perbandingan_model_cv.csv", encoding="utf-8")
    tabel_uji.to_csv(out / "perbandingan_model_uji.csv", encoding="utf-8")
    tabel_tangan.to_csv(out / "perbandingan_model_tangan.csv", encoding="utf-8")
    waktu = {}
    for nama, buat in list(KANDIDAT.items())[2:]:
        mulai = time.perf_counter()
        buat().fit(X_dev, y_dev)
        waktu[nama] = round(time.perf_counter() - mulai, 3)
    print("\nWAKTU LATIH (detik):", waktu)
