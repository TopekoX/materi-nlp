"""Feature engineering untuk teks kebencanaan (pelajaran Level 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from nlp_hub.data import RANDOM_STATE, kodekan_label, muat_dataset, muat_uji_tangan
from nlp_hub.features import NAMA_FITUR, FiturTangan, fitur_tangan, tabel_fitur
from nlp_hub.konsol import pakai_utf8

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")
pakai_utf8()

# --8<-- [start:contoh]
contoh = ["TOLONG!! Air naik di Jl. Melati RT 08 🙏", "Tidak ada korban jiwa, kejadian kemarin sudah berlalu"]
tabel = pd.DataFrame([fitur_tangan(t) for t in contoh]).T
tabel.columns = ["laporan", "info_lama"]
print(tabel.to_string())
# --8<-- [end:contoh]

# --8<-- [start:per_kelas]
df = muat_dataset()
fitur = tabel_fitur(df["text"])
rata = fitur.groupby(df["label"]).mean().T.round(3)
rata["selisih"] = (rata["Emergency"] - rata["Non-Emergency"]).round(3)
print(rata.to_string())
# --8<-- [end:per_kelas]

# --8<-- [start:model]
def buat_model():
    return Pipeline([
        ("fitur", FiturTangan()),
        ("skala", StandardScaler()),
        ("lr", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
    ])


X, y, grup = df["text"].to_numpy(), kodekan_label(df["label"]).to_numpy(), df["event_id"]
lipatan = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
f1_makro, recall_e = [], []
for i_latih, i_uji in lipatan.split(X, y, groups=grup):
    m = buat_model().fit(X[i_latih], y[i_latih])
    p = m.predict(X[i_uji])
    f1_makro.append(f1_score(y[i_uji], p, average="macro"))
    recall_e.append(recall_score(y[i_uji], p, pos_label=1))
print(f"F1 makro (CV) : {np.mean(f1_makro):.3f} ± {np.std(f1_makro):.3f}")
print(f"Recall E (CV) : {np.mean(recall_e):.3f} ± {np.std(recall_e):.3f}")

uji = muat_uji_tangan()
model = buat_model().fit(X, y)
p = model.predict(uji["text"].to_numpy())
yt = kodekan_label(uji["label"]).to_numpy()
print(f"F1 makro (tulis-tangan): {f1_score(yt, p, average='macro'):.3f}")
print(f"Recall E (tulis-tangan): {recall_score(yt, p, pos_label=1):.3f}")
# --8<-- [end:model]

# --8<-- [start:koefisien]
koef = model.named_steps["lr"].coef_[0]
for i in np.argsort(-np.abs(koef))[:6]:
    print(f"{NAMA_FITUR[i]:18} {koef[i]:+.2f}")
# --8<-- [end:koefisien]
