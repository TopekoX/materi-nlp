"""Logistic Regression: sigmoid, prediksi manual, regularisasi, koefisien (pelajaran Level 4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
from sklearn.metrics import f1_score

from nlp_hub.data import bagi_latih_val_uji, kodekan_label, muat_dataset
from nlp_hub.modeling import buat_pipeline

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

# --8<-- [start:sigmoid]
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


for z in [-4, -2, 0, 2, 4]:
    print(f"z={z:+d}  sigmoid={sigmoid(z):.4f}")
for p in [0.9, 0.5, 0.1]:
    print(f"y=1, p={p}: log-loss = {-np.log(p):.3f}")
# --8<-- [end:sigmoid]

df = muat_dataset()
latih, val, uji = bagi_latih_val_uji(df)
y_latih, y_val = kodekan_label(latih["label"]), kodekan_label(val["label"])
model = buat_pipeline("lr").fit(latih["text"], y_latih)

# --8<-- [start:manual]
teks = val["text"].iloc[0]
x = model[:-1].transform([teks])                    # vektor TF-IDF (1 x V), sparse
w = model.named_steps["model"].coef_[0]             # bobot per kata
b = model.named_steps["model"].intercept_[0]        # bias
z = float((x @ w)[0] + b)
print(teks)
print(f"z = w.x + b = {z:.4f}   sigmoid(z) = {sigmoid(z):.4f}")
print("predict_proba Emergency:", round(float(model.predict_proba([teks])[0, 1]), 4))
print("label sebenarnya:", int(y_val.iloc[0]))
# --8<-- [end:manual]

# --8<-- [start:koefisien]
nama = model.named_steps["tfidf"].get_feature_names_out()
urut = np.argsort(w)
print("mendorong Non-Emergency:", [(nama[i], round(float(w[i]), 2)) for i in urut[:5]])
print("mendorong Emergency    :", [(nama[i], round(float(w[i]), 2)) for i in urut[::-1][:5]])
print("bias:", round(float(b), 3))
# --8<-- [end:koefisien]

# --8<-- [start:regularisasi]
for C in [0.01, 0.1, 1, 10, 100, 1000]:
    m = buat_pipeline("lr", C=C).fit(latih["text"], y_latih)
    f_latih = f1_score(y_latih, m.predict(latih["text"]), average="macro")
    f_val = f1_score(y_val, m.predict(val["text"]), average="macro")
    besar = np.abs(m.named_steps["model"].coef_[0]).max()
    print(f"C={C:<6} F1 latih={f_latih:.3f}  F1 validasi={f_val:.3f}  |koefisien| maks={besar:.1f}")
# --8<-- [end:regularisasi]
