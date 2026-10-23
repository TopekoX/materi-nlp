"""Arsitektur pipeline inferensi: lapisan, penyimpanan artefak bermetadata, dan biaya batch."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.konsol import pakai_utf8
from nlp_hub.layanan import ArtefakTidakValid, Penilai, muat_artefak, simpan_artefak
from nlp_hub.proyek import model_rujukan, siapkan

pakai_utf8()
ARTEFAK = Path(__file__).resolve().parent / "artefak"       # diabaikan git (.gitignore)

# --8<-- [start:lapisan]
d = siapkan()
model = model_rujukan(d)                                     # Linear SVM pada data pengembangan (452 teks)
print("langkah pipeline:", [nama for nama, _ in model.steps])
teks = "Tolong, air banjir sudah masuk ke rumah kami."
bersih = model.named_steps["praproses"].transform([teks])
X = model.named_steps["tfidf"].transform(bersih)
skor = model.named_steps["model"].decision_function(X)
print("1. teks mentah   :", teks)
print("2. setelah praproses:", bersih[0])
print("3. matriks TF-IDF   :", X.shape, "dengan", X.nnz, "nilai tidak nol")
print("4. skor keputusan   :", round(float(skor[0]), 4), "(sama dengan model.decision_function:", bool(skor[0] == model.decision_function([teks])[0]), ")")
# --8<-- [end:lapisan]

# --8<-- [start:simpan]
meta = simpan_artefak(model, ARTEFAK, versi="svm-tfidf-sintetis-0.1", ambang=0.0,
                      catatan="Linear SVM rujukan Level 5; ambang 0 = batas bawaan, BELUM divalidasi.")
print({k: meta[k] for k in ("model_version", "jenis_keluaran", "ambang", "ambang_tervalidasi")})
print("panjang sha256:", len(meta["sha256"]))
# --8<-- [end:simpan]

# --8<-- [start:muat]
dimuat, meta_muat = muat_artefak(ARTEFAK)
penilai = Penilai(dimuat, meta_muat)
print(penilai.nilai([teks]))
print("skor sama dengan model asli:", penilai.nilai([teks])[0]["skor"] == round(float(model.decision_function([teks])[0]), 4))
# --8<-- [end:muat]

# --8<-- [start:rusak]
berkas = ARTEFAK / "model.joblib"
asli = berkas.read_bytes()
try:
    berkas.write_bytes(asli + b"x")                          # mensimulasikan berkas yang berubah
    muat_artefak(ARTEFAK)
except ArtefakTidakValid as e:
    print("ditolak:", e)
finally:
    berkas.write_bytes(asli)                                 # kembalikan agar skrip lain tetap bekerja
print("setelah dipulihkan, dapat dimuat lagi:", muat_artefak(ARTEFAK)[1]["model_version"])
# --8<-- [end:rusak]

# --8<-- [start:batch]
kumpulan = list(d.uji["text"]) * 4
mulai = time.perf_counter()
for t in kumpulan:
    model.decision_function([t])
detik_satuan = time.perf_counter() - mulai
mulai = time.perf_counter()
model.decision_function(kumpulan)
detik_batch = time.perf_counter() - mulai
print(f"{len(kumpulan)} teks: satu per satu {detik_satuan * 1000:.0f} ms | satu batch {detik_batch * 1000:.0f} ms | batch lebih cepat: {detik_batch < detik_satuan}")
# --8<-- [end:batch]
