"""Data leakage akibat preprocessing dan pembagian data (pelajaran Level 2).

Semua angka dicetak dari eksekusi nyata dengan seed tetap.
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

from nlp_hub.data import RANDOM_STATE, bagi_latih_uji, kodekan_label, muat_dataset
from nlp_hub.preprocessing import KonfigurasiPraproses, PraprosesTeks

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

df = muat_dataset()
y = kodekan_label(df["label"]).to_numpy()
bersih = PraprosesTeks(KonfigurasiPraproses()).transform(df["text"])  # preprocessing tanpa state: aman dilakukan di awal

# --8<-- [start:label_acak]
def vektor():
    return TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5))  # ribuan fitur untuk 564 teks (p jauh lebih besar dari n)


def model():
    return LogisticRegression(C=100, class_weight="balanced", max_iter=2000)


for seed in [42, 1, 2]:
    y_acak = np.random.RandomState(seed).permutation(y)  # label diacak: TIDAK ADA hubungan nyata teks-label
    lipat = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)

    # CARA SALAH: seleksi fitur memakai label dari SELURUH data, baru validasi silang
    X_semua = vektor().fit_transform(bersih)
    X_dipilih = SelectKBest(chi2, k=100).fit_transform(X_semua, y_acak)
    salah = cross_val_score(model(), X_dipilih, y_acak, cv=lipat, scoring="balanced_accuracy").mean()

    # CARA BENAR: seleksi fitur berada di dalam pipeline, dihitung ulang pada tiap lipatan
    pipa = Pipeline([("tfidf", vektor()), ("pilih", SelectKBest(chi2, k=100)), ("lr", model())])
    benar = cross_val_score(pipa, bersih, y_acak, cv=lipat, scoring="balanced_accuracy").mean()
    print(f"seed {seed:2}: salah={salah:.3f}  benar={benar:.3f}  fitur={X_semua.shape[1]}")
# --8<-- [end:label_acak]

# --8<-- [start:kosakata]
latih, uji = bagi_latih_uji(df)
v_semua = TfidfVectorizer().fit(PraprosesTeks().transform(df["text"]))
v_latih = TfidfVectorizer().fit(PraprosesTeks().transform(latih["text"]))
kata_uji = set(TfidfVectorizer().fit(PraprosesTeks().transform(uji["text"])).vocabulary_)
print("kosakata fit-semua:", len(v_semua.vocabulary_))
print("kosakata fit-latih:", len(v_latih.vocabulary_))
print("kata hanya di uji :", len(kata_uji - set(v_latih.vocabulary_)))
print("contoh:", sorted(kata_uji - set(v_latih.vocabulary_))[:8])
# --8<-- [end:kosakata]

# --8<-- [start:duplikat]
mentah = muat_dataset(hapus_duplikat=False)
hasil = []
for seed in range(10):
    pembagi = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    i_latih, i_uji = next(pembagi.split(mentah, mentah["label"]))
    teks_latih = set(mentah.iloc[i_latih]["text"])
    hasil.append(sum(t in teks_latih for t in mentah.iloc[i_uji]["text"]))
print("teks uji yang punya salinan persis di data latih (10 seed):", hasil)
# --8<-- [end:duplikat]

# --8<-- [start:strategi]
def skor_cv(pembagi, grup=None):
    pipa = Pipeline([("pp", PraprosesTeks()), ("tfidf", TfidfVectorizer()), ("lr", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))])
    f1 = []
    for i_latih, i_uji in pembagi.split(df, y, groups=grup):
        pipa.fit(df["text"].iloc[i_latih], y[i_latih])
        f1.append(f1_score(y[i_uji], pipa.predict(df["text"].iloc[i_uji]), average="macro"))
    return np.mean(f1), np.std(f1)

acak = skor_cv(StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE))
per_kejadian = skor_cv(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE), df["event_id"])
per_templat = skor_cv(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE), df["template_id"])
print(f"acak          : {acak[0]:.3f} ± {acak[1]:.3f}")
print(f"per kejadian  : {per_kejadian[0]:.3f} ± {per_kejadian[1]:.3f}")
print(f"per templat   : {per_templat[0]:.3f} ± {per_templat[1]:.3f}")
# --8<-- [end:strategi]
