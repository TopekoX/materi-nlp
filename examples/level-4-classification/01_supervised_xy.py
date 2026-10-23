"""Supervised learning, X dan y, serta label encoding (pelajaran Level 4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
from sklearn.metrics import accuracy_score, recall_score
from sklearn.preprocessing import LabelEncoder

from nlp_hub.data import kodekan_label, muat_dataset

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

# --8<-- [start:xy]
df = muat_dataset()
X = df["text"]      # fitur: teks mentah
y = df["label"]     # target: label berupa teks
print(type(X).__name__, X.shape, "|", type(y).__name__, y.shape)
print(X.iloc[0])
print(y.iloc[0])
print(list(y.unique()))
# --8<-- [end:xy]

# --8<-- [start:manual]
y_num = kodekan_label(y)
print(y_num.value_counts().sort_index().to_dict())
print(list(zip(y.iloc[:4], y_num.iloc[:4])))
# --8<-- [end:manual]

# --8<-- [start:labelencoder]
le = LabelEncoder()
y_le = le.fit_transform(y)
print(le.classes_, "->", list(range(len(le.classes_))))
print("Emergency dikodekan sebagai:", int(le.transform(["Emergency"])[0]))
# --8<-- [end:labelencoder]

# --8<-- [start:jebakan]
y_benar = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0])   # 1 = Emergency (kodekan_label)
y_pred = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])    # model hanya menemukan 1 dari 4 Emergency
print("accuracy                          :", accuracy_score(y_benar, y_pred))
print("recall Emergency (pos_label=1)    :", recall_score(y_benar, y_pred, pos_label=1))
print("recall kelas 0 (Non-Emergency)    :", recall_score(y_benar, y_pred, pos_label=0))
# Jika kode terbalik (Emergency = 0, seperti LabelEncoder), recall(pos_label=1 bawaan) menjawab pertanyaan yang salah:
y_balik, p_balik = 1 - y_benar, 1 - y_pred
print("recall 'default' pada kode terbalik:", recall_score(y_balik, p_balik))
# --8<-- [end:jebakan]

# --8<-- [start:inverse]
KODE_KE_LABEL = {0: "Non-Emergency", 1: "Emergency"}
print([KODE_KE_LABEL[k] for k in y_pred])
# --8<-- [end:inverse]
