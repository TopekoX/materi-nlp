"""Tabel perbandingan eksperimen yang dihitung dari kode (Tahap F proyek; pelajaran Level 5)."""
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import StratifiedGroupKFold

from nlp_hub.eksperimen import bootstrap_metrik, metrik_emergency, selang_persentil
from nlp_hub.modeling import buat_pipeline
from nlp_hub.proyek import siapkan

warnings.filterwarnings("ignore")
d = siapkan()
MODEL = {
    "Baseline: selalu Non-Emergency": lambda: DummyClassifier(strategy="most_frequent"),
    "Multinomial NB": lambda: buat_pipeline("nb"),
    "Logistic Regression": lambda: buat_pipeline("lr"),
    "Linear SVM": lambda: buat_pipeline("svm"),
}
X_dev = d.dev["text"].to_numpy()


def md(df):
    """Mengubah DataFrame menjadi tabel Markdown (agar dapat disalin ke laporan)."""
    kolom = [df.index.name or "model"] + list(df.columns)
    baris = ["| " + " | ".join(kolom) + " |", "|" + "|".join(["---"] * len(kolom)) + "|"]
    for nama, r in df.iterrows():
        baris.append("| " + " | ".join([str(nama)] + [str(v) for v in r]) + " |")
    return "\n".join(baris)


# --8<-- [start:cv]
baris = {}
for nama, buat in MODEL.items():
    hasil = []
    for i_latih, i_uji in StratifiedGroupKFold(5, shuffle=True, random_state=42).split(X_dev, d.y_dev, groups=d.dev["event_id"]):
        hasil.append(metrik_emergency(d.y_dev[i_uji], buat().fit(X_dev[i_latih], d.y_dev[i_latih]).predict(X_dev[i_uji])))
    t = pd.DataFrame(hasil)
    baris[nama] = {k: f"{t[k].mean():.3f} ± {t[k].std(ddof=0):.3f}" for k in ["akurasi", "presisi_e", "recall_e", "f1_e", "f1_makro"]}
tabel_cv = pd.DataFrame(baris).T
tabel_cv.index.name = "model"
print(md(tabel_cv))
# --8<-- [end:cv]

# --8<-- [start:uji]
def tabel_uji(df, y):
    isi = {}
    for nama, buat in MODEL.items():
        p = buat().fit(X_dev, d.y_dev).predict(df["text"].to_numpy())
        m = metrik_emergency(y, p)
        lo, hi = selang_persentil(bootstrap_metrik(y, p, "recall_e"))
        fn, fp = int(((y == 1) & (p == 0)).sum()), int(((y == 0) & (p == 1)).sum())
        isi[nama] = {"akurasi": f"{m['akurasi']:.3f}", "presisi E": f"{m['presisi_e']:.3f}", "recall E": f"{m['recall_e']:.3f}",
                     "selang 95% recall E": f"[{lo:.2f}, {hi:.2f}]", "F1 E": f"{m['f1_e']:.3f}", "F1 makro": f"{m['f1_makro']:.3f}",
                     "FN": fn, "FP": fp}
    t = pd.DataFrame(isi).T
    t.index.name = "model"
    return t


t_sintetis, t_tangan = tabel_uji(d.uji, d.y_uji), tabel_uji(d.tangan, d.y_tangan)
print("UJI SINTETIS (112 teks, 38 Emergency)")
print(md(t_sintetis))
print()
print("TULIS-TANGAN (48 teks, 24 Emergency)")
print(md(t_tangan))
# --8<-- [end:uji]

# --8<-- [start:waktu]
waktu = {}
for nama, buat in MODEL.items():
    ukur = []
    for _ in range(5):
        mulai = time.perf_counter()
        buat().fit(X_dev, d.y_dev)
        ukur.append(time.perf_counter() - mulai)
    waktu[nama] = f"{np.median(ukur):.3f}"
print("WAKTU LATIH median 5 kali (detik):", waktu)
# --8<-- [end:waktu]

# Tabel disimpan sebagai berkas Markdown agar halaman materi menyertakan hasil yang SAMA dengan keluaran skrip.
out = Path(__file__).resolve().parent / "hasil"
out.mkdir(exist_ok=True)
for nama_berkas, tabel in [("tabel_cv.md", tabel_cv), ("tabel_uji_sintetis.md", t_sintetis), ("tabel_tulis_tangan.md", t_tangan)]:
    (out / nama_berkas).write_text(md(tabel) + chr(10), encoding="utf-8")
