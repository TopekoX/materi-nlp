"""Class imbalance dan baseline sederhana (pelajaran Level 5)."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score

from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.modeling import buat_pipeline
from nlp_hub.proyek import model_rujukan, siapkan

warnings.filterwarnings("ignore")
d = siapkan()
model = model_rujukan(d)
p_uji = model.predict(d.uji["text"])

# --8<-- [start:prevalensi]
rng = np.random.RandomState(42)
idx_e = np.where(d.y_uji == 1)[0]
idx_n = np.where(d.y_uji == 0)[0]
baris = []
for k in [38, 19, 8, 4]:
    hasil = []
    for _ in range(500):
        pilih = np.concatenate([rng.choice(idx_e, k, replace=False), idx_n])       # semua Non-Emergency + k Emergency
        m = metrik_emergency(d.y_uji[pilih], p_uji[pilih])
        hasil.append([m["akurasi"], m["presisi_e"], m["recall_e"], m["f1_e"], (d.y_uji[pilih] == 0).mean()])
    rata = np.mean(hasil, axis=0)
    baris.append({"Emergency": k, "porsi E": round(k / (k + len(idx_n)), 3), "akurasi": rata[0].round(3), "presisi E": rata[1].round(3),
                  "recall E": rata[2].round(3), "F1 E": rata[3].round(3), "akurasi 'selalu 0'": rata[4].round(3)})
print(pd.DataFrame(baris).to_string(index=False))
# --8<-- [end:prevalensi]

# --8<-- [start:baseline]
def baris_metrik(nama, p_u, p_t):
    mu, mt = metrik_emergency(d.y_uji, p_u), metrik_emergency(d.y_tangan, p_t)
    return {"model": nama, "uji: akurasi": round(mu["akurasi"], 3), "uji: recall E": round(mu["recall_e"], 3), "uji: F1 E": round(mu["f1_e"], 3),
            "tangan: akurasi": round(mt["akurasi"], 3), "tangan: recall E": round(mt["recall_e"], 3), "tangan: F1 E": round(mt["f1_e"], 3)}


X_dev, y_dev = d.dev["text"].to_numpy(), d.y_dev
tabel = []
for nama, base in [("selalu Non-Emergency", DummyClassifier(strategy="most_frequent")),
                   ("acak sesuai proporsi latih", DummyClassifier(strategy="stratified", random_state=42)),
                   ("selalu Emergency", DummyClassifier(strategy="constant", constant=1))]:
    base.fit(X_dev, y_dev)
    tabel.append(baris_metrik(nama, base.predict(d.uji["text"]), base.predict(d.tangan["text"])))
kata_kunci = lambda teks: np.array([int("tolong" in t.lower()) for t in teks])
tabel.append(baris_metrik("kata kunci 'tolong'", kata_kunci(d.uji["text"]), kata_kunci(d.tangan["text"])))
tabel.append(baris_metrik("Linear SVM", p_uji, model.predict(d.tangan["text"])))
print(pd.DataFrame(tabel).to_string(index=False))
# --8<-- [end:baseline]

# --8<-- [start:bobot]
tabel2 = []
for nama, algo in [("svm", "svm"), ("lr", "lr")]:
    for bobot in [None, "balanced"]:
        m = buat_pipeline(algo, class_weight=bobot).fit(X_dev, y_dev)
        tabel2.append(baris_metrik(f"{nama}, class_weight={bobot}", m.predict(d.uji["text"]), m.predict(d.tangan["text"])))
print(pd.DataFrame(tabel2)[["model", "uji: recall E", "uji: F1 E", "tangan: recall E", "tangan: F1 E"]].to_string(index=False))
# --8<-- [end:bobot]
