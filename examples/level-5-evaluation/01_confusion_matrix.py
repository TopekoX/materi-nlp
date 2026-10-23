"""Confusion matrix: TP, TN, FP, FN (pelajaran Level 5)."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

from nlp_hub.proyek import model_rujukan, siapkan

warnings.filterwarnings("ignore")
d = siapkan()
model = model_rujukan(d)                       # Linear SVM, dilatih pada 452 teks pengembangan
pred_uji = model.predict(d.uji["text"])
pred_tangan = model.predict(d.tangan["text"])


# --8<-- [start:manual]
def hitung_manual(y_benar, y_pred):
    tp = int(((y_benar == 1) & (y_pred == 1)).sum())   # Emergency, ditebak Emergency
    tn = int(((y_benar == 0) & (y_pred == 0)).sum())   # Non-Emergency, ditebak Non-Emergency
    fp = int(((y_benar == 0) & (y_pred == 1)).sum())   # Non-Emergency, salah ditebak Emergency
    fn = int(((y_benar == 1) & (y_pred == 0)).sum())   # Emergency, terlewat
    return tp, tn, fp, fn


tp, tn, fp, fn = hitung_manual(d.y_uji, pred_uji)
print(f"uji sintetis: TP={tp} TN={tn} FP={fp} FN={fn} | total={tp + tn + fp + fn} = {len(d.y_uji)}")
tn2, fp2, fn2, tp2 = confusion_matrix(d.y_uji, pred_uji, labels=[0, 1]).ravel()
print("sama dengan scikit-learn:", (tp, tn, fp, fn) == (tp2, tn2, fp2, fn2))
# --8<-- [end:manual]

# --8<-- [start:tabel]
def tabel(y, p):
    m = confusion_matrix(y, p, labels=[1, 0])          # urutan [Emergency, Non-Emergency]
    return pd.DataFrame(m, index=["sebenarnya Emergency", "sebenarnya Non-Emergency"],
                        columns=["ditebak Emergency", "ditebak Non-Emergency"])


print("UJI SINTETIS (112 teks)")
print(tabel(d.y_uji, pred_uji).to_string())
print("\nTULIS-TANGAN (48 teks)")
print(tabel(d.y_tangan, pred_tangan).to_string())
# --8<-- [end:tabel]

# --8<-- [start:contoh]
def contoh(df, y, p, y_benar, y_tebak, n=2):
    idx = np.where((y == y_benar) & (p == y_tebak))[0][:n]
    return [df["text"].iloc[i][:75] for i in idx]


print("FN (Emergency terlewat), tulis-tangan:")
for t in contoh(d.tangan, d.y_tangan, pred_tangan, 1, 0, 3):
    print("  -", t)
print("FP (Non-Emergency ditandai Emergency), uji sintetis:")
for t in contoh(d.uji, d.y_uji, pred_uji, 0, 1, 2):
    print("  -", t)
# --8<-- [end:contoh]
