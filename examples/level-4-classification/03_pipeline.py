"""Pipeline scikit-learn: merangkai preprocessing, TF-IDF, dan model (pelajaran Level 4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

from sklearn.base import clone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from nlp_hub.data import bagi_latih_uji, kodekan_label, muat_dataset
from nlp_hub.preprocessing import KonfigurasiPraproses, PraprosesTeks

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

latih, uji = bagi_latih_uji(muat_dataset())
X_latih, y_latih = latih["text"], kodekan_label(latih["label"])
X_uji, y_uji = uji["text"], kodekan_label(uji["label"])

# --8<-- [start:manual]
praproses = PraprosesTeks(KonfigurasiPraproses())
tfidf = TfidfVectorizer()
model = LogisticRegression(max_iter=1000, random_state=42)

bersih = praproses.fit_transform(X_latih)       # langkah 1: teks -> teks bersih
matriks = tfidf.fit_transform(bersih)           # langkah 2: teks bersih -> matriks (BELAJAR dari latih)
model.fit(matriks, y_latih)                     # langkah 3: matriks -> model

uji_bersih = praproses.transform(X_uji)         # uji: hanya transform, tidak fit
pred_manual = model.predict(tfidf.transform(uji_bersih))
print(type(bersih).__name__, len(bersih), "|", matriks.shape)
print(pred_manual[:10])
# --8<-- [end:manual]

# --8<-- [start:pipeline]
pipa = Pipeline([
    ("praproses", PraprosesTeks(KonfigurasiPraproses())),
    ("tfidf", TfidfVectorizer()),
    ("model", LogisticRegression(max_iter=1000, random_state=42)),
])
pipa.fit(X_latih, y_latih)
pred_pipa = pipa.predict(X_uji)
print(pred_pipa[:10])
print("sama dengan cara manual:", bool((pred_pipa == pred_manual).all()))
# --8<-- [end:pipeline]

# --8<-- [start:intip]
print(list(pipa.named_steps))
perantara = pipa[:-1].transform(X_uji)          # keluaran semua langkah KECUALI model
print("matriks fitur uji:", perantara.shape, "| ukuran kosakata dipelajari dari latih:", len(pipa.named_steps["tfidf"].vocabulary_))
print(pipa.named_steps["tfidf"].get_feature_names_out()[:6])
# --8<-- [end:intip]

# --8<-- [start:params]
param = pipa.get_params()
print(param["model__C"], param["tfidf__ngram_range"])
lain = clone(pipa).set_params(model__C=10, tfidf__ngram_range=(1, 2))
print(lain.get_params()["model__C"], lain.get_params()["tfidf__ngram_range"])
print("model asli tidak berubah:", pipa.get_params()["model__C"])
print("salinan sudah dilatih?:", hasattr(lain.named_steps["tfidf"], "vocabulary_"))
# --8<-- [end:params]
