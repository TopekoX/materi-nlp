"""Word n-gram dan character n-gram (pelajaran Level 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

from sklearn.feature_extraction.text import CountVectorizer

from nlp_hub.data import muat_dataset
from nlp_hub.preprocessing import PraprosesTeks

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

# --8<-- [start:manual]
def ngram_kata(token, n):
    return [" ".join(token[i:i + n]) for i in range(len(token) - n + 1)]


token = "tidak ada korban jiwa".split()
print(ngram_kata(token, 1))
print(ngram_kata(token, 2))
print(ngram_kata(token, 3))
# --8<-- [end:manual]

# --8<-- [start:vectorizer]
kalimat = ["tidak ada korban jiwa", "ada korban jiwa"]
cv = CountVectorizer(ngram_range=(1, 2))
cv.fit(kalimat)
print(list(cv.get_feature_names_out()))
# --8<-- [end:vectorizer]

# --8<-- [start:karakter]
def ngram_karakter(kata, n):
    kata = f" {kata} "
    return {kata[i:i + n] for i in range(len(kata) - n + 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b)


for lain in ["tolooong", "tlg", "banjir"]:
    print(f"tolong vs {lain:9} 3-gram bersama: {sorted(ngram_karakter('tolong', 3) & ngram_karakter(lain, 3))}  Jaccard={jaccard(ngram_karakter('tolong', 3), ngram_karakter(lain, 3)):.2f}")
# --8<-- [end:karakter]

# --8<-- [start:ukuran]
teks = PraprosesTeks().transform(muat_dataset()["text"])
for nama, v in [
    ("kata 1-gram", CountVectorizer()),
    ("kata 1-2 gram", CountVectorizer(ngram_range=(1, 2))),
    ("kata 1-3 gram", CountVectorizer(ngram_range=(1, 3))),
    ("karakter 2-5", CountVectorizer(analyzer="char_wb", ngram_range=(2, 5))),
]:
    print(f"{nama:14} fitur = {len(v.fit(teks).vocabulary_)}")
# --8<-- [end:ukuran]
