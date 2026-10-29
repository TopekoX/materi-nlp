"""Tahap F: evaluasi akhir pada uji sintetis dan tulis-tangan, tabel dari kode, dan error analysis FN/FP."""
import json
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # folder examples/

import pandas as pd

from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.konsol import pakai_utf8
from nlp_hub.modeling import buat_pipeline
from nlp_hub.proyek import siapkan

pakai_utf8()
warnings.filterwarnings("ignore")
d = siapkan()
X_dev = d.dev["text"].to_numpy()

# --8<-- [start:tabel]
model, waktu, baris = {}, {}, []
for nama, kode in (("Multinomial NB", "nb"), ("Logistic Regression", "lr"), ("Linear SVM", "svm")):
    mulai = time.perf_counter()
    model[nama] = buat_pipeline(kode).fit(X_dev, d.y_dev)
    waktu[nama] = time.perf_counter() - mulai
    for set_data, df, y in (("uji sintetis", d.uji, d.y_uji), ("tulis-tangan", d.tangan, d.y_tangan)):
        p = model[nama].predict(df["text"].to_numpy())
        m = metrik_emergency(y, p)
        baris.append({"model": nama, "set": set_data, "akurasi": m["akurasi"], "presisi E": m["presisi_e"], "recall E": m["recall_e"],
                      "F1 E": m["f1_e"], "F1 makro": m["f1_makro"], "FN": int(((y == 1) & (p == 0)).sum()), "FP": int(((y == 0) & (p == 1)).sum())})
tabel = pd.DataFrame(baris)
print(tabel.round(3).to_string(index=False))
# --8<-- [end:tabel]

# --8<-- [start:indobert]
berkas = Path(__file__).resolve().parents[2] / "level-6-deep-learning" / "berat" / "hasil" / "indobenchmark_indobert_base_p1.json"
if berkas.exists():
    laporan = json.loads(berkas.read_text(encoding="utf-8"))
    print(f"IndoBERT ({laporan[0]['model']}), {len(laporan)} seed; rata-rata (min-maks):")
    for set_data in ("uji sintetis", "tulis-tangan"):
        for kunci in ("recall_e", "presisi_e", "f1_makro"):
            v = pd.Series([r[set_data][kunci] for r in laporan])
            print(f"  {set_data:13} {kunci:10} {v.mean():.3f} ({v.min():.3f}-{v.max():.3f})")
else:
    print("hasil IndoBERT belum ada: jalankan berat/13_ulang_seed.py (lihat halaman Tahap G)")
# --8<-- [end:indobert]

# --8<-- [start:galat]
svm = model["Linear SVM"]
skor = svm.decision_function(d.tangan["text"].to_numpy())
tangan = d.tangan.assign(skor=skor, pred=(skor >= 0).astype(int), benar=d.y_tangan)
fn = tangan[(tangan["benar"] == 1) & (tangan["pred"] == 0)].sort_values("skor", ascending=False)
fp = tangan[(tangan["benar"] == 0) & (tangan["pred"] == 1)]
print(f"Linear SVM pada tulis-tangan: FN = {len(fn)}, FP = {len(fp)}")
for _, r in fn.head(4).iterrows():
    print(f"  FN skor {r['skor']:+.3f} | {r['text'][:70]}")
print("catatan penulis pada FN:", [c for c in fn["catatan"].fillna("-").tolist()][:9])
# --8<-- [end:galat]

# --8<-- [start:waktu]
for nama, detik in waktu.items():
    print(f"{nama:20} waktu latih {detik * 1000:.0f} ms")
# --8<-- [end:waktu]
