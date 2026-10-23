"""Error analysis: false negative dan false positive (pelajaran Level 5)."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
import pandas as pd

from nlp_hub.features import tabel_fitur
from nlp_hub.preprocessing import praproses
from nlp_hub.proyek import model_rujukan, siapkan

warnings.filterwarnings("ignore")
d = siapkan()
model = model_rujukan(d)
skor = model.decision_function(d.tangan["text"])
pred = (skor > 0).astype(int)
vektor, svm = model.named_steps["tfidf"], model.named_steps["model"]
analisis = vektor.build_analyzer()

# --8<-- [start:daftar]
fn = np.where((d.y_tangan == 1) & (pred == 0))[0]
urut = fn[np.argsort(-skor[fn])]                        # dari yang paling dekat batas
for i in urut:
    print(f"skor={skor[i]:+.2f} | {d.tangan['text'].iloc[i][:88]}")
# --8<-- [end:daftar]

# --8<-- [start:sebab]
def sumbangan(teks, n=3):
    """Kata yang paling mendorong ke Emergency dan ke Non-Emergency untuk satu teks (bobot x TF-IDF)."""
    x = model[:-1].transform([teks])
    nama = vektor.get_feature_names_out()
    kontribusi = x.multiply(svm.coef_[0]).toarray()[0]
    urut = np.argsort(kontribusi)
    pos = [(nama[i], round(float(kontribusi[i]), 2)) for i in urut[::-1][:n] if kontribusi[i] > 0]
    neg = [(nama[i], round(float(kontribusi[i]), 2)) for i in urut[:n] if kontribusi[i] < 0]
    return pos, neg


for i in urut[:3]:
    pos, neg = sumbangan(d.tangan["text"].iloc[i])
    print(d.tangan["text"].iloc[i][:60])
    print("  mendorong Emergency   :", pos)
    print("  mendorong Non-Emergency:", neg)
# --8<-- [end:sebab]

# --8<-- [start:profil]
def cakupan(teks):
    token = analisis(praproses(teks))
    return float(np.mean([k in vektor.vocabulary_ for k in token])) if token else 0.0


tabel = pd.DataFrame({
    "kelompok": np.where(d.y_tangan == 0, "TN", np.where(pred == 1, "TP", "FN")),
    "cakupan kosakata": [cakupan(t) for t in d.tangan["text"]],
})
fitur = tabel_fitur(d.tangan["text"])
tabel["ada_lokasi"] = fitur["ada_lokasi"].to_numpy()
tabel["kata_permintaan"] = fitur["kata_permintaan"].to_numpy()
tabel["kata_baru_terjadi"] = fitur["kata_baru_terjadi"].to_numpy()
print(tabel.groupby("kelompok").agg(n=("kelompok", "size"), cakupan=("cakupan kosakata", "mean"), lokasi=("ada_lokasi", "mean"),
                                    permintaan=("kata_permintaan", "mean"), baru_terjadi=("kata_baru_terjadi", "mean")).round(2).to_string())
# --8<-- [end:profil]

# --8<-- [start:fp]
skor_uji = model.decision_function(d.uji["text"])
fp = np.where((d.y_uji == 0) & (skor_uji > 0))[0]
for i in fp:
    pos, neg = sumbangan(d.uji["text"].iloc[i])
    print(f"skor={skor_uji[i]:+.2f} | {d.uji['text'].iloc[i][:60]} | pendorong: {pos}")
# --8<-- [end:fp]
