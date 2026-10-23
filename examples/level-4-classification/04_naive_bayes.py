"""Multinomial Naive Bayes: hitung dengan tangan, lalu pada dataset (pelajaran Level 4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import f1_score
from sklearn.naive_bayes import MultinomialNB

from nlp_hub.data import bagi_latih_val_uji, kodekan_label, muat_dataset
from nlp_hub.modeling import buat_pipeline

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

# --8<-- [start:data_kecil]
dokumen = ["tolong air masuk rumah", "air naik tolong evakuasi", "webinar mitigasi banjir", "tips siaga banjir gratis"]
label = np.array([1, 1, 0, 0])  # 1 = Emergency, 0 = Non-Emergency
cv = CountVectorizer()
X = cv.fit_transform(dokumen).toarray()
kata = cv.get_feature_names_out()
V = len(kata)
print("kosakata (V =", V, "):", list(kata))
prior = np.array([(label == c).mean() for c in (0, 1)])
print("prior P(c):", prior)
# --8<-- [end:data_kecil]

# --8<-- [start:probabilitas]
alpha = 1.0
hitung = np.array([X[label == c].sum(axis=0) for c in (0, 1)])       # N_tc: kemunculan kata t di kelas c
total = hitung.sum(axis=1)                                          # N_c: total token di kelas c
P_kata = (hitung + alpha) / (total[:, None] + alpha * V)             # P(t|c) dengan smoothing Laplace
print("total token per kelas:", total)
for t in ["tolong", "banjir", "air"]:
    j = list(kata).index(t)
    print(f"P({t}|Non-Emergency)={P_kata[0, j]:.4f}  P({t}|Emergency)={P_kata[1, j]:.4f}")
# --8<-- [end:probabilitas]

# --8<-- [start:prediksi_manual]
baru = "tolong banjir air"
x = cv.transform([baru]).toarray()[0]
log_pasca = np.log(prior) + (x * np.log(P_kata)).sum(axis=1)         # log P(c) + sum_t n_t log P(t|c)
pasca = np.exp(log_pasca - log_pasca.max())
pasca /= pasca.sum()                                                 # ubah ke probabilitas yang jumlahnya 1
print("log skor [Non-E, E]:", log_pasca.round(4))
print("P(c|dokumen) [Non-E, E]:", pasca.round(4))
# --8<-- [end:prediksi_manual]

# --8<-- [start:cocok]
nb = MultinomialNB(alpha=1.0).fit(X, label)
print("probabilitas sklearn  :", nb.predict_proba(x[None, :])[0].round(4))
print("sama dengan manual    :", bool(np.allclose(nb.predict_proba(x[None, :])[0], pasca)))
# --8<-- [end:cocok]

# --8<-- [start:dataset]
df = muat_dataset()
latih, val, uji = bagi_latih_val_uji(df)
model = buat_pipeline("nb").fit(latih["text"], kodekan_label(latih["label"]))
nama = model.named_steps["tfidf"].get_feature_names_out()
selisih = model.named_steps["model"].feature_log_prob_[1] - model.named_steps["model"].feature_log_prob_[0]
urut = np.argsort(selisih)
print("condong Non-Emergency:", [nama[i] for i in urut[:6]])
print("condong Emergency    :", [nama[i] for i in urut[::-1][:6]])
# --8<-- [end:dataset]

# --8<-- [start:alpha]
y_val = kodekan_label(val["label"])
for a in [0.01, 0.1, 0.5, 1.0, 2.0]:
    m = buat_pipeline("nb", alpha=a).fit(latih["text"], kodekan_label(latih["label"]))
    print(f"alpha={a:<5} F1 makro validasi = {f1_score(y_val, m.predict(val['text']), average='macro'):.3f}")
# --8<-- [end:alpha]
