"""Audit kebocoran, ketidakpastian, dan reproducibility (pelajaran Level 5)."""
import hashlib
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
import pandas as pd
import scipy
import sklearn
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedGroupKFold

from nlp_hub.data import FOLDER_DATA, RANDOM_STATE, bagi_latih_uji, kodekan_label
from nlp_hub.eksperimen import bootstrap_metrik, metrik_emergency, selang_persentil, selisih_recall_bootstrap
from nlp_hub.modeling import buat_pipeline
from nlp_hub.proyek import model_rujukan, siapkan

warnings.filterwarnings("ignore")
d = siapkan()

# --8<-- [start:audit]
def audit(latih, uji):
    return {
        "teks sama di latih dan uji": len(set(latih["text"]) & set(uji["text"])),
        "kejadian di latih dan uji": len(set(latih["event_id"]) & set(uji["event_id"])),
        "templat uji yang juga ada di latih": f"{len(set(uji['template_id']) & set(latih['template_id']))} dari {uji['template_id'].nunique()}",
        "teks tulis-tangan yang sama dengan teks latih": len(set(d.tangan["text"]) & set(latih["text"])),
    }


for k, v in audit(d.dev, d.uji).items():
    print(f"{k:48}: {v}")
# --8<-- [end:audit]

# --8<-- [start:label_acak]
X, grup = d.df["text"].to_numpy(), d.df["event_id"]
y_asli = kodekan_label(d.df["label"]).to_numpy()
skor = []
for seed in [1, 2, 3]:
    y_acak = np.random.RandomState(seed).permutation(y_asli)
    hasil = []
    for i_latih, i_uji in StratifiedGroupKFold(5, shuffle=True, random_state=seed).split(X, y_acak, groups=grup):
        m = buat_pipeline("svm").fit(X[i_latih], y_acak[i_latih])
        hasil.append(balanced_accuracy_score(y_acak[i_uji], m.predict(X[i_uji])))
    skor.append(np.mean(hasil))
print("balanced accuracy, label diacak (pipeline lengkap, CV per kejadian):", np.round(skor, 3))
# --8<-- [end:label_acak]

# --8<-- [start:bootstrap]
model = model_rujukan(d)
for nama, df, y in [("uji sintetis (112)", d.uji, d.y_uji), ("tulis-tangan (48)", d.tangan, d.y_tangan)]:
    p = model.predict(df["text"])
    m = metrik_emergency(y, p)
    for metrik in ["recall_e", "f1_makro"]:
        lo, hi = selang_persentil(bootstrap_metrik(y, p, metrik))
        print(f"{nama:20} {metrik:9} = {m[metrik]:.3f}   selang 95% bootstrap [{lo:.3f}, {hi:.3f}]")
# --8<-- [end:bootstrap]

# --8<-- [start:bandingkan]
prediksi = {a: buat_pipeline(a).fit(d.dev["text"].to_numpy(), d.y_dev).predict(d.tangan["text"]) for a in ["nb", "svm", "lr"]}
for a, b in [("nb", "lr"), ("nb", "svm"), ("svm", "lr")]:
    lo, hi = selang_persentil(selisih_recall_bootstrap(d.y_tangan, prediksi[a], prediksi[b]))
    r_a = metrik_emergency(d.y_tangan, prediksi[a])["recall_e"]
    r_b = metrik_emergency(d.y_tangan, prediksi[b])["recall_e"]
    print(f"selisih recall tulis-tangan {a} - {b}: {r_a - r_b:+.3f}  selang 95% [{lo:+.3f}, {hi:+.3f}]")
# --8<-- [end:bandingkan]

# --8<-- [start:seed]
hasil = []
for seed in range(10):
    latih, uji = bagi_latih_uji(d.df, seed=seed)
    m = buat_pipeline("svm").fit(latih["text"], kodekan_label(latih["label"]))
    hasil.append(metrik_emergency(kodekan_label(uji["label"]).to_numpy(), m.predict(uji["text"])))
tabel = pd.DataFrame(hasil)
print(tabel[["f1_makro", "recall_e", "presisi_e"]].agg(["mean", "std", "min", "max"]).round(3).to_string())
a = buat_pipeline("svm").fit(d.dev["text"].to_numpy(), d.y_dev).decision_function(d.tangan["text"])
b = buat_pipeline("svm").fit(d.dev["text"].to_numpy(), d.y_dev).decision_function(d.tangan["text"])
print("dua pelatihan dengan seed sama menghasilkan skor identik:", bool(np.array_equal(a, b)))
# --8<-- [end:seed]

# --8<-- [start:jejak]
sha = hashlib.sha256((FOLDER_DATA / "synthetic_disaster_id.csv").read_bytes()).hexdigest()[:12]
print(f"scikit-learn={sklearn.__version__} numpy={np.__version__} pandas={pd.__version__} scipy={scipy.__version__}")
print(f"python={sys.version.split()[0]} | seed={RANDOM_STATE} | sha256 data (12 awal)={sha}")
# --8<-- [end:jejak]
