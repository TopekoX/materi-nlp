"""Embedding kata dari ko-kemunculan: korpus mini terkontrol, dataset sintetis, dan kata di luar kosakata."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np

from nlp_hub.embedding import (
    bangun_kosakata, embedding_svd, kosinus, matriks_koterjadian, ngram_karakter, ppmi, tetangga_terdekat,
    vektor_subword,
)
from nlp_hub.konsol import pakai_utf8

pakai_utf8()
np.set_printoptions(precision=2, suppress=True, linewidth=110)

# --8<-- [start:korpus]
korpus_mini = [
    "air sungai naik banjir merendam rumah",
    "hujan deras air naik banjir merendam jalan",
    "banjir merendam rumah warga air naik",
    "gempa guncang rumah retak tembok",
    "gempa kuat guncang jalan retak tembok",
    "gempa guncang warga lari rumah retak",
    "hujan deras sungai meluap air naik",
    "tembok retak gempa guncang kuat",
]
token_mini = [kalimat.split() for kalimat in korpus_mini]
kosakata = bangun_kosakata(token_mini, min_hitung=2)
print("ukuran kosakata:", len(kosakata))
print("kosakata:", kosakata)
# --8<-- [end:korpus]

# --8<-- [start:koterjadian]
C = matriks_koterjadian(token_mini, kosakata, jendela=2)
i_banjir, i_air, i_gempa = (kosakata.index(k) for k in ("banjir", "air", "gempa"))
print("bentuk matriks C:", C.shape)
print("C[banjir, air]  =", C[i_banjir, i_air])
print("C[banjir, gempa] =", C[i_banjir, i_gempa])
print("C simetris:", bool(np.allclose(C, C.T)))
# --8<-- [end:koterjadian]

# --8<-- [start:ppmi_svd]
P = ppmi(C)
E = embedding_svd(P, dimensi=4)
print("bentuk embedding E:", E.shape, "(satu baris 4 angka per kata)")
print("vektor 'banjir':", E[i_banjir])
# --8<-- [end:ppmi_svd]

# --8<-- [start:kemiripan]
pasangan = [("banjir", "air"), ("banjir", "gempa"), ("gempa", "retak"), ("gempa", "guncang"), ("air", "retak")]
for a, b in pasangan:
    print(f"kosinus({a}, {b}) = {kosinus(E[kosakata.index(a)], E[kosakata.index(b)]):+.2f}")
print("tetangga 'banjir':", tetangga_terdekat("banjir", kosakata, E, k=3))
print("tetangga 'gempa' :", tetangga_terdekat("gempa", kosakata, E, k=3))
# --8<-- [end:kemiripan]

# --8<-- [start:dataset]
from nlp_hub.data import muat_dataset
from nlp_hub.preprocessing import praproses_token

token_nyata = [praproses_token(t) for t in muat_dataset()["text"]]
kosakata_nyata = bangun_kosakata(token_nyata, min_hitung=3)
E_nyata = embedding_svd(ppmi(matriks_koterjadian(token_nyata, kosakata_nyata, jendela=4)), dimensi=10)
print("jumlah teks:", len(token_nyata), "| kosakata (>=3 kali):", len(kosakata_nyata))
for kata in ("banjir", "tolong", "air"):
    print(f"tetangga '{kata}':", [w for w, _ in tetangga_terdekat(kata, kosakata_nyata, E_nyata, k=4)])
# --8<-- [end:dataset]

# --8<-- [start:oov]
for kata in ("banjir", "banjirnya", "bnjir"):
    print(f"{kata!r}: di kosakata mini? {kata in kosakata}")
print("potongan 'banjir':", ngram_karakter("banjir", 3, 4))
for kata in ("banjirnya", "bnjir", "xyz"):
    v, dipakai = vektor_subword(kata, kosakata, E, n_min=3, n_max=4)
    print(f"{kata!r}: dibentuk dari {dipakai}; kosinus ke 'banjir' = {kosinus(v, E[i_banjir]):+.2f}")
# --8<-- [end:oov]
