"""Menyimpan model, memuat ulang, dan memprediksi teks baru (pelajaran Level 4)."""
import hashlib
import json
import subprocess
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import joblib
import numpy as np
import pandas as pd
import sklearn

from nlp_hub.data import RANDOM_STATE, bagi_latih_val_uji, kodekan_label, muat_dataset
from nlp_hub.modeling import buat_pipeline

warnings.filterwarnings("ignore")

ARTEFAK = Path(__file__).resolve().parent / "artefak"   # folder ini diabaikan git (.gitignore)
ARTEFAK.mkdir(exist_ok=True)
df = muat_dataset()
latih, val, uji = bagi_latih_val_uji(df)
dev = pd.concat([latih, val], ignore_index=True)
X_dev, y_dev = dev["text"], kodekan_label(dev["label"])

# --8<-- [start:simpan]
model = buat_pipeline("lr").fit(X_dev, y_dev)
berkas = ARTEFAK / "model_lr.joblib"
joblib.dump(model, berkas)
sha256 = hashlib.sha256(berkas.read_bytes()).hexdigest()
metadata = {
    "model_version": "lr-tfidf-sintetis-0.1",
    "scikit_learn": sklearn.__version__,
    "python": sys.version.split()[0],
    "seed": RANDOM_STATE,
    "data": "dataset SINTETIS; bukan untuk penggunaan operasional",
    "sha256": sha256,
}
(ARTEFAK / "model_lr.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
print("berkas model ada:", berkas.exists(), "| ukuran > 10 KB:", berkas.stat().st_size > 10_000)
print({k: metadata[k] for k in ["model_version", "scikit_learn", "seed"]})
# --8<-- [end:simpan]

# --8<-- [start:muat]
sha_sekarang = hashlib.sha256(berkas.read_bytes()).hexdigest()
assert sha_sekarang == json.loads((ARTEFAK / "model_lr.json").read_text(encoding="utf-8"))["sha256"], "berkas berubah!"
dimuat = joblib.load(berkas)
p_asli, p_muat = model.predict(uji["text"]), dimuat.predict(uji["text"])
print("prediksi identik setelah dimuat:", bool((p_asli == p_muat).all()))
print("probabilitas identik:", bool(np.allclose(model.predict_proba(uji["text"]), dimuat.predict_proba(uji["text"]))))
# --8<-- [end:muat]

# --8<-- [start:baru]
baru = [
    "Tolong, air sudah masuk rumah kami di Jl. Melati RT 04, ada lansia yang tidak bisa jalan",
    "Musim hujan sudah dekat, waspada banjir ya semuanya",
    "gempa barusan kuat bgt, atap sekolah runtuh dan ada yg tertimpa",
    "Banjir kemarin sudah surut, terima kasih relawan",
]
proba = dimuat.predict_proba(baru)[:, 1]
for teks, p in zip(baru, proba):
    label = "Emergency" if p >= 0.5 else "Non-Emergency"
    print(f"P(Emergency)={p:.3f} -> {label:13} | {teks[:60]}")
# --8<-- [end:baru]

# --8<-- [start:svm_skor]
svm = buat_pipeline("svm").fit(X_dev, y_dev)
for teks, s in zip(baru, svm.decision_function(baru)):
    print(f"skor keputusan={s:+.3f} -> {'Emergency' if s > 0 else 'Non-Emergency':13} | {teks[:60]}")
# --8<-- [end:svm_skor]

# --8<-- [start:tanpa_paket]
kode = f"import joblib; joblib.load(r'{berkas}')"
hasil = subprocess.run([sys.executable, "-I", "-c", kode], capture_output=True, text=True, cwd=str(ARTEFAK))
print("keluar:", hasil.returncode, "|", hasil.stderr.strip().splitlines()[-1])
# --8<-- [end:tanpa_paket]
