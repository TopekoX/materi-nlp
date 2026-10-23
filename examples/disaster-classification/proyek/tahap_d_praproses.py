"""Tahap D: membandingkan beberapa strategi preprocessing dengan protokol evaluasi yang sama (tanpa menetapkan 'terbaik' lebih dulu)."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # folder examples/

from nlp_hub.eksperimen import evaluasi_pipeline
from nlp_hub.konsol import pakai_utf8
from nlp_hub.modeling import buat_pipeline
from nlp_hub.preprocessing import KonfigurasiPraproses
from nlp_hub.proyek import siapkan

pakai_utf8()
warnings.filterwarnings("ignore")

# --8<-- [start:strategi]
STRATEGI = {
    "minimal (tanpa normalisasi informal)": KonfigurasiPraproses(informal=False, huruf_berulang=False),
    "dasar (bawaan)": KonfigurasiPraproses(),
    "+ negasi": KonfigurasiPraproses(negasi=True),
    "+ angka/waktu/lokasi": KonfigurasiPraproses(angka_waktu_lokasi=True),
    "+ stopword konservatif": KonfigurasiPraproses(stopword=True),
}
d = siapkan()
print(f"{'strategi':38} {'F1 makro CV':>12} {'recall E CV':>12} {'recall E tulis-tangan':>22}")
for nama, k in STRATEGI.items():
    h = evaluasi_pipeline(lambda k=k: buat_pipeline("svm", konfigurasi=k), d.dev, d.tangan)
    print(f"{nama:38} {h['cv_rata']['f1_makro']:12.3f} {h['cv_rata']['recall_e']:12.3f} {h['tangan']['recall_e']:22.3f}")
# --8<-- [end:strategi]
