"""Kunci jawaban kode untuk Latihan Level 4-5 (model dan evaluasi)."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # folder examples/

import numpy as np
from sklearn.model_selection import train_test_split

from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.konsol import pakai_utf8
from nlp_hub.modeling import buat_pipeline
from nlp_hub.proyek import siapkan


# --8<-- [start:metrik]
def hitung_metrik(tp, fp, fn, tn):
    """Metrik kelas positif dari confusion matrix. Pembagi nol dikembalikan sebagai 0.0, bukan galat."""
    bagi = lambda a, b: a / b if b else 0.0
    presisi, recall = bagi(tp, tp + fp), bagi(tp, tp + fn)
    return {"akurasi": bagi(tp + tn, tp + fp + fn + tn), "presisi": presisi, "recall": recall,
            "f1": bagi(2 * presisi * recall, presisi + recall)}
# --8<-- [end:metrik]


if __name__ == "__main__":
    pakai_utf8()
    warnings.filterwarnings("ignore")
    # --8<-- [start:jalan_metrik]
    print({k: round(v, 3) for k, v in hitung_metrik(tp=15, fp=0, fn=9, tn=24).items()})
    # data 5% Emergency: model yang selalu menjawab Non-Emergency
    print({k: round(v, 3) for k, v in hitung_metrik(tp=0, fp=0, fn=50, tn=950).items()})
    # --8<-- [end:jalan_metrik]
    d = siapkan()
    X, y = d.df["text"].to_numpy(), (d.df["label"] == "Emergency").astype(int).to_numpy()
    # --8<-- [start:bocor]
    acak_latih, acak_uji, ya, yu = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
    skor_acak = metrik_emergency(yu, buat_pipeline("svm").fit(acak_latih, ya).predict(acak_uji))
    skor_kelompok = metrik_emergency(d.y_uji, buat_pipeline("svm").fit(d.latih["text"].to_numpy(), (d.latih["label"] == "Emergency").astype(int)).predict(d.uji["text"]))
    print(f"pembagian acak per baris : F1 makro {skor_acak['f1_makro']:.3f}, recall E {skor_acak['recall_e']:.3f}")
    print(f"pembagian per event_id   : F1 makro {skor_kelompok['f1_makro']:.3f}, recall E {skor_kelompok['recall_e']:.3f}")
    # --8<-- [end:bocor]
    # --8<-- [start:ambang]
    model = buat_pipeline("svm").fit(d.dev["text"].to_numpy(), d.y_dev)
    skor = model.decision_function(d.tangan["text"])
    for t in (0.0, -0.2, -0.4):
        m = metrik_emergency(d.y_tangan, (skor >= t).astype(int))
        fp = int(((d.y_tangan == 0) & (skor >= t)).sum())
        print(f"ambang {t:+.1f}: recall E {m['recall_e']:.3f} | presisi E {m['presisi_e']:.3f} | FP {fp}")
    # --8<-- [end:ambang]
