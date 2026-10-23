"""Threshold, kurva presisi-recall, dan ROC/AUC (pelajaran Level 5)."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold, cross_val_predict

from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.modeling import buat_pipeline
from nlp_hub.proyek import model_rujukan, siapkan

warnings.filterwarnings("ignore")
d = siapkan()
model = model_rujukan(d)
s_uji = model.decision_function(d.uji["text"])
s_tan = model.decision_function(d.tangan["text"])

# --8<-- [start:skor]
print("skor keputusan SVM, rentang uji sintetis   :", s_uji.min().round(2), "sampai", s_uji.max().round(2))
print("skor keputusan SVM, rentang tulis-tangan   :", s_tan.min().round(2), "sampai", s_tan.max().round(2))
print("tulis-tangan, rata-rata skor Emergency     :", s_tan[d.y_tangan == 1].mean().round(3))
print("tulis-tangan, rata-rata skor Non-Emergency :", s_tan[d.y_tangan == 0].mean().round(3))
# --8<-- [end:skor]

# --8<-- [start:ambang]
baris = []
for t in [-0.8, -0.6, -0.4, -0.2, 0.0, 0.2]:
    m = metrik_emergency(d.y_tangan, (s_tan >= t).astype(int))
    tp = int(((d.y_tangan == 1) & (s_tan >= t)).sum())
    fp = int(((d.y_tangan == 0) & (s_tan >= t)).sum())
    baris.append({"ambang": t, "TP": tp, "FP": fp, "FN": 24 - tp, "presisi E": round(m["presisi_e"], 3), "recall E": round(m["recall_e"], 3), "F1 E": round(m["f1_e"], 3)})
print(pd.DataFrame(baris).to_string(index=False))
# --8<-- [end:ambang]

# --8<-- [start:auc]
for nama, y, s in [("uji sintetis", d.y_uji, s_uji), ("tulis-tangan", d.y_tangan, s_tan)]:
    print(f"{nama:13} ROC-AUC={roc_auc_score(y, s):.3f}  AP (PR-AUC)={average_precision_score(y, s):.3f}")
# --8<-- [end:auc]

# --8<-- [start:pilih]
# Ambang dipilih HANYA dari data pengembangan: skor keputusan hasil validasi silang (tiap teks dinilai
# oleh model yang tidak pernah melihat kejadian teks itu).
lipatan = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
s_cv = cross_val_predict(buat_pipeline("svm"), d.dev["text"].to_numpy(), d.y_dev, cv=lipatan, groups=d.dev["event_id"], method="decision_function")
presisi, recall, ambang = precision_recall_curve(d.y_dev, s_cv)
memenuhi = [(t, p) for p, r, t in zip(presisi[:-1], recall[:-1], ambang) if r >= 0.95]
t_pilih = max(t for t, _ in memenuhi)           # ambang tertinggi yang masih mencapai recall CV >= 0.95
print(f"ambang terpilih dari validasi silang (recall CV >= 0.95): {t_pilih:.3f}")
for nama, y, s in [("data pengembangan (CV)", d.y_dev, s_cv), ("uji sintetis", d.y_uji, s_uji), ("tulis-tangan", d.y_tangan, s_tan)]:
    for label, t in [("ambang 0 (bawaan)", 0.0), ("ambang terpilih ", t_pilih)]:
        m = metrik_emergency(y, (s >= t).astype(int))
        print(f"{nama:22} {label}: presisi={m['presisi_e']:.3f} recall={m['recall_e']:.3f} F1={m['f1_e']:.3f}")
# --8<-- [end:pilih]
