"""Ablation study dan robustness terhadap variasi bahasa (pelajaran Level 5)."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from nlp_hub.data import RANDOM_STATE
from nlp_hub.eksperimen import evaluasi_pipeline, metrik_emergency
from nlp_hub.modeling import buat_pipeline
from nlp_hub.perturbasi import PERTURBASI
from nlp_hub.preprocessing import KonfigurasiPraproses
from nlp_hub.proyek import model_rujukan, siapkan

warnings.filterwarnings("ignore")
d = siapkan()

# --8<-- [start:ablation]
VARIAN = {
    "rujukan (preprocessing dasar, unigram)": lambda: buat_pipeline("svm"),
    "- normalisasi informal & huruf berulang": lambda: buat_pipeline("svm", KonfigurasiPraproses(informal=False, huruf_berulang=False)),
    "- token URL/mention": lambda: buat_pipeline("svm", KonfigurasiPraproses(url=False, mention=False)),
    "- hashtag dipecah (dihapus)": lambda: buat_pipeline("svm", KonfigurasiPraproses(hashtag="hapus")),
    "- emoji (dihapus)": lambda: buat_pipeline("svm", KonfigurasiPraproses(emoji="hapus")),
    "- IDF (hanya TF)": lambda: buat_pipeline("svm", vektor=TfidfVectorizer(use_idf=False)),
    "+ bigram": lambda: buat_pipeline("svm", vektor=TfidfVectorizer(ngram_range=(1, 2))),
    "tanpa preprocessing sama sekali": lambda: Pipeline([("tfidf", TfidfVectorizer()), ("model", LinearSVC(random_state=RANDOM_STATE))]),
}
baris = {}
for nama, buat in VARIAN.items():
    h = evaluasi_pipeline(buat, d.df, d.tangan)
    baris[nama] = {
        "F1 makro CV": f"{h['cv_rata']['f1_makro']:.3f} ± {h['cv_std']['f1_makro']:.3f}",
        "Recall E CV": f"{h['cv_rata']['recall_e']:.3f} ± {h['cv_std']['recall_e']:.3f}",
        "F1 makro tangan": round(h["tangan"]["f1_makro"], 3),
        "Recall E tangan": round(h["tangan"]["recall_e"], 3),
    }
print(pd.DataFrame(baris).T.to_string())
# --8<-- [end:ablation]

# --8<-- [start:robustness]
def skor_perturbasi(model, df, y, f):
    teks = [f(t) for t in df["text"]]
    return metrik_emergency(y, model.predict(teks))


model_pp = model_rujukan(d)                                                             # dengan preprocessing dasar
model_mentah = Pipeline([("tfidf", TfidfVectorizer()), ("model", LinearSVC(random_state=RANDOM_STATE))]).fit(d.dev["text"].to_numpy(), d.y_dev)
for nama_set, df, y in [("uji sintetis", d.uji, d.y_uji), ("tulis-tangan", d.tangan, d.y_tangan)]:
    print(f"\n{nama_set}: recall Emergency setelah perturbasi (asli -> perturbasi)")
    asli_pp = metrik_emergency(y, model_pp.predict(df["text"]))["recall_e"]
    asli_mentah = metrik_emergency(y, model_mentah.predict(df["text"]))["recall_e"]
    print(f"{'':22} {'dgn preprocessing':>20}  {'tanpa preprocessing':>20}")
    print(f"{'asli':22} {asli_pp:>20.3f}  {asli_mentah:>20.3f}")
    for nama, f in PERTURBASI.items():
        a = skor_perturbasi(model_pp, df, y, f)["recall_e"]
        b = skor_perturbasi(model_mentah, df, y, f)["recall_e"]
        print(f"{nama:22} {a:>20.3f}  {b:>20.3f}")
# --8<-- [end:robustness]
