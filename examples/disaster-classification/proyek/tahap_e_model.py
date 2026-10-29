"""Tahap E: tiga baseline TF-IDF (NB, Regresi Logistik, Linear SVM) dengan pembagian dan protokol yang sama."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # folder examples/

from nlp_hub.eksperimen import evaluasi_pipeline
from nlp_hub.konsol import pakai_utf8
from nlp_hub.modeling import buat_pipeline
from nlp_hub.proyek import siapkan

pakai_utf8()
warnings.filterwarnings("ignore")

# --8<-- [start:cv]
d = siapkan()
print("pembagian: 5 lipatan per event_id pada", len(d.dev), "teks pengembangan; model dibuat baru di tiap lipatan")
hasil = {}
for nama in ("nb", "lr", "svm"):
    hasil[nama] = evaluasi_pipeline(lambda n=nama: buat_pipeline(n), d.dev, d.tangan)
    cv, sd, tg = hasil[nama]["cv_rata"], hasil[nama]["cv_std"], hasil[nama]["tangan"]
    print(f"{nama:4} CV F1 makro {cv['f1_makro']:.3f} ± {sd['f1_makro']:.3f} | CV recall E {cv['recall_e']:.3f} | tulis-tangan recall E {tg['recall_e']:.3f}")
# --8<-- [end:cv]

# --8<-- [start:waktu]
for nama, h in hasil.items():
    print(f"{nama:4} waktu latih satu model pada {len(d.dev)} teks: {h['detik_latih'] * 1000:.0f} ms")
# --8<-- [end:waktu]
