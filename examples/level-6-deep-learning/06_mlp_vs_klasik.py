"""MLP NumPy pada TF-IDF melawan Linear SVM: overfitting, regularisasi, early stopping, dan variasi antar seed."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.jaringan import MLPBiner
from nlp_hub.konsol import pakai_utf8
from nlp_hub.modeling import buat_pipeline
from nlp_hub.preprocessing import KonfigurasiPraproses, PraprosesTeks
from nlp_hub.proyek import siapkan

pakai_utf8()

# --8<-- [start:data]
d = siapkan()
y_latih = (d.latih["label"] == "Emergency").astype(int).to_numpy()
y_val = (d.val["label"] == "Emergency").astype(int).to_numpy()
praproses = PraprosesTeks(KonfigurasiPraproses())
tfidf = TfidfVectorizer(min_df=2)
X_latih = tfidf.fit_transform(praproses.transform(d.latih["text"])).toarray()       # fit HANYA pada data latih
ubah = lambda teks: tfidf.transform(praproses.transform(teks)).toarray()
X_val, X_uji, X_tangan = ubah(d.val["text"]), ubah(d.uji["text"]), ubah(d.tangan["text"])
print("bentuk X_latih:", X_latih.shape, "| X_val:", X_val.shape, "| X_uji:", X_uji.shape, "| X_tangan:", X_tangan.shape)
print("proporsi Emergency pada latih:", round(float(y_latih.mean()), 3))
# --8<-- [end:data]

# --8<-- [start:kurva]
model = MLPBiner(n_masuk=X_latih.shape[1], n_tersembunyi=32, seed=0)
r = model.latih(X_latih, y_latih, epoch=60, lr=0.01, optimizer="adam", X_val=X_val, y_val=y_val)
for e in (0, 4, 9, 19, 39, 59):
    print(f"epoch {e + 1:2}: loss latih {r['loss_latih'][e]:.4f} | loss validasi {r['loss_val'][e]:.4f}")
print("epoch dengan loss validasi terendah:", r["epoch_terbaik"] + 1)
# --8<-- [end:kurva]

# --8<-- [start:bandingkan]
def laporkan(nama, prediksi_uji, prediksi_tangan):
    u, t = metrik_emergency(d.y_uji, prediksi_uji), metrik_emergency(d.y_tangan, prediksi_tangan)
    print(f"{nama:34} F1 makro uji {u['f1_makro']:.3f} | recall E uji {u['recall_e']:.3f} | recall E tulis-tangan {t['recall_e']:.3f} | presisi E tulis-tangan {t['presisi_e']:.3f}")

svm = buat_pipeline("svm").fit(d.latih["text"].to_numpy(), y_latih)
laporkan("Linear SVM (latih)", svm.predict(d.uji["text"]), svm.predict(d.tangan["text"]))

for seed in range(3):
    m = MLPBiner(n_masuk=X_latih.shape[1], n_tersembunyi=32, seed=seed)
    m.latih(X_latih, y_latih, epoch=60, lr=0.01, X_val=X_val, y_val=y_val, sabar=5)
    laporkan(f"MLP early stopping, seed {seed}", m.prediksi(X_uji), m.prediksi(X_tangan))
# --8<-- [end:bandingkan]

# --8<-- [start:regularisasi]
for l2 in (0.0, 0.001, 0.01):
    m = MLPBiner(n_masuk=X_latih.shape[1], n_tersembunyi=32, l2=l2, seed=0)
    r = m.latih(X_latih, y_latih, epoch=60, lr=0.01, X_val=X_val, y_val=y_val)
    selisih = r["loss_val"][-1] - r["loss_latih"][-1]
    print(f"l2={l2:<5}: loss latih akhir {r['loss_latih'][-1]:.4f} | loss validasi akhir {r['loss_val'][-1]:.4f} | selisih {selisih:+.4f}")
# --8<-- [end:regularisasi]
