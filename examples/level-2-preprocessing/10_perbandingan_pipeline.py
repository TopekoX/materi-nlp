"""Membandingkan konfigurasi preprocessing secara empiris (pelajaran Level 2).

Pengklasifikasi (TF-IDF + Logistic Regression) hanya dipakai sebagai ALAT UKUR;
penjelasannya ada di Level 3 dan 4. Semua angka dicetak dari eksekusi nyata.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline

from nlp_hub.data import RANDOM_STATE, kodekan_label, muat_dataset, muat_uji_tangan
from nlp_hub.preprocessing import KonfigurasiPraproses, PraprosesTeks

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

# --8<-- [start:definisi]
KONFIGURASI = {
    "A dasar": KonfigurasiPraproses(),
    "B tanpa informal": KonfigurasiPraproses(informal=False, huruf_berulang=False),
    "C emoji dihapus": KonfigurasiPraproses(emoji="hapus"),
    "D hashtag dihapus": KonfigurasiPraproses(hashtag="hapus"),
    "E + tanda seru": KonfigurasiPraproses(tanda_seru=True),
    "F + angka/waktu/lokasi": KonfigurasiPraproses(angka_waktu_lokasi=True),
    "G + stopword konservatif": KonfigurasiPraproses(stopword="konservatif"),
    "H + stopword Sastrawi": KonfigurasiPraproses(stopword="sastrawi"),
    "I + negasi": KonfigurasiPraproses(negasi=True),
    "J + stemming": KonfigurasiPraproses(stem=True),
    "K + koreksi typo": KonfigurasiPraproses(typo=True),
}
# --8<-- [end:definisi]


# --8<-- [start:model]
def buat_model(konfigurasi):
    return Pipeline([
        ("praproses", PraprosesTeks(konfigurasi)),
        ("tfidf", TfidfVectorizer()),
        ("klasifikasi", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
    ])
# --8<-- [end:model]


# --8<-- [start:evaluasi]
def evaluasi(konfigurasi, df, uji_tangan):
    X, y, grup = df["text"].to_numpy(), kodekan_label(df["label"]).to_numpy(), df["event_id"]
    lipatan = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    f1_makro, recall_e = [], []
    for idx_latih, idx_uji in lipatan.split(X, y, groups=grup):
        model = buat_model(konfigurasi).fit(X[idx_latih], y[idx_latih])
        prediksi = model.predict(X[idx_uji])
        f1_makro.append(f1_score(y[idx_uji], prediksi, average="macro"))
        recall_e.append(recall_score(y[idx_uji], prediksi, pos_label=1))
    model = buat_model(konfigurasi).fit(X, y)
    y_tangan = kodekan_label(uji_tangan["label"]).to_numpy()
    p_tangan = model.predict(uji_tangan["text"].to_numpy())
    return {
        "F1 makro (CV)": f"{np.mean(f1_makro):.3f} ± {np.std(f1_makro):.3f}",
        "Recall E (CV)": f"{np.mean(recall_e):.3f} ± {np.std(recall_e):.3f}",
        "F1 makro (tulis-tangan)": round(f1_score(y_tangan, p_tangan, average="macro"), 3),
        "Recall E (tulis-tangan)": round(recall_score(y_tangan, p_tangan, pos_label=1), 3),
    }
# --8<-- [end:evaluasi]


# --8<-- [start:jalankan]
if __name__ == "__main__":
    df, uji_tangan = muat_dataset(), muat_uji_tangan()
    print(f"scikit-learn {sklearn.__version__}, seed {RANDOM_STATE}, latih/CV: {len(df)} teks, tulis-tangan: {len(uji_tangan)} teks")
    baris = {nama: evaluasi(k, df, uji_tangan) for nama, k in KONFIGURASI.items()}
    tabel = pd.DataFrame(baris).T
    print(tabel.to_string())
    hasil = Path(__file__).resolve().parent / "hasil"
    hasil.mkdir(exist_ok=True)
    tabel.to_csv(hasil / "perbandingan_pipeline.csv", encoding="utf-8")
# --8<-- [end:jalankan]
