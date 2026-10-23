"""Penyiapan data standar proyek untuk Level 5 dan seterusnya (satu tempat agar semua skrip konsisten)."""
from types import SimpleNamespace

import pandas as pd

from .data import bagi_latih_val_uji, kodekan_label, muat_dataset, muat_uji_tangan
from .modeling import buat_pipeline


def siapkan():
    """Memuat data dan pembagian standar.

    Atribut: df, latih, val, uji, dev (latih+validasi), tangan, serta y_dev, y_uji, y_tangan (0/1).
    """
    df = muat_dataset()
    latih, val, uji = bagi_latih_val_uji(df)
    dev = pd.concat([latih, val], ignore_index=True)
    tangan = muat_uji_tangan()
    return SimpleNamespace(
        df=df, latih=latih, val=val, uji=uji, dev=dev, tangan=tangan,
        y_dev=kodekan_label(dev["label"]).to_numpy(),
        y_uji=kodekan_label(uji["label"]).to_numpy(),
        y_tangan=kodekan_label(tangan["label"]).to_numpy(),
    )


def model_rujukan(data, algoritma="svm", **param):
    """Melatih model rujukan Level 5 pada data pengembangan (452 teks). Bawaan: Linear SVM.

    Linear SVM dipilih sebagai rujukan karena F1 makro validasi silang tertinggi di Level 4
    (bukan berdasarkan set tulis-tangan).
    """
    return buat_pipeline(algoritma, **param).fit(data.dev["text"].to_numpy(), data.y_dev)
