"""Kesalahan umum saat training dan cara mengenalinya (pelajaran Level 4).

Setiap bagian memicu galat atau kesalahan sungguhan, lalu mencetak pesan aslinya.
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.preprocessing import OneHotEncoder

from nlp_hub.data import bagi_latih_val_uji, kodekan_label, muat_dataset, muat_uji_tangan
from nlp_hub.modeling import buat_pipeline

warnings.filterwarnings("ignore")
df = muat_dataset()
latih, val, uji = bagi_latih_val_uji(df)
y_latih = kodekan_label(latih["label"])


def tampil(judul, fungsi):
    try:
        fungsi()
        print(f"{judul}: tidak ada galat")
    except Exception as e:  # noqa: BLE001 (sengaja menangkap semua untuk pelajaran)
        print(f"{judul}: {type(e).__name__}: {str(e).splitlines()[0][:110]}")


# --8<-- [start:galat]
tampil("1 path salah       ", lambda: pd.read_csv("data/tidak_ada.csv"))
tampil("2 kolom salah      ", lambda: df["teks"])
tampil("3 nilai kosong     ", lambda: TfidfVectorizer().fit_transform(["banjir naik", np.nan]))
tampil("4 tipe data salah  ", lambda: buat_pipeline("lr").fit([123, 456], [0, 1]))
tampil("5 API lama         ", lambda: OneHotEncoder(sparse=False))
tampil("6 label tak cocok  ", lambda: buat_pipeline("lr").fit(latih["text"], y_latih[:-5]))
# --8<-- [end:galat]


# --8<-- [start:bentuk]
v = TfidfVectorizer().fit(latih["text"])
model_matriks = buat_pipeline("lr").named_steps["model"]
model_matriks.fit(v.transform(latih["text"]), y_latih)
v_lain = TfidfVectorizer().fit(uji["text"])   # SALAH: kosakata dari data uji
tampil("7 bentuk fitur beda", lambda: model_matriks.predict(v_lain.transform(uji["text"])))
# --8<-- [end:bentuk]

# --8<-- [start:overfit]
rng = np.random.RandomState(0)
kecil = latih.iloc[rng.choice(len(latih), 30, replace=False)]
m = buat_pipeline("lr", C=1000).fit(kecil["text"], kodekan_label(kecil["label"]))
y_uji = kodekan_label(uji["label"])
print("pelatihan 30 teks:  F1 latih =", round(f1_score(kodekan_label(kecil["label"]), m.predict(kecil["text"]), average="macro"), 3),
      "| F1 uji =", round(f1_score(y_uji, m.predict(uji["text"]), average="macro"), 3))
# --8<-- [end:overfit]

# --8<-- [start:metrik]
tangan = muat_uji_tangan()
y_t = kodekan_label(tangan["label"]).to_numpy()
acak = np.zeros_like(y_t)  # selalu Non-Emergency pada data tulis-tangan SEIMBANG
y_tidak_seimbang = np.array([1] * 5 + [0] * 95)
print("tulis-tangan (seimbang), selalu 0: akurasi =", accuracy_score(y_t, acak))
print("data 5% Emergency, selalu 0       : akurasi =", accuracy_score(y_tidak_seimbang, np.zeros(100, dtype=int)), "| recall Emergency =", recall_score(y_tidak_seimbang, np.zeros(100, dtype=int)))
# --8<-- [end:metrik]
