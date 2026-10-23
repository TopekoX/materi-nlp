"""Pipeline preprocessing yang dapat diuji dan diaudit (pelajaran Level 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

from sklearn.base import clone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from nlp_hub.data import muat_dataset
from nlp_hub.konsol import pakai_utf8
from nlp_hub.preprocessing import KonfigurasiPraproses, PraprosesTeks, praproses

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")
pakai_utf8()
df = muat_dataset()

# --8<-- [start:sebelum_sesudah]
lengkap = KonfigurasiPraproses(angka_waktu_lokasi=True, negasi=True, stopword=True, stem=True)
for teks in df["text"].iloc[[0, 1, 2, 3]]:
    print("MENTAH :", teks)
    print("DASAR  :", praproses(teks))
    print("LENGKAP:", praproses(teks, lengkap))
    print()
# --8<-- [end:sebelum_sesudah]

# --8<-- [start:audit]
def audit(teks_seri, konfigurasi):
    """Ringkasan sanity check: berapa teks menjadi kosong, dan rata-rata jumlah token."""
    hasil = [praproses(t, konfigurasi).split() for t in teks_seri]
    return {
        "teks_kosong": sum(len(h) == 0 for h in hasil),
        "rata_token": round(sum(len(h) for h in hasil) / len(hasil), 2),
    }


print("dasar   :", audit(df["text"], KonfigurasiPraproses()))
print("lengkap :", audit(df["text"], lengkap))
print("sastrawi:", audit(df["text"], KonfigurasiPraproses(stopword="sastrawi")))
# --8<-- [end:audit]

# --8<-- [start:pipeline]
model = Pipeline([
    ("praproses", PraprosesTeks(lengkap)),
    ("tfidf", TfidfVectorizer()),
    ("lr", LogisticRegression(max_iter=1000)),
])
print([nama for nama, _ in model.steps])
salinan = clone(model).set_params(praproses__konfigurasi=KonfigurasiPraproses())
print(model.get_params()["praproses__konfigurasi"].stem, salinan.get_params()["praproses__konfigurasi"].stem)
# --8<-- [end:pipeline]
