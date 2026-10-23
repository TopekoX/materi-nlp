"""Representasi teks dengan scikit-learn: parameter, kebocoran vokabular, perbandingan (Level 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import StandardScaler

from nlp_hub.data import RANDOM_STATE, bagi_latih_uji, kodekan_label, muat_dataset, muat_uji_tangan
from nlp_hub.eksperimen import evaluasi_pipeline
from nlp_hub.features import FiturTangan
from nlp_hub.preprocessing import KonfigurasiPraproses, PraprosesTeks

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

# --8<-- [start:parameter]
teks = PraprosesTeks().transform(muat_dataset()["text"])
for nama, v in [
    ("bawaan", TfidfVectorizer()),
    ("min_df=2", TfidfVectorizer(min_df=2)),
    ("min_df=5", TfidfVectorizer(min_df=5)),
    ("max_df=0.5", TfidfVectorizer(max_df=0.5)),
    ("max_features=100", TfidfVectorizer(max_features=100)),
    ("ngram (1,2) + min_df=2", TfidfVectorizer(ngram_range=(1, 2), min_df=2)),
]:
    print(f"{nama:24} fitur = {len(v.fit(teks).vocabulary_)}")
# --8<-- [end:parameter]

# --8<-- [start:bocor]
df = muat_dataset()
y = kodekan_label(df["label"]).to_numpy()
semua = PraprosesTeks().transform(df["text"])
pembagi = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
selisih_kosakata, skor_bocor, skor_benar = [], [], []
for i_latih, i_uji in pembagi.split(df, y, groups=df["event_id"]):
    teks_latih = [semua[i] for i in i_latih]
    teks_uji = [semua[i] for i in i_uji]
    # SALAH: kosakata dan IDF dipelajari dari latih + uji
    v_bocor = TfidfVectorizer().fit(semua)
    m_bocor = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE).fit(v_bocor.transform(teks_latih), y[i_latih])
    # BENAR: hanya dari latih
    v_benar = TfidfVectorizer().fit(teks_latih)
    m_benar = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE).fit(v_benar.transform(teks_latih), y[i_latih])
    selisih_kosakata.append(len(v_bocor.vocabulary_) - len(v_benar.vocabulary_))
    skor_bocor.append((m_bocor.predict(v_bocor.transform(teks_uji)) == y[i_uji]).mean())
    skor_benar.append((m_benar.predict(v_benar.transform(teks_uji)) == y[i_uji]).mean())
print("kata tambahan di kosakata bocor per lipatan:", selisih_kosakata)
print(f"akurasi bocor: {np.mean(skor_bocor):.4f}  benar: {np.mean(skor_benar):.4f}")
# --8<-- [end:bocor]

# --8<-- [start:cakupan]
latih, uji = bagi_latih_uji(df)
v = TfidfVectorizer().fit(PraprosesTeks().transform(latih["text"]))  # kosakata hanya dari latih
analisis = v.build_analyzer()


def cakupan(teks_mentah):
    """Rata-rata proporsi token tiap teks yang ada di kosakata latih."""
    hasil = []
    for t in PraprosesTeks().transform(teks_mentah):
        token = analisis(t)
        hasil.append(np.mean([k in v.vocabulary_ for k in token]) if token else 0.0)
    return np.array(hasil)


tangan = muat_uji_tangan()
print("uji sintetis (kejadian terpisah):", round(float(cakupan(uji["text"]).mean()), 3))
tangan["cakupan"] = cakupan(tangan["text"])
print("tulis-tangan, per kelas:")
print(tangan.groupby("label")["cakupan"].mean().round(3).to_string())
# --8<-- [end:cakupan]

# --8<-- [start:bandingkan]
def lr():
    return LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)


dasar = KonfigurasiPraproses()
lengkap = KonfigurasiPraproses(angka_waktu_lokasi=True, negasi=True, stopword=True, stem=True)
KANDIDAT = {
    "1 TF-IDF, tanpa preprocessing": lambda: Pipeline([("v", TfidfVectorizer()), ("lr", lr())]),
    "2 TF-IDF, preprocessing dasar": lambda: Pipeline([("p", PraprosesTeks(dasar)), ("v", TfidfVectorizer()), ("lr", lr())]),
    "3 TF-IDF, preprocessing lengkap": lambda: Pipeline([("p", PraprosesTeks(lengkap)), ("v", TfidfVectorizer()), ("lr", lr())]),
    "4 BoW hitungan (dasar)": lambda: Pipeline([("p", PraprosesTeks(dasar)), ("v", CountVectorizer()), ("lr", lr())]),
    "5 BoW biner (dasar)": lambda: Pipeline([("p", PraprosesTeks(dasar)), ("v", CountVectorizer(binary=True)), ("lr", lr())]),
    "6 TF-IDF 1-2 gram, min_df=2": lambda: Pipeline([("p", PraprosesTeks(dasar)), ("v", TfidfVectorizer(ngram_range=(1, 2), min_df=2)), ("lr", lr())]),
    "7 TF-IDF karakter 2-5": lambda: Pipeline([("p", PraprosesTeks(dasar)), ("v", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5))), ("lr", lr())]),
    "8 16 fitur tangan saja": lambda: Pipeline([("f", FiturTangan()), ("s", StandardScaler()), ("lr", lr())]),
    "9 TF-IDF + 16 fitur tangan": lambda: Pipeline([
        ("gabung", FeatureUnion([
            ("kata", Pipeline([("p", PraprosesTeks(dasar)), ("v", TfidfVectorizer())])),
            ("tangan", Pipeline([("f", FiturTangan()), ("s", StandardScaler())])),
        ])),
        ("lr", lr()),
    ]),
}

if __name__ == "__main__":
    uji_tangan = muat_uji_tangan()
    baris, waktu = {}, {}
    for nama, buat in KANDIDAT.items():
        h = evaluasi_pipeline(buat, df, uji_tangan)
        baris[nama] = {
            "F1 makro CV": f"{h['cv_rata']['f1_makro']:.3f} ± {h['cv_std']['f1_makro']:.3f}",
            "Recall E CV": f"{h['cv_rata']['recall_e']:.3f} ± {h['cv_std']['recall_e']:.3f}",
            "F1 makro tangan": round(h["tangan"]["f1_makro"], 3),
            "Recall E tangan": round(h["tangan"]["recall_e"], 3),
            "Presisi E tangan": round(h["tangan"]["presisi_e"], 3),
        }
        waktu[nama] = round(h["detik_latih"], 3)
    print(pd.DataFrame(baris).T.to_string())
    out = Path(__file__).resolve().parent / "hasil"
    out.mkdir(exist_ok=True)
    pd.DataFrame(baris).T.to_csv(out / "perbandingan_representasi.csv", encoding="utf-8")
    print("WAKTU LATIH (detik):", waktu)
# --8<-- [end:bandingkan]
