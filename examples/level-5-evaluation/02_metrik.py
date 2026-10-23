"""Accuracy, precision, recall, F1, dan rata-rata makro/mikro/berbobot (pelajaran Level 5)."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
from sklearn.metrics import (
    accuracy_score, classification_report, f1_score, fbeta_score, precision_score, recall_score,
)

from nlp_hub.proyek import model_rujukan, siapkan

warnings.filterwarnings("ignore")
d = siapkan()
model = model_rujukan(d)
p_tangan = model.predict(d.tangan["text"])
y = d.y_tangan

# --8<-- [start:manual]
tp = int(((y == 1) & (p_tangan == 1)).sum())
tn = int(((y == 0) & (p_tangan == 0)).sum())
fp = int(((y == 0) & (p_tangan == 1)).sum())
fn = int(((y == 1) & (p_tangan == 0)).sum())
akurasi = (tp + tn) / (tp + tn + fp + fn)
presisi = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * presisi * recall / (presisi + recall)
print(f"TP={tp} TN={tn} FP={fp} FN={fn}")
print(f"akurasi={akurasi:.3f} presisi={presisi:.3f} recall={recall:.3f} F1={f1:.3f}")
print("sama dengan scikit-learn:",
      np.allclose([akurasi, presisi, recall, f1],
                  [accuracy_score(y, p_tangan), precision_score(y, p_tangan), recall_score(y, p_tangan), f1_score(y, p_tangan)]))
# --8<-- [end:manual]

# --8<-- [start:laporan]
print(classification_report(y, p_tangan, target_names=["Non-Emergency", "Emergency"], digits=3))
# --8<-- [end:laporan]

# --8<-- [start:rata_rata]
p_uji = model.predict(d.uji["text"])
for nama, yy, pp in [("uji sintetis (74 Non-E, 38 E)", d.y_uji, p_uji), ("tulis-tangan (24 Non-E, 24 E)", y, p_tangan)]:
    f1_kelas = f1_score(yy, pp, average=None)
    dukungan = np.bincount(yy)
    print(nama)
    print("  F1 per kelas [Non-E, E]:", f1_kelas.round(3), "| dukungan:", dukungan)
    print(f"  macro={f1_score(yy, pp, average='macro'):.3f}  weighted={f1_score(yy, pp, average='weighted'):.3f}  micro={f1_score(yy, pp, average='micro'):.3f}  akurasi={accuracy_score(yy, pp):.3f}")
    print(f"  macro manual={f1_kelas.mean():.3f}  weighted manual={(f1_kelas * dukungan).sum() / dukungan.sum():.3f}")
# --8<-- [end:rata_rata]

# --8<-- [start:fbeta]
for beta in [0.5, 1, 2]:
    print(f"F{beta:<3} = {fbeta_score(y, p_tangan, beta=beta):.3f}")
# --8<-- [end:fbeta]

# --8<-- [start:ketergantungan]
y_t = np.array([1] * 5 + [0] * 95)
semua_nol = np.zeros(100, dtype=int)
temukan_semua = np.ones(100, dtype=int)
for nama, p in [("selalu Non-Emergency", semua_nol), ("selalu Emergency", temukan_semua)]:
    print(f"{nama:21} akurasi={accuracy_score(y_t, p):.2f} presisi={precision_score(y_t, p, zero_division=0):.2f} recall={recall_score(y_t, p):.2f} F1={f1_score(y_t, p, zero_division=0):.3f}")
# --8<-- [end:ketergantungan]
