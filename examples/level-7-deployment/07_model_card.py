"""Menyusun model card dari metadata artefak dan metrik yang dihitung ulang (bukan diketik tangan)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.konsol import pakai_utf8
from nlp_hub.layanan import muat_artefak, pastikan_artefak
from nlp_hub.proyek import siapkan

pakai_utf8()
ARTEFAK = Path(__file__).resolve().parent / "artefak"
pastikan_artefak(ARTEFAK)

# --8<-- [start:metrik]
model, meta = muat_artefak(ARTEFAK)
d = siapkan()
baris_metrik = []
for nama, df, y in (("uji sintetis (112 teks)", d.uji, d.y_uji), ("tulis-tangan (48 teks)", d.tangan, d.y_tangan)):
    # CATATAN: model artefak dilatih pada latih+validasi; set uji sintetis TIDAK dipakai melatih.
    m = metrik_emergency(y, model.predict(df["text"]))
    baris_metrik.append(f"| {nama} | {m['recall_e']:.3f} | {m['presisi_e']:.3f} | {m['f1_makro']:.3f} |")
print("\n".join(baris_metrik))
# --8<-- [end:metrik]

# --8<-- [start:kartu]
kartu = f"""# Model card: {meta['model_version']}

## Ringkasan
Linear SVM di atas TF-IDF untuk memisahkan pos Indonesia menjadi `Emergency` dan `Non-Emergency`.
Keluaran adalah **skor keputusan** (bukan probabilitas). Ambang {meta['ambang']} adalah batas bawaan model,
**belum divalidasi** untuk penggunaan operasional.

## Penggunaan yang dimaksud
Demonstrasi pendidikan pada NLP Learning Hub.

## Penggunaan yang TIDAK sesuai
Penentuan keadaan darurat otomatis, pengganti verifikasi manusia, pemantauan individu, keputusan alokasi sumber daya.

## Data
{meta['data']}. Label ditentukan dari jenis templat atau oleh satu penulis; tidak ada anotator independen.
Lihat `examples/disaster-classification/DATA_CARD.md`.

## Evaluasi (dihitung ulang saat kartu ini dibuat)
| Set | Recall Emergency | Presisi Emergency | F1 makro |
|---|---|---|---|
{chr(10).join(baris_metrik)}

Set tulis-tangan kecil (24 Emergency) dan dilabeli oleh penulis yang sama dengan penulis data latih;
selang kepercayaan lebar (lihat Level 5).

## Keterbatasan yang diketahui
- Kata/hazard di luar kosakata latih tidak dikenali (cakupan kosakata tulis-tangan sekitar 0,55).
- Ambang dari validasi sintetis tidak berlaku pada gaya tulisan berbeda.
- Tidak ada uji bahasa daerah, kode-campur, gambar, atau urutan percakapan.

## Lingkungan
scikit-learn {meta['scikit_learn']}, Python {meta['python']}, checksum SHA-256 `{meta['sha256'][:16]}...`.
"""
(ARTEFAK / "MODEL_CARD.md").write_text(kartu, encoding="utf-8")
print("model card ditulis; jumlah baris:", len(kartu.splitlines()))
print("memuat peringatan penggunaan tidak sesuai:", "TIDAK sesuai" in kartu)
# --8<-- [end:kartu]
