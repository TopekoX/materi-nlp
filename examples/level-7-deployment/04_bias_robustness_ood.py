"""Bias (uji kontrafaktual), robustness terhadap register, dan data di luar distribusi (OOD)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import numpy as np

from nlp_hub.kamus import NAMA_TEMPAT_CONTOH
from nlp_hub.konsol import pakai_utf8
from nlp_hub.perturbasi import huruf_besar, perpanjang_huruf, singkat
from nlp_hub.proyek import model_rujukan, siapkan

pakai_utf8()
d = siapkan()
model = model_rujukan(d)

# --8<-- [start:lokasi]
POLA = re.compile("|".join(re.escape(n) for n in NAMA_TEMPAT_CONTOH), re.IGNORECASE)
uji_e = d.uji[(d.y_uji == 1) & d.uji["text"].str.contains(POLA)]
print("teks Emergency di uji yang menyebut salah satu dari 10 nama tempat:", len(uji_e))


def ganti_tempat(teks, nama_baru):
    return POLA.sub(nama_baru.title(), teks)


def selisih_skor(daftar_nama):
    sel, balik = [], 0
    for teks in uji_e["text"]:
        dasar = model.decision_function([teks])[0]
        for nama in daftar_nama:
            s = model.decision_function([ganti_tempat(teks, nama)])[0]
            sel.append(s - dasar)
            balik += int((dasar >= 0) != (s >= 0))
    return np.array(sel), balik


sel, balik = selisih_skor(NAMA_TEMPAT_CONTOH)
print(f"tempat DIKENAL model : rata-rata |selisih skor| {np.abs(sel).mean():.3f}, terbesar {np.abs(sel).max():.3f}, label berbalik {balik} dari {len(sel)}")
BARU = ("rawa kuning", "batu layar", "tegal mulya", "ujung karang", "lereng biru")
sel, balik = selisih_skor(BARU)
print(f"tempat BARU (fiktif) : rata-rata |selisih skor| {np.abs(sel).mean():.3f}, terbesar {np.abs(sel).max():.3f}, label berbalik {balik} dari {len(sel)}")
# --8<-- [end:lokasi]

# --8<-- [start:register]
uji_e_semua = d.uji[d.y_uji == 1]["text"]
for nama, f in (("singkatan informal", singkat), ("HURUF BESAR", huruf_besar), ("huruf diperpanjang", perpanjang_huruf)):
    asli = model.decision_function(list(uji_e_semua))
    ubah = model.decision_function([f(t) for t in uji_e_semua])
    print(f"{nama:19}: rata-rata skor {asli.mean():+.3f} -> {ubah.mean():+.3f} | recall E {np.mean(asli >= 0):.3f} -> {np.mean(ubah >= 0):.3f}")
# --8<-- [end:register]

# --8<-- [start:ood]
PROBE = [
    ("Tsunami kecil menerjang pantai, warga panik berlarian ke bukit, tolong kirim bantuan", 1),
    ("Sinkhole muncul di depan rumah kami, jalan amblas, ada anak yang hampir jatuh. Tolong!", 1),
    ("Kami terjebak di lift gedung yang mati listrik karena badai, ada ibu hamil, mohon bantuan", 1),
    ("Webinar kesiapsiagaan tsunami minggu depan, daftar gratis", 0),
    ("Dulu sinkhole besar pernah terjadi di kota ini, sekarang sudah ditutup", 0),
    ("Saya baca artikel tentang badai tropis yang melanda tahun lalu", 0),
]
kosakata = set(model.named_steps["tfidf"].vocabulary_)
for teks, y in PROBE:
    s = model.decision_function([teks])[0]
    token = model.named_steps["praproses"].transform([teks])[0].split()
    asing = [t for t in token if t not in kosakata]
    print(f"{'E' if y else 'N'} | skor {s:+.3f} -> {'Emergency' if s >= 0 else 'Non-Emergency':13} | {'benar' if (s >= 0) == bool(y) else 'SALAH':5} | kata asing: {asing}")
# --8<-- [end:ood]
