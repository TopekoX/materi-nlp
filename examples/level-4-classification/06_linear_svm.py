"""Linear SVM: margin, decision function, hinge loss, dan tanpa probabilitas (pelajaran Level 4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
from sklearn.metrics import f1_score

from nlp_hub.data import bagi_latih_val_uji, kodekan_label, muat_dataset
from nlp_hub.modeling import buat_pipeline

warnings.filterwarnings("ignore")

# --8<-- [start:hinge]
def hinge(y_pm, f):
    """Kerugian hinge untuk label -1/+1 dan skor f: max(0, 1 - y*f)."""
    return max(0.0, 1.0 - y_pm * f)


for f in [2.0, 1.0, 0.5, -1.0]:
    print(f"y=+1, f={f:+.1f}: hinge = {hinge(+1, f):.1f}")
# --8<-- [end:hinge]

df = muat_dataset()
latih, val, uji = bagi_latih_val_uji(df)
y_latih, y_val = kodekan_label(latih["label"]), kodekan_label(val["label"])
model = buat_pipeline("svm").fit(latih["text"], y_latih)

# --8<-- [start:keputusan]
skor = model.decision_function(val["text"])
print(np.round(skor[:6], 3))
print(model.predict(val["text"])[:6], y_val.to_numpy()[:6])
print("tanda skor sama dengan prediksi:", bool(((skor > 0).astype(int) == model.predict(val["text"])).all()))
dalam_margin = int((np.abs(skor) < 1).sum())
print(f"teks validasi dengan |skor| < 1 (dekat/di dalam margin): {dalam_margin} dari {len(skor)}")
# --8<-- [end:keputusan]

# --8<-- [start:tanpa_proba]
try:
    model.predict_proba(val["text"])
except AttributeError as galat:
    print("AttributeError:", str(galat)[:90])
# --8<-- [end:tanpa_proba]

# --8<-- [start:regularisasi]
for C in [0.01, 0.1, 1, 10, 100]:
    m = buat_pipeline("svm", C=C).fit(latih["text"], y_latih)
    f_latih = f1_score(y_latih, m.predict(latih["text"]), average="macro")
    f_val = f1_score(y_val, m.predict(val["text"]), average="macro")
    print(f"C={C:<5} F1 latih={f_latih:.3f}  F1 validasi={f_val:.3f}")
# --8<-- [end:regularisasi]

# --8<-- [start:koefisien]
nama = model.named_steps["tfidf"].get_feature_names_out()
w = model.named_steps["model"].coef_[0]
urut = np.argsort(w)
print("mendorong Non-Emergency:", [(nama[i], round(float(w[i]), 2)) for i in urut[:5]])
print("mendorong Emergency    :", [(nama[i], round(float(w[i]), 2)) for i in urut[::-1][:5]])
# --8<-- [end:koefisien]
