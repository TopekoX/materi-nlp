"""TF-IDF: hitung dengan tangan, lalu cocokkan dengan scikit-learn (pelajaran Level 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from nlp_hub.data import bagi_latih_uji, muat_dataset
from nlp_hub.preprocessing import PraprosesTeks

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

dokumen = ["banjir naik air naik", "tolong air masuk rumah", "gempa kuat"]

# --8<-- [start:idf]
cv = CountVectorizer()
tf = cv.fit_transform(dokumen).toarray()          # tf[i, j] = kemunculan kata j di dokumen i
kata = cv.get_feature_names_out()
n = tf.shape[0]
df_kata = (tf > 0).sum(axis=0)                    # di berapa dokumen tiap kata muncul
idf = np.log((1 + n) / (1 + df_kata)) + 1         # rumus idf "smooth" milik scikit-learn
print(pd.DataFrame({"kata": kata, "df": df_kata, "idf": idf.round(4)}).to_string(index=False))
# --8<-- [end:idf]

# --8<-- [start:manual]
mentah = tf[0] * idf                              # tf x idf untuk dokumen pertama
norma = np.sqrt((mentah ** 2).sum())              # panjang vektor (norma L2)
manual = mentah / norma
for k, a, b in zip(kata, mentah.round(4), manual.round(4)):
    if a > 0:
        print(f"{k:7} tf*idf={a:.4f}  setelah L2={b:.4f}")
print("norma L2 mentah:", norma.round(4), "| panjang hasil:", np.linalg.norm(manual).round(4))
# --8<-- [end:manual]

# --8<-- [start:cocok]
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(dokumen).toarray()
print("idf sama dengan sklearn :", np.allclose(tfidf.idf_, idf))
print("vektor sama dengan sklearn:", np.allclose(X[0], manual))
# --8<-- [end:cocok]

# --8<-- [start:dataset]
latih, uji = bagi_latih_uji(muat_dataset())
teks_latih = PraprosesTeks().transform(latih["text"])
v = TfidfVectorizer()
v.fit(teks_latih)
urut = np.argsort(v.idf_)
nama = v.get_feature_names_out()
print("IDF terendah :", [(nama[i], round(float(v.idf_[i]), 2)) for i in urut[:5]])
print("IDF tertinggi:", [(nama[i], round(float(v.idf_[i]), 2)) for i in urut[-3:]])
contoh = teks_latih[0]  # PraprosesTeks mengembalikan list string
vektor = v.transform([contoh]).toarray()[0]
atas = np.argsort(vektor)[::-1][:5]
print(contoh)
print([(nama[i], round(float(vektor[i]), 3)) for i in atas])
# --8<-- [end:dataset]
