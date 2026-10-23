"""Kalibrasi skor SVM menjadi probabilitas (Platt) dan pemilihan ambang pada data validasi."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
from sklearn.linear_model import LogisticRegression

from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.kalibrasi import ece, pilih_ambang_target_recall, skor_brier, tabel_reliabilitas
from nlp_hub.konsol import pakai_utf8
from nlp_hub.modeling import buat_pipeline
from nlp_hub.proyek import siapkan

pakai_utf8()

# --8<-- [start:skor]
d = siapkan()
y_latih = (d.latih["label"] == "Emergency").astype(int).to_numpy()
y_val = (d.val["label"] == "Emergency").astype(int).to_numpy()
svm = buat_pipeline("svm").fit(d.latih["text"].to_numpy(), y_latih)       # dilatih HANYA pada data latih
s_val, s_uji, s_tangan = (svm.decision_function(x["text"]) for x in (d.val, d.uji, d.tangan))
print("rentang skor validasi:", round(float(s_val.min()), 2), "sampai", round(float(s_val.max()), 2))
print("skor mentah SVM sebagai 'probabilitas' tidak valid: nilainya bisa negatif atau > 1")
# --8<-- [end:skor]

# --8<-- [start:platt]
platt = LogisticRegression().fit(s_val.reshape(-1, 1), y_val)              # p = sigmoid(a*skor + b), dicocokkan pada VALIDASI
ke_proba = lambda s: platt.predict_proba(np.asarray(s).reshape(-1, 1))[:, 1]
print(f"a = {platt.coef_[0][0]:.3f}, b = {platt.intercept_[0]:.3f}")
for nama, s, y in (("validasi", s_val, y_val), ("uji sintetis", s_uji, d.y_uji), ("tulis-tangan", s_tangan, d.y_tangan)):
    p = ke_proba(s)
    print(f"{nama:13}: ECE {ece(y, p):.3f} | Brier {skor_brier(y, p):.3f}")
# --8<-- [end:platt]

# --8<-- [start:reliabilitas]
print("tulis-tangan: bin | n | rata-rata prediksi | frekuensi Emergency nyata")
for bawah, atas, n, pred, nyata in tabel_reliabilitas(d.y_tangan, ke_proba(s_tangan), n_bin=5):
    print(f"  {bawah:.1f}-{atas:.1f} | {n:2} | {pred:.2f} | {nyata:.2f}")
# --8<-- [end:reliabilitas]

# --8<-- [start:ambang]
ambang, presisi_val, recall_val = pilih_ambang_target_recall(y_val, s_val, target_recall=0.95)
print(f"ambang dari VALIDASI (target recall 0,95): {ambang:.3f} -> presisi {presisi_val:.3f}, recall {recall_val:.3f}")
for nama, s, y in (("uji sintetis", s_uji, d.y_uji), ("tulis-tangan", s_tangan, d.y_tangan)):
    for judul, a in (("ambang 0 (bawaan)", 0.0), ("ambang dari validasi", ambang)):
        m = metrik_emergency(y, (s >= a).astype(int))
        print(f"{nama:13} {judul:21}: recall E {m['recall_e']:.3f} | presisi E {m['presisi_e']:.3f}")
# --8<-- [end:ambang]

# --8<-- [start:pilih_salah]
try:
    pilih_ambang_target_recall(np.zeros(5, dtype=int), np.arange(5.0), 0.9)
except ValueError as e:
    print("galat yang diharapkan:", e)
# --8<-- [end:pilih_salah]
