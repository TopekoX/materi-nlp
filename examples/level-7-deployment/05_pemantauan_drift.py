"""Pemantauan data drift dengan PSI: jendela lalu lintas yang stabil, bergeser gaya, dan bergeser isi."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np

from nlp_hub.interpretasi import cakupan_kosakata
from nlp_hub.konsol import pakai_utf8
from nlp_hub.modeling import buat_pipeline
from nlp_hub.pantau import psi, ringkas_aliran
from nlp_hub.perturbasi import tambah_derau
from nlp_hub.proyek import siapkan

pakai_utf8()

# --8<-- [start:acuan]
d = siapkan()
y_latih = (d.latih["label"] == "Emergency").astype(int).to_numpy()
model = buat_pipeline("svm").fit(d.latih["text"].to_numpy(), y_latih)
acuan_teks = list(d.val["text"])                       # acuan = data validasi (tidak dipakai melatih)
acuan_skor = model.decision_function(acuan_teks)
acuan_panjang = [len(t) for t in acuan_teks]
print("acuan:", ringkas_aliran(acuan_skor, acuan_panjang))
# --8<-- [end:acuan]

# --8<-- [start:jendela]
uji = list(d.uji["text"])
jendela = {
    "uji sintetis (distribusi sama)": uji,
    "uji + emoji/hashtag/URL": [tambah_derau(t) for t in uji],
    "hanya tulis-tangan": list(d.tangan["text"]),
    "hanya info edukasi (isi bergeser)": list(d.df[d.df["post_type"] == "edukasi"]["text"]),
}
print(f"{'jendela':36} {'PSI skor':>9} {'PSI panjang':>12} {'cakupan kosakata':>17}")
for nama, teks in jendela.items():
    skor = model.decision_function(teks)
    print(f"{nama:36} {psi(acuan_skor, skor):9.3f} {psi(acuan_panjang, [len(t) for t in teks]):12.3f} {cakupan_kosakata(model, teks):17.2f}")
# --8<-- [end:jendela]

# --8<-- [start:bootstrap]
rng = np.random.default_rng(0)
psi_acak = [psi(acuan_skor, rng.choice(acuan_skor, size=48, replace=True)) for _ in range(500)]
print(f"PSI antara acuan dan sampel acak 48 teks dari acuan SENDIRI: median {np.median(psi_acak):.3f}, persentil 95 {np.percentile(psi_acak, 95):.3f}")
# --8<-- [end:bootstrap]
