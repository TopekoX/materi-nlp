"""RNN, LSTM, dan GRU dengan NumPy: satu kalimat melewati tiga jenis sel, dan hilangnya gradien."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np

from nlp_hub.atensi import jalankan_urutan, langkah_gru, langkah_lstm, langkah_rnn
from nlp_hub.konsol import pakai_utf8

pakai_utf8()
np.set_printoptions(precision=3, suppress=True, linewidth=110)

# --8<-- [start:masukan]
kata = ["tolong", "air", "masuk", "rumah"]
rng = np.random.default_rng(7)
dim_x, dim_h = 3, 4
embedding = {k: rng.normal(size=dim_x) for k in kata}      # embedding acak (belum dilatih)
deret_x = np.stack([embedding[k] for k in kata])
print("bentuk deret_x (T, dim_x):", deret_x.shape)
# --8<-- [end:masukan]

# --8<-- [start:rnn]
Wx = rng.normal(scale=0.5, size=(dim_x, dim_h))
Wh = rng.normal(scale=0.5, size=(dim_h, dim_h))
b = np.zeros(dim_h)
h0 = np.zeros(dim_h)
keadaan = jalankan_urutan(lambda x, h: langkah_rnn(x, h, Wx, Wh, b), deret_x, h0)
print("bentuk keadaan (T, dim_h):", keadaan.shape)
for k, h in zip(kata, keadaan):
    print(f"setelah {k:7}: h = {h}")
print("rentang nilai h (tanh membatasi ke (-1, 1)):", float(keadaan.min()), "sampai", float(keadaan.max()))
# --8<-- [end:rnn]

# --8<-- [start:lstm]
W_lstm = rng.normal(scale=0.5, size=(dim_x + dim_h, 4 * dim_h))
b_lstm = np.zeros(4 * dim_h)
b_lstm[:dim_h] = 1.0     # bias gerbang lupa dimulai positif agar sel awalnya cenderung mengingat (praktik umum)
h, c = np.zeros(dim_h), np.zeros(dim_h)
for k, x in zip(kata, deret_x):
    h, c, g = langkah_lstm(x, h, c, W_lstm, b_lstm)
    print(f"{k:7}: gerbang lupa f = {g['f']} | masuk i = {g['i']}")
print("sel memori c akhir:", c)
print("keadaan tersembunyi h akhir:", h)
# --8<-- [end:lstm]

# --8<-- [start:gru]
Wz, Wr, Wc = (rng.normal(scale=0.5, size=(dim_x + dim_h, dim_h)) for _ in range(3))
bz = br = bc = np.zeros(dim_h)
h = np.zeros(dim_h)
for k, x in zip(kata, deret_x):
    h, g = langkah_gru(x, h, Wz, Wr, Wc, bz, br, bc)
    print(f"{k:7}: gerbang pembaruan z = {g['z']} | reset r = {g['r']}")
print("keadaan tersembunyi h akhir:", h)
# --8<-- [end:gru]

# --8<-- [start:parameter]
def n_param_rnn(dx, dh): return dx * dh + dh * dh + dh
def n_param_lstm(dx, dh): return 4 * ((dx + dh) * dh + dh)
def n_param_gru(dx, dh): return 3 * ((dx + dh) * dh + dh)
for dx, dh in ((3, 4), (100, 128)):
    print(f"dim_x={dx:3}, dim_h={dh:3} -> RNN {n_param_rnn(dx, dh):6} | GRU {n_param_gru(dx, dh):6} | LSTM {n_param_lstm(dx, dh):6} parameter")
# --8<-- [end:parameter]

# --8<-- [start:hilang]
# Seberapa besar pengaruh keadaan awal h0 terhadap keadaan setelah T langkah? Norma hasil kali Jacobian.
Wh_besar = rng.normal(size=(8, 8))
Wh_besar *= 0.9 / np.max(np.abs(np.linalg.eigvals(Wh_besar)))      # jari-jari spektral 0,9
for T in (5, 20, 50):
    h, jac = np.zeros(8), np.eye(8)
    for _ in range(T):
        x = rng.normal(size=8)
        h = np.tanh(x + h @ Wh_besar)
        jac = ((1 - h ** 2)[:, None] * Wh_besar.T) @ jac                  # Jacobian satu langkah: diag(1 - h^2) Wh^T
    print(f"T={T:2}: norma dh_T/dh_0 = {np.linalg.norm(jac):.2e}")
# --8<-- [end:hilang]
