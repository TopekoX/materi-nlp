"""Stopwords dan keterbatasannya (pelajaran Level 2)."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.data import muat_dataset
from nlp_hub.kamus import STOPWORDS_KONSERVATIF
from nlp_hub.preprocessing import KonfigurasiPraproses, praproses, praproses_token, stopwords_sastrawi

# --8<-- [start:daftar]
sastrawi = stopwords_sastrawi()
print(len(sastrawi), len(STOPWORDS_KONSERVATIF))
penting = ["tidak", "belum", "bukan", "jangan", "tolong", "mohon", "butuh", "kami", "ada", "masih", "sudah", "segera"]
print("di Sastrawi  :", [k for k in penting if k in sastrawi])
print("di konservatif:", [k for k in penting if k in STOPWORDS_KONSERVATIF])
# --8<-- [end:daftar]

# --8<-- [start:efek]
k_sastrawi = KonfigurasiPraproses(stopword="sastrawi")
k_konservatif = KonfigurasiPraproses(stopword="konservatif")
for teks in ["Tolong, air belum surut dan listrik tidak ada", "Ada korban jiwa", "Tidak ada korban jiwa"]:
    print(repr(teks))
    print("  sastrawi   :", praproses(teks, k_sastrawi))
    print("  konservatif:", praproses(teks, k_konservatif))
# --8<-- [end:efek]

# --8<-- [start:frekuensi]
df = muat_dataset()
token_per_dok = [set(praproses_token(t)) for t in df["text"]]
df_kata = Counter(k for s in token_per_dok for k in s)
for kata, jumlah in df_kata.most_common(12):
    print(f"{kata:10} {jumlah:4} dokumen  sastrawi={kata in sastrawi}  konservatif={kata in STOPWORDS_KONSERVATIF}")
# --8<-- [end:frekuensi]

# --8<-- [start:per_kelas]
emergency = df["label"] == "Emergency"
for kata in ["tolong", "yang", "di", "tidak", "air"]:
    ada = [kata in s for s in token_per_dok]
    e = sum(a and m for a, m in zip(ada, emergency))
    n = sum(a and not m for a, m in zip(ada, emergency))
    print(f"{kata:8} Emergency={e:3}/{emergency.sum()}  Non-Emergency={n:3}/{(~emergency).sum()}")
# --8<-- [end:per_kelas]
