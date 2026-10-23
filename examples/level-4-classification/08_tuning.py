"""Hyperparameter, cross-validation, dan GridSearchCV (pelajaran Level 4)."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold, cross_val_score

from nlp_hub.data import RANDOM_STATE, bagi_latih_val_uji, kodekan_label, muat_dataset, muat_uji_tangan
from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.modeling import buat_pipeline

warnings.filterwarnings("ignore")

df = muat_dataset()
latih, val, uji = bagi_latih_val_uji(df)
dev = pd.concat([latih, val], ignore_index=True)
X_dev, y_dev, grup = dev["text"].to_numpy(), kodekan_label(dev["label"]).to_numpy(), dev["event_id"].to_numpy()
tangan = muat_uji_tangan()

# --8<-- [start:cv]
lipatan = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
for i, (i_latih, i_uji) in enumerate(lipatan.split(X_dev, y_dev, groups=grup), start=1):
    print(f"lipatan {i}: latih={len(i_latih)} uji={len(i_uji)} Emergency di uji={int(y_dev[i_uji].sum())} kejadian di uji={len(set(grup[i_uji]))}")
skor = cross_val_score(buat_pipeline("svm"), X_dev, y_dev, cv=lipatan, groups=grup, scoring="f1_macro")
print("F1 makro per lipatan:", skor.round(3), "| rata-rata", skor.mean().round(3), "| std", skor.std().round(3))
# --8<-- [end:cv]

# --8<-- [start:grid]
GRID = {
    "nb": {"tfidf__ngram_range": [(1, 1), (1, 2)], "tfidf__min_df": [1, 2], "model__alpha": [0.1, 0.5, 1.0]},
    "lr": {"tfidf__ngram_range": [(1, 1), (1, 2)], "tfidf__min_df": [1, 2], "model__C": [0.1, 1, 10, 100]},
    "svm": {"tfidf__ngram_range": [(1, 1), (1, 2)], "tfidf__min_df": [1, 2], "model__C": [0.1, 1, 10]},
}
pencarian = {}
for nama, grid in GRID.items():
    gs = GridSearchCV(
        buat_pipeline(nama), grid, cv=lipatan,
        scoring={"f1_makro": "f1_macro", "recall_e": "recall"}, refit="f1_makro", n_jobs=1,
    )
    gs.fit(X_dev, y_dev, groups=grup)
    pencarian[nama] = gs
    n_kombinasi = len(gs.cv_results_["params"])
    print(f"{nama:4} kombinasi={n_kombinasi:2} (fit={n_kombinasi * 5:3})  terbaik: F1 makro CV={gs.best_score_:.4f}  {gs.best_params_}")
# --8<-- [end:grid]

# --8<-- [start:seri]
for nama in ["lr", "svm"]:
    hasil = pd.DataFrame(pencarian[nama].cv_results_)
    atas = hasil.sort_values("rank_test_f1_makro").head(5)
    print(f"\n5 kombinasi teratas untuk {nama}:")
    print(atas[["param_tfidf__ngram_range", "param_tfidf__min_df", f"param_model__C", "mean_test_f1_makro", "std_test_f1_makro", "rank_test_f1_makro"]].round(4).to_string(index=False))
# --8<-- [end:seri]

# --8<-- [start:akhir]
y_uji, y_tangan = kodekan_label(uji["label"]).to_numpy(), kodekan_label(tangan["label"]).to_numpy()
print("\nModel dengan parameter terbaik (refit pada 452 teks), diuji sekali:")
for nama, gs in pencarian.items():
    m_uji = metrik_emergency(y_uji, gs.predict(uji["text"].to_numpy()))
    m_tan = metrik_emergency(y_tangan, gs.predict(tangan["text"].to_numpy()))
    bawaan = buat_pipeline(nama).fit(X_dev, y_dev)
    b_tan = metrik_emergency(y_tangan, bawaan.predict(tangan["text"].to_numpy()))
    print(f"{nama:4} uji sintetis F1 makro={m_uji['f1_makro']:.3f} recall E={m_uji['recall_e']:.3f} | tulis-tangan F1 makro={m_tan['f1_makro']:.3f} recall E={m_tan['recall_e']:.3f} | (bawaan, tulis-tangan recall E={b_tan['recall_e']:.3f})")
# --8<-- [end:akhir]
