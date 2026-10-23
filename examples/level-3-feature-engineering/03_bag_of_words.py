"""Bag of Words dengan CountVectorizer (pelajaran Level 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from nlp_hub.data import bagi_latih_uji, muat_dataset
from nlp_hub.preprocessing import PraprosesTeks

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

# --8<-- [start:kecil]
dokumen = ["banjir naik air naik", "tolong air masuk rumah", "gempa kuat"]
cv = CountVectorizer()
X = cv.fit_transform(dokumen)
print(cv.get_feature_names_out())
print(X.shape)
print(pd.DataFrame(X.toarray(), columns=cv.get_feature_names_out()).to_string())
# --8<-- [end:kecil]

# --8<-- [start:biner]
biner = CountVectorizer(binary=True)
print(biner.fit_transform(dokumen).toarray()[0])
print(X.toarray()[0])
# --8<-- [end:biner]

# --8<-- [start:oov]
baru = ["banjir setinggi pinggang di rumah kami"]
print(cv.transform(baru).toarray())
print([k for k in baru[0].split() if k not in cv.vocabulary_])
# --8<-- [end:oov]

# --8<-- [start:dataset]
latih, uji = bagi_latih_uji(muat_dataset())
teks_latih = PraprosesTeks().transform(latih["text"])
teks_uji = PraprosesTeks().transform(uji["text"])
vektor = CountVectorizer()
X_latih = vektor.fit_transform(teks_latih)
X_uji = vektor.transform(teks_uji)
print("latih:", X_latih.shape, "uji:", X_uji.shape)
print("elemen tak nol (latih):", X_latih.nnz, f"kepadatan={X_latih.nnz / (X_latih.shape[0] * X_latih.shape[1]):.3%}")
analisis = vektor.build_analyzer()  # cara vektor memecah teks menjadi fitur
print("jumlah kata uji yang tidak ada di kosakata latih:", len({k for t in teks_uji for k in analisis(t)} - set(vektor.vocabulary_)))
# --8<-- [end:dataset]
