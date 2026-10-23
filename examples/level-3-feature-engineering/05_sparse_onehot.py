"""Sparse matrix dan one-hot encoding (pelajaran Level 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder

from nlp_hub.data import muat_dataset
from nlp_hub.preprocessing import PraprosesTeks

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

# --8<-- [start:struktur]
dokumen = ["banjir naik air naik", "tolong air masuk rumah", "gempa kuat"]
X = CountVectorizer().fit_transform(dokumen)          # matriks CSR
print(type(X).__name__, X.shape, "elemen tak nol:", X.nnz)
print("data   :", X.data)
print("indices:", X.indices)
print("indptr :", X.indptr)
# --8<-- [end:struktur]

# --8<-- [start:memori]
teks = PraprosesTeks().transform(muat_dataset()["text"])
besar = CountVectorizer().fit_transform(teks)
padat = besar.toarray()
sparse_byte = besar.data.nbytes + besar.indices.nbytes + besar.indptr.nbytes
print("bentuk:", besar.shape, "| tipe data:", padat.dtype)
print("padat  :", padat.nbytes, "byte")
print("sparse :", sparse_byte, "byte")
print(f"rasio  : {padat.nbytes / sparse_byte:.1f}x")
# --8<-- [end:memori]

# --8<-- [start:onehot_kata]
kosakata = ["banjir", "genangan", "gempa", "kuat"]
satu_panas = np.eye(len(kosakata), dtype=int)
for kata, v in zip(kosakata, satu_panas):
    print(f"{kata:9}", v)
print("banjir . genangan =", int(satu_panas[0] @ satu_panas[1]))
print("banjir . banjir   =", int(satu_panas[0] @ satu_panas[0]))
# --8<-- [end:onehot_kata]

# --8<-- [start:bow_penjumlahan]
token = ["banjir", "naik", "naik"]
indeks = {"banjir": 0, "naik": 1, "air": 2}
jumlah = sum(np.eye(3, dtype=int)[indeks[t]] for t in token)
print(jumlah)
# --8<-- [end:bow_penjumlahan]

# --8<-- [start:kategori]
df = muat_dataset()
enc = OneHotEncoder(sparse_output=False)
hasil = enc.fit_transform(df[["post_type"]])
print(list(enc.categories_[0]))
print(hasil.shape, hasil[0].astype(int))
print(df["post_type"].iloc[0])
# --8<-- [end:kategori]
