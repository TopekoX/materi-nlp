"""Interpretabilitas model linear TF-IDF: kontribusi fitur, oklusi kata, dan jebakan penjelasan."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np

from nlp_hub.interpretasi import cakupan_kosakata, kontribusi_linear, oklusi_kata
from nlp_hub.konsol import pakai_utf8
from nlp_hub.proyek import model_rujukan, siapkan

pakai_utf8()

d = siapkan()
model = model_rujukan(d)

# --8<-- [start:global]
koef = model.named_steps["model"].coef_[0]
nama = model.named_steps["tfidf"].get_feature_names_out()
urut = np.argsort(koef)
print("fitur dengan koefisien paling NEGATIF (condong Non-Emergency):", [(nama[i], round(float(koef[i]), 2)) for i in urut[:6]])
print("fitur dengan koefisien paling POSITIF (condong Emergency)    :", [(nama[i], round(float(koef[i]), 2)) for i in urut[::-1][:6]])
# --8<-- [end:global]

# --8<-- [start:lokal]
teks = "Tolong, air banjir sudah masuk ke rumah kami."
kontribusi, intersep = kontribusi_linear(model, teks, atas=6)
for fitur, nilai in kontribusi:
    print(f"  {fitur:10} {nilai:+.3f}")
semua, _ = kontribusi_linear(model, teks, atas=1000)
print(f"jumlah semua kontribusi + intersep ({intersep:+.3f}) = {sum(v for _, v in semua) + intersep:.4f}")
print(f"skor dari model.decision_function              = {model.decision_function([teks])[0]:.4f}")
# --8<-- [end:lokal]

# --8<-- [start:oklusi]
hasil, dasar = oklusi_kata(model, teks)
print(f"skor dasar {dasar:+.3f}; perubahan bila satu kata dihapus (positif = kata itu menaikkan skor):")
for kata, delta in sorted(hasil, key=lambda kv: -abs(kv[1]))[:5]:
    print(f"  {kata:10} {delta:+.3f}")
# --8<-- [end:oklusi]

# --8<-- [start:salah]
tangan = d.tangan
skor = model.decision_function(tangan["text"])
fn = tangan[(d.y_tangan == 1) & (skor < 0)].head(2)
for _, baris in fn.iterrows():
    s = model.decision_function([baris["text"]])[0]
    kontribusi, _ = kontribusi_linear(model, baris["text"], atas=4)
    print(f"\n[{baris['source_id']}] FN, skor {s:+.3f}: {baris['text'][:75]}")
    print("   kontribusi terbesar:", [(f, round(v, 2)) for f, v in kontribusi])
print("\ncakupan kosakata teks ini:", round(cakupan_kosakata(model, list(fn["text"])), 2), "| seluruh tulis-tangan:", round(cakupan_kosakata(model, list(tangan["text"])), 2))
# --8<-- [end:salah]
