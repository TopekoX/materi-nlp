"""Kunci jawaban kode untuk Latihan Level 2-3 (preprocessing dan representasi teks)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # folder examples/

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from nlp_hub.konsol import pakai_utf8
from nlp_hub.preprocessing import KonfigurasiPraproses, praproses, praproses_token, stopwords_sastrawi, tandai_negasi


# --8<-- [start:idf_tangan]
def idf_tangan(korpus_token, kata):
    """IDF gaya scikit-learn (smooth_idf=True): ln((1 + n) / (1 + df)) + 1."""
    n = len(korpus_token)
    df = sum(kata in dokumen for dokumen in korpus_token)
    return np.log((1 + n) / (1 + df)) + 1
# --8<-- [end:idf_tangan]


if __name__ == "__main__":
    pakai_utf8()
    # --8<-- [start:praproses]
    mentah = "TOLOOONG!! Air udh masuk rmh kami 😭 https://contoh.example/1 #BanjirParah"
    print(praproses(mentah))
    print(praproses_token("Tidak ada korban jiwa", KonfigurasiPraproses(negasi=True)))
    print("'tidak' dibuang stopword Sastrawi?", "tidak" in stopwords_sastrawi())
    # --8<-- [end:praproses]
    # --8<-- [start:bow]
    korpus = ["air masuk rumah", "tolong air naik", "tolong tolong kirim bantuan"]
    cv = CountVectorizer()
    X = cv.fit_transform(korpus)
    print("kosakata:", list(cv.get_feature_names_out()))
    print(X.toarray())
    # --8<-- [end:bow]
    # --8<-- [start:tfidf]
    token = [k.split() for k in korpus]
    tv = TfidfVectorizer(norm=None)
    tv.fit(korpus)
    idx = list(tv.get_feature_names_out()).index("tolong")
    print("IDF 'tolong' dengan tangan :", round(float(idf_tangan(token, "tolong")), 4))
    print("IDF 'tolong' dari sklearn  :", round(float(tv.idf_[idx]), 4))
    print("IDF 'air' dengan tangan    :", round(float(idf_tangan(token, "air")), 4))
    tf = TfidfVectorizer(norm=None).fit_transform(korpus).toarray()
    print("TF-IDF dokumen 3, kata 'tolong' (tf=2):", round(float(tf[2, idx]), 4), "= 2 x IDF")
    # --8<-- [end:tfidf]
    # --8<-- [start:ngram]
    bi = CountVectorizer(ngram_range=(1, 2)).fit(["tidak ada korban", "ada korban jiwa"])
    print(sorted(bi.get_feature_names_out()))
    # --8<-- [end:ngram]
